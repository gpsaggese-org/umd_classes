# class_scripts

Course management tools and utilities for generating lecture materials.

## Structure of the Dir

```
{class_dir}/
  lectures_source/     # Input: Lesson*.txt files
  lectures/            # Output: Generated PDF files
  lectures_script/     # Output: Generated script files
  lectures_quizzes/    # Output: Multiple choice quiz files
  lectures_recap/      # Output: Discussion/recap question files
  book/                # Output: Book chapter files
```

## Description of Files

- `common_utils.py`: Shared utility functions for argument validation, file finding, directory management, and PDF page counting

| Script | Location | Description |
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

---

# Available Scripts Reference

## Counting and Analysis Scripts

### `count_book_pages.py`

Counts pages in all PDF files in the `{DIR}/book/` directory using macOS `mdls` command to extract PDF metadata.

**Usage:**
```bash
> ./count_book_pages.py data605
> ./count_book_pages.py msml610
```

### `count_lecture_pages.py`

Counts pages in all PDF files in the `{DIR}/lectures/` directory and displays page counts for each lecture PDF file.

**Usage:**
```bash
> ./count_lecture_pages.py data605
> ./count_lecture_pages.py msml610
```

### `count_words.py`

Counts words in all files in the `{DIR}/lectures_script/` directory to help track lecture length and content volume.

**Usage:**
```bash
> ./count_words.py data605
> ./count_words.py msml610
```

## Generation Scripts

### `gen_slides.py`

Generates lecture slide PDFs from source files using `notes_to_pdf.py` to convert markdown to PDF. Accepts additional options to pass through to `notes_to_pdf.py`.

**Usage:**
```bash
> ./gen_slides.py data605 01.1
> ./gen_slides.py msml610 02.3 --theme dark
```

### `gen_lecture_script.py`

Generates complete lecture scripts from slides using LLM. Automatically creates intro and outro sections, combines all sections, and lints the final output.

**Usage:**
```bash
> ./gen_lecture_script.py data605 01.1
> ./gen_lecture_script.py msml610 02.3 --force
```

### `gen_book_chapter.py`

Generates a book chapter from lecture source material. Performs PDF generation, chapter creation, and pandoc conversion, then opens the final PDF in Skim viewer.

**Usage:**
```bash
> ./gen_book_chapter.py data605 01.1
> ./gen_book_chapter.py msml610 02.3
```

### `gen_quizzes.py`

Generates questions from lecture content using LLM. Supports two modes:
- Multiple choice quizzes: 20 questions with 5 answers each → `{DIR}/lectures_quizzes/<lesson>.quizzes.md`
- Discussion/review questions: 3-6 open-ended questions → `{DIR}/lectures_recap/<lesson>.recap.md`
- Automatically formats output using `lint_txt.py` with prettier (use `--no_lint` to skip)

**Usage:**
```bash
> ./gen_quizzes.py --for_class_quizzes data605 01.1
> ./gen_quizzes.py --for_class_recap msml610 02.3
> ./gen_quizzes.py --for_class_recap data605 01.2 --no_lint
> ./gen_quizzes.py --for_class_quizzes data605 01.1 --model gpt-4
```

## Slide Improvement Scripts

### `slide_check.py`

Checks and fixes text in lecture slides using LLM. Corrects spelling, grammar, and formatting issues using `process_slides.py` with `text_check_fix` action.

**Usage:**
```bash
> ./slide_check.py data605 01.1
> ./slide_check.py msml610 02.3 --dry-run
```

### `slide_improve.py`

Improves lecture slides using LLM suggestions. Enhances clarity, structure, and pedagogical effectiveness using `process_slides.py` with `slide_improve` action.

**Usage:**
```bash
> ./slide_improve.py data605 01.1
> ./slide_improve.py msml610 02.3 --max-suggestions 5
```

### `slide_reduce.py`

Reduces and simplifies lecture slides using LLM. Removes redundancy and condenses content using `process_slides.py` with `slide_reduce` action.

**Usage:**
```bash
> ./slide_reduce.py data605 01.1
> ./slide_reduce.py msml610 02.3 --target-length 50
```

## Utility Scripts

### `get_lecture_file.py`

Finds and prints the path to a lecture source file matching `{DIR}/lectures_source/Lesson{LESSON}*`. Validates that exactly one matching file exists.

