# class_scripts

Course management tools and utilities for generating lecture materials.

## Structure of the Dir

No subdirectories.

## Description of Files

- `common_utils.py`
  - Shared utility functions for argument validation, file finding, directory management, and PDF page counting

| Script | Status | Description |
| :------- | :------- | :------- |
| `concatenate_pdfs.py` | `helpers_root/dev_scripts_helpers/documentation/` | Combines multiple PDF files into a single PDF (used for creating full book from chapters) |
| `count_book_pages.py` | `class_scripts/` | Counts pages in all PDF files in `{DIR}/book/` directory using macOS `mdls` command |
| `count_lecture_pages.py` | `class_scripts/` | Counts pages in all PDF files in `{DIR}/lectures/` directory using macOS `mdls` command |
| `count_words.py` | `class_scripts/` | Counts words in all files in `{DIR}/lectures_script/` directory to track lecture length |
| `gen_book_chapter.py` | `class_scripts/` | Generates book chapters from lecture source material; performs PDF generation, chapter creation, and pandoc conversion |
| `gen_lecture_script.py` | `class_scripts/` | Generates complete lecture scripts from slides using LLM; creates intro/outro sections automatically |
| `gen_quizzes.py` | `class_scripts/` | Generates multiple choice quizzes (20 questions) or discussion/review questions (3-6 questions) from lecture content |
| `gen_slides.py` | `class_scripts/` | Generates lecture slide PDFs from source files using `notes_to_pdf.py` for markdown-to-PDF conversion |
| `generate_slide_script.py` | `helpers_root/dev_scripts_helpers/slides/` | Generates lecture scripts from slide content; groups slides and lints output |
| `get_lecture_file.py` | `class_scripts/` | Finds and prints the path to a lecture source file matching `{DIR}/lectures_source/Lesson{LESSON}*` |
| `lint_txt.py` | `helpers_root/dev_scripts_helpers/documentation/` | Lints and formats text files using prettier; used by `gen_quizzes.py` for output formatting |
| `llm_cli.py` | `helpers_root/dev_scripts_helpers/llms/` | LLM command-line interface for AI-powered text transformations and content generation |
| `llm_transform.py` | `helpers_root/dev_scripts_helpers/llms/` | Applies LLM transformations to content with various prompts (slide_improve, etc.) |
| `notes_to_pdf.py` | `helpers_root/dev_scripts_helpers/documentation/` | Converts markdown/notes to PDF format (slides, documents, etc.); used by `gen_slides.py` |
| `process_lessons.py` | `helpers_root/dev_scripts_helpers/slides/` | Main orchestration script for generating PDFs/scripts; supports multiple actions with pattern matching and dry-run mode |
| `process_slides.py` | `helpers_root/dev_scripts_helpers/slides/` | Processes slides with LLM transformations (text_check, slide_reduce, slide_check, slide_format_figures); runs in Docker |
| `slide_check.py` | `class_scripts/` | Checks and fixes text in lecture slides using LLM; corrects spelling, grammar, and formatting |
| `slide_improve.py` | `class_scripts/` | Improves lecture slides using LLM suggestions; enhances clarity, structure, and pedagogical effectiveness |
| `slide_reduce.py` | `class_scripts/` | Reduces and simplifies lecture slides using LLM; removes redundancy and condenses content |

## Description of Executables

### `count_book_pages.py`

**What It Does**

- Counts pages in all PDF files in the `{DIR}/book/` directory
- Uses macOS `mdls` command to extract PDF metadata
- Displays page counts for each book PDF file

**Examples**

- Count pages in all book PDFs for data605:
  ```bash
  > ./count_book_pages.py data605
  ```

- Count pages in all book PDFs for msml610:
  ```bash
  > ./count_book_pages.py msml610
  ```

### `count_lecture_pages.py`

**What It Does**

- Counts pages in all PDF files in the `{DIR}/lectures/` directory
- Uses macOS `mdls` command to extract PDF metadata
- Displays page counts for each lecture PDF file

**Examples**

- Count pages in all lecture PDFs for data605:
  ```bash
  > ./count_lecture_pages.py data605
  ```

- Count pages in all lecture PDFs for msml610:
  ```bash
  > ./count_lecture_pages.py msml610
  ```

### `count_words.py`

**What It Does**

- Counts words in all files in the `{DIR}/lectures_script/` directory
- Displays word counts for each lecture script file
- Helps track lecture length and content volume

**Examples**

