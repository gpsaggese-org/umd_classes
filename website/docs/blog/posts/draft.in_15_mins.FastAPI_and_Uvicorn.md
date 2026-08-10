---
title: "FastAPI and Uvicorn in 15 mins"
draft: true
authors:
    - gpsaggese
date: 2026-08-10
description:
categories:
    - Python
    - Software Engineering
---

TL;DR `FastAPI` is a modern Python framework for building APIs with automatic
validation and docs, and `uvicorn` is the ASGI server that runs it.

<!-- more -->

## Introduction

- `FastAPI` is a Python web framework for building APIs
    - Uses standard Python type hints to validate requests and responses
    - Generates interactive API documentation automatically (Swagger UI and
      ReDoc)
    - Runs on `asyncio`, so it handles many concurrent requests efficiently
- `uvicorn` is the server that actually runs a `FastAPI` app
    - `FastAPI` only defines routes and logic: it doesn't listen on a socket
    - `uvicorn` implements the ASGI protocol and accepts HTTP connections,
      then hands each request to the `FastAPI` app
    - The two are almost always used together, the same way `Flask` is used
      together with `gunicorn`

- Why engineers care:
    - **Fewer bugs**: type hints double as request/response validation, so
      malformed input is rejected before it reaches your code
    - **Free documentation**: every endpoint shows up in an interactive
      `/docs` page, so there's no separate API spec to maintain by hand
    - **Performance**: built on `Starlette` and `Pydantic`, `FastAPI` is one
      of the fastest Python frameworks available, close to Node.js and Go for
      I/O-bound workloads
    - **Async native**: first-class support for `async def` endpoints, useful
      when calling databases, other APIs, or LLM services

- When to use it:
    - Building a JSON REST API or a microservice
    - Serving an ML model behind an HTTP endpoint
    - Any backend where request validation and API docs save real time
    - Not the best fit for a server-rendered, template-heavy website: `Django`
      or `Flask` with Jinja2 are more mature for that use case

- Similar tools:
    - `Flask`: simpler, synchronous by default, no built-in validation
    - `Django REST Framework`: full batteries-included stack, more setup, more
      opinionated
    - `Litestar`: another ASGI framework with a similar feature set
    - `gunicorn`: production process manager, often paired with `uvicorn`
      workers instead of used alone

- Official resources:
    - Installation: <https://fastapi.tiangolo.com/#installation>
    - Documentation: <https://fastapi.tiangolo.com/>
    - Tutorial: <https://fastapi.tiangolo.com/tutorial/>
    - `uvicorn` documentation: <https://www.uvicorn.org/>

## Prerequisites

- Python
- Basic HTTP knowledge: GET/POST, status codes, JSON
- Comfort with Python type hints helps but isn't required
- `pip` or `uv` for installing packages

## Installation

- Create and activate a virtual environment:

    ```bash
    > python3 -m venv .venv
    > source .venv/bin/activate
    ```

- Install `fastapi` and `uvicorn`:

    ```bash
    > pip install fastapi "uvicorn[standard]"
    ```

    - The `[standard]` extra pulls in `uvloop` and `httptools`, which make
      `uvicorn` significantly faster

- With `uv` instead:
    ```bash
    > uv pip install fastapi "uvicorn[standard]"
    ```

- Verify the installation:

    ```bash
    > python -c "import fastapi; print(fastapi.__version__)"
    0.115.6

    > uvicorn --version
    Running uvicorn 0.34.0 with CPython 3.11.9 on Darwin
    ```

## Core Concepts

- **ASGI over WSGI**: `FastAPI` and `uvicorn` speak ASGI (Asynchronous Server
  Gateway Interface), the async successor to WSGI
  - ASGI lets a single worker handle many concurrent connections without blocking
    on I/O, unlike the one-request-per-thread model of WSGI servers like
    `gunicorn` running `Flask`
- **Path operations**: a `FastAPI` app is a set of functions decorated with an
  HTTP method and a path, e.g., `@app.get("/items/{id}")`
  - `FastAPI` reads the function's type hints to know what to validate and what
    to return.
- **Pydantic models**: request bodies and responses are described as Python
  classes with typed fields. `FastAPI` validates incoming JSON against these
  classes and returns a clear error if it doesn't match.

- How a request flows through the stack:

    ```mermaid
    flowchart LR
        Client -->|HTTP request| Uvicorn
        Uvicorn -->|ASGI call| FastAPI["FastAPI app"]
        FastAPI -->|route + validate| Handler["your endpoint function"]
        Handler -->|response| FastAPI
        FastAPI -->|ASGI response| Uvicorn
        Uvicorn -->|HTTP response| Client
    ```

## Your First API