**Usage:**
```bash
> ./get_lecture_file.py data605 01.1
> ./get_lecture_file.py msml610 02.3
```

## Orchestration Scripts

### `process_lessons.py`

Main orchestration script for generating PDF slides and/or reading scripts from lecture materials. Supports multiple actions, pattern matching, and dry-run mode.

**Actions:**
- `generate_pdf`: Generate PDF slides
- `generate_script`: Generate reading scripts
- `reduce_slide`: Reduce slides using LLM transformation (modifies source in place)
- `check_slide`: Check slides using LLM transformation (creates separate report file)
- `improve_slide`: Improve slides using LLM transformation
- `book_chapter`: Generate book chapter PDF from lecture content
- `generate_class_quizzes`: Generate multiple choice quizzes from lecture content
- `generate_class_recap`: Generate open-ended discussion/review questions from lecture content

**Lecture Patterns:**
- Single lecture: `01.1`
- Wildcard pattern: `01*`
- Multiple patterns: `01*:02*:03.1` (separated by colons)

**Usage:**
```bash
> process_lessons.py --lectures 01.1 --class data605 --action generate_pdf
> process_lessons.py --lectures 01*:02* --class data605 --action generate_script
> process_lessons.py --lectures 01* --class msml610 --action generate_pdf --action generate_script
> process_lessons.py --lectures 01* --class msml610  # Default: generate_pdf
> process_lessons.py --lectures 01* --class data605 --all
> process_lessons.py --lectures 01* --class data605 --skip_action generate_script
> process_lessons.py --lectures 01.1 --limit 1:3 --class data605 --action generate_pdf
> process_lessons.py --lectures "0*" --class data605 --action generate_pdf --action generate_script
```

**Command Line Arguments:**
- `--lectures`: Lecture pattern(s) to process
- `--class`: Class directory name (`data605` or `msml610`)
- `--action`: Actions to execute (can be specified multiple times)
- `--skip_action`: Actions to skip (mutually exclusive with `--action`)
- `--all`: Execute all available actions (mutually exclusive with `--action`)
- `--limit`: Slide range to process (e.g., `1:3`). Only valid when a single lecture file matches the pattern. Only applies to `generate_pdf` action
- `--dry_run`: Print commands without executing them
- `--log_level`: Logging verbosity (optional)

---

# Common Workflows

## Generating Course Materials

### Generate PDF slides for all lessons in a course

```bash
> process_lessons.py --lectures "0*:1*" --class data605 --action generate_pdf
```

Generates PDF files for all lessons starting with 0 or 1 (e.g., 01.1, 01.2, 10.1, etc.) in `data605/lectures/`.

### Generate both PDF slides and reading scripts

```bash
> process_lessons.py --lectures 01* --class msml610 --action generate_pdf --action generate_script
```

Generates PDFs in `lectures/` and scripts in `lectures_script/`.

### Generate PDF and book chapter for a single lesson

```bash
> process_lessons.py --lectures 01.1 --class data605 --action generate_pdf --action book_chapter
```

Creates slide PDF and corresponding book chapter with pandoc conversion.

## Assessment Generation

### Generate multiple choice quizzes

```bash
> process_lessons.py --lectures 01* --class data605 --action generate_class_quizzes
```

Creates 20-question quizzes saved to `lectures_quizzes/<lesson>.quizzes.md`.

Alternatively, use the direct script:
```bash
> ./gen_quizzes.py --for_class_quizzes data605 01.1
```

### Generate discussion/review questions

```bash
> process_lessons.py --lectures 01* --class data605 --action generate_class_recap
```

Creates 3-6 open-ended discussion questions saved to `lectures_recap/<lesson>.recap.md`.

Alternatively, use the direct script:
```bash
> ./gen_quizzes.py --for_class_recap data605 01.1
```

## Slide Quality Improvement

### Check and fix spelling/grammar in slides

```bash
> process_lessons.py --lectures 01.1 --class data605 --action check_slide
```

Advanced usage (check one lecture from inside the container):
```bash
> SRC_NAME=$(ls $DIR/lectures_source/Lesson02*); echo $SRC_NAME
> DST_NAME=process_slides.txt
docker> process_slides.py --in_file $SRC_NAME --action text_check --out_file $DST_NAME --use_llm_transform --limit 0:10
> vimdiff $SRC_NAME process_slides.txt
```

Alternatively, use the direct script:
```bash
> ./slide_check.py data605 01.1
```