- Count words in all lecture scripts for data605:
  ```bash
  > ./count_words.py data605
  ```

- Count words in all lecture scripts for msml610:
  ```bash
  > ./count_words.py msml610
  ```

### `gen_book_chapter.py`

**What It Does**

- Generates a book chapter from lecture source material
- Performs multiple steps: PDF generation, chapter creation, pandoc conversion
- Opens the final PDF in Skim viewer

**Examples**

- Generate book chapter for data605 lesson 01.1:
  ```bash
  > ./gen_book_chapter.py data605 01.1
  ```

- Generate book chapter for msml610 lesson 02.3:
  ```bash
  > ./gen_book_chapter.py msml610 02.3
  ```

### `gen_lecture_script.py`

**What It Does**

- Generates a complete lecture script from slides using LLM
- Creates intro and outro sections automatically
- Combines all sections and lints the final output

**Examples**

- Generate lecture script for data605 lesson 01.1:
  ```bash
  > ./gen_lecture_script.py data605 01.1
  ```

- Generate lecture script with extra options:
  ```bash
  > ./gen_lecture_script.py msml610 02.3 --force
  ```

### `gen_quizzes.py`

**What It Does**

- Generates questions from lecture content using LLM via llm_cli.py
- Two modes:
  - Multiple choice quizzes: 20 questions with 5 answers each
    - Saved to: `{DIR}/lectures_quizzes/<lesson>.quizzes.md`
  - Discussion/review questions: 3-6 open-ended questions
    - Saved to: `{DIR}/lectures_recap/<lesson>.recap.md`
- Automatically formats output using lint_txt.py with prettier (use `--no_lint` to skip)

**Examples**

- Generate multiple choice quizzes for data605 lesson 01.1:
  ```bash
  > ./gen_quizzes.py --for_class_quizzes data605 01.1
  ```

- Generate discussion/review questions for msml610 lesson 02.3:
  ```bash
  > ./gen_quizzes.py --for_class_recap msml610 02.3
  ```

- Generate quizzes without linting:
  ```bash
  > ./gen_quizzes.py --for_class_recap data605 01.2 --no_lint
  ```

- Generate quizzes with extra LLM options:
  ```bash
  > ./gen_quizzes.py --for_class_quizzes data605 01.1 --model gpt-4
  ```

### `gen_slides.py`

**What It Does**

- Generates lecture slide PDFs from source files
- Uses notes_to_pdf.py to convert markdown to PDF
- Accepts additional options to pass through to notes_to_pdf.py

**Examples**

- Generate slides for data605 lesson 01.1:
  ```bash
  > ./gen_slides.py data605 01.1
  ```

- Generate slides with extra options:
  ```bash
  > ./gen_slides.py msml610 02.3 --theme dark
  ```

### `get_lecture_file.py`

**What It Does**

- Finds and prints the path to a lecture source file
- Searches for files matching `{DIR}/lectures_source/Lesson{LESSON}*`
- Validates that exactly one matching file exists

**Examples**

- Find lecture file for data605 lesson 01.1:
  ```bash
  > ./get_lecture_file.py data605 01.1
  ```

- Find lecture file for msml610 lesson 02.3:
  ```bash
  > ./get_lecture_file.py msml610 02.3
  ```

### `slide_check.py`

**What It Does**

- Checks and fixes text in lecture slides using LLM
- Uses process_slides.py with text_check_fix action
- Corrects spelling, grammar, and formatting issues

**Examples**

- Check and fix slides for data605 lesson 01.1:
  ```bash
  > ./slide_check.py data605 01.1
  ```

- Check slides with extra options:
  ```bash
  > ./slide_check.py msml610 02.3 --dry-run
  ```

### `slide_improve.py`

**What It Does**

- Improves lecture slides using LLM suggestions
- Uses process_slides.py with slide_improve action
- Enhances clarity, structure, and pedagogical effectiveness

**Examples**

- Improve slides for data605 lesson 01.1:
  ```bash
  > ./slide_improve.py data605 01.1
  ```

- Improve slides with extra options:
  ```bash
  > ./slide_improve.py msml610 02.3 --max-suggestions 5
  ```

### `slide_reduce.py`

**What It Does**

- Reduces and simplifies lecture slides using LLM
- Uses process_slides.py with slide_reduce action
- Removes redundancy and condenses content

**Examples**

- Reduce slides for data605 lesson 01.1:
  ```bash
  > ./slide_reduce.py data605 01.1
  ```

