#!/bin/bash -e
dir="data605/lectures_video_script/"
for f in "$dir"/*; do
    if [[ -f "$f" ]]; then
        printf "%s\t%s\n" "$(basename "$f")" "$(wc -w < "$f")"
    fi
done
