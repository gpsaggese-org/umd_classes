# Summary
A comprehensive suite of command-line tools and scripts for managing university
courses, generating lecture materials (slides, scripts, quizzes), and improving
slide quality through automated LLM-powered transformations

## Structure of the Dir
- `lectures_commentary/`: Output directory for lecture commentary
- `lectures_quizzes/`: Output directory for multiple choice quiz files
- `lectures_recap/`: Output directory for discussion and recap question files
- `lectures_video_script/`: Output directory for generated script files
- `lectures_source/`: Input directory containing `Lesson*.txt` files
- `lectures_pdf/`: Output directory for generated PDF files

## Description of Files
- `common_utils.py`: Shared utility functions for argument validation, file
  finding, directory management, and PDF page counting

- The scripts implement the following functions:
  - _Analysis_: Counting and Analysis Scripts
  - _Generation_: Generation Scripts
  - _Improvement_: Slide Improvement Scripts
  - _Processing_: Image and PDF Processing Scripts
  - _Test_: Test Utilities
  - _Utility_: Utility Scripts
  - _Orchestration_: Orchestration Scripts

- Under `class_scripts`

| Script                              | Goal          | Function                                                             |
| :---------------------------------- | :------------ | :------------------------------------------------------------------- |
| `common_utils.py`                   | Utility       | Argument validation, file finding, directory management              |
| `count_lecture_commentary_pages.py` | Analysis      | Count pages in book PDFs                                             |
| `count_lecture_slides.py`           | Analysis      | Count slides, headers, lines, words, and characters in source files  |
| `count_lecture_pages.py`            | Analysis      | Count pages in lecture PDFs                                          |
| `count_words.py`                    | Analysis      | Count words in lecture scripts                                       |
| `extract_png_from_pdf.py`           | Processing    | Extract PDF pages as PNG images with customizable DPI                |
| `gen_lecture_commentary.py`         | Generation    | Generate book chapters from lecture source material                  |
| `gen_lecture_script.py`             | Generation    | Generate lecture scripts from slides with intro/outro sections       |
| `gen_quizzes.py`                    | Generation    | Generate quizzes (20 MC) or discussion questions (3-6) from lectures |
| `gen_slides.py`                     | Generation    | Generate lecture slide PDFs from source files                        |
| `gen_slides_test_utils.py`          | Test          | Helper functions for slide generation testing and validation         |
| `generate_book_chapter.py`          | Generation    | Generate book chapters from markdown and PDF/PNG images              |
| `generate_class_images.py`          | Generation    | Generate images using DALL-E from text prompts                       |
| `generate_slide_script.py`          | Generation    | Generate lecture scripts from slide content with LLM                 |
| `get_lecture_file.py`               | Utility       | Find and print path to lecture source file                           |
| `create_book_toc_from_slides.py`    | Generation    | Extract table of contents from lecture slides                        |
| `for_loop_lessons.py`               | Orchestration | Main orchestrator for generating PDFs, scripts, and materials        |
| `for_loop_slides.py`                | Orchestration | Transform slides using LLM with specified rules                      |
| `process_slides.py`                 | Processing    | Process slides with LLM transformations (reduce, check, improve)     |
| `slide_check.py`                    | Quality       | Check and fix text in lecture slides (spelling, grammar)             |
| `slide_improve.py`                  | Quality       | Improve slides using LLM suggestions                                 |
| `slide_reduce.py`                   | Quality       | Reduce and simplify slides using LLM                                 |
| `slides_utils.py`                   | Utility       | Extract and process slide content                                    |

- Under `helpers_root/dev_scripts_helpers/documentation`

| Script                | Description                                                            |
| :-------------------- | :--------------------------------------------------------------------- |
| `concatenate_pdfs.py` | Combines multiple PDF files into one (creates full book from chapters) |
| `lint_txt.py`         | Lints and formats text using prettier; used for quiz output            |
| `notes_to_pdf.py`     | Converts markdown to PDF (slides, documents); used by gen_slides.py    |

## Script Dependency Hierarchy

- `for_loop_lessons.py` (Main orchestrator)
  - action=`generate_pdf`
    - `notes_to_pdf.py`
  - action=`generate_tex`
    - `notes_to_pdf.py`
  - action=`generate_script`
    - `generate_slide_script.py`
    - `lint_txt.py`
  - action=`reduce_slide`
    - `process_slides.py`
  - action=`check_slide`
    - `process_slides.py`
  - action=`improve_slide` (not yet implemented)
  - action=`generate_book_chapter`
    - `gen_lecture_commentary.py`
  - action=`generate_class_quizzes`
    - `gen_quizzes.py`
  - action=`generate_class_recap`
    - `gen_quizzes.py`
  - action=`generate_toc`
    - `extract_toc_from_txt.py`

