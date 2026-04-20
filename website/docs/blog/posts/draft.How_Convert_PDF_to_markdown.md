---
title: "How to Convert PDF to Markdown in Python"
draft: true
authors:
  - gpsaggese
date: 2026-04-19
description:
categories:
  - Developer Tools
  - Python
---

# Summary
Converting PDFs to Markdown in Python is fundamentally an extraction and
reconstruction problem. PDFs encode layout, not semantics, and each library
differs in how much structure it infers automatically versus how much control it
gives you. This guide covers four essential libraries with installation, usage,
and practical examples.

<!-- more -->

## Why Convert PDFs to Markdown?
- PDFs are layout-focused, not semantic: preserve visual structure, lose meaning
- Markdown is portable: version control friendly, tool independent, human
  readable
- LLMs work better with Markdown: cleaner input, better parsing, easier to
  fine-tune
- Single-source publishing: convert once, render to HTML, PDF, EPUB
- Automation: batch convert documents, integrate with pipelines

## Quick Comparison
| Library       | Speed                                    | Accuracy                                   | Learning Curve                           | Best For                   |
| :------------ | :--------------------------------------- | :----------------------------------------- | :--------------------------------------- | :------------------------- |
| `pymupdf4llm` | <span style="color:green">Fast</span>    | <span style="color:green">Good</span>      | <span style="color:green">Easy</span>    | Simple docs, speed         |
| `marker-pdf`  | <span style="color:yellow">Medium</span> | <span style="color:green">Excellent</span> | <span style="color:yellow">Medium</span> | Academic, structured       |
| `markitdown`  | <span style="color:yellow">Medium</span> | <span style="color:green">Good</span>      | <span style="color:green">Easy</span>    | Multi-format pipelines     |
| `pdfplumber`  | <span style="color:red">Slow</span>      | <span style="color:red">Manual</span>      | <span style="color:red">Hard</span>      | Custom logic, full control |

## Installation
**Quick start without installing:**

- You can use `uvx` to run any of these tools without installation
- Ideal for one-off conversions or testing different libraries
- Trade cold-start time (package download) for zero disk footprint
- See each library's "Using uvx" subsection for examples

### Pymupdf4llm
- Install package:
  ```bash
  > pip install pymupdf4llm
  ```
- Verify installation (via CLI):
  ```bash
  # Run help to verify command is available.
  > pymupdf4llm --help
  ```

### Marker-pdf
- Install package:
  ```bash
  > pip install marker-pdf
  ```
- Verify installation (via CLI):
  ```bash
  # Run help to verify command is available.
  > marker --help
  ```

### Markitdown
- Install package:
  ```bash
  > pip install markitdown
  ```
- Verify installation (via CLI):
  ```bash
  # Run help to verify command is available.
  > markitdown --help
  ```

### Pdfplumber
- Install package:
  ```bash
  > pip install pdfplumber
  ```
- Verify installation (via Python):
  ```bash
  > python -c "import pdfplumber; print(pdfplumber.__version__)"
  0.10.3
  ```
- Note: `pdfplumber` is primarily a library without a CLI
  - Use Python import verification above
  - Always accessed via Python scripts, not command-line directly

## Basic Usage

### Pymupdf4llm: Fast and Simple
- Best for: Speed and simplicity, LLM-friendly output
- Designed for large language models, uses lightweight heuristics

**CLI usage:**

- Convert single PDF:
  ```bash
  # Convert input.pdf to Markdown.
  > pymupdf4llm input.pdf > output.md
  ```

**Using uvx (no installation needed):**

- Run directly with `uvx`:
  ```bash
  # Convert PDF without installing.
  > uvx pymupdf4llm input.pdf > output.md
  ```
- Convenient for one-off conversions, trades cold-start time for zero setup

**Python usage:**

- Convert PDF to Markdown:
  ```python
  from pymupdf4llm import to_markdown

  md = to_markdown("input.pdf")
  with open("output.md", "w") as f:
      f.write(md)
  ```

### Marker-pdf: High-Fidelity Layout Detection
- Best for: Academic papers, structured documents, tables
- Uses machine learning for headings, tables, figures

**CLI usage:**

- Convert with layout detection:
  ```bash
  # Convert input.pdf with layout analysis.
  > marker input.pdf --output output.md
  ```

**Using uvx (no installation needed):**

