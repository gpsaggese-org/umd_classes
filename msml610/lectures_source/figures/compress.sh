#\cp -f ../figures/*.png .

if [[ 0 == 1 ]]; then
for file in *.png; do
  echo "Processing $file"
  du -h "$file"
  #magick "$file" -strip -quality 80 -define png:compression-level=9 "$file"
  pngquant --quality=60-80 --ext .png --force "$file" && oxipng -o6 "$file"
  du -h "$file"
  echo
done
fi;

if [[ 1 == 1 ]]; then
find . -maxdepth 1 -type f -name "*.png" -size +1M | while read file; do
  echo "Processing: $file"

  echo -n "Before: "
  du -h "$file"

  jpg="${file%.png}.jpg"
  magick "$file" -background white -alpha remove -quality 85 "$jpg"

  echo -n "After:  "
  du -h "$jpg"

  rm "$file"
  echo
done
fi;
