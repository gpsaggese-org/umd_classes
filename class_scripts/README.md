# Class_scripts

# Summary
A comprehensive suite of command-line tools and scripts for managing university
courses, generating lecture materials (slides, scripts, quizzes), and improving
slide quality through automated LLM-powered transformations.

## Structure of the Dir
- `lectures_source/`: Input directory containing `Lesson*.txt` files
- `lectures/`: Output directory for generated PDF files
- `lectures_script/`: Output directory for generated script files
- `lectures_quizzes/`: Output directory for multiple choice quiz files
- `lectures_recap/`: Output directory for discussion and recap question files
- `book/`: Output directory for book chapter files

## Description of Files
- `common_utils.py`: Shared utility functions for argument validation, file
  finding, directory management, and PDF page counting

| Script                     | Location                                          | Description                                                                                                             |
| :------------------------- | :------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------- |
| `concatenate_pdfs.py`      | `helpers_root/dev_scripts_helpers/documentation/` | Combines multiple PDF files into a single PDF (used for creating full book from chapters)                               |
| `count_book_pages.py`      | `class_scripts/`                                  | Counts pages in all PDF files in `{DIR}/book/` directory using macOS `mdls` command                                     |
| `count_lecture_slides.py`  | `class_scripts/`                                  | Counts slides, headers, lines, words, and characters in `{DIR}/lectures_source/` files with markdown/csv/tsv output     |
| `count_pdf_pages.py`       | `class_scripts/`                                  | Counts pages in all PDF files in `{DIR}/lectures/` directory using macOS `mdls` command                                 |
| `count_words.py`           | `class_scripts/`                                  | Counts words in all files in `{DIR}/lectures_script/` directory to track lecture length                                 |
| `extract_png_from_pdf.py`  | `class_scripts/`                                  | Extracts PNG images from PDF files with sequential numbering and customizable DPI                                       |
| `gen_book_chapter.py`      | `class_scripts/`                                  | Generates book chapters from lecture source material; performs PDF generation, chapter creation, and pandoc conversion  |
| `gen_lecture_script.py`    | `class_scripts/`                                  | Generates complete lecture scripts from slides using LLM; creates intro/outro sections automatically                    |
| `gen_quizzes.py`           | `class_scripts/`                                  | Generates multiple choice quizzes (20 questions) or discussion/review questions (3-6 questions) from lecture content    |
| `gen_slides.py`            | `class_scripts/`                                  | Generates lecture slide PDFs from source files using `notes_to_pdf.py` for markdown-to-PDF conversion                   |
| `generate_book_chapter.py` | `class_scripts/`                                  | Generates book chapters from markdown and PDF/PNG images with LLM-based commentary and pandoc conversion                |
| `generate_class_images.py` | `class_scripts/`                                  | Generates images using OpenAI's DALL-E API from text prompts; supports standard and HD quality                          |
| `generate_slide_script.py` | `class_scripts/`                                  | Generates lecture scripts from slide content; groups slides and lints output                                            |
| `get_lecture_file.py`      | `class_scripts/`                                  | Finds and prints the path to a lecture source file matching `{DIR}/lectures_source/Lesson{LESSON}*`                     |
| `lint_txt.py`              | `helpers_root/dev_scripts_helpers/documentation/` | Lints and formats text files using prettier; used by `gen_quizzes.py` for output formatting                             |
| `llm_cli.py`               | `helpers_root/dev_scripts_helpers/llms/`          | LLM command-line interface for AI-powered text transformations and content generation                                   |
| `llm_transform.py`         | `helpers_root/dev_scripts_helpers/llms/`          | Applies LLM transformations to content with various prompts (slide_improve, etc.)                                       |
| `notes_to_pdf.py`          | `helpers_root/dev_scripts_helpers/documentation/` | Converts markdown/notes to PDF format (slides, documents, etc.); used by `gen_slides.py`                                |
| `for_loop_lessons.py`      | `class_scripts/`                                  | Main orchestration script for generating PDFs/scripts; supports multiple actions with pattern matching and dry-run mode |
| `process_slides.py`        | `class_scripts/`                                  | Processes slides with LLM transformations (text_check, slide_reduce, slide_check, slide_format_figures); runs in Docker |
| `slide_check.py`           | `class_scripts/`                                  | Checks and fixes text in lecture slides using LLM; corrects spelling, grammar, and formatting                           |
| `slide_improve.py`         | `class_scripts/`                                  | Improves lecture slides using LLM suggestions; enhances clarity, structure, and pedagogical effectiveness               |
| `slide_reduce.py`          | `class_scripts/`                                  | Reduces and simplifies lecture slides using LLM; removes redundancy and condenses content                               |
| `slides_utils.py`          | `class_scripts/`                                  | Utility functions for extracting and processing slide content                                                           |

