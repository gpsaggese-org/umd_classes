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

TL;DR: Manage all your markdown files (blogs, skills, research, stories) from one unified command instead of juggling multiple directories.

<!-- more -->

## The Problem: Scattered Content

If you maintain multiple types of markdown content—blog posts, skill documentation, research notes, and stories—you know the pain. Each lives in a different directory structure, requires different workflows, and forces you to remember which command goes where.

Writing `md skill edit notebook.utils_library` works fine until you need to switch to a different directory for a blog post. Finding research ideas means typing long paths instead of simple commands. You can't quickly list all your content types without constant context switching.

The friction adds up. What if you could manage everything from one place?

## Enter the `md` Command
The `md` command is a unified interface for managing four types of markdown
content:

- **skill**: `.claude/skills/` directory—Claude Code skill documentation
- **blog**: `blog/posts/` directory—blog posts
- **research**: `research/ideas/` directory—research notes and ideas
- **story**: `short_stories/` directory—short story content

Instead of remembering different directory paths and commands, you get a
consistent interface that works the same way regardless of content type.

## Core Actions
The `md` command supports four main actions:

- **list**: Show files matching a pattern (supports prefix matching)
- **edit**: Create or edit files in your preferred editor
- **describe**: List files with their descriptions
- **directory**: Print the directory path for a content type

## Usage Examples
List all your skills:
```bash
> md skill list
> md sk l
```

Edit or create a blog post:
```bash
> md blog edit My_New_Post
```

Find research items about causality:
```bash
> md research list causal
> md res l causal
```

Show descriptions of all stories:
```bash
> md story describe
> md story de
```

Print the skill directory path:
```bash
> md sk dir
```

## Smart Prefix Matching
Both content types and actions support prefix matching—type only the first
letters and the command figures out the rest:

- `sk` → `skill`, `bl` → `blog`, `res` → `research`, `st` → `story`
- `l` → `list`, `e` → `edit`, `de` → `describe`, `dir` → `directory`

This means fewer keystrokes and faster content management.

## Multiple Edits
Need to update multiple skills at once? The `edit` action supports editing
multiple files in a single command:
```bash
> md skill edit notebook.utils_library notebook.split_cells
```

Both files open in your editor, and you can edit them together. Perfect for
refactoring related content.

## Pattern Matching for Discovery
When listing, you can filter by pattern. This makes discovery fast:
```bash
> md research list causal        # Find research about causality
> md blog list optimization      # Find posts about optimization
> md skill list notebook         # Find notebook-related skills
```

The pattern is case-insensitive and matches any part of the filename.

## Why This Matters
Single, consistent interface reduces cognitive load. You don't need to remember
directory paths, different command syntaxes, or whether you're editing in the
skills directory or the blog directory.

The `md` command treats all your content equally—whether it's a blog post,
research note, skill documentation, or story, the workflow is the same.

## Getting Started
The `md` command is part of the development tools in the helpers repository. To
use it:
```bash
> md skill list                           # See what you can manage
> md blog edit My_First_Post             # Create your first blog post
> md research describe                    # Explore your research ideas
```

Start with `md --help` to see the full documentation built into the command
itself.

## The Pattern Extends
This unified approach to content management is powerful because it's extensible.
As you add new content types or directories, the same pattern applies—consistent
actions, consistent naming, consistent behavior.

One command to manage them all.
