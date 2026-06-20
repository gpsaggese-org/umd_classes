---
title: "Markdown Viewers on macOS: Terminal and Browser Options"
authors:
    - gpsaggese
date: 2026-06-19
draft: true
categories:
    - Developer Tools
---

TL;DR: Render markdown from terminal using `glow` (for terminal viewing), `mdcat`
(for rich formatting), `grip` (for GitHub-accurate previews with images), or
`pandoc` (for maximum flexibility).

<!-- more -->

## Overview

- Markdown is the standard format for documentation, notes, READMEs, and
  technical writing
- macOS users have several options for viewing Markdown from the command line
- Tools range from simple terminal renderers to full-featured browser previews
  with image support
- Choice depends on your workflow:
    - Terminal-only with attractive formatting: `glow` or `mdcat`
    - GitHub-accurate previews with images: `grip`
    - Document conversion to PDF/HTML: `pandoc`

// TODO(ai_gp): Add link to the github project and documentation
// for each program

// TODO(ai_gp): Add a screenshot for each of this tools using
// ./helpers_root/dev_scripts_helpers/system_tools/save_screenshot.py
// ./helpers_root/dev_scripts_helpers/system_tools/website_screenshot.py

// TODO(ai_gp): Find the last version and release date

## Glow

- **What it is**: One of the most popular terminal Markdown viewers with
  attractive formatting
- **Installation**:
    ```bash
    > brew install glow
    ```
- **Usage**:
    ```bash
    > glow README.md
    ```
- **Advantages**:
    - Fancy terminal interface with multiple themes
    - Fast and lightweight
    - Excellent for reading documentation
    - No dependencies beyond the binary
- **Disadvantages**:
    - Does not display images inline
    - Primarily focused on terminal viewing only
- **Best for**: Everyday terminal documentation reading

- **Tips and tricks**:

- Disable pager
  ```
  > more /Users/saggese/Library/Preferences/glow/glow.yml
  # style name or JSON path (default "auto")
  style: "auto"
  # mouse support (TUI-mode only)
  mouse: true
  # use pager to display markdown
  #pager: true
  # word-wrap at width
  width: 80
  # show all files, including hidden and ignored.
  all: false
  # line-numbers: true
  ```

glow -l --tui website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md

// TODO(ai_gp): Explain tui vs pager

## mdcat

- **What it is**: Rich Markdown renderer written in Rust with advanced
  formatting support
- **Installation**:
    ```bash
    > brew install mdcat
    ```
- **Usage**:
    ```bash
    > mdcat README.md
    ```
- **Advantages**:
    - Excellent formatting quality
    - Handles tables and syntax highlighting well
    - Supports hyperlinks
    - Can display inline images in compatible terminals
- **Disadvantages**:
    - Image support depends on terminal capabilities
    - More complex than Glow
- **Best with**:
// TODO(ai_gp): Explain this
    - Kitty
    - WezTerm
    - Other terminals supporting modern image protocols
- **Best for**: Users with modern terminal emulators seeking rich formatting

## Grip

- **What it is**: Renders Markdown exactly as GitHub would, served locally
  through a web browser
- **Installation**:
    ```bash
    > pip install grip
    ```
- **Usage**:
    ```bash
    > grip README.md
    ```
    Then open `http://localhost:6419`
   - Using `uvx`
    ```
    > uvx grip website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md -b --quiet
    ```
- **Advantages**:
    - GitHub-flavored Markdown rendering
    - Full image support
    - Excellent table rendering
    - Matches GitHub appearance exactly
- **Disadvantages**:
    - Requires a web browser
    - Runs a local web server
- **Best for**: Previewing work before pushing to GitHub

## Pandoc

- **What it is**: The Swiss Army knife of document conversion with multiple
  output formats
- **Installation**:
    ```bash
    > brew install pandoc
    ```
- **Usage examples**:
    ```bash
    > pandoc README.md -o /tmp/readme.html
    > open /tmp/readme.html
    ```
    ```bash
    > pandoc README.md -o README.pdf
    > open README.pdf
    ```
- **Advantages**:
    - Full image support
    - Multiple output formats (HTML, PDF, DOCX, etc.)
    - Highly customizable with templates
    - Industry-standard converter
- **Disadvantages**:
    - More complex than dedicated viewers
    - Primarily a converter rather than a real-time viewer
- **Best for**: Document conversion and maximum flexibility

## mdless

- **What it is**: Pager-like interface for reading Markdown with familiar
  navigation
- **Installation**:
    ```bash
    > brew install mdless
    ```
- **Usage**:
    ```bash
    > mdless README.md
    ```
- **Advantages**:
    - Simple and lightweight
    - Familiar pager interface (`less`-like)
    - Good for large documents
- **Disadvantages**:
    - Limited styling compared to alternatives
    - No image rendering
- **Best for**: Reading long documents with familiar pager shortcuts

## rich-cli

- **What it is**: Colorful terminal rendering built on Python's Rich library
- **Installation**:
    ```bash
    > pip install rich-cli
    ```
- **Usage**:
    ```bash
    > rich README.md
    ```
- **Advantages**:
    - Attractive formatting with color support
    - Easy installation via pip
    - Good Unicode support
- **Disadvantages**:
    - No image rendering
    - Less feature-rich than mdcat
- **Best for**: Quick terminal previews with minimal setup

## Comparison Table

| Tool     | Terminal | Images  | GitHub Style | Browser |
| :------- | :------- | :------ | :----------- | :------ |
| Glow     | Yes      | No      | No           | No      |
| mdcat    | Yes      | Limited | No           | No      |
| mdless   | Yes      | No      | No           | No      |
| rich-cli | Yes      | No      | No           | No      |
| Grip     | No       | Yes     | Yes          | Yes     |
| Pandoc   | Optional | Yes     | Varies       | Yes     |

## Recommended Workflows

- **Reading documentation in the terminal**:
    ```bash
    > glow README.md
    ```
- **Rich terminal rendering with advanced formatting**:
    ```bash
    > mdcat README.md
    ```
- **GitHub-accurate preview**:
    ```bash
    > grip README.md
    ```
- **Convert to HTML with images**:
    ```bash
    > pandoc README.md -o /tmp/readme.html && open /tmp/readme.html
    ```
- **Generate PDF**:
    ```bash
    > pandoc README.md -o README.pdf && open README.pdf
    ```

## Conclusion

- **For everyday terminal viewing**: Use `glow`
- **For richer terminal rendering**: Use `mdcat`
- **For GitHub-accurate previews**: Use `grip`
- **For document conversion**: Use `pandoc`
- **For image rendering**: Browser-based solutions (`grip` or `pandoc` to HTML)
  remain most reliable on macOS
