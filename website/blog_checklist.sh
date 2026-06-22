#!/bin/bash
FILE=$1
echo "Processing $FILE ..."
#MODEL="--model deepseek/deepseek-v4-flash"
MODEL=""
#cc --model $MODEL -p "/coding.todoai_gp $FILE"
cc $MODEL -p "/blog.humanize $FILE"
cc $MODEL -p "/blog.add_links $FILE"
website/publish_blog.py --file $FILE
