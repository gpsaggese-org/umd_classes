# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
this repository.

## Overview

This is the **UMD Classes Repository** — a comprehensive collection of educational
materials, tutorials, and projects for two graduate-level computer science courses
at the University of Maryland:

- **DATA605: Big Data Systems** — distributed systems, scalable data engineering,
  and big data technologies
- **MSML610: Advanced Machine Learning** — advanced ML techniques, research
  methods, and applied projects

The repository also contains shared development infrastructure and utilities via
the **helpers** subsystem.

## Repository Architecture

### Course Content Directories

| Directory | Purpose |
|-----------|---------|
| **data605/** | Lectures, tutorials, labs, and materials for DATA605: Big Data Systems |
| **msml610/** | Lectures, tutorials, labs, and materials for MSML610: Advanced Machine Learning |
| **class_project/** | Student project templates, examples, and guidelines |
| **tutorials/** | Standalone ML and data engineering tutorials (generic, not course-specific) |
| **class_scripts/** | Shell scripts and utilities for class operations |
| **dev_scripts_umd_classes/** | Development scripts specific to UMD classes repo management |

### Supporting Directories

| Directory | Purpose |
|-----------|---------|
| **helpers_root/** | Shared development infrastructure, utilities, and tools (see helpers_root/CLAUDE.md) |
| **assets/** | Logos, images, static content |
| **papers/** | Research papers, reading lists, academic references |
| **research/** | Research projects and experimental work |
| **books/** | Book references and educational materials |
| **website/** | Documentation and project website |

### Configuration and Infrastructure

- **`helpers_root/.claude/`** — Shared Claude Code configuration (symlinked as `.claude`)
- **`helpers_root/.pytest_cache/`** — Test cache for development
- **`helpers_root/config_root/`** — Configuration management system
- **`helpers_root/dev_scripts_helpers/`** — Development automation scripts

## Development Guidelines

### For Code Development

For all Python code, development patterns, testing conventions, and module
organization, refer to:

> **→ See `helpers_root/CLAUDE.md`** for comprehensive development guidance

This includes:
- Python code style and conventions
- Testing framework and patterns
- Module naming (`h<module>` convention)
- Task automation via `invoke`
- Linting and code quality checks

Key development commands are documented in `helpers_root/CLAUDE.md`.

### For Educational Content

#### Jupyter Notebooks and Scripts

- Follow `helpers_root/.claude/skills/notebook.format_rules/SKILL.md` for notebook structure
- Pair notebooks with Python scripts using jupytext (`*.py:percent` format)
- Create utility modules (`*_utils.py`) for shared code in tutorials
- Use standard initialization cells with logging setup
- Keep cells focused on single concepts

#### Tutorial Structure

Each tutorial should include:
- **README.md** — Overview and prerequisites
- **Jupyter notebook** — Interactive instruction with examples
- **Python script** — Paired jupytext version of the notebook
- **`*_utils.py`** — Shared utility functions and helpers
- **test/** — Optional test cases for tutorial code

#### Documentation

- Use Markdown following `helpers_root/.claude/skills/markdown.format_rules/SKILL.md`
- Include clear examples and expected outputs
- Add references to external resources
- Keep content up-to-date with latest library versions

### For Projects and Assignments

- Use `class_project/` templates as starting points
- Follow Python conventions from `helpers_root/CLAUDE.md`
- Include clear README with learning objectives
- Provide example solutions or hints in separate branches/directories
- Structure projects for Docker deployment (see `helpers_root/dev_scripts_helpers/`)

## Working with Symlinks

The repository uses symlinks from root to `helpers_root/` for centralized
configuration:

```
.claude → helpers_root/.claude
.pytest_cache → helpers_root/.pytest_cache
.coveragerc → helpers_root/.coveragerc
conftest.py → helpers_root/conftest.py
# ... etc
```

This enables shared configuration while maintaining directory separation. When
working with symlinked files, the actual content lives in `helpers_root/`.

## Key Files and Configuration

- **`helpers_root/repo_config.yaml`** — Repository metadata, Docker config, S3
  buckets
- **`helpers_root/pytest.ini`** — Test markers and configuration
- **`helpers_root/pyproject.toml`** — Ruff linting rules (line length 81, Python
  3.11)
- **`how_to_contribute.md`** — Contribution guidelines for this repository
- **`.gitignore`** — Standard Python/Docker ignore patterns

## Development Workflow

### Creating New Course Material

1. **Create directory structure** under `data605/` or `msml610/`
   ```
   tutorials/Tutorial_Name/
   ├── README.md
   ├── tutorial.ipynb
   ├── tutorial.py (jupytext paired)
   ├── tutorial_utils.py
   ├── Dockerfile (if applicable)
   └── requirements.txt
   ```

2. **Follow code conventions** from `helpers_root/CLAUDE.md`

3. **Add tests** if including substantial code (see testing patterns in
   `helpers_root/CLAUDE.md`)

4. **Document thoroughly** with examples and expected outputs

## Reference Links

- **Repository README**: See `README.md` for public-facing overview
- **Contribution Guide**: `how_to_contribute.md`
- **Helpers Guide**: `helpers_root/CLAUDE.md` (development infrastructure)
- **Course-Specific READMEs**:
  - `data605/README.md` — DATA605 specifics
  - `msml610/README.md` — MSML610 specifics

## Notes for Claude

- This repository serves both **educational** and **development** purposes
- Students and instructors should focus on course directories (`data605/`, `msml610/`)
- Development contributors should also reference `helpers_root/CLAUDE.md`
- All development must follow the patterns and conventions documented in `helpers_root/CLAUDE.md`
- When working with tests or infrastructure, defer to helpers documentation for authoritative patterns
