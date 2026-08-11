# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # FastAPI API Overview
#
# A runnable walkthrough of the core `FastAPI` building blocks:
# - Path operations
# - Request validation
# - Dependency injection
# - Error handling
# - The automatic interactive docs
#
# `FastAPI` apps are served by `uvicorn`
# - This notebook uses `fastapi.testclient.TestClient` instead, which drives the app in-process without opening a real socket, so every cell runs instantly.
#
# **What you will learn:**
# - How path and query parameters are typed and validated
# - How request bodies are validated with `pydantic` models
# - How to share logic across endpoints with `Depends()`
# - How to return structured errors with `HTTPException`
# - Where the automatic `/docs`, `/redoc`, and `/openapi.json` come from
#
# Related notebook: `fastapi.example.ipynb` runs a complete app with a real
# `uvicorn` server and real HTTP calls over the network.

# %% [markdown]
# ## Mental Model
#
# | Object | Description | Additional Info |
# |--------|-------------|-----------------|
# | `FastAPI()` | Application instance | Holds every registered route; passed to `TestClient` or `uvicorn` |
# | `@app.get(path)` / `@app.post(path)` | Path operation decorator | Registers a function as the handler for one HTTP method + path |
# | `TestClient(app)` | In-process test client | Drives the app without opening a real socket |
# | `pydantic.BaseModel` subclass | Request/response schema | Field types define validation rules and the `/openapi.json` shape |
# | `fastapi.Query(default, ...)` | Query parameter declaration | Adds constraints (`ge`, `le`, ...) beyond a plain default value |
# | `fastapi.Depends(func)` | Dependency injection | Shares parsing/validation logic across multiple endpoints |
# | `fastapi.HTTPException(status_code, detail)` | Structured error | Raised inside a handler; `FastAPI` turns it into a JSON error response |

# %%
# !pip install --quiet -r tutorial_requirements.txt

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import fastapi
import fastapi.testclient
import pydantic

import helpers.hdbg as hdbg

hdbg.init_logger(verbosity=logging.INFO)
_LOG = logging.getLogger(__name__)

# %% [markdown]
# ## 1. Path Operations
#
# - A path operation is a Python function decorated with an HTTP method and a path, e.g. `@app.get("/items/{item_id}")`
# - `FastAPI` reads the function's type hints to know how to parse and validate each argument

# %%
# Create a `FastAPI` application: an empty app with no routes yet.
demo_app = fastapi.FastAPI()

# Create a client that calls `demo_app` directly, without opening a real
# socket (useful for unit testing).
demo_client = fastapi.testclient.TestClient(demo_app)
# `demo_client` can now issue requests against any route on `demo_app`.

# - A path operation is an "endpoint":
#   - One URL path: `/`
#   - One HTTP method: `get`
#   - The function that handles it: `read_root()`
@demo_app.get("/")
def read_root() -> dict:
    """
    Return a simple greeting.
    """
    return {"message": "Hello, World"}
# Outcome: GET / is now registered on `demo_app`, handled by `read_root()`.


# %%
# Call GET / and confirm the greeting comes back.
response = demo_client.get("/")
_LOG.info("GET / -> %s %s", response.status_code, response.json())


# %%
# Register an "items" endpoint accepting an integer path parameter.
@demo_app.get("/items/{item_id}")
def read_item(item_id: int) -> dict:
    """
    Echo back a path parameter, coerced to `int`.
    """
    return {"item_id": item_id}
# Outcome: GET /items/{item_id} is now registered, handled by `read_item()`.


# %%
# Call GET /items/42; `"42"` in the URL is coerced to the `int` 42.
path = "/items/42"
response = demo_client.get(path)
_LOG.info("GET %s -> %s %s", path, response.status_code, response.json())
# Outcome: 200 OK with {"item_id": 42}.

# %%
# Call GET /items/not_a_number: the path segment cannot be coerced to `int`.
response = demo_client.get("/items/not_a_number")
_LOG.info("GET /items/not_a_number -> %s", response.status_code)
_LOG.info("Validation error detail: %s", response.json()["detail"][0]["msg"])
# Outcome: 422 Unprocessable Entity; `read_item()` never runs.