- **Wrapper/Convenience Scripts**
  - `gen_slides.py`
    - `notes_to_pdf.py`
  - `gen_lecture_script.py`
    - `generate_slide_script.py`
    - `llm_cli.py`
    - `lint_txt.py`
  - `gen_lecture_commentary.py`
    - `notes_to_pdf.py`
    - `generate_book_chapter.py`
  - `slide_check.py`
    - `process_slides.py`
  - `slide_improve.py`
    - `process_slides.py`
  - `slide_reduce.py`
    - `process_slides.py`

- **Quiz/Assessment Generation**
  - `gen_quizzes.py`
    - `llm_cli.py`
    - `lint_txt.py`

- **Standalone Analysis/Utility Scripts** (no dependencies on other scripts)
  - `count_lecture_pages.py`
  - `count_lecture_commentary_pages.py`
  - `count_lecture_slides.py`
  - `count_words.py`
  - `get_lecture_file.py`
  - `extract_png_from_pdf.py`
  - `generate_class_images.py`

# Counting and Analysis Scripts

## `class_scripts/count_lecture_commentary_pages.py`

- Counts pages in all PDF files in the `{DIR}/book/` directory using macOS
  `mdls` command to extract PDF metadata
- Count pages for a specific class:
  ```bash
  > count_lecture_commentary_pages.py data605
  > count_lecture_commentary_pages.py msml610
  Lesson01.1-Intro.book_chapter.pdf	12
  Lesson01.2-Big_Data.book_chapter.pdf	18
  Lesson01.3-Is_Data_Science_Just_Hype.book_chapter.pdf	16
  Lesson01.4-Data_Models.book_chapter.pdf	14
  ```

## `class_scripts/count_lecture_slides.py`

- Counts slides, headers (at 3 levels), lines, words, and characters in lecture
  source files in `{DIR}/lectures_source/` directory
- Displays results in a formatted table supporting markdown (default), TSV, and
  CSV output formats
- Count lecture slides with default markdown output:
  ```bash
  > count_lecture_slides.py data605
  > count_lecture_slides.py msml610
  | File                                             |   Slides |   H1 |   H2 |   H3 |   Lines |   Words |   Chars |
  |--------------------------------------------------|----------|------|------|------|---------|---------|---------|
  | Lesson01.1-Intro.txt                             |        9 |    0 |    0 |    0 |     201 |     723 |    5903 |
  | Lesson01.2-Big_Data.txt                          |       16 |    0 |    0 |    0 |     309 |    1282 |    8845 |
  | Lesson01.3-Is_Data_Science_Just_Hype.txt         |       13 |    0 |    0 |    0 |     185 |     671 |    5274 |
  | Lesson02.1-Git.txt                               |       14 |    0 |    0 |    0 |     364 |    1265 |    9457 |
  ```
- Count with TSV format for easy spreadsheet import:
  ```bash
  > count_lecture_slides.py msml610 --format tsv
  File	  Slides	  H1	  H2	  H3	  Lines	  Words	  Chars
  Lesson01.1-Intro.txt	       9	   0	   0	   0	    201	    723	   5903
  Lesson01.2-Big_Data.txt	      16	   0	   0	   0	    309	   1282	   8845
  ```
- Count with CSV format:
  ```bash
  > count_lecture_slides.py msml610 --format csv
  File,Slides,H1,H2,H3,Lines,Words,Chars
  Lesson01.1-Intro.txt,9,0,0,0,201,723,5903
  Lesson01.2-Big_Data.txt,16,0,0,0,309,1282,8845
  ```

## `class_scripts/count_lecture_pages.py`

- Counts pages in all PDF files in the `{DIR}/lectures_pdf/` directory and
  displays page counts for each lecture PDF file
- Count pages for lecture PDFs:
  ```bash
  > count_lecture_pages.py data605
  > count_lecture_pages.py msml610
  Lesson01.1-Intro.pdf	8
  Lesson01.2-Big_Data.pdf	9
  Lesson01.3-Is_Data_Science_Just_Hype.pdf	10
  Lesson01.4-Data_Models.pdf	12
  Lesson02.1-Git.pdf	15
  ```

## `class_scripts/count_words.py`

- Counts words in all files in the `{DIR}/lectures_video_script/` directory to help
  track lecture length and content volume
