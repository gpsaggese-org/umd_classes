---
title: "Markdown Viewers on macOS: Terminal and Browser Options"
authors:
    - gpsaggese
date: 2026-06-22
categories:
    - "Developer Tools"
draft: false
---

TL;DR: Render markdown from terminal using `glow` (for terminal viewing),
`mdcat` (for rich formatting), `grip` (for GitHub-accurate previews with
images), or `pandoc` (for document conversion and flexibility).

<!-- more -->

## Overview

[Markdown](https://www.markdownguide.org/) is the standard format for
documentation, notes, READMEs, and technical writing. macOS users have several
options for viewing it from the command line, ranging from simple terminal
renderers to full-featured browser previews with image support. The right tool
depends on your workflow:

- **Terminal-only with attractive formatting**: `glow` or `mdcat`
- **GitHub-accurate previews with images**: `grip`
- **Document conversion to PDF/HTML**: `pandoc`

## Glow

- **What it is**: One of the most popular terminal Markdown viewers with
  attractive formatting
- **GitHub**: [charmbracelet/glow](https://github.com/charmbracelet/glow)
- **Latest Release**: v1.5.1 (January 2025)
- **Installation**:
    ```bash
    > brew install glow
    ```
- **Usage**:
    ```bash
    > glow README.md
    ```
    See [glow documentation](https://github.com/charmbracelet/glow#readme) for
    advanced options and paging modes.

<!-- capture_iterm_command.py --command "glow -p $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/test_markdown.md" --output_file $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/fig1.glow_demo.png -->

![Glow terminal output displaying formatted markdown](./draft.how_to.Render_md_from_terminal.md.figs/fig1.glow_demo.png)

- **Advantages**:
    - Fancy terminal interface with multiple themes
    - Fast and lightweight
    - Great for reading documentation
    - No dependencies beyond the binary
- **Disadvantages**:
    - Does not display images inline
    - Terminal-only
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

    ```
    > glow -l --tui website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md
    ```

**TUI vs Pager modes**:

- **TUI** (Terminal User Interface): Interactive full-screen mode with keyboard
  navigation. Glow enters full-screen, lets you scroll, search, and navigate
  with arrow keys and hotkeys. Best for exploring long documents.
- **Pager**: Pipes output through a pager like `less`, streaming content
  progressively. Familiar if you're used to `less`, `more`, or `man` pages.

## mdcat

- **What it is**: Rich Markdown renderer written in Rust with advanced
  formatting support
- **GitHub**: [swsnr/mdcat](https://github.com/swsnr/mdcat)
- **Latest Release**: v0.32.1 (October 2024)
- **Installation**:
    ```bash
    > brew install mdcat
    ```
- **Usage**:
    ```bash
    > mdcat README.md
    ```
    For image rendering, see
    [mdcat terminal support](https://github.com/swsnr/mdcat#terminal-support).

<!--
> capture_iterm_command.py --command "mdcat -p $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/test_markdown.md" --output_file $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/fig2.mdcat_demo.png
-->

![mdcat terminal rendering with rich formatting and syntax highlighting](./draft.how_to.Render_md_from_terminal.md.figs/fig2.mdcat_demo.png)

- **Advantages**:
    - Good formatting quality
    - Handles tables and syntax highlighting well
    - Supports hyperlinks
    - Can display inline images in compatible terminals
- **Disadvantages**:
    - Image support depends on terminal capabilities
    - More complex than Glow
- **Works best with**: Terminal emulators that support image protocols:
    - [Kitty](https://sw.kovidgoyal.net/kitty/) (native image protocol support)
    - [WezTerm](https://wezfurlong.org/wezterm/) (sixel and image support)
    - [iTerm2](https://iterm2.com/) (inline image support)
- **Best for**: Terminal users who want rich formatting and image support

## Grip

- **What it is**: Renders Markdown exactly as GitHub would, served locally
  through a web browser
- **GitHub**: [joeyespo/grip](https://github.com/joeyespo/grip)
- **Latest Release**: v4.6.1 (January 2024)
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
    See [grip's feature list](https://github.com/joeyespo/grip#features) for
    rendering customization.

<!--
> uvx grip -b --quiet $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/test_markdown.md
> ./helpers_root/dev_scripts_helpers/system_tools/capture_browser_screenshot.py --url "http://localhost:6419" --output /Users/saggese/src/umd_classes2/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/fig3.grip_browser.png
-->

![Grip browser view showing GitHub-flavored markdown rendering](./draft.how_to.Render_md_from_terminal.md.figs/fig3.grip_browser.png)

- **Advantages**:
    - GitHub-flavored Markdown rendering
    - Full image support
    - Good table rendering
    - Matches GitHub appearance exactly
- **Disadvantages**:
    - Requires a web browser
    - Runs a local web server
- **Best for**: Previewing work before pushing to GitHub

## mdless

- **What it is**: Pager-like interface for reading Markdown with familiar
  navigation
- **GitHub**: [ttscoff/mdless](https://github.com/ttscoff/mdless)
- **Latest Release**: v2.1.17 (March 2025)
- **Installation**:
    ```bash
    > brew install mdless
    ```
- **Usage**:
    ```bash
    > mdless README.md
    ```

<!-- ![mdless pager interface with markdown navigation](./draft.how_to.Render_md_from_terminal.md.figs/fig5.mdless_pager.png) -->

- **Advantages**:
    - Simple and lightweight
    - Familiar pager interface (`less`-like)
    - Good for large documents
- **Disadvantages**:
    - Limited styling compared to other tools
    - No image rendering
- **Best for**: Reading long documents with familiar pager shortcuts

## rich-cli

- **What it is**: Colorful terminal rendering built on Python's Rich library
- **GitHub**: [Textualize/rich-cli](https://github.com/Textualize/rich-cli)
- **Latest Release**: v1.8.1 (December 2024)
- **Installation**:
    ```bash
    > pip install rich-cli
    ```
- **Usage**:
    ```bash
    > rich README.md
    ```

```
> uvx --from rich-cli rich website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md --pager
```

<!--
> capture_iterm_command.py --command "uvx --from rich-cli rich $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md --pager" --output_file $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/fig6.richcli_demo.png
-->

![rich-cli colorful terminal output with rich formatting](./draft.how_to.Render_md_from_terminal.md.figs/fig6.richcli_demo.png)

- **Advantages**:
    - Colorful terminal output
    - Easy installation via pip
    - Good Unicode support
- **Disadvantages**:
    - No image rendering
    - Fewer features than mdcat
- **Best for**: Quick terminal previews with minimal setup

## Pandoc

- **What it is**: The Swiss Army knife of document conversion with multiple
  output formats
- **GitHub**: [jgm/pandoc](https://github.com/jgm/pandoc)
- **Latest Release**: v3.1.12.2 (April 2025)
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
    For advanced options and output formats, see
    [pandoc's user guide](https://pandoc.org/MANUAL.html).

<!--
> pandoc $GIT_ROOT/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/test_markdown.md -o /tmp/readme.html; open /tmp/readme.html
> ./helpers_root/dev_scripts_helpers/system_tools/capture_browser_screenshot.py --url "file:///private/tmp/readme.html" --output /Users/saggese/src/umd_classes2/website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md.figs/fig4.pandoc_html_output.png
-->

![Pandoc converting markdown to HTML and displaying in browser](./draft.how_to.Render_md_from_terminal.md.figs/fig4.pandoc_html_output.png)

- **Advantages**:
    - Full image support
    - Multiple output formats (HTML, PDF, DOCX, etc.)
    - Highly customizable with templates
    - Industry-standard converter
- **Disadvantages**:
    - More complex than dedicated viewers
    - Converts rather than previews in real-time
- **Best for**: Document conversion and flexibility

## Comparison Table

| Tool     | Terminal | Images  | GitHub Style | Browser |
| :------- | :------- | :------ | :----------- | :------ |
| Glow     | Yes      | No      | No           | No      |
| mdcat    | Yes      | Limited | No           | No      |
| mdless   | Yes      | No      | No           | No      |
| rich-cli | Yes      | No      | No           | No      |
| Grip     | No       | Yes     | Yes          | Yes     |
| Pandoc   | Optional | Yes     | Varies       | Yes     |

- **Everyday terminal viewing**: `glow`
- **Richer terminal rendering**: `mdcat`
- **GitHub-accurate previews**: `grip`
- **Document conversion**: `pandoc`
- **Image rendering**: Browser-based solutions (`grip` or `pandoc` to HTML) work
  best on macOS

## Beyond Individual Tools

I've built a tool called `open_md.py` that combines the strengths of all these
approaches. It supports multiple rendering backends (pandoc, grip), integrates
with Docker, and automatically preprocesses embedded diagrams. See the
[`helpers_open_md` blog post](in_10_mins.helpers_open_md.md)
works, or check out the
[`open_md.py` source code](https://github.com/causify-ai/helpers/blob/master/helpers_root/dev_scripts_helpers/documentation/open_md.py)
directly.