# %% [markdown]
# ## 2. Query Parameters
#
# Function arguments that are not part of the path become query parameters.
# A default value makes the parameter optional.

# %%
# Register an endpoint whose non-path arguments become query parameters.
@demo_app.get("/items/")
def list_items(skip: int = 0, limit: int = 10) -> dict:
    """
    Report the pagination parameters that were parsed.
    """
    return {"skip": skip, "limit": limit}
# Outcome: GET /items/ is now registered, handled by `list_items()`.

# %%
# Call GET /items/ with explicit `skip` and `limit` query parameters.
response = demo_client.get("/items/", params={"skip": 5, "limit": 20})
_LOG.info("GET /items/?skip=5&limit=20 -> %s", response.json())
# Outcome: {"skip": 5, "limit": 20}, parsed straight from the query string.

# %%
# Call GET /items/ with no query parameters at all.
response = demo_client.get("/items/")
_LOG.info("GET /items/ (defaults) -> %s", response.json())
# Outcome: {"skip": 0, "limit": 10}, falling back to the function's defaults.

# %% [markdown]
# ## 3. Request Body and Validation
#
# - A request body is described as a `pydantic` model
# - `BookCreate` and `Book` are defined directly below (not imported from
#   `fastapi_utils`), so the full request/response shape is visible here

# %%
# Payload accepted when creating a book: no `id` yet, the server assigns it.
class BookCreate(pydantic.BaseModel):
    """
    Payload accepted when creating a book.
    """

    title: str = pydantic.Field(..., description="Book title.")
    author: str = pydantic.Field(..., description="Book author.")
    year: int = pydantic.Field(..., ge=0, description="Publication year.")
    in_stock: bool = True


# A book as returned by the API, including its server-assigned ID.
class Book(pydantic.BaseModel):
    """
    A book as stored and returned by the API, including its ID.
    """

    id: int = pydantic.Field(..., description="Unique book identifier.")
    title: str = pydantic.Field(..., description="Book title.")
    author: str = pydantic.Field(..., description="Book author.")
    year: int = pydantic.Field(..., ge=0, description="Publication year.")
    in_stock: bool = True


# %% [markdown]
# - The route registration's arguments each control a different thing:
#   - `"/books"`: the path this handler responds to
#   - `response_model=Book`: the return value is validated and serialized
#     against `Book`, and the shape is documented in `/docs`
#   - `status_code=201`: the HTTP status returned on success ("Created")
# - `payload: BookCreate` is the request body: `FastAPI` parses and validates
#   the incoming JSON against `BookCreate` before `create_book()` ever runs

# %%
# Register POST /books; `payload` is validated against `BookCreate` first.
@demo_app.post("/books", response_model=Book, status_code=201)
def create_book(payload: BookCreate) -> Book:
    """
    Echo the validated payload back as a `Book` with a fixed ID.

    A real implementation would persist the book; see
    `fastapi_utils.create_book_app()` for that version.
    """
    return Book(id=1, **payload.model_dump())
# Outcome: POST /books is now registered, handled by `create_book()`.


# Call POST /books with a complete, valid payload.
response = demo_client.post(
    "/books", json={"title": "Fluent Python", "author": "Luciano Ramalho", "year": 2015}
)
_LOG.info("POST /books (valid) -> %s %s", response.status_code, response.json())
# Outcome: 201 Created with the echoed `Book`, `id` set to 1.

# %%
# Call POST /books with a payload missing required fields.
response = demo_client.post("/books", json={"title": "Missing Fields"})
_LOG.info("POST /books (invalid) -> %s", response.status_code)
for error in response.json()["detail"]:
    _LOG.info("  %s: %s", error["loc"], error["msg"])
# Outcome: 422 Unprocessable Entity; `create_book()` never runs.

# %% [markdown]
# ## 4. Dependency Injection
#
# - `Depends()` lets multiple endpoints share the same parameter-parsing logic instead of repeating it
# - `FastAPI` calls the dependency function first and passes its return value into the endpoint