- Count words in lecture scripts:
  ```bash
  > count_words.py data605
  > count_words.py msml610
  Lesson01.1-Intro.script.txt	1346
  Lesson01.2-Big_Data.script.txt	2088
  Lesson01.3-Is_Data_Science_Just_Hype.script.txt	1339
  Lesson01.4-Data_Models.script.txt	1957
  Lesson02.1-Git.script.txt	2811
  ```

# Generation Scripts

## `class_scripts/gen_slides.py`

- Generates lecture slide PDFs from source files using `notes_to_pdf.py` to
  convert markdown to PDF
- Accepts additional options to pass through to `notes_to_pdf.py`
- Generate slides with default settings:
  ```bash
  > gen_slides.py data605 01.1
  Running command: notes_to_pdf.py --input=data605/lectures_source/Lesson01.1-Intro.txt --output=data605/lectures/Lesson01.1-Intro.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after
  [notes_to_pdf output...]
  PDF generated: data605/lectures/Lesson01.1-Intro.pdf
  ```
- Generate slides with custom theme:
  ```bash
  > gen_slides.py msml610 02.3 --theme dark
  ```

## `class_scripts/gen_lecture_script.py`

- Generates complete lecture scripts from slides using LLM
- Automatically creates intro and outro sections, combines all sections, and
  lints the final output
- Generate lecture script:
  ```bash
  > gen_lecture_script.py data605 01.1
  Generating lecture script for Lesson01.1
  Reading slides from: data605/lectures_source/Lesson01.1-Intro.txt
  Generating intro section...
  Generating script sections...
  Generating outro section...
  Combining and linting output...
  Script saved to: data605/lectures_video_script/Lesson01.1-Intro.script.txt
  Total words: 1346
  ```
- Generate script with forced regeneration:
  ```bash
  > gen_lecture_script.py msml610 02.3 --force
  ```

## `class_scripts/generate_slide_script.py`

- Processes markdown slides and generates presentation scripts using LLM
- Groups slides for batch processing to optimize LLM API calls
- Supports limiting slide ranges and customizable grouping strategies
- Generate script from markdown slides with default settings:
  ```bash
  > generate_slide_script.py --in_file slides.md --out_file script.md
  ```
- Process slides in groups of 5 for more context:
  ```bash
  > generate_slide_script.py --in_file lecture.txt --out_file script.txt --slides_per_group 5
  ```
- Process specific slide range:
  ```bash
  > generate_slide_script.py --in_file slides.md --out_file script.md --limit "10:20"
  ```
- Enable verbose logging for debugging:
  ```bash
  > generate_slide_script.py --in_file slides.md --out_file script.md --log_level DEBUG
  ```

## `class_scripts/generate_book_chapter.py`

- Processes markdown slides with PNG images or PDF file to create book chapter
  format
- Extracts title from markdown file (e.g., from `\text{\blue{Lesson 2.1: Git}}`)
  and adds YAML preamble for pandoc metadata
- Extracts PNG images from PDF automatically when `--input_pdf_file` is provided
- Validates that the number of slides in markdown matches the number of PNG
  files (expects `num_slides + 1 = num_pngs` to account for title slide)
- Properly aligns title slide (first PNG) with content slides (remaining PNGs)
  to ensure header, slide image, and commentary are synchronized
- First slide (PNG 1) is treated as title slide with only the image (no title or
  commentary)
- Content slides (PNG 2+) are paired with corresponding markdown slides, with
  centered headers formatted as "idx / tot: title" and LLM-based commentary
- Supports optional page breaks via `--add_new_page` flag to insert `\newpage`
  commands before each slide (disabled by default)
- Formats output with `prettier` for consistent markdown formatting

- Generate book chapter from markdown and PNG directory:
  ```bash
  > generate_book_chapter.py --input_file data605/lectures_source/Lesson01.1-Intro.txt --input_png_dir output --output_dir test
  ```
- Generate book chapter from markdown and PDF file:
  ```bash
  > generate_book_chapter.py --input_file data605/lectures_source/Lesson01.1-Intro.txt --input_pdf_file data605/lectures_pdf/Lesson01.1-Intro.pdf --output_dir test
  ```
- Process with custom image width:
  ```bash
  > generate_book_chapter.py --input_file lecture.txt --input_pdf_file lecture.pdf --output_dir ./book_chapters/ --image_width 50%
  ```
- Generate with page breaks before each slide:
  ```bash
  > generate_book_chapter.py --input_file lecture.txt --input_pdf_file lecture.pdf --output_dir ./book_chapters/ --add_new_page
  ```

- Converting to PDF with pandoc, after generating the book chapter markdown,
  convert it to PDF using pandoc with custom header styling:
  ```bash
  > pandoc test/Lesson01.1-Intro.book_chapter.txt -o output.pdf --include-in-header=header-style.tex
  ```