- Run directly with `uvx`:
  ```bash
  # Convert with ML detection without installing.
  > uvx marker input.pdf --output output.md
  ```

**Python usage:**

- Convert with ML-based detection:
  ```python
  from marker.convert import convert_single_pdf

  result = convert_single_pdf("input.pdf")
  with open("output.md", "w") as f:
      f.write(result.markdown)
  ```

### Markitdown: Multi-Format Support
- Best for: Mixed document types (PDF, DOCX, PPTX)
- Prioritizes consistency across formats

**CLI usage:**

- Convert multiple formats:
  ```bash
  # Convert PDF to Markdown.
  > markitdown input.pdf -o output.md
  # Convert DOCX to Markdown.
  > markitdown input.docx -o output.md
  # Convert PPTX to Markdown.
  > markitdown input.pptx -o output.md
  ```

**Using uvx (no installation needed):**

- Run directly with `uvx`:
  ```bash
  # Convert without installing.
  > uvx markitdown input.pdf -o output.md
  ```
- Works for all supported formats via single `uvx` call

**Python usage:**

- Convert with format detection:
  ```python
  from markitdown import MarkItDown

  md = MarkItDown()
  result = md.convert("input.pdf")
  with open("output.md", "w") as f:
      f.write(result.text_content)
  ```

### Pdfplumber: Full Control
- Best for: Custom extraction, precise control over layout
- Low-level tool: you build the Markdown conversion

**Python usage:**

- Manual extraction with layout control:
  ```python
  import pdfplumber

  markdown_lines = []

  with pdfplumber.open("input.pdf") as pdf:
      for page in pdf.pages:
          # Extract text with layout preservation.
          text = page.extract_text()
          if text:
              markdown_lines.append(text)

  with open("output.md", "w") as f:
      f.write("\n\n".join(markdown_lines))
  ```

- Extract tables:
  ```python
  import pdfplumber

  with pdfplumber.open("input.pdf") as pdf:
      for page in pdf.pages:
          # Find and extract tables.
          tables = page.extract_tables()
          for table in tables:
              print(table)
  ```

## Advanced Features

### Custom Extraction with Pdfplumber
- Extract specific page ranges:
  ```python
  import pdfplumber

  with pdfplumber.open("input.pdf") as pdf:
      # Extract pages 1-5.
      for page in pdf.pages[0:5]:
          text = page.extract_text()
          print(text)
  ```

- Crop and extract regions:
  ```python
  import pdfplumber

  with pdfplumber.open("input.pdf") as pdf:
      page = pdf.pages[0]
      # Crop to top-left quadrant.
      cropped = page.crop((0, 0, page.width/2, page.height/2))
      text = cropped.extract_text()
  ```

### Batch Processing
- Convert multiple PDFs:
  ```python
  from pathlib import Path
  from pymupdf4llm import to_markdown

  pdf_dir = Path("pdfs")
  output_dir = Path("markdown")
  output_dir.mkdir(exist_ok=True)

  for pdf_file in pdf_dir.glob("*.pdf"):
      md = to_markdown(str(pdf_file))
      output_file = output_dir / f"{pdf_file.stem}.md"
      output_file.write_text(md)
      print(f"Converted {pdf_file.name}")
  ```

### Integration with LLM Processing
- Convert and send to LLM:
  ```python
  from pymupdf4llm import to_markdown

  md = to_markdown("document.pdf")
  
  # Process with language model.
  from anthropic import Anthropic

  client = Anthropic()
  response = client.messages.create(
      model="claude-3-5-sonnet-20241022",
      max_tokens=1024,
      messages=[
          {"role": "user", "content": f"Summarize:\n{md}"}
      ],
  )
  print(response.content[0].text)
  ```

## Specialized Tool: Pdf_to_md.py Script
The `pdf_to_md.py` script in `helpers_root/dev_scripts_helpers/documentation/`
provides a production-ready solution for converting PDFs to Markdown with proper
image extraction and heading detection.

**Features:**

- Extracts text from PDFs and converts to Markdown with proper heading levels
- Automatically detects and extracts images, saves to `images/` subdirectory
- Analyzes font sizes to distinguish `h1`, `h2`, `h3` headings from body text
- Detects vector graphics and renders them as images
- Preserves image positioning based on PDF layout
- Applies prettier formatting for clean Markdown output
- Supports verbose logging for debugging conversions
- Automatically manages image duplicates via xref tracking
- Uses `uv` for dependency management (no installation needed)

