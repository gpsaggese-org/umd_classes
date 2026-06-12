#!/bin/bash
FILE=$1
echo "Processing $FILE ..."
MODEL="deepseek/deepseek-v4-flash"
cc --model $MODEL -p "/coding.todoai_gp $FILE"
cc --model $MODEL -p "/blog.humanize $FILE"
cc --model $MODEL -p "/blog.add_links $FILE"