- Reduce slides with extra options:
  ```bash
  > ./slide_reduce.py msml610 02.3 --target-length 50
  ```

### `process_lessons.py`

**What It Does**

- Main script for generating PDF slides and reading scripts from lecture source
  files
- Supports multiple actions including PDF generation script generation and LLM
  transformations
- Can process single or multiple lectures using pattern matching
- Provides dry-run mode to preview commands without execution

**Examples**

- Generate PDF slides for a specific lecture:
  ```bash
  > process_lessons.py --lectures 01.1 --class data605 --action generate_pdf
  ```

- Generate reading scripts for multiple lectures:
  ```bash
  > process_lessons.py --lectures 01*:02* --class data605 --action generate_script
  ```

- Generate both PDFs and scripts:
  ```bash
  > process_lessons.py --lectures 01* --class msml610 --action generate_pdf --action generate_script
  ```

- Generate all slides for multiple lessons:
  ```bash
  > process_lessons.py --lectures 0*:1* --class data605 --action generate_pdf
  ```

## Check correctness of all the slides

- Check one lecture from inside the container (advanced)
  ```bash
  > SRC_NAME=$(ls $DIR/lectures_source/Lesson02*); echo $SRC_NAME
  > DST_NAME=process_slides.txt
  docker> process_slides.py --in_file $SRC_NAME --action text_check --out_file $DST_NAME --use_llm_transform --limit 0:10
  > vimdiff $SRC_NAME process_slides.txt
  ```
  This runs the check inside Docker and compares the output with vimdiff.

## Improve slides

- Improve a specific lecture using LLM
  ```bash
  > llm_transform.py -i data605/lectures_source/Lesson07.2-Data_Wrangling.txt -p slide_improve -v DEBUG
  ```
  This uses AI to improve the content and formatting of the slides.

## Reduce all slides

- Reduce from inside the container (advanced)
  ```bash
  > SRC_NAME=$(ls $DIR/lectures_source/Lesson04.2*); echo $SRC_NAME
  > process_slides.py --in_file $SRC_NAME --action slide_reduce --out_file $SRC_NAME --use_llm_transform --limit 0:10
  ```
  This reduces only the first 10 slides using the container environment.

## Generate the PDF for all the slides

- Generate PDFs for multiple lessons
  ```bash
  > process_lessons.py --lectures 0*:1* --class data605 --action generate_pdf
  ```
  This generates PDF files for all lessons starting with 0 or 1 (e.g., 01.1, 01.2, 10.1, etc.).

## Generate the lecture script

- Generate the intro for a lecture
  ```bash
  > TAG=08.3; llm_cli.py -i data605/lectures_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to do an introduction in 50 word the content of the slides starting with In this lesson" -o -
  ```
  This creates a 50-word introduction for Lesson 08.3.

- Generate the outro for a lecture
  ```bash
  > TAG=08.3; llm_cli.py -i data605/lectures_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to summarize what was discussed in less than 50 word in the slides like In this lesson we have discussed" -o -
  ```
  This creates a 50-word summary/conclusion for Lesson 08.3.

- Generate script from inside a container (advanced)
  ```bash
  > i docker_bash --base-image=623860924167.dkr.ecr.eu-north-1.amazonaws.com/cmamp --skip-pull

  docker> sudo /bin/bash -c "(source /venv/bin/activate; pip install --upgrade openai)"

  docker> generate_slide_script.py \
    --in_file data605/lectures_source/Lesson01-Intro.txt \
    --out_file data605/lectures_source/Lesson01-Intro.script.txt \
    --slides_per_group 3 \
    --limit 1:5
  ```
  This generates a script for slides 1-5, grouping 3 slides at a time.

## Convert markdown to PDF

- Convert markdown notes to PDF slides
  ```bash
  > notes_to_pdf.py --input data605/lectures_md/final_enhanced_markdown_lecture_2.txt --output tmp.pdf --type slides --skip_action cleanup_after --debug_on_error --toc_type navigation --filter_by_slides 1:4
  ```
  This converts markdown lecture notes to PDF format (slides 1-4 only).

## Run the tutorials

- Start Jupyter in Docker
  ```bash
  > cd msml610/tutorials
  > i docker_jupyter --skip-pull --stage local --version 1.0.0
  ```
  This starts a Jupyter Lab server in a Docker container.

- Open a specific notebook
  ```bash
  > open -a "Chrome" http://127.0.0.1:5011/lab/tree/notebooks/Bayesian_Coin.ipynb
  ```
  This opens the Bayesian Coin tutorial in Chrome.