**Installation:**

- Script is self-contained with `uv`:
  ```bash
  # Runs with uv, installs dependencies automatically.
  > ./helpers_root/dev_scripts_helpers/documentation/pdf_to_md.py \
    --input document.pdf \
    --output output_dir
  ```
- Or call via `uv run`:
  ```bash
  # Use uv to run the script.
  > uv run ./helpers_root/dev_scripts_helpers/documentation/pdf_to_md.py \
    --input document.pdf \
    --output output_dir
  ```

**Usage:**

- Basic conversion:
  ```bash
  # Convert PDF to Markdown with images.
  > ./helpers_root/dev_scripts_helpers/documentation/pdf_to_md.py \
    --input input.pdf \
    --output output_dir
  ```
- With verbose logging to debug conversion:
  ```bash
  # See detailed processing information.
  > ./helpers_root/dev_scripts_helpers/documentation/pdf_to_md.py \
    --input input.pdf \
    --output output_dir \
    -v DEBUG
  ```

**Output Structure:**

- Creates output directory with:
  - `output_dir/input.md`: Converted Markdown file
  - `output_dir/images/`: Directory containing all extracted images
    - Page images: `page_1_img_1.png`, `page_1_img_2.jpg`, etc.
    - Rendered pages: `page_1_rendered_1.png` (for vector graphics)

**Example Output:**

- Input PDF: `research.pdf`
- Output structure:
  ```text
  output_dir/
  ├── research.md
  └── images/
      ├── page_1_img_1.png
      ├── page_2_img_1.jpg
      └── page_3_rendered_1.png
  ```

**When to Use pdf_to_md.py:**

- PDFs with mixed text, tables, and images
- Academic papers or technical documents with vector graphics
- Need automatic heading detection based on font sizes
- Require image preservation and proper positioning
- Want a single, tested script rather than building custom logic
- Need verbose debugging information during conversion

**Comparison with Other Tools:**

| Aspect             | pdf_to_md.py           | pymupdf4llm | marker-pdf |
| :----------------- | :--------------------- | :---------- | :--------- |
| Image extraction   | Yes, with positioning  | No          | Limited    |
| Heading detection  | Font-size based        | Heuristics  | ML-based   |
| Image organization | Separate `images/` dir | Embedded    | Embedded   |
| Vector graphics    | Renders to image       | No          | No         |
| Debugging output   | Verbose logging        | No          | Limited    |
| Use case           | Production docs        | LLM input   | Academic   |


## Common Gotchas
**Scanned PDFs (images, not text)**

- Problem: `pymupdf4llm` and others extract nothing from scanned PDFs
- Solution: Use OCR library first
  ```bash
  # Install Tesseract OCR.
  > pip install pytesseract pillow pdf2image
  ```
- Convert scanned PDF to text-based PDF
## When to Use Each Library
- **Use `pymupdf4llm`** for:
  - Speed is priority
  - Feeding PDFs to LLMs
  - Simple documents without complex layouts
  - Batch processing large numbers of PDFs

- **Use `marker-pdf`** for:
  - Academic papers and research documents
  - High-fidelity structure preservation
  - Complex layouts with tables and figures
  - When accuracy is critical

- **Use `markitdown`** for:
  - Mixed document formats (PDF, DOCX, PPTX)
  - Need consistency across formats
  - General-purpose document conversion

- **Use `pdfplumber`** for:
  - Custom extraction logic
  - Full programmatic control
  - Complex pipelines
  - When you need to build your own Markdown conversion


<!--

  	•	Nougat (best for arXiv papers)
      - https://github.com/facebookresearch/nougat
	•	GROBID (best for structured extraction)

  marker has a REPL interface
  cat >config.yml
  inputs:
  - /Users/saggese/Downloads/2011.00641v1.pdf

  output: output
  rm -rf output; printf "run\nexit\n"  | uvx --python 3.11 marker --config config.yml

https://github.com/timf34/arxiv2md

https://github.com/docling-project/docling

https://github.com/tonydavis629/markxiv

uvx markitdown[pdf] ~/Downloads/2011.00641v1.pdf -o output.md
Decent job

pandoc /Users/saggese/papers/2016_Ribeiro_et_al_Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.pdf -t gfm --wrap=none --markdown-headings=atx -o paper_md.md

Convert a latex to markdown using pandoc
-->