# Counting and Analysis Scripts
## `count_book_pages.py`

- Counts pages in all PDF files in the `{DIR}/book/` directory using macOS
  `mdls` command to extract PDF metadata
- Count pages for a specific class:
  ```bash
  > count_book_pages.py data605
  > count_book_pages.py msml610
  ```

## `count_lecture_slides.py`

- Counts slides, headers (at 3 levels), lines, words, and characters in lecture
  source files in `{DIR}/lectures_source/` directory
- Displays results in a formatted table supporting markdown (default), TSV, and
  CSV output formats
- Count lecture slides with default markdown output:
  ```bash
  > count_lecture_slides.py data605
  > count_lecture_slides.py msml610
  ```
- Count with TSV format for easy spreadsheet import:
  ```bash
  > count_lecture_slides.py msml610 --format tsv
  ```
- Count with CSV format:
  ```bash
  > count_lecture_slides.py msml610 --format csv
  ```

## `count_pdf_pages.py`

- Counts pages in all PDF files in the `{DIR}/lectures/` directory and displays
  page counts for each lecture PDF file
- Count pages for lecture PDFs:
  ```bash
  > count_pdf_pages.py data605
  > count_pdf_pages.py msml610
  ```

## `count_words.py`

- Counts words in all files in the `{DIR}/lectures_script/` directory to help
  track lecture length and content volume
- Count words in lecture scripts:
  ```bash
  > count_words.py data605
  > count_words.py msml610
  ```

# Generation Scripts
## `gen_slides.py`

- Generates lecture slide PDFs from source files using `notes_to_pdf.py` to
  convert markdown to PDF
- Accepts additional options to pass through to `notes_to_pdf.py`
- Generate slides with default settings:
  ```bash
  > gen_slides.py data605 01.1
  ```
- Generate slides with custom theme:
  ```bash
  > gen_slides.py msml610 02.3 --theme dark
  ```

## `gen_lecture_script.py`

- Generates complete lecture scripts from slides using LLM
- Automatically creates intro and outro sections, combines all sections, and
  lints the final output
- Generate lecture script:
  ```bash
  > gen_lecture_script.py data605 01.1
  ```
- Generate script with forced regeneration:
  ```bash
  > gen_lecture_script.py msml610 02.3 --force
  ```

## `generate_slide_script.py`

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

## `generate_book_chapter.py`

- Processes markdown slides with PNG images or PDF file to create book chapter
  format
- Extracts title from markdown file (e.g., from `\text{\blue{Lesson 2.1: Git}}`)
  and adds YAML preamble for pandoc metadata
- Extracts PNG images from PDF automatically when --input_pdf_file is provided
- Validates that the number of slides in markdown matches the number of PNG
  files (expects num_slides + 1 = num_pngs to account for title slide)
- Properly aligns title slide (first PNG) with content slides (remaining PNGs)
  to ensure header, slide image, and commentary are synchronized
- First slide (PNG 1) is treated as title slide with only the image (no title or
  commentary)
