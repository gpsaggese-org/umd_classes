#!/bin/bash -xe
cd website
# --no-history squashes the gh-pages branch to a single commit per deploy
# instead of appending one, so it doesn't grow forever (the site embeds the
# large generated Jupyter Books under docs/jupyter_books/).
mkdocs gh-deploy --no-history
open https://gpsaggese.github.io/
