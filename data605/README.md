# Summary

This directory contains course materials for DATA605, including lecture content,
tutorials, book chapters, and supporting infrastructure for building and
deploying course materials

# Directory Structure

## Course Content

- `lectures/`: Final compiled lecture PDFs organized by lesson number
  - Contains all lecture presentations in PDF format
  - Named as `Lesson##.#-Topic.pdf`

- `lectures_source/`: Source text files for lecture content
  - Contains raw text content for lectures
  - Includes images directory with lecture diagrams and figures
  - Used as input for generating lecture PDFs

- `lectures_video_script/`: Video presentation scripts for lectures
  - Contains script files with speaking notes for each lesson
  - Named as `Lesson##.#-Topic.script.txt`

- `lectures_recap.secret/`: Lecture recap materials

## Book and Publishing

- `book/`: Compiled book chapters and full course book
  - Contains individual chapter PDFs
  - Includes full `book.pdf` combining all chapters
  - Contains PNG image directories for each chapter

## Tutorials

- `tutorials/`: Hands-on tutorial materials organized by topic
  - `tutorial_airflow/`: Apache Airflow workflow tutorials
  - `tutorial_dask/`: Dask parallel computing tutorials
  - `tutorial_docker/`: Docker containerization tutorials
  - `tutorial_docker_compose/`: Docker Compose multi-container tutorials
  - `tutorial_git/`: Git version control tutorials
  - `tutorial_github/`: GitHub platform tutorials
  - `tutorial_jupyter/`: Jupyter notebook tutorials
  - `tutorial_mongodb/`: MongoDB database tutorials
  - `tutorial_pandas/`: Pandas data analysis tutorials
  - `tutorial_parquet/`: Parquet file format tutorials
  - `tutorial_postgres/`: PostgreSQL database tutorials
  - `tutorial_spark/`: Apache Spark tutorials

## Infrastructure

- `dev_scripts/`: Development automation scripts
  - Contains Docker management scripts
  - Includes formatting and linting utilities
  - Contains Jupyter and tmux setup scripts

- `project_template/`: Shared Docker configuration files
  - Contains common Docker setup scripts
  - Includes bashrc and sudoers configuration
  - Contains Jupyter extension installation scripts

- `gp/`: Group project database materials
  - Contains SQL dump file for project database
  - Includes README with group project instructions

## Archives

- `lectures_Spring2023/`: Archived lecture PDFs from Spring 2023 semester
  - Historical reference materials

- `lectures_Spring2025/`: Archived lecture PDFs from Spring 2025 semester
  - Historical reference materials

# Generating Course Syllabus and Table of Contents

## Overview

Extract headers and create a comprehensive syllabus from all lecture materials using the `for_loop_lessons.py` orchestration script.

## Generate Complete Course Syllabus

Extract all lecture headers and create a consolidated syllabus:

```bash
cd /Users/saggese/src/umd_classes1
for_loop_lessons.py --class data605 --action generate_toc
```

This generates:
- **Output file**: `data605/all_tocs.md`
- **Content**: All lecture headers organized hierarchically (up to 5 levels deep)
- **Format**: Markdown with lecture structure preserved

## Generate Syllabus for Specific Lectures

Extract headers from a subset of lectures using pattern matching:

```bash
# Single lecture pattern
for_loop_lessons.py --class data605 --lectures "01*" --action generate_toc

# Multiple lecture patterns (colon-separated)
for_loop_lessons.py --class data605 --lectures "01*:02*:03.1" --action generate_toc

# Continuous range (inclusive)
for_loop_lessons.py --class data605 --lectures "01.1-03.2" --action generate_toc
```

## Implementation Details

The `generate_toc` action:
1. Iterates through all specified lecture source files in `lectures_source/`
2. Calls `extract_toc_from_txt.py` to extract headers from each file (up to 5 levels)
3. Prepends each lecture's headers with the lecture filename as a header
4. Consolidates all extracted headers into a single markdown file
5. Outputs to `<class>/all_tocs.md` (e.g., `data605/all_tocs.md`)

## Output Format

The syllabus markdown file contains structured headers with proper indentation:
```markdown
# Lesson01.1-Intro.txt

## Main Topic
### Subtopic 1
#### Sub-subtopic
### Subtopic 2

# Lesson01.2-Topic.txt

## Another Main Topic
...
```

This provides a complete overview of the course curriculum and lecture structure.
