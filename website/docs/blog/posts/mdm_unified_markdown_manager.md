---
title: "Unified Markdown Manager: One Command to Rule All Your Content"
authors:
  - gpsaggese
date: 2026-03-29
description: "Simplify managing markdown files across your projects with a single command"
categories:
  - Productivity
  - Developer Tools
---

TL;DR: Manage all your markdown files (blogs, skills, research) from one unified
command instead of juggling multiple directories.

<!-- more -->

## The Problem: Scattered Content
Different types of markdown (e.g., blog posts, agent skill documentation, and
research notes) live in separate directories with distinct commands and
workflows. Searching across content types means knowing each directory's
location.

`mdm` was built to solve this.

## The Solution: A Unified Interface
The `mdm` (Markdown Manager) script provides a consistent interface for managing
different types of markdown content across your projects:

- **skill**: `.claude/skills/` directory—Claude Code skill documentation
- **blog**: `blog/posts/` directory—blog posts and articles
- **research**: `research/ideas/` directory—research notes and conceptual ideas
- **story**: `short_stories/` directory—creative writing and short story content

One command works for all four types. Same interface, same predictable behavior,
whether you're managing blog posts or research notes. The script merges what
were separate bash families (`skill*`, `blog*`, `res*`, `story*`) into a single
tool.

## Core Actions
- **list**: Display files (skill names for skills, full paths for others).
  Supports pattern filtering
- **full_list**: Display all files with complete paths
- **edit**: Open file in editor, or create new with template
- **directory**: Print the directory path

## Usage Examples

### Discovering Your Content
View all available skills in your system (displaying skill names only):
```bash
> mdm skill list
> mdm sk l
```

Shows all skills by name (e.g., `blog.add_figures`,
`notebook.format_rules`)—useful for auditing what you have or finding something
you half-remember.

### Full Path Listing
Display all files with their complete filesystem paths:
```bash
> mdm skill full_list
> mdm res f
```

Useful when you need the absolute path for scripting or batch operations.

### Creating and Editing Content
Create a new blog post or edit an existing one:
```bash
> mdm blog edit My_New_Post
```

The editor opens directly to the file, whether it exists or not. If the file
doesn't exist, `mdm` automatically creates it with an appropriate template—blog
posts receive YAML frontmatter with title, author, date fields, and skill files
receive a summary section header.

### Pattern-Based Searching
Find all research notes related to causality:
```bash
> mdm research list causal
> mdm res l causal
```

Pattern matching works across all content types, enabling quick discovery
without manually browsing directories.

### Accessing Directories
Retrieve the full path to a content type's directory:
```bash
> mdm sk dir
```

Useful when you need direct filesystem access or want to perform batch
operations on multiple files.

## Smart Prefix Matching
Both content types and actions support intelligent prefix matching, allowing you
to type only the first letters of a command and let the system resolve the
complete term:

- Content type shortcuts: `sk` → `skill`, `bl` → `blog`, `res` → `research`,
  `st` → `story`
- Action shortcuts: `l` → `list`, `f` → `full_list`, `e` → `edit`, `d` →
  `directory`

So `mdm sk l` works the same as
`mdm skill list`.

## Batch Operations
When refactoring or coordinating updates across related documentation, the
`edit` action supports simultaneous editing of multiple files:
```bash
> mdm skill edit notebook.utils_library notebook.split_cells
```

Both files open at once, so you can sync changes across related documentation
without constant context-switching.

## Why This Works
Muscle memory transfers instantly. Learn the patterns once with blog posts, and
they work the same way with skills or research notes. No context-switching tax.
No decision fatigue.

Automatic template generation means you never stare at a blank file—each new
post or skill gets initialized with the right structure already in place.

## Getting Started
Run these three commands and you'll have the idea:
```bash
> mdm skill list      # View all available skills
> mdm blog edit My_First_Post  # Create and open a new blog post
> mdm research list   # List all research items
```

For more, `--help` has the full details.

## Scaling to New Content Types
Add a fifth content type tomorrow and the same patterns apply. No new command
structures to learn. No friction.

Teams benefit immediately—when someone new joins and needs to manage
documentation, they're productive from day one because the interface is already
predictable.