## `class_scripts/gen_quizzes.py`

- Generates questions from lecture content using LLM
- Supports two modes:
  - _Multiple choice quizzes_: 20 questions with 5 answers each →
    `{DIR}/lectures_quizzes/<lesson>.quizzes.md`
  - _Discussion/review questions_: 3-6 open-ended questions →
    `{DIR}/lectures_recap/<lesson>.recap.md`
- Automatically formats output using `lint_txt.py` with prettier (use
  `--no_lint` to skip)
- Generate multiple choice quiz:
  ```bash
  > gen_quizzes.py --for_class_quizzes data605 01.1
  Reading lecture from: data605/lectures_source/Lesson01.1-Intro.txt
  Generating 20 multiple choice questions...
  Formatting with prettier...
  Quiz saved to: data605/lectures_quizzes/Lesson01.1-Intro.quizzes.md
  Generated 20 questions with 5 options each
  ```
- Generate discussion questions:
  ```bash
  > gen_quizzes.py --for_class_recap msml610 02.3
  Reading lecture from: msml610/lectures_source/Lesson02.3-...txt
  Generating 5 discussion questions...
  Recap saved to: msml610/lectures_recap/Lesson02.3-...recap.md
  ```
- Generate without linting:
  ```bash
  > gen_quizzes.py --for_class_recap data605 01.2 --no_lint
  ```
- Generate with specific model:
  ```bash
  > gen_quizzes.py --for_class_quizzes data605 01.1 --model gpt-4
  ```

## `class_scripts/create_book_toc_from_slides.py`

- Extracts and combines table of contents from lecture slides into a structured
  document
- Supports two modes:
  - batch processing to separate file
  - in-place insertion
- Parses lesson files from `### Lessons` sections in markdown files from
  `book_map.md`
- Creates combined TOC with chapter organization and formatted lesson sections

- Generate combined TOC to separate file:
  ```bash
  > create_book_toc_from_slides.py --input=book_map.md --output=book_toc.md --max_level=2
  Found 8 chapters
  Processing lectures: 100%|████████| 24/24
  Wrote output to 'book_toc.md'
  ```
- Insert TOC directly into a markdown file (in-place mode):
  ```bash
  > create_book_toc_from_slides.py --input=book.Causal_Probabilistic_ML/book_map.md --in_place --max_level=3
  Inserted TOC into 'book.Causal_Probabilistic_ML/book_map.md'
  ```