- Create `main.py`:

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "Hello, World"}
    ```

- Run it with `uvicorn`:

    ```bash
    > uvicorn main:app --reload
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process
    INFO:     Application startup complete.
    ```

    - `main:app` means "the `app` object inside `main.py`"
    - `--reload` restarts the server on code changes, useful only in
      development

- Test it in another terminal:

    ```bash
    > curl http://127.0.0.1:8000/
    {"message":"Hello, World"}
    ```

## Path and Query Parameters

- Path parameters are typed directly in the function signature:

    ```python
    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}
    ```

    ```bash
    > curl http://127.0.0.1:8000/items/42
    {"item_id":42}

    > curl http://127.0.0.1:8000/items/not_a_number
    {"detail":[{"type":"int_parsing", "loc":["path","item_id"], ...}]}
    ```

    - Passing a non-integer returns a `422 Unprocessable Entity` automatically:
      no manual validation code needed

- Query parameters are function arguments not in the path, with defaults for
  optional ones:

    ```python
    @app.get("/items/")
    def list_items(skip: int = 0, limit: int = 10):
        return {"skip": skip, "limit": limit}
    ```

    ```bash
    > curl "http://127.0.0.1:8000/items/?skip=5&limit=20"
    {"skip":5,"limit":20}
    ```

## Request Body and Validation

- Define the expected shape of a request body as a `Pydantic` model:

    ```python
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        price: float
        in_stock: bool = True


    @app.post("/items/")
    def create_item(item: Item):
        return item
    ```

- Send a request with a JSON body:

    ```bash
    > curl -X POST http://127.0.0.1:8000/items/ \
        -H "Content-Type: application/json" \
        -d '{"name": "Widget", "price": 9.99}'
    {"name":"Widget","price":9.99,"in_stock":true}
    ```

- Omit a required field and `FastAPI` rejects the request before your code
  runs:

    ```bash
    > curl -X POST http://127.0.0.1:8000/items/ \
        -H "Content-Type: application/json" \
        -d '{"name": "Widget"}'
    {"detail":[{"type":"missing", "loc":["body","price"], "msg":"Field required"}]}
    ```

## Automatic Interactive Docs

- With the server running, open in a browser:
    - `http://127.0.0.1:8000/docs`: interactive Swagger UI, lets you call
      endpoints directly from the page
    - `http://127.0.0.1:8000/redoc`: ReDoc, a read-only reference view
    - `http://127.0.0.1:8000/openapi.json`: the raw OpenAPI schema

- These pages update automatically as you add or change endpoints: there's no
  separate spec file to keep in sync

## Running with Uvicorn

- Development: auto-reload on file changes

    ```bash
    > uvicorn main:app --reload
    ```

- Production-like local run: bind to all interfaces, use multiple workers

    ```bash
    > uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    ```

    - Each worker is a separate process handling its own connections
    - For real production deployments, most teams still front `uvicorn`
      workers with `gunicorn` for process management, or use a container
      orchestrator that restarts crashed processes

- Run it programmatically instead of from the CLI:

    ```python
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    ```

    ```bash
    > python main.py
    ```

## Async Endpoints

- A path operation can be `def` or `async def`:

    ```python
    @app.get("/sync-example")
    def sync_endpoint():
        return {"type": "sync"}


    @app.get("/async-example")
    async def async_endpoint():
        return {"type": "async"}
    ```

- How `FastAPI` treats each:
    - `def` endpoints run in a thread pool, so a slow one doesn't block other
      requests
    - `async def` endpoints run directly on the event loop, so they can serve
      thousands of concurrent requests with a single worker
- Use `async def` when the endpoint awaits I/O with an async library, e.g.,
  `httpx`, `asyncpg`, or an async database driver
- Use plain `def` for CPU-bound or blocking code, or when using a sync-only
  library like `requests` or the standard `psycopg2`

## Handling Errors

- Raise `HTTPException` to return a specific status code and message:

    ```python
    from fastapi import HTTPException

    items_db = {1: "Widget", 2: "Gadget"}


    @app.get("/items/{item_id}")
    def get_item(item_id: int):
        if item_id not in items_db:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item_id": item_id, "name": items_db[item_id]}
    ```

    ```bash
    > curl -i http://127.0.0.1:8000/items/99
    HTTP/1.1 404 Not Found
    {"detail":"Item not found"}
    ```

## Testing Your API

- `FastAPI` ships a `TestClient` built on `httpx`, so tests run without a live
  server:

    ```python
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)


    def test_read_root():
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, World"}
    ```

    ```bash
    > pytest test_main.py -v
    test_main.py::test_read_root PASSED
    ```

## Common Gotchas

- Blocking calls inside `async def` stall the whole worker
    - E.g., calling `time.sleep()` or `requests.get()` inside `async def`
      blocks every other concurrent request on that worker
    - Fix: use the async version of the library, or keep the endpoint as plain
      `def`
- `--reload` is a development-only flag
    - It watches the filesystem and adds overhead, so don't run it in
      production
- CORS needs an explicit middleware
    - Browsers block cross-origin requests by default; add
      `fastapi.middleware.cors.CORSMiddleware` and list allowed origins
- `Pydantic` version matters
    - `Pydantic` v2 changed some APIs from v1 (e.g., `.dict()` became
      `.model_dump()`); check which major version a tutorial targets

## FastAPI vs Other Frameworks

| Feature             | FastAPI      | Flask         | Django REST Framework |
| :------------------ | :----------- | :------------ | :--------------------- |
| Protocol             | ASGI (async) | WSGI (sync)   | WSGI (sync)             |
| Request validation   | Built-in     | Manual/plugin | Serializers              |
| Interactive docs     | Built-in     | Plugin        | Plugin                    |
| Learning curve       | Low          | Low           | Medium/High                |
| Best for             | APIs, ML     | Small apps    | Full-stack apps              |

- `FastAPI` and `uvicorn` are a good default for a new Python API in 2026:
  they cover validation, docs, and performance out of the box, with less
  boilerplate than the alternatives
