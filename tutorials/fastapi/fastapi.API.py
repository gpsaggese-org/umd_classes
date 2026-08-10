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
# - path operations
# - request validation
# - dependency injection
# - error handling
# - the automatic interactive docs.
#
# `FastAPI` apps are served by `uvicorn`
# - This notebook uses `fastapi.testclient.TestClient` instead, which drives the
# app in-process without opening a real socket, so every cell runs instantly.
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

# %%
# !pip install --quiet -r tutorial_requirements.txt

# %%
# %load_ext autoreload
# %autoreload 2

import logging

# TODO(ai_gp): Use import fastapi
from fastapi import Depends, FastAPI, Query

import fastapi_utils

# TODO(ai_gp): Use the official function for the logging.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %% [markdown]
# ## 1. Path Operations
#
# - A path operation is a Python function decorated with an HTTP method and a path, e.g. `@app.get("/items/{item_id}")`
# - `FastAPI` reads the function's type hints to know how to parse and validate each argument

# %%
demo_app = FastAPI()


# @demo_app.get("/")
# def read_root() -> dict:
#     """
#     Return a simple greeting.
#     """
#     return {"message": "Hello, World"}


@demo_app.get("/items/{item_id}")
def read_item(item_id: int) -> dict:
    """
    Echo back a path parameter, coerced to `int`.
    """
    return {"item_id": item_id}


demo_client = fastapi_utils.make_test_client(demo_app)

# %%
response = demo_client.get("/items/42")
_LOG.info("GET /items/42 -> %s %s", response.status_code, response.json())

# %%
# A non-integer path segment fails validation before `read_item()` ever runs.
response = demo_client.get("/items/not_a_number")
_LOG.info("GET /items/not_a_number -> %s", response.status_code)
_LOG.info("Validation error detail: %s", response.json()["detail"][0]["msg"])

# %% [markdown]
# ## 2. Query Parameters
#
# Function arguments that are not part of the path become query parameters.
# A default value makes the parameter optional.

# %%
@demo_app.get("/items/")
def list_items(skip: int = 0, limit: int = 10) -> dict:
    """
    Report the pagination parameters that were parsed.
    """
    return {"skip": skip, "limit": limit}

# TODO(ai_gp): Split each call into a cell.
response = demo_client.get("/items/", params={"skip": 5, "limit": 20})
_LOG.info("GET /items/?skip=5&limit=20 -> %s", response.json())
# TODO(ai_gp): Add a comment explaining the output for each cell.

response = demo_client.get("/items/")
_LOG.info("GET /items/ (defaults) -> %s", response.json())

# %% [markdown]
# ## 3. Request Body and Validation
#
# - A request body is described as a `pydantic` model
# - `fastapi_utils` defines `BookCreate` and `Book` for the tutorial
#     - Reusing them here keeps this notebook and `fastapi.example.ipynb` consistent

# %%
@demo_app.post("/books", response_model=fastapi_utils.Book, status_code=201)
def create_book(payload: fastapi_utils.BookCreate) -> fastapi_utils.Book:
    """
    Echo the validated payload back as a `Book` with a fixed ID.

    A real implementation would persist the book; see
    `fastapi_utils.create_book_app()` for that version.
    """
    return fastapi_utils.Book(id=1, **payload.model_dump())


response = demo_client.post(
    "/books", json={"title": "Fluent Python", "author": "Luciano Ramalho", "year": 2015}
)
_LOG.info("POST /books (valid) -> %s %s", response.status_code, response.json())

# %%
# Omitting a required field fails validation before `create_book()` runs.
response = demo_client.post("/books", json={"title": "Missing Fields"})
_LOG.info("POST /books (invalid) -> %s", response.status_code)
for error in response.json()["detail"]:
    _LOG.info("  %s: %s", error["loc"], error["msg"])

# %% [markdown]
# ## 4. Dependency Injection
#
# - `Depends()` lets multiple endpoints share the same parameter-parsing logic instead of repeating it
# - `FastAPI` calls the dependency function first and passes its return value into the endpoint

# %%
def pagination_params(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)
) -> dict:
    """
    Parse and validate pagination parameters shared across endpoints.
    """
    return {"skip": skip, "limit": limit}


@demo_app.get("/books")
def list_books_demo(pagination: dict = Depends(pagination_params)) -> dict:
    """
    Show the pagination values resolved by the shared dependency.
    """
    return pagination


response = demo_client.get("/books", params={"limit": 5})
_LOG.info("GET /books?limit=5 -> %s", response.json())

# An out-of-range value is rejected by the dependency's own `Query()` bounds.
response = demo_client.get("/books", params={"limit": 500})
_LOG.info("GET /books?limit=500 -> %s", response.status_code)

# %% [markdown]
# ## 5. Error Handling with HTTPException
#
# `fastapi_utils.create_book_app()` builds a small catalog API on top of the
# same models. Looking up a missing book raises `HTTPException`, which
# `FastAPI` turns into a JSON error response with the given status code.

# %%
catalog_app = fastapi_utils.create_book_app()
catalog_client = fastapi_utils.make_test_client(catalog_app)

response = catalog_client.get("/books/999")
_LOG.info("GET /books/999 -> %s %s", response.status_code, response.json())

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
response = catalog_client.get("/openapi.json")
schema = response.json()
_LOG.info("OpenAPI title: %s", schema["info"]["title"])
_LOG.info("Registered paths: %s", sorted(schema["paths"].keys()))

# %% [markdown]
# ## 7. Testing with TestClient
#
# `TestClient` is not just a notebook convenience: it is the same tool used
# in automated `pytest` tests, since it drives the app in-process.

# %%
def test_health_check() -> None:
    """
    Confirm the catalog app reports itself as healthy.
    """
    result = catalog_client.get("/health")
    assert result.status_code == 200
    assert result.json() == {"status": "ok"}


test_health_check()
_LOG.info("test_health_check() passed.")