- Book map format with `### Lessons` section:
  ```markdown
  ## 1: Chapter Title
  
  ### Lessons
  - `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
  - `msml610/lectures_source/Lesson08.2-Causal_Models.txt`
  ```
- After running with `--in_place`, inserts:
  ```markdown
  ### Current TOC
  
  // msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt
  
  - Topic 1 (5)
    - Subtopic A (2)
  - Topic 2 (8)
  
  // msml610/lectures_source/Lesson08.2-Causal_Models.txt
  
  - Introduction (3)
  ```

## `class_scripts/process_slides.py`

- Extracts individual slides from markdown files and processes each with LLM
  prompts
- Supports various actions like slide reduction, text checking, and improvement
- Provides parallel processing with incremental execution and error recovery

- Process slides with LLM transformation:
  ```bash
  > process_slides.py --in_file lecture.txt --action slide_reduce --out_file output.txt --use_llm_transform
  Processing input file: lecture.txt
  Found 15 slides
  Processing with action: slide_reduce (threads: 4)
  Slide 1/15: Processing... [2.5s]
  Slide 2/15: Processing... [2.3s]
  ...
  Completed: 15/15 slides
  Output saved to: output.txt
  Processing time: 45s
  ```
- Check slide quality and generate report:
  ```bash
  > process_slides.py --in_file lecture.txt --action text_check --out_file check_report.txt --use_llm_transform
  ```
- Process specific slide range with parallel execution:
  ```bash
  > process_slides.py --in_file lecture.txt --action slide_reduce --out_file output.txt --limit "1:5" --num_threads 4
  ```
- Continue processing on errors with multiple attempts:
  ```bash
  > process_slides.py --in_file lecture.txt --action slide_reduce --out_file output.txt --no_abort_on_error --num_attempts 3 --skip_on_error
  ```

# Slide Improvement Scripts

## `class_scripts/slide_check.py`

- Checks and fixes text in lecture slides using LLM
- Corrects spelling, grammar, and formatting issues using `process_slides.py`
  with `text_check_fix` action
- Check and fix slides:
  ```bash
  > slide_check.py data605 01.1
  Checking slides in: data605/lectures_source/Lesson01.1-Intro.txt
  Processing 9 slides with LLM text check...
  Slide 1: Fixed 2 spelling errors, 1 grammar issue
  Slide 2: No issues found
  Slide 3: Fixed 1 capitalization error
  ...
  Results saved to: data605/lectures_source/Lesson01.1-Intro.txt
  Total issues fixed: 8
  ```
- Preview changes without executing:
  ```bash
  > slide_check.py msml610 02.3 --dry-run
  ```

## `class_scripts/slide_improve.py`

- Improves lecture slides using LLM suggestions
- Enhances clarity, structure, and pedagogical effectiveness using
  `process_slides.py` with `slide_improve` action
- Improve slides:
  ```bash
  > slide_improve.py data605 01.1
  Improving slides in: data605/lectures_source/Lesson01.1-Intro.txt
  Processing 9 slides with LLM improvement suggestions...
  Slide 1: Suggested clearer explanation of key concepts
  Slide 2: Suggested adding examples for better understanding
  Slide 3: Suggested reorganizing content for better flow
  ...
  Suggestions saved to: data605/lectures_source/Lesson01.1-Intro.improved.txt
  Total suggestions: 7
  ```
- Limit suggestions:
  ```bash
  > slide_improve.py msml610 02.3 --max-suggestions 5
  ```

## `class_scripts/slide_reduce.py`

- Reduces and simplifies lecture slides using LLM
- Removes redundancy and condenses content using `process_slides.py` with
  `slide_reduce` action
- Reduce slide content:
  ```bash
  > slide_reduce.py data605 01.1
  Reducing slides in: data605/lectures_source/Lesson01.1-Intro.txt
  Processing 9 slides with LLM reduction...
  Slide 1: Reduced from 150 words to 95 words (37% reduction)
  Slide 2: Reduced from 120 words to 78 words (35% reduction)
  Slide 3: No reduction needed (already concise)
  ...
  Results saved to: data605/lectures_source/Lesson01.1-Intro.reduced.txt
  Total reduction: 35% (avg)
  ```
- Set target length:
  ```bash
  > slide_reduce.py msml610 02.3 --target-length 50
  ```

# Image and PDF Processing Scripts
## `class_scripts/extract_png_from_pdf.py`

- Extracts each page of a PDF file as a separate PNG image
- Numbers output files sequentially (slides001.png, slides002.png, etc.)
- Supports customizable DPI for image quality control
- Creates output directory automatically with optional from-scratch mode
- Extract all pages from a PDF with default settings:
  ```bash
  > extract_png_from_pdf.py --input_file data605/lectures_pdf/Lesson01.1-Intro.pdf --output_dir output
  Processing PDF file: data605/lectures_pdf/Lesson01.1-Intro.pdf
  Output directory: output
  Converting PDF to images with DPI=200
  Found 8 pages in PDF
  Extracting pages: 100%|████████| 8/8
  Successfully extracted 8 PNG images to output
  ```
  Output files created: `output/slides001.png`, `output/slides002.png`, ..., `output/slides008.png`

- Extract with higher DPI for better image quality:
  ```bash
  > extract_png_from_pdf.py --input_file lecture.pdf --output_dir slides --dpi 300
  ```
- Create output directory from scratch:
  ```bash
  > extract_png_from_pdf.py --input_file presentation.pdf --output_dir ./images/ --from_scratch
  ```

## `class_scripts/generate_class_images.py`

- Generates multiple images using OpenAI's DALL-E 3 API from text prompts
- Supports both standard and HD quality image generation in 1024x1024 resolution
- Includes special workload mode for generating predefined image sets for course
  materials
- Generate 5 HD quality images from a prompt:
  ```bash
  > generate_class_images.py "A sunset over mountains" --dst_dir ./images
  Generating 5 images with prompt: 'A sunset over mountains'
  Resolution: 1024x1024, Quality: hd
  Generating image 1/5
  Downloading image to ./images/image_01_hd.png
  Saved image to: ./images/image_01_hd.png
  Generating image 2/5
  Downloading image to ./images/image_02_hd.png
  Saved image to: ./images/image_02_hd.png
  ...
  Image generation complete. Images saved to: ./images
  ```
- Generate standard quality images with custom count:
  ```bash
  > generate_class_images.py "A cat wearing a hat" --dst_dir ./images --count 3 --low_res
  ```
- Generate images for MSML610 course workload:
  ```bash
  > generate_class_images.py --dst_dir ./course_images --workload MSML610
  ```

# Test Utilities

## `class_scripts/gen_slides_test_utils.py`

- Shared utilities for slide generation testing. Provides helper functions for
  discovering lessons, testing slide generation, and validating output.

# Utility Scripts
## `class_scripts/get_lecture_file.py`

- Finds and prints the path to a lecture source file matching
  `{DIR}/lectures_source/Lesson{LESSON}*`
- Validates that exactly one matching file exists
- Find lecture file:
  ```bash
  > get_lecture_file.py data605 01.1
  > get_lecture_file.py msml610 02.3
  Lecture file: data605/lectures_source/Lesson01.1-Intro.txt
  ```

# Orchestration Scripts

## `class_scripts/for_loop_slides.py`

Transforms lecture slides using LLM with specified rules. Reads slides from lesson
files, applies LLM-based transformations based on a rule prompt, and writes the
transformed slides back to the file or output.

**Key features:**

- Extracts slides from lesson files while preserving file structure
- Applies LLM transformations using specified rule prompts
- Processes slides in configurable batches for efficiency
- Supports multiple batch modes: individual, shared_prompt, combined
- Integrates with `hllm_cli._process_batches` for batch processing

**Command Line Arguments:**

- `--input_file`: Input lesson file containing slides (required)
- `--output_file`: Output file for transformed slides (optional)
- `--prompt_file` or `--prompt`: Rule prompt to guide transformation
- `--model`: LLM model to use (default: "claude-opus-4")
- `--batch_size`: Number of slides per batch (default: 1)
- `--batch_mode`: Batch processing mode - "individual", "shared_prompt", or
  "combined" (default: "individual")
- `-v/--log_level`: Set logging verbosity (DEBUG, INFO, WARNING, ERROR)

**Usage Examples:**

- Transform slides using a prompt file:
  ```bash
  > for_loop_slides.py --input_file data605/lectures_source/Lesson01.1-Intro.txt \
      --prompt_file my_rules.prompt.md --output_file output.txt
  ```

- Transform slides in batches with custom model:
  ```bash
  > for_loop_slides.py --input_file msml610/lectures_source/Lesson02.1-*.txt \
      --prompt "Simplify the content" --model claude-opus-4 --batch_size 5
  ```

- Transform with combined batch mode:
  ```bash
  > for_loop_slides.py --input_file lecture.txt --prompt_file rules.txt \
      --batch_mode combined --batch_size 3
  ```

## `class_scripts/for_loop_lessons.py`

Orchestrates the generation of multiple outputs from lecture source files for
educational materials. This is the main entry point for processing lecture
content into various formats.

**Key features:**

- Converts lecture text source files to PDF slides using `notes_to_pdf.py`
- Generates reading scripts from lecture materials with transition text
- Applies LLM-based transformations for slide reduction and quality checking
- Generates book chapters from lecture content
- Supports batch processing of multiple lectures using pattern matching
- Provides slide range limiting for focused processing
- Includes dry-run mode for previewing commands

**Available Actions:**

- `generate_pdf`: Generate presentation slides from text source files
- `generate_script`: Generate instructor reading scripts with commentary
- `reduce_slide`: Apply LLM transformation to reduce slide content
- `check_slide`: Apply LLM validation to check slide quality
- `improve_slide`: Apply LLM transformation to improve slide content
- `book_chapter`: Generate book chapter PDF from lecture content
- `generate_class_quizzes`: Generate multiple choice quizzes from lecture
  content using LLM
- `generate_class_recap`: Generate open-ended discussion/review questions from
  lecture content using LLM
- `generate_toc`: Extract table of contents (headers) from all lectures and
  create a consolidated course syllabus

**Lecture Pattern Examples:**

- Single lecture: `01.1`
- Wildcard pattern: `01*`
- Multiple patterns: `01*:02*:03.1` (separated by colons)
- Continuous range: `01.1-03.2` (inclusive)

**Command Line Arguments:**

- `--lectures`: Lecture(s) to process (required)
  - Single pattern: '01.1' or '01\*'
  - Union of patterns (colon-separated): '01*:02*:03.1'
  - Continuous range (hyphen-separated): '01.1-03.2' (inclusive)
  - Note: Range and union syntax cannot be mixed
- `--class`: Class directory name (required, choices: data605, msml610)
- `--action`: Actions to perform (default: generate_pdf)
  - Can specify multiple: `--action generate_pdf --action generate_script`
- `--limit`: Optional slide range to process (e.g., '1:3')
  - Only works when processing a single lecture file
- `--dry_run`: Print commands without executing them
- `-v/--log_level`: Set logging verbosity (DEBUG, INFO, WARNING, ERROR)

**Usage Examples:**

- Generate PDF for single lecture:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --class data605 --action generate_pdf
  ```