- Content slides (PNG 2+) are paired with corresponding markdown slides, with
  centered headers formatted as "idx / tot: title" and LLM-based commentary
- Supports optional page breaks via --add_new_page flag to insert `\newpage`
  commands before each slide (disabled by default)
- Formats output with prettier for consistent markdown formatting
- Generate book chapter from markdown and PNG directory:
  ```bash
  > generate_book_chapter.py --input_file data605/lectures_source/Lesson01.1-Intro.txt --input_png_dir output --output_dir test
  ```
- Generate book chapter from markdown and PDF file:
  ```bash
  > generate_book_chapter.py --input_file data605/lectures_source/Lesson01.1-Intro.txt --input_pdf_file data605/lectures/Lesson01.1-Intro.pdf --output_dir test
  ```
- Process with custom image width:
  ```bash
  > generate_book_chapter.py --input_file lecture.txt --input_pdf_file lecture.pdf --output_dir ./book_chapters/ --image_width 50%
  ```
- Generate with page breaks before each slide:
  ```bash
  > generate_book_chapter.py --input_file lecture.txt --input_pdf_file lecture.pdf --output_dir ./book_chapters/ --add_new_page
  ```

**Converting to PDF with pandoc**:

After generating the book chapter markdown, convert it to PDF using pandoc with
custom header styling:

```bash
> pandoc test/Lesson01.1-Intro.book_chapter.txt -o output.pdf --include-in-header=header-style.tex
```

## `gen_quizzes.py`

- Generates questions from lecture content using LLM
- Supports two modes:
  - **Multiple choice quizzes**: 20 questions with 5 answers each →
    `{DIR}/lectures_quizzes/<lesson>.quizzes.md`
  - **Discussion/review questions**: 3-6 open-ended questions →
    `{DIR}/lectures_recap/<lesson>.recap.md`
- Automatically formats output using `lint_txt.py` with prettier (use
  `--no_lint` to skip)
- Generate multiple choice quiz:
  ```bash
  > gen_quizzes.py --for_class_quizzes data605 01.1
  ```
- Generate discussion questions:
  ```bash
  > gen_quizzes.py --for_class_recap msml610 02.3
  ```
- Generate without linting:
  ```bash
  > gen_quizzes.py --for_class_recap data605 01.2 --no_lint
  ```
- Generate with specific model:
  ```bash
  > gen_quizzes.py --for_class_quizzes data605 01.1 --model gpt-4
  ```

## `process_slides.py`

- Extracts individual slides from markdown files and processes each with LLM
  prompts
