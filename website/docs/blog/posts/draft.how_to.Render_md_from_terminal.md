Markdown Viewers on macOS: Terminal and Browser Options

Markdown has become the standard format for documentation, notes, READMEs, and technical writing. macOS users have several options for viewing Markdown from the command line, ranging from simple terminal renderers to full-featured browser previews with image support.

Quick Recommendation

Choose the tool that matches your needs:

Goal	Recommended Tool
Beautiful terminal reading	glow
Rich terminal rendering	mdcat
GitHub-style preview with images	grip
Maximum flexibility and conversions	pandoc
Lightweight pager	mdless

⸻

Glow

Glow is one of the most popular terminal Markdown viewers. It renders Markdown with attractive formatting directly in the terminal.

Installation

brew install glow

Usage

glow README.md

Pros

* Beautiful terminal interface
* Fast and lightweight
* Multiple themes
* Excellent for reading documentation

Cons

* Does not display images inline
* Primarily focused on terminal viewing

⸻

mdcat

mdcat is a rich Markdown renderer written in Rust. It supports advanced formatting and can leverage terminal capabilities.

Installation

brew install mdcat

Usage

mdcat README.md

Pros

* Excellent formatting
* Handles tables well
* Supports hyperlinks
* Can display inline images in some terminals

Cons

* Image support depends on terminal capabilities
* More complex than Glow

Best With

* Kitty
* WezTerm
* Other terminals supporting modern image protocols

⸻

Grip

Grip renders Markdown exactly as GitHub would and serves it locally through a web browser.

Installation

pip install grip

Usage

grip README.md

Then open:

http://localhost:6419

Pros

* GitHub-flavored Markdown
* Full image support
* Excellent table rendering
* Matches GitHub appearance

Cons

* Requires a browser
* Runs a local web server

⸻

Pandoc

Pandoc is the Swiss Army knife of document conversion.

Installation

brew install pandoc

Convert to HTML

pandoc README.md -o /tmp/readme.html
open /tmp/readme.html

Convert to PDF

pandoc README.md -o README.pdf
open README.pdf

Pros

* Full image support
* Multiple output formats
* Highly customizable
* Industry-standard converter

Cons

* More complex than dedicated viewers
* Primarily a converter rather than a viewer

⸻

mdless

mdless provides a pager-like interface for reading Markdown.

Installation

brew install mdless

Usage

mdless README.md

Pros

* Simple and lightweight
* Familiar pager interface
* Good for large documents

Cons

* Limited styling
* No image rendering

⸻

rich-cli

Built on Python’s Rich library, rich-cli provides colorful terminal rendering.

Installation

pip install rich-cli

Usage

rich README.md

Pros

* Attractive formatting
* Easy installation
* Good Unicode support

Cons

* No image rendering
* Less feature-rich than mdcat

⸻

Comparison

Tool	Terminal	Images	GitHub Style	Browser
Glow	Yes	No	No	No
mdcat	Yes	Limited	No	No
mdless	Yes	No	No	No
rich-cli	Yes	No	No	No
Grip	No	Yes	Yes	Yes
Pandoc	Optional	Yes	Depends	Yes

⸻

Recommended Workflows

Reading Documentation in the Terminal

glow README.md

Rich Terminal Rendering

mdcat README.md

GitHub-Style Preview

grip README.md

Full HTML Rendering with Images

pandoc README.md -o /tmp/readme.html && open /tmp/readme.html

Generate a PDF

pandoc README.md -o README.pdf && open README.pdf

Conclusion

For most users:

* Use Glow for everyday terminal viewing.
* Use mdcat when you want richer terminal rendering.
* Use Grip for GitHub-accurate previews.
* Use Pandoc when images and document conversion are important.

If image rendering is required, browser-based solutions such as Grip or Pandoc-generated HTML remain the most reliable options on macOS.


---
Scripts in this repo

open_md_on_github.sh
open_md.sh