- Generate scripts for multiple lectures:
  ```bash
  > for_loop_lessons.py --lectures 01*:02* --class data605 --action generate_script
  ```

- Multiple actions on same lectures:
  ```bash
  > for_loop_lessons.py --lectures 01* --class msml610 --action generate_pdf --action generate_script
  ```

- Partial slide processing:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --limit 1:3 --class data605 --action generate_pdf
  ```

- Process a continuous range of lessons:
  ```bash
  > for_loop_lessons.py --lectures "01.1-03.2" --class data605 --action generate_pdf
  ```

- Reduce slide content using LLM for a single lecture:
  ```bash
  > for_loop_lessons.py --lectures "01.1" --class data605 --action reduce_slide
  ```

- Generate multiple choice quizzes from lecture content:
  ```bash
  > for_loop_lessons.py --lectures "01.1" --class data605 --action generate_class_quizzes
  ```

- Process with verbose logging for debugging:
  ```bash
  > for_loop_lessons.py --lectures "01.1" --class data605 --action generate_pdf -v DEBUG
  ```

**Workflow:**

1. Parse lecture patterns or ranges from command line arguments (e.g., '01*',
   '01.1', '01*:03\*', '01.1-03.2')
2. Find matching lecture source files in `<class>/lectures_source/` directory
3. For each matching file, execute specified actions in sequence
4. Output generated files to appropriate directories:
   - PDF slides → `<class>/lectures_pdf/`
   - Scripts → `<class>/lectures_video_script/`
   - Book chapters → `<class>/lectures_commentary/`
   - Multiple choice quizzes → `<class>/lectures_quizzes/`
   - Discussion/recap questions → `<class>/lectures_recap/`

# Common Workflows

## Generating Course Materials
**Generate PDF Slides for All Lessons in a Course**

- Generates PDF files for all lessons starting with 0 or 1 (e.g., 01.1, 01.2,
  10.1, etc.) in `data605/lectures_pdf/`:
  ```bash
  > for_loop_lessons.py --lectures "0*:1*" --class data605 --action generate_pdf
  ```

**Generate Both PDF Slides and Reading Scripts**

- Generates PDFs in `lectures_pdf/` and scripts in `lectures_video_script/`:
  ```bash
  > for_loop_lessons.py --lectures 01* --class msml610 --action generate_pdf --action generate_script
  ```

**Generate PDF and Book Chapter for a Single Lesson**

- Creates slide PDF and corresponding book chapter with pandoc conversion:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --class data605 --action generate_pdf --action book_chapter
  ```

