\cp -f ../figures/*.png .
for file in *.png; do
  echo "Processing $file"
  du -h "$file"
  #magick "$file" -strip -quality 80 -define png:compression-level=9 "$file"
  pngquant --quality=60-80 --ext .png --force "$file" && oxipng -o6 "$file"
  du -h "$file"
  echo
done
