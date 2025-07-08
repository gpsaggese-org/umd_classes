#!/bin/bash -e

# MSML610/example.txt
# MSML610/Gallery.txt

# > ls -1 MSML610/Lesson*
FILES=$(ls -1 MSML610/Lesson*)

for FILE in $FILES; do
    echo
    echo "# #############################################################################"
    echo "# $FILE"
    echo "# #############################################################################"
    cmd="extract_headers_from_markdown.py -i $FILE"
    eval $cmd
done