# %%
# `pagination_params()` is a plain function, not a route: `FastAPI` calls it
# before the endpoint runs, parsing and validating `skip`/`limit` from the
# query string the same way it would for a path operation's own arguments.
def pagination_params(
    skip: int = fastapi.Query(0, ge=0),
    limit: int = fastapi.Query(10, ge=1, le=100),
) -> dict:
    """
    Parse and validate pagination parameters shared across endpoints.
    """
    return {"skip": skip, "limit": limit}


# `fastapi.Depends(pagination_params)` wires the dependency into the
# endpoint: the `pagination` argument below is `pagination_params()`'s
# *return value*, already parsed and validated, not the function itself.
@demo_app.get("/books")
def list_books_demo(
    pagination: dict = fastapi.Depends(pagination_params),
) -> dict:
    """
    Show the pagination values resolved by the shared dependency.
    """
    return pagination
# Outcome: GET /books is now registered, handled by `list_books_demo()`.


# %%
# Call GET /books?limit=5; the dependency parses and validates `limit`.
response = demo_client.get("/books", params={"limit": 5})
_LOG.info("GET /books?limit=5 -> %s", response.json())
# Outcome: {"skip": 0, "limit": 5}.

# %%
# An out-of-range value is rejected by the dependency's own `Query()` bounds.
response = demo_client.get("/books", params={"limit": 500})
_LOG.info("GET /books?limit=500 -> %s", response.status_code)
# Outcome: 422 Unprocessable Entity; `list_books_demo()` never runs.

# %% [markdown]
# ## 5. Error Handling with HTTPException
#
# Raising `fastapi.HTTPException(status_code, detail)` inside a handler
# short-circuits it: `FastAPI` turns the exception into a JSON error
# response with the given status code, instead of running the rest of the
# function.

# %%
# A tiny in-memory catalog, keyed by ID.
books_by_id = {
    1: Book(id=1, title="Fluent Python", author="Luciano Ramalho", year=2015)
}


# Register GET /books/{book_id}; a missing ID raises `HTTPException(404)`.
@demo_app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> Book:
    """
    Fetch a book by ID, or raise a 404 if it is missing.
    """
    if book_id not in books_by_id:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Book {book_id} not found"
        )
    return books_by_id[book_id]
# Outcome: GET /books/{book_id} is now registered, handled by `get_book()`.


# Register a `/health` endpoint, used later to test that the app is up.
@demo_app.get("/health")
def health() -> dict:
    """
    Report that the service is up.
    """
    return {"status": "ok"}
# Outcome: GET /health is now registered, handled by `health()`.


# %%
# Call GET /books/999; no book with that ID exists in `books_by_id`.
response = demo_client.get("/books/999")
_LOG.info("GET /books/999 -> %s %s", response.status_code, response.json())
# Outcome: 404 Not Found with {"detail": "Book 999 not found"}.

# %% [markdown]
# ## 6. Automatic Interactive Docs
#
# Every `FastAPI` app serves three documentation endpoints for free, derived
# from the same type hints used for validation:
# - `/docs`: interactive Swagger UI
# - `/redoc`: read-only ReDoc reference
# - `/openapi.json`: the raw OpenAPI schema
#
# `fastapi.example.ipynb` opens these in a browser against a real server;
# here, `TestClient` fetches the schema directly.

# %%
# Call GET /openapi.json to fetch the schema `FastAPI` generated automatically.
response = demo_client.get("/openapi.json")
schema = response.json()
_LOG.info("OpenAPI title: %s", schema["info"]["title"])
_LOG.info("Registered paths: %s", sorted(schema["paths"].keys()))
# Outcome: 200 OK; the schema lists every route registered on `demo_app` above.

# %% [markdown]
# ## 7. Testing with TestClient
#
# `TestClient` is not just a notebook convenience: it is the same tool used
# in automated `pytest` tests, since it drives the app in-process.

# %%
def test_health_check() -> None:
    """
    Confirm the demo app reports itself as healthy.
    """
    result = demo_client.get("/health")
    assert result.status_code == 200
    assert result.json() == {"status": "ok"}


# Run the test the same way `pytest` would: call it directly.
test_health_check()
_LOG.info("test_health_check() passed.")
# Outcome: both assertions held; no `AssertionError` was raised.