## Fix slides with LLM

- Fix slides using a prompt template
  ```bash
  > FILE=data605/lectures_source/Lesson09.2-Spark_Primitives.txt
  > llm_cli.py --input $FILE -pf "fix_slides.prompt.md" -o improved.md --model "gpt-4o" -b
  ```
  This uses GPT-4o to fix and improve the slides based on the prompt template.

# process_lessons.py
## Goal

This script generates PDF slides and/or reading scripts for lecture materials, and
can process slides using LLM transformations

## Usage Examples

- Generate PDF slides for a specific lecture
  ```bash
  > process_lessons.py --lectures 01.1 --class data605 --action generate_pdf
  ```

- Generate reading scripts for multiple lectures
  ```bash
  > process_lessons.py --lectures 01*:02* --class data605 --action generate_script
  ```

- Generate both PDFs and scripts
  ```bash
  > process_lessons.py --lectures 01* --class msml610 --action generate_pdf --action generate_script
  ```

- Generate using default actions (generate_pdf only)
  ```bash
  > process_lessons.py --lectures 01* --class msml610
  ```

- Generate all available actions
  ```bash
  > process_lessons.py --lectures 01* --class data605 --all
  ```

- Skip specific actions
  ```bash
  > process_lessons.py --lectures 01* --class data605 --skip_action generate_script
  ```

- Reduce slides using LLM transformation (modifies in place)
  ```bash
  > process_lessons.py --lectures 01.1 --class data605 --action reduce_slide
  ```

- Check slides using LLM transformation (creates separate report)
  ```bash
  > process_lessons.py --lectures 01.1 --class data605 --action check_slide
  ```

- Generate specific slides from a lecture
  ```bash
  > process_lessons.py --lectures 01.1 --limit 1:3 --class data605 --action generate_pdf
  ```

- Process all lectures in a class
  ```bash
  > process_lessons.py --lectures "0*" --class data605 --action generate_pdf --action generate_script
  ```

## Command Line Arguments

- `--lectures`: Lecture pattern(s) to process. Can be:
  - Single lecture: `01.1`
  - Wildcard pattern: `01*`
  - Multiple patterns: `01*:02*:03.1` (separated by colons)
- `--class`: Class directory name (`data605` or `msml610`)
- `--action`: Actions to execute. Can be specified multiple times:
  - `generate_pdf`: Generate PDF slides
  - `generate_script`: Generate reading scripts
  - `reduce_slide`: Reduce slides using LLM transformation (modifies source in
    place)
  - `check_slide`: Check slides using LLM transformation (creates separate
    report file)
  - `improve_slide`: Improve slides using LLM transformation
  - `book_chapter`: Generate book chapter PDF from lecture content
  - `generate_class_quizzes`: Generate multiple choice quizzes from lecture
    content
  - `generate_class_recap`: Generate open-ended discussion/review questions from
    lecture content
  - Default: `generate_pdf` (if no action specified)
- `--skip_action`: Actions to skip (mutually exclusive with `--action`)
- `--all`: Execute all available actions (mutually exclusive with `--action`)
- `--limit`: Slide range to process (e.g., `1:3`). Only valid when a single
  lecture file matches the pattern. Only applies to `generate_pdf` action.
- `--dry_run`: Print commands without executing them
- `--log_level`: Logging verbosity (optional)

## Architecture

### Data Flow

```
- Command Line Arguments
- Parse patterns, actions, and options
- Select actions to execute (based on --action, --skip_action, --all, or defaults)
- Find matching lecture files
- For each file:
  - Process PDF action (if selected)
    - notes_to_pdf.py → lectures/*.pdf
  - Process script action (if selected)
    - generate_slide_script.py → lectures_script/*.script.txt
    - perl (remove prefixes) → lectures_script/*.script.txt
    - lint_txt.py → lectures_script/*.script.txt
  - Process slide_reduce action (if selected)
    - process_slides.py --action slide_reduce --use_llm_transform → modifies source in place
  - Process slide_check action (if selected)
    - process_slides.py --action slide_check --use_llm_transform → creates *.slide_check.txt
```

### Directory Structure

```
{class_dir}/
  lectures_source/     # Input: Lesson*.txt files
  lectures/            # Output: Generated PDF files
  lectures_script/     # Output: Generated script files
  lectures_quizzes/    # Output: Multiple choice quiz files
  lectures_recap/      # Output: Discussion/recap question files
  book/                # Output: Book chapter files
```