### Improve slide clarity and structure

```bash
> process_lessons.py --lectures 01.1 --class data605 --action improve_slide
```

Alternatively, use the direct script:
```bash
> ./slide_improve.py data605 01.1
```

Or use `llm_transform.py` directly:
```bash
> llm_transform.py -i data605/lectures_source/Lesson07.2-Data_Wrangling.txt -p slide_improve -v DEBUG
```

### Reduce slide length and remove redundancy

```bash
> process_lessons.py --lectures 01.1 --class data605 --action reduce_slide
```

Advanced usage (reduce from inside the container):
```bash
> SRC_NAME=$(ls $DIR/lectures_source/Lesson04.2*); echo $SRC_NAME
> process_slides.py --in_file $SRC_NAME --action slide_reduce --out_file $SRC_NAME --use_llm_transform --limit 0:10
```

Alternatively, use the direct script:
```bash
> ./slide_reduce.py data605 01.1
```

### Fix slides with custom LLM prompt

```bash
> FILE=data605/lectures_source/Lesson09.2-Spark_Primitives.txt
> llm_cli.py --input $FILE -pf "fix_slides.prompt.md" -o improved.md --model "gpt-4o" -b
```

Uses GPT-4o to fix and improve slides based on a prompt template.

## Lecture Script Generation

### Generate complete lecture script with intro/outro

```bash
> ./gen_lecture_script.py data605 01.1
```

Or use `process_lessons.py`:
```bash
> process_lessons.py --lectures 01.1 --class data605 --action generate_script
```

### Generate just the intro for a lecture

```bash
> TAG=08.3; llm_cli.py -i data605/lectures_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to do an introduction in 50 word the content of the slides starting with In this lesson" -o -
```

Creates a 50-word introduction for Lesson 08.3.

### Generate just the outro/summary for a lecture

```bash
> TAG=08.3; llm_cli.py -i data605/lectures_script/Lesson${TAG}*.script.txt -p "You are a college professor and you need to summarize what was discussed in less than 50 word in the slides like In this lesson we have discussed" -o -
```

Creates a 50-word summary/conclusion for Lesson 08.3.

### Generate scripts from inside a container (advanced)

```bash
> i docker_bash --base-image=623860924167.dkr.ecr.eu-north-1.amazonaws.com/cmamp --skip-pull

docker> sudo /bin/bash -c "(source /venv/bin/activate; pip install --upgrade openai)"

docker> generate_slide_script.py \
  --in_file data605/lectures_source/Lesson01-Intro.txt \
  --out_file data605/lectures_source/Lesson01-Intro.script.txt \
  --slides_per_group 3 \
  --limit 1:5
```

Generates a script for slides 1-5, grouping 3 slides at a time.

## Format Conversion

### Convert markdown notes to PDF slides

```bash
> notes_to_pdf.py --input data605/lectures_md/final_enhanced_markdown_lecture_2.txt --output tmp.pdf --type slides --skip_action cleanup_after --debug_on_error --toc_type navigation --filter_by_slides 1:4
```

Converts markdown lecture notes to PDF format (slides 1-4 only).

## Analysis and Reporting

### Count pages in all book PDFs

```bash
> ./count_book_pages.py data605
```

### Count pages in all lecture PDFs

```bash
> ./count_lecture_pages.py data605
```

### Count words in all lecture scripts

```bash
> ./count_words.py data605
```

Helps track lecture length and content volume.

## Partial Processing

### Generate specific slides from a lecture (slides 1-3 only)

```bash
> process_lessons.py --lectures 01.1 --limit 1:3 --class data605 --action generate_pdf
```

Only applies to `generate_pdf` action when a single lecture file matches.

### Preview commands without executing (dry-run)

```bash
> process_lessons.py --lectures 01* --class data605 --action generate_pdf --dry_run
```

Prints all commands that would be executed without running them.

## Running Interactive Tutorials

### Start Jupyter Lab in Docker

```bash
> cd msml610/tutorials
> i docker_jupyter --skip-pull --stage local --version 1.0.0
```

Starts a Jupyter Lab server in a Docker container.

### Open a specific notebook in Chrome

```bash
> open -a "Chrome" http://127.0.0.1:5011/lab/tree/notebooks/Bayesian_Coin.ipynb
```

Opens the Bayesian Coin tutorial in Chrome.

