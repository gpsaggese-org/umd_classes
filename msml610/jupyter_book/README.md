# MSML610 Jupyter Book

- This directory is a [Jupyter Book](https://jupyterbook.org/) (v2, powered by
  [mystmd](https://mystmd.org/)) project that renders all the MSML610 tutorial
  notebooks in [`../tutorials`](../tutorials) as a browsable website.

- The table of contents is defined in `myst.yml` and references the notebooks in
  place (via `../tutorials/...` paths): nothing is copied or duplicated.

## Installation

- Create the dedicated virtual environment and install `jupyter-book` v2:
  ```bash
  > ./create_venv.sh
  ```

- Activate it in a new shell:
  ```bash
  > source ./setenv.sh
  ```

## Render

### Local live preview

- From this directory, start the live-reload dev server:
  ```bash
  > jupyter-book start
  ```
- The book is served at `http://localhost:3000` and rebuilds as notebooks
  under `../tutorials` or files in this directory change.

### Static HTML build

- Build a fully static export of the site:
  ```bash
  > jupyter-book build --html
  ```
- Output is written to `_build/html/` (git-ignored). Notebooks are
  re-executed on build (`jupyter.execute: true` in `myst.yml`), so the
  tutorials' dependencies must be installed in the active environment.

## Publish via the website's MkDocs site

The rendered book is published as a static sub-site inside the personal
website in [`$GIT_ROOT/website`](../../website), which is built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). MkDocs
copies any non-Markdown files under `website/docs/` into the built site
as-is (the same mechanism used for `website/docs/class_links/*.html`), so
publishing is just: build the book, drop its static output under
`website/docs/`, then build/deploy the website as usual.

1. Build the static book (see above):
   ```bash
   > jupyter-book build --html
   ```

2. Copy the build output into the website's docs tree, under a
   `jupyter_books/msml610` sub-path:
   ```bash
   > rm -rf ../../website/docs/jupyter_books/msml610
   > mkdir -p ../../website/docs/jupyter_books
   > cp -r _build/html ../../website/docs/jupyter_books/msml610
   ```

3. Preview the full website locally:
   ```bash
   > cd ../../website
   > mkdocs serve
   # or: ./preview_website.sh
   ```
   The book is available at `http://127.0.0.1:8000/jupyter_books/msml610/`.

4. Deploy to GitHub Pages:
   ```bash
   > cd ../../website
   > mkdocs gh-deploy
   # or: ./publish_website.sh
   ```
   The book is then live at
   `https://gpsaggese.github.io/jupyter_books/msml610/`.

The book is not added to `nav:` in `website/mkdocs.yml`, so it is reachable
by direct link but does not appear in the site's top navigation: the same
treatment given to `class_links`.