## Assessment Generation
**Generate Multiple Choice Quizzes**

- Creates 20-question quizzes saved to `lectures_quizzes/<lesson>.quizzes.md`:
  ```bash
  > for_loop_lessons.py --lectures 01* --class data605 --action generate_class_quizzes
  ```

- Alternatively, use the direct script:
  ```bash
  > gen_quizzes.py --for_class_quizzes data605 01.1
  ```

**Generate Discussion/review Questions**

- Creates 3-6 open-ended discussion questions saved to
  `lectures_recap/<lesson>.recap.md`:
  ```bash
  > for_loop_lessons.py --lectures 01* --class data605 --action generate_class_recap
  ```

- Alternatively, use the direct script:
  ```bash
  > gen_quizzes.py --for_class_recap data605 01.1
  ```

## Slide Quality Improvement
**Check and Fix Spelling/grammar in Slides**

- Use for_loop_lessons.py:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --class data605 --action check_slide
  ```

- **Advanced usage** (check one lecture from inside the container):
  ```bash
  > SRC_NAME=$(ls $DIR/lectures_source/Lesson02*); echo $SRC_NAME
  > DST_NAME=process_slides.txt
  > i docker_bash
  docker> process_slides.py --in_file $SRC_NAME --action text_check --out_file $DST_NAME --use_llm_transform --limit 0:10
  > vimdiff $SRC_NAME process_slides.txt
  ```

- Alternatively, use the direct script:
  ```bash
  > slide_check.py data605 01.1
  ```

**Improve Slide Clarity and Structure**

- Use for_loop_lessons.py:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --class data605 --action improve_slide
  ```

- Alternatively, use the direct script:
  ```bash
  > slide_improve.py data605 01.1
  ```

- Or use `llm_transform.py` directly:
  ```bash
  > llm_transform.py -i data605/lectures_source/Lesson07.2-Data_Wrangling.txt -p slide_improve -v DEBUG
  ```

