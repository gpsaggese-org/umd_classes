When running

notes_to_pdf.py --input=msml610/lectures_source/Lesson13.1-Explainability.txt --output=output.tex --type=slides --toc_type=navigation --slides_engine=beamer --skip_action=cleanup_after --skip_action=open --no_pdf

There are 2 problems that need to be fixed

1) the command fails "Failing because there were warnings." but the script
   continues, which is incorrect

```
################################################################################
action=run_pandoc
################################################################################
> container run --rm --user $(id -u):$(id -g) -e AM_GDRIVE_PATH -e AM_TELEGRAM_TOKEN -e ARTIFICIAL_ANALYSIS_API_KEY -e CSFY_AWS_PROFILE -e CSFY_AWS_S3_BUCKET -e CSFY_ECR_BASE_PATH -e CSFY_HOST_NAME -e CSFY_HOST_OS_NAME -e CSFY_HOST_OS_VERSION -e CSFY_HOST_USER_NAME -e OPENAI_API_KEY -
e QUANDL_API_KEY --workdir /app --mount type=bind,source=/Users/saggese/src/umd_classes2,target=/app tmp.pandoc_texlive.arm64.9a4bae9a /app/tmp.notes_to_pdf.render_image2.txt --output /app/tmp.notes_to_pdf.render_image2.tex -t beamer --slide-level 4 -V theme:SimplePlus --include-in-he
ader=latex_abbrevs.sty --fail-if-warnings --resource-path=.
[0/6] [0s]
[1/6] Fetching image [0s]
[2/6] Unpacking image [0s]
[3/6] Fetching kernel [0s]
[4/6] Fetching init image [0s]
[5/6] Unpacking init image [0s]
[6/6] Starting container [0s]
[6/6] Starting container [1s]
[6/6] Starting container [2s]
[6/6] Starting container [3s]
[6/6] Starting container [4s]
[6/6] Starting container [5s]
[6/6] Starting container [6s]
[WARNING] Div at /app/tmp.notes_to_pdf.render_image2.txt line 807 column 1 unclosed at /app/tmp.notes_to_pdf.render_image2.txt line 837 column 1, closing implicitly.
[WARNING] Div at /app/tmp.notes_to_pdf.render_image2.txt line 806 column 1 unclosed at /app/tmp.notes_to_pdf.render_image2.txt line 837 column 1, closing implicitly.
Failing because there were warnings.
[0/6] [0s]
[1/6] Fetching image [0s]
[2/6] Unpacking image [0s]
[3/6] Fetching kernel [0s]
[4/6] Fetching init image [0s]
[5/6] Unpacking init image [0s]
[6/6] Starting container [0s]
[6/6] Starting container [1s]
[6/6] Starting container [2s]
[6/6] Starting container [3s]
[6/6] Starting container [4s]
[6/6] Starting container [5s]
[6/6] Starting container [6s]
[WARNING] Div at /app/tmp.notes_to_pdf.render_image2.txt line 807 column 1 unclosed at /app/tmp.notes_to_pdf.render_image2.txt line 837 column 1, closing implicitly.
[WARNING] Div at /app/tmp.notes_to_pdf.render_image2.txt line 806 column 1 unclosed at /app/tmp.notes_to_pdf.render_image2.txt line 837 column 1, closing implicitly.
Failing because there were warnings.
```

2) There are warnings that should be debugged

[WARNING] Div at /app/tmp.notes_to_pdf.render_image2.txt line 807 column 1 unclosed at /app/tmp.notes_to_pdf.render_image2.txt line 837 column 1, closing implicitly.
[WARNING] Div at /app/tmp.notes_to_pdf.render_image2.txt line 806 column 1 unclosed at /app/tmp.notes_to_pdf.render_image2.txt line 837 column 1, closing implicitly.

Find an explanation for both issues
