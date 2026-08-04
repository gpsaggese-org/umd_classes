#!/usr/bin/env bash
# """
# Regenerate the class links pages under `website/docs/class_links/` by
# running `class_scripts/publish_class_links.py` for each course/book.
#
# Usage:
# > ./website/update_class_links.sh
# """
set -euo pipefail

# Course/book directories to scan for lessons, one `--dir` per generated page.
DIRS=("data605" "msml610" "book_springer")

OUT_DIR="website/docs/class_links"

for dir in "${DIRS[@]}"; do
    out_file="${OUT_DIR}/${dir}.links.html"
    ./class_scripts/publish_class_links.py \
        --dir "$dir" \
        --out_file "$out_file" \
        --do_not_fail_on_warnings \
        --use_master
done