**Reduce Slide Length and Remove Redundancy**

- Use for_loop_lessons.py:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --class data605 --action reduce_slide
  ```

- **Advanced usage** (reduce from inside the container):
  ```bash
  > SRC_NAME=$(ls $DIR/lectures_source/Lesson04.2*); echo $SRC_NAME
  > docker> process_slides.py --in_file $SRC_NAME --action slide_reduce --out_file $SRC_NAME --use_llm_transform --limit 0:10
  ```

- Alternatively, use the direct script:
  ```bash
  > slide_reduce.py data605 01.1
  ```

**Fix Slides with Custom LLM Prompt**

- Uses GPT-4o to fix and improve slides based on a prompt template:
  ```bash
  > FILE=data605/lectures_source/Lesson09.2-Spark_Primitives.txt
  > llm_cli.py --input $FILE -pf "fix_slides.prompt.md" -o improved.md --model "gpt-4o" -b
  ```

## Lecture Script Generation
**Generate Complete Lecture Script with Intro/outro**

- Use the direct script:
  ```bash
  > gen_lecture_script.py data605 01.1
  ```

- Or use `for_loop_lessons.py`:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --class data605 --action generate_script
  ```

**Generate Just the Intro for a Lecture**

- Creates a 50-word introduction for Lesson 08.3:
  ```bash
  > TAG=08.3; llm_cli.py -i data605/lectures_video_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to do an introduction in 50 word the content of the slides starting with In this lesson" -o -
  ```

**Generate Just the Outro/summary for a Lecture**

- Creates a 50-word summary/conclusion for Lesson 08.3:
  ```bash
  > TAG=08.3; llm_cli.py -i data605/lectures_video_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to summarize what was discussed in less than 50 word in the slides like In this lesson we have discussed" -o -
  ```

**Generate Scripts From Inside a Container (advanced)**

- Generates a script for slides 1-5, grouping 3 slides at a time:
  ```bash
  > i docker_bash --base-image=623860924167.dkr.ecr.eu-north-1.amazonaws.com/cmamp --skip-pull
  docker> sudo /bin/bash -c "(source /venv/bin/activate; pip install --upgrade openai)"
  docker> generate_slide_script.py \
    --in_file data605/lectures_source/Lesson01-Intro.txt \
    --out_file data605/lectures_source/Lesson01-Intro.script.txt \
    --slides_per_group 3 \
    --limit 1:5
  ```

## Format Conversion
**Convert Markdown Notes to PDF Slides**

- Converts markdown lecture notes to PDF format (slides 1-4 only):
  ```bash
  > notes_to_pdf.py --input data605/lectures_md/final_enhanced_markdown_lecture_2.txt --output tmp.pdf --type slides --skip_action cleanup_after --debug_on_error --toc_type navigation --filter_by_slides 1:4
  ```

## Course Syllabus and Structure

**Generate Complete Course Syllabus**

- Extracts all lecture headers and creates a consolidated syllabus:
  ```bash
  > for_loop_lessons.py --class data605 --action generate_toc
  > for_loop_lessons.py --class msml610 --action generate_toc
  ```
- Output: `<class>/all_tocs.md` containing all lecture headers organized hierarchically

**Generate Syllabus for Specific Lectures**

- Extract headers from pattern-matched lectures:
  ```bash
  > for_loop_lessons.py --class data605 --lectures "01*" --action generate_toc
  > for_loop_lessons.py --class data605 --lectures "01*:02*:03.1" --action generate_toc
  > for_loop_lessons.py --class data605 --lectures "01.1-03.2" --action generate_toc
  ```

## Analysis and Reporting
**Count Pages in All Book PDFs**
```bash
> count_lecture_commentary_pages.py data605
```

**Count Pages in All Lecture PDFs**
```bash
> count_lecture_pages.py data605
```

**Count Words in All Lecture Scripts**

- Helps track lecture length and content volume:
  ```bash
  > count_words.py data605
  ```

## Partial Processing
**Generate Specific Slides From a Lecture (slides 1-3 Only)**

- Only applies to `generate_pdf` action when a single lecture file matches:
  ```bash
  > for_loop_lessons.py --lectures 01.1 --limit 1:3 --class data605 --action generate_pdf
  ```

**Preview Commands Without Executing (dry-run)**

- Prints all commands that would be executed without running them:
  ```bash
  > for_loop_lessons.py --lectures 01* --class data605 --action generate_pdf --dry_run
  ```

# Invariants
- All and only scripts in `class_scripts` and `helpers_root/dev_scripts_helpers/documentation`
  are present
- Each description of the script is accurate
