# Summary

This directory contains course materials for MSML610, including lecture content,
tutorials, book chapters, and supporting infrastructure for building and
deploying course materials

# Directory Structure

## Course Content

- `lectures/`: Final compiled lecture PDFs organized by lesson number
  - Contains all lecture presentations in PDF format
  - Named as `Lesson##.#-Topic.pdf`

- `lectures_source/`: Source text files for lecture content
  - Contains raw text content for lectures
  - Includes `figures/` and `figures.hires/` directories with lecture diagrams
  - Includes `covers/` directory with lesson covers
  - Used as input for generating lecture PDFs

- `lectures_tex/`: LaTeX source files for lectures
  - Contains LaTeX markup for lecture presentations
  - Used for generating final PDF lecture materials

## Book and Publishing

- `book/`: Compiled book chapters and course book materials
  - Contains individual chapter PDFs with `.book_chapter.pdf` suffix
  - Contains text versions of chapters (`.book_chapter.txt`)
  - Contains PNG image directories for each chapter

- `jupyter_book/`: Jupyter Book configuration and build files
  - Contains the Jupyter Book project setup for the course
  - Used for generating interactive HTML versions of course materials

## Tutorials

- `tutorials/`: Hands-on tutorial materials organized by topic
  - Contains Jupyter notebooks and Python scripts for each lesson
  - Named as `L##_##_topic.ipynb` and `L##_##_topic.py`
  - See `helpers/htutorial.py` at repository root for tutorial utility functions
  - Includes `notebook_template.ipynb` for creating new notebooks

## Infrastructure

- `devops/`: Development operations automation
  - `docker_build/`: Docker image build configuration
  - `docker_run/`: Docker container runtime scripts
  - `compose/`: Docker Compose multi-container configuration
  - `env/`: Environment variable configuration

## Supporting Materials

- `mats/`: Course materials and resources
  - Contains additional course-related documents and references

- `test/`: Test suite and validation scripts
  - Contains test files for course materials and utilities

## Archives

- `lectures_Fall2025/`: Archived lecture PDFs from Fall 2025 semester
  - Historical reference materials

# Generating Course Syllabus and Table of Contents

## Overview

Extract headers and create a comprehensive syllabus from all lecture materials using the `for_loop_lessons.py` orchestration script.

## Generate Complete Course Syllabus

Extract all lecture headers and create a consolidated syllabus:

```bash
cd /Users/saggese/src/umd_classes1
for_loop_lessons.py --class msml610 --action generate_toc
```

This generates:
- **Output file**: `msml610/all_tocs.md`
- **Content**: All lecture headers organized hierarchically (up to 5 levels deep)
- **Format**: Markdown with lecture structure preserved

## Generate Syllabus for Specific Lectures

Extract headers from a subset of lectures using pattern matching:

```bash
# Single lecture pattern
for_loop_lessons.py --class msml610 --lectures "01*" --action generate_toc

# Multiple lecture patterns (colon-separated)
for_loop_lessons.py --class msml610 --lectures "01*:02*:03.1" --action generate_toc

# Continuous range (inclusive)
for_loop_lessons.py --class msml610 --lectures "01.1-03.2" --action generate_toc
```

## Implementation Details

The `generate_toc` action:
1. Iterates through all specified lecture source files in `lectures_source/`
2. Calls `extract_toc_from_txt.py` to extract headers from each file (up to 5 levels)
3. Prepends each lecture's headers with the lecture filename as a header
4. Consolidates all extracted headers into a single markdown file
5. Outputs to `<class>/all_tocs.md` (e.g., `msml610/all_tocs.md`)

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
