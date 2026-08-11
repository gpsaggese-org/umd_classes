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
# # FastAPI: Book Catalog API
#
# This notebook builds and runs a small "Book Catalog" REST API end to end:
# - `fastapi_utils.create_book_app()` builds the `FastAPI` app
# - `fastapi_utils.run_server_in_background()` serves it with a real
#   `uvicorn` server, on a background thread so the rest of the notebook can
#   keep running
# - `httpx` drives the app over real HTTP, the same way a browser or another
#   service would
#
# This is the production-shaped path.
# - `fastapi.API.ipynb` covers the same app's building blocks in-process with
#     `TestClient`, which is faster for exploration but skips the network entirely.
#
# **Must run top to bottom after a kernel restart.**

# %%
# !pip install --quiet -r tutorial_requirements.txt

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import httpx

import fastapi_utils
import helpers.hdbg as hdbg
import helpers.hintrospection as hintros

hdbg.init_logger(verbosity=logging.INFO)
_LOG = logging.getLogger(__name__)

PORT = 8010
BASE_URL = f"http://127.0.0.1:{PORT}"

# %% [markdown]
# ## Part 1: Build the App
#
# `create_book_app()` wires up the routes and seeds an in-memory catalog.
# Listing `app.routes` shows exactly what got registered, which is a useful
# sanity check before starting the server.

# %%
hintros.print_obj_info(fastapi_utils.create_book_app)

# %%
# Build the app: wires up the routes and seeds the in-memory catalog.
app = fastapi_utils.create_book_app()

for route in app.routes:
    methods = ",".join(sorted(getattr(route, "methods", []) or []))
    _LOG.info("%-6s %s", methods, getattr(route, "path", route))
# Outcome: `app` is a ready-to-serve `FastAPI` instance; the log lists every
# registered route, including the built-in `/docs`, `/redoc`, and
# `/openapi.json`, plus the catalog's `/health` and `/books` routes.

# %% [markdown]
# ## Part 2: Start the Server
#
# `run_server_in_background()` starts `uvicorn` on a daemon thread.
# `wait_for_server()` polls `/health` until the socket accepts connections,
# so the next cell never races the server startup.

# %%
# Start `uvicorn` on a daemon thread, then block until `/health` responds.
server, server_thread = fastapi_utils.run_server_in_background(app, port=PORT)
fastapi_utils.wait_for_server(f"{BASE_URL}/health")
_LOG.info("Server is up at %s", BASE_URL)
# Outcome: the server is accepting real TCP connections at `BASE_URL`.

# %% [markdown]
# ## Part 3: List and Filter Books
#
# These are real HTTP requests: `httpx` opens a TCP connection to
# `127.0.0.1:8010` instead of calling the app object directly.

# %%
# List every book in the catalog.
response = httpx.get(f"{BASE_URL}/books")
response.raise_for_status()
_LOG.info("All books: %s", [book["title"] for book in response.json()])
# Outcome: all 3 seeded books, in insertion order.

# Filter to only out-of-stock books via the `in_stock` query parameter.
response = httpx.get(f"{BASE_URL}/books", params={"in_stock": False})
_LOG.info("Out-of-stock books: %s", [book["title"] for book in response.json()])
# Outcome: just "Designing Data-Intensive Applications", the only seed book
# marked out of stock.

# Cap the result to one book via the `limit` query parameter.
response = httpx.get(f"{BASE_URL}/books", params={"limit": 1})
_LOG.info("First book only: %s", [book["title"] for book in response.json()])
# Outcome: only "Fluent Python", the first seeded book.

# %% [markdown]
# ## Part 4: Create, Update, and Delete a Book

# %%
# Create a new book; the server assigns the `id`.
response = httpx.post(
    f"{BASE_URL}/books",
    json={"title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "year": 1999},
)
response.raise_for_status()
new_book = response.json()
_LOG.info("Created book %s: %s", new_book["id"], new_book["title"])
# Outcome: 201 Created; `new_book["id"]` is 4, the next free ID after the
# 3 seeded books.

# %%
# Replace the new book's fields, flipping it to out of stock.
response = httpx.patch(
    f"{BASE_URL}/books/{new_book['id']}",
    json={
        "title": new_book["title"],
        "author": new_book["author"],
        "year": new_book["year"],
        "in_stock": False,
    },
)
response.raise_for_status()
_LOG.info("Updated book: %s", response.json())
# Outcome: 200 OK; the same book is returned with `in_stock` now `False`.

# %%
# Delete the book that was just created and updated.
response = httpx.delete(f"{BASE_URL}/books/{new_book['id']}")
_LOG.info("DELETE status: %s", response.status_code)
# Outcome: 204 No Content; the book is removed from the catalog.

# Confirm the deletion: the same ID should no longer resolve.
response = httpx.get(f"{BASE_URL}/books/{new_book['id']}")
_LOG.info("GET after delete: %s", response.status_code)
# Outcome: 404 Not Found.

# %% [markdown]
# ## Part 5: Handle Errors
#
# A missing book returns `404`; an invalid payload never reaches the handler
# and returns `422` with a description of what failed.

# %%
# Look up a book ID that was never created.
response = httpx.get(f"{BASE_URL}/books/99999")
_LOG.info("GET missing book -> %s %s", response.status_code, response.json())
# Outcome: 404 Not Found with {"detail": "Book 99999 not found"}.

# Send a payload missing the required `author` and `year` fields.
response = httpx.post(f"{BASE_URL}/books", json={"title": "No Author or Year"})
_LOG.info("POST invalid payload -> %s", response.status_code)
for error in response.json()["detail"]:
    _LOG.info("  %s: %s", error["loc"], error["msg"])
# Outcome: 422 Unprocessable Entity; the handler never runs, and the
# response lists both missing fields.

# %% [markdown]
# ## Part 6: Inspect the Live Docs
#
# With the server running, `/openapi.json` is reachable over HTTP, and so are
# the human-facing `/docs` (Swagger UI) and `/redoc` pages. Point a browser at
# `http://127.0.0.1:8010/docs` while this notebook's server is up to try it
# interactively.

# %%
# Fetch the OpenAPI schema `FastAPI` generated automatically.
response = httpx.get(f"{BASE_URL}/openapi.json")
schema = response.json()
_LOG.info("OpenAPI title: %s", schema["info"]["title"])
_LOG.info("Registered paths: %s", sorted(schema["paths"].keys()))
# Outcome: title "Book Catalog API"; paths are /books, /books/{book_id},
# and /health.

# %% [markdown]
# ## Part 7: Shut Down the Server
#
# Always stop the background server before the kernel exits, so the port is
# freed for the next run.

# %%
# Stop the background `uvicorn` server and join its thread.
fastapi_utils.stop_server(server, server_thread)
_LOG.info("Server thread alive: %s", server_thread.is_alive())
# Outcome: `False`; the server thread has exited and the port is freed.

# %% [markdown]
# ## Wrap-up
#
# This notebook covered the full lifecycle of a `FastAPI` service: build the
# app, serve it with `uvicorn`, call it over real HTTP, and shut it down
# cleanly. See `README.md` for how to run the same app from the command line
# with `uvicorn fastapi_utils:app --reload` instead of from a notebook.
