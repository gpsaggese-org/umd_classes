#!/bin/bash
# Find published blog posts (draft: false) sorted by date.
# Usage: ./website/find_published_blogs.sh

results=()
for f in website/docs/blog/posts/*.md; do
  draft=$(grep -i "^draft:" "$f" | awk '{print $2}')
  if [ "$draft" = "false" ]; then
    date=$(grep -i "^date:" "$f" | sed 's/^date: *//')
    results+=("$date|$f")
  fi
done

# Sort by date descending (most recent first) and print formatted output
printf "%s\n" "${results[@]}" | sort -t"|" -k1,1 -r | while IFS="|" read -r date path; do
  echo "- $date: \`$path\`"
done