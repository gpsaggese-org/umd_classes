Step 1
create a script called compress_pdf.py using a dockerized version the code
in compress_pdf() in
./helpers_root/dev_scripts_helpers/documentation/lib_notes_to_pdf.py
if --backend "ghostscript_global"

Step 2
if --backend "ghostscript_dockerized"

docker pull minidocks/ghostscript
docker run --rm -v "$(pwd)":/data minidocks/ghostscript \
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
     -dNOPAUSE -dBATCH -dQUIET \
     -sOutputFile=/data/compressed.pdf /data/original.pdf

using the infrastructure already present in hdocker.py

## Plan
- [x] Step 1: create `compress_pdf.py`
  - [x] Add CLI script `helpers_root/dev_scripts_helpers/documentation/compress_pdf.py`
    following the `_parse()`/`_main()` script conventions
  - [x] Add `--input`/`-i`, `--output`/`-o` (default: overwrite `--input` in
    place), `--quality`, and `--backend` (choices: `ghostscript_global`,
    `ghostscript_dockerized`) CLI args
  - [x] Implement the `ghostscript_global` backend, adapted from
    `compress_pdf()` in `lib_notes_to_pdf.py` (host `gs` binary, not Docker)
  - [x] Have `ghostscript_dockerized` raise `NotImplementedError` (left for
    step 2)
  - [x] Add unit tests `helpers_root/dev_scripts_helpers/documentation/test/test_compress_pdf.py`
  - [x] `git add` the new files (no commit)
- [ ] Step 2 (not requested this run): implement `ghostscript_dockerized`
  backend using `helpers/hdocker.py`

## Result
- Done: created `compress_pdf.py` with a `--backend` flag; implemented the
  `ghostscript_global` path
  - Adapted `compress_pdf()` from `lib_notes_to_pdf.py`: same `gs` flags
    (`-sDEVICE=pdfwrite -dPDFSETTINGS=<quality> -dNOPAUSE -dQUIET -dBATCH`),
    generalized to support `--output` (not just in-place) via a
    `<output>.compressed.tmp` intermediate file
  - Found and fixed a real bug during testing: on this repo's thin client, a
    bare `gs` on `PATH` resolves to `dev_scripts_helpers/git/gs` (a `git
    status` alias), not Ghostscript, since that dir is ahead of
    `/opt/homebrew/bin` on `PATH`. Added `_find_gs_binary()`, which checks
    known Ghostscript install paths first, falling back to a plain `PATH`
    lookup
  - Verified end-to-end on a real PDF (`msml610/lectures_pdf/Lesson01.1-Intro.pdf`
    copy): compressed 1.5MB -> 616KB in place
  - Added `test_compress_pdf.py` (6 tests, all passing) covering
    `_find_gs_binary()`, `_compress_pdf_ghostscript_global()` (in-place and
    separate output file, via `capture_sys_calls`), and the CLI end-to-end
    (default backend, and `ghostscript_dockerized` raising
    `NotImplementedError`)
  - `git add`ed `compress_pdf.py` and its test file in `helpers_root` (not
    committed)
- Not done: Step 2 (`ghostscript_dockerized` backend) — out of scope for
  this run (`ARGUMENTS: step 1`); the `--backend` flag already has the
  choice wired up and raises `NotImplementedError` until implemented
