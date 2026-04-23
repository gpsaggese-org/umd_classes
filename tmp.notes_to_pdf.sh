#/bin/bash -xe
# cleanup_before
## skipping this action
# preprocess_notes
/Users/saggese/src/umd_classes1/helpers_root/dev_scripts_helpers/documentation/preprocess_notes.py --input msml610/lectures_source/Lesson08.4.txt --output /Users/saggese/src/umd_classes1/msml610/lectures/tmp.notes_to_pdf.preprocess_notes.txt --type slides --toc_type navigation
# render_images
/Users/saggese/src/umd_classes1/helpers_root/dev_scripts_helpers/documentation/render_images.py --input /Users/saggese/src/umd_classes1/msml610/lectures/tmp.notes_to_pdf.preprocess_notes.txt --output /Users/saggese/src/umd_classes1/msml610/lectures/tmp.notes_to_pdf.render_image.txt
# run_pandoc
docker run --rm --user $(id -u):$(id -g) -e AM_GDRIVE_PATH -e AM_TELEGRAM_TOKEN -e CSFY_AWS_PROFILE -e CSFY_AWS_S3_BUCKET -e CSFY_ECR_BASE_PATH -e CSFY_HOST_NAME -e CSFY_HOST_OS_NAME -e CSFY_HOST_OS_VERSION -e CSFY_HOST_USER_NAME -e OPENAI_API_KEY -e OPENROUTER_API_KEY -e QUANDL_API_KEY --workdir /app --mount type=bind,source=/Users/saggese/src/umd_classes1,target=/app tmp.pandoc_texlive.arm64.8689d816 /app/msml610/lectures/tmp.notes_to_pdf.render_image2.txt --output /app/msml610/lectures/tmp.notes_to_pdf.render_image2.pdf -t beamer --slide-level 4 -V theme:SimplePlus --include-in-header=latex_abbrevs.sty --fail-if-warnings --resource-path=msml610/lectures
# compress_pdf
## skipping this action
\cp -af /Users/saggese/src/umd_classes1/msml610/lectures/tmp.notes_to_pdf.render_image2.pdf msml610/lectures/Lesson08.4.pdf
# copy_to_gdrive
## skipping this action
# open
# cleanup_after
## skipping this action