- Supports various actions like slide reduction, text checking, and improvement
- Provides parallel processing with incremental execution and error recovery
- Process slides with LLM transformation:
  ```bash
  > process_slides.py --in_file lecture.txt --action slide_reduce --out_file output.txt --use_llm_transform
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
## `slide_check.py`

- Checks and fixes text in lecture slides using LLM
- Corrects spelling, grammar, and formatting issues using `process_slides.py`
  with `text_check_fix` action
- Check and fix slides:
  ```bash
  > slide_check.py data605 01.1
  ```
- Preview changes without executing:
  ```bash
  > slide_check.py msml610 02.3 --dry-run
  ```

## `slide_improve.py`

- Improves lecture slides using LLM suggestions
- Enhances clarity, structure, and pedagogical effectiveness using
  `process_slides.py` with `slide_improve` action
- Improve slides:
  ```bash
  > slide_improve.py data605 01.1
  ```
- Limit suggestions:
  ```bash
  > slide_improve.py msml610 02.3 --max-suggestions 5
  ```

## `slide_reduce.py`

- Reduces and simplifies lecture slides using LLM
- Removes redundancy and condenses content using `process_slides.py` with
  `slide_reduce` action
- Reduce slide content:
  ```bash
  > slide_reduce.py data605 01.1
  ```
- Set target length:
  ```bash
  > slide_reduce.py msml610 02.3 --target-length 50
  ```

# Image and PDF Processing Scripts
## `extract_png_from_pdf.py`

- Extracts each page of a PDF file as a separate PNG image
- Numbers output files sequentially (slides001.png, slides002.png, etc.)
- Supports customizable DPI for image quality control
- Creates output directory automatically with optional from-scratch mode
- Extract all pages from a PDF with default settings:
  ```bash
  > extract_png_from_pdf.py --input_file data605/lectures/Lesson01.1-Intro.pdf --output_dir output
  ```
- Extract with higher DPI for better image quality:
  ```bash
  > extract_png_from_pdf.py --input_file lecture.pdf --output_dir slides --dpi 300
  ```
- Create output directory from scratch:
  ```bash
  > extract_png_from_pdf.py --input_file presentation.pdf --output_dir ./images/ --from_scratch
  ```

## `generate_class_images.py`

- Generates multiple images using OpenAI's DALL-E 3 API from text prompts
- Supports both standard and HD quality image generation in 1024x1024 resolution
- Includes special workload mode for generating predefined image sets for course
  materials
- Generate 5 HD quality images from a prompt:
  ```bash
  > generate_class_images.py "A sunset over mountains" --dst_dir ./images
  ```
- Generate standard quality images with custom count:
  ```bash
  > generate_class_images.py "A cat wearing a hat" --dst_dir ./images --count 3 --low_res
  ```
- Generate images for MSML610 course workload:
  ```bash
  > generate_class_images.py --dst_dir ./course_images --workload MSML610
  ```

# Utility Scripts
## `get_lecture_file.py`

- Finds and prints the path to a lecture source file matching
  `{DIR}/lectures_source/Lesson{LESSON}*`
- Validates that exactly one matching file exists
- Find lecture file:
  ```bash
  > get_lecture_file.py data605 01.1
  > get_lecture_file.py msml610 02.3
  ```

# Orchestration Scripts
## `for_loop_lessons.py`

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
   - PDF slides → `<class>/lectures/`
   - Scripts → `<class>/lectures_script/`
   - Book chapters → `<class>/book/`
   - Multiple choice quizzes → `<class>/lectures_quizzes/`
   - Discussion/recap questions → `<class>/lectures_recap/`

# Common Workflows

## Generating Course Materials
**Generate PDF Slides for All Lessons in a Course**

- Generates PDF files for all lessons starting with 0 or 1 (e.g., 01.1, 01.2,
  10.1, etc.) in `data605/lectures/`:
  ```bash
  > for_loop_lessons.py --lectures "0*:1*" --class data605 --action generate_pdf
  ```

**Generate Both PDF Slides and Reading Scripts**

- Generates PDFs in `lectures/` and scripts in `lectures_script/`:
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
  > TAG=08.3; llm_cli.py -i data605/lectures_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to do an introduction in 50 word the content of the slides starting with In this lesson" -o -
  ```

**Generate Just the Outro/summary for a Lecture**

- Creates a 50-word summary/conclusion for Lesson 08.3:
  ```bash
  > TAG=08.3; llm_cli.py -i data605/lectures_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to summarize what was discussed in less than 50 word in the slides like In this lesson we have discussed" -o -
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

## Analysis and Reporting
**Count Pages in All Book PDFs**
```bash
> count_book_pages.py data605
```

**Count Pages in All Lecture PDFs**
```bash
> count_pdf_pages.py data605
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

## Running Interactive Tutorials
**Start Jupyter Lab in Docker**

- Starts a Jupyter Lab server in a Docker container:
  ```bash
  > cd msml610/tutorials
  > i docker_jupyter --skip-pull --stage local --version 1.0.0
  ```

**Open a Specific Notebook in Chrome**

- Opens the Bayesian Coin tutorial in Chrome:
  ```bash
  > open -a "Chrome" http://127.0.0.1:5011/lab/tree/notebooks/Bayesian_Coin.ipynb
  ```
