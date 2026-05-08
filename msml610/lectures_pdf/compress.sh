#quality="/ebook"
quality="/printer"
for f in Lesson*.pdf; do
  echo $f
  dst_file="compressed2-$f"
  /opt/homebrew/bin/gs -sDEVICE=pdfwrite -dPDFSETTINGS=$quality -dNOPAUSE -dQUIET -dBATCH \
      -sOutputFile="$dst_file" "$f"
  du -h $f
  du -h $dst_file
done
