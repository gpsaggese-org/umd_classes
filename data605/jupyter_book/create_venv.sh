#!/bin/bash -xe

# Shared with msml610/jupyter_book and tutorials/jupyter_book: all books build
# with the same jupyter-book version, so they reuse one venv.
DIR="~/src/venv/client_venv.jupyter_book2"

SCRIPT_PATH="$(realpath "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

python3 -m venv $DIR
source $DIR/bin/activate
pip install -r $SCRIPT_DIR/requirements.txt
