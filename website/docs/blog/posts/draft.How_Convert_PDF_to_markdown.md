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
| Library       | Speed  | Accuracy  | Best For                   | Learning Curve |
| :------------ | :----- | :-------- | :------------------------- | :------------- |
| `pymupdf4llm` | Fast   | Good      | Simple docs, speed         | Easy           |
| `marker-pdf`  | Medium | Excellent | Academic, structured       | Medium         |
| `markitdown`  | Medium | Good      | Multi-format pipelines     | Easy           |
| `pdfplumber`  | Slow   | Manual    | Custom logic, full control | Hard           |

## Installation

### Pymupdf4llm
- Install package:
  ```bash
  > pip install pymupdf4llm
  ```
- Verify installation:
  ```bash
  > python -c "import pymupdf4llm; print(pymupdf4llm.__version__)"
  0.4.16
  ```

### Marker-pdf
- Install package:
  ```bash
  > pip install marker-pdf
  ```
- Verify installation:
  ```bash
  > python -c "import marker; print(marker.__version__)"
  0.2.5
  ```

### Markitdown
- Install package:
  ```bash
  > pip install markitdown
  ```
- Verify installation:
  ```bash
  > python -c "from markitdown import MarkItDown; print('markitdown installed')"
  markitdown installed
  ```

### Pdfplumber
- Install package:
  ```bash
  > pip install pdfplumber
  ```
- Verify installation:
  ```bash
  > python -c "import pdfplumber; print(pdfplumber.__version__)"
  0.10.3
  ```

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

## Practical Examples

### Convert Academic Paper to Summary
- Extract key sections from PDF:
  ```python
  from pymupdf4llm import to_markdown
  from anthropic import Anthropic

  # Convert PDF to Markdown.
  md = to_markdown("research_paper.pdf")

  # Extract abstract and conclusions.
  client = Anthropic()
  response = client.messages.create(
      model="claude-3-5-sonnet-20241022",
      max_tokens=2048,
      messages=[
          {
              "role": "user",
              "content": f"Extract abstract and key findings:\n{md}"
          }
      ],
  )
  print(response.content[0].text)
  ```

### Batch Convert with Progress Tracking
- Convert directory of PDFs:
  ```python
  from pathlib import Path
  from pymupdf4llm import to_markdown
  from tqdm import tqdm

  pdf_dir = Path("documents")
  output_dir = Path("converted")
  output_dir.mkdir(exist_ok=True)

  pdfs = list(pdf_dir.glob("*.pdf"))
  for pdf_file in tqdm(pdfs, desc="Converting PDFs"):
      try:
          md = to_markdown(str(pdf_file))
          output_file = output_dir / f"{pdf_file.stem}.md"
          output_file.write_text(md)
      except Exception as e:
          print(f"Error converting {pdf_file.name}: {e}")
  ```

### Extract Tables and Convert to CSV
- Convert tables from PDF:
  ```python
  import pdfplumber
  import csv

  with pdfplumber.open("data.pdf") as pdf:
      for page_num, page in enumerate(pdf.pages):
          tables = page.extract_tables()
          for table_num, table in enumerate(tables):
              # Write table to CSV.
              output_file = f"table_p{page_num}_t{table_num}.csv"
              with open(output_file, "w", newline="") as f:
                  writer = csv.writer(f)
                  writer.writerows(table)
  ```

## Common Gotchas
**Scanned PDFs (images, not text)**

- Problem: `pymupdf4llm` and others extract nothing from scanned PDFs
- Solution: Use OCR library first
  ```bash
  # Install Tesseract OCR.
  > pip install pytesseract pillow pdf2image
  ```
- Convert scanned PDF to text-based PDF:
  ```python
  from pdf2image import convert_from_path
  import pytesseract
  from PIL import Image

  images = convert_from_path("scanned.pdf")
  text_lines = []
  for image in images:
      text = pytesseract.image_to_string(image)
      text_lines.append(text)
  
  with open("extracted.txt", "w") as f:
      f.write("\n\n".join(text_lines))
  ```

**Encoding and Special Characters**

- Problem: Non-ASCII characters may be corrupted
- Solution: Write with UTF-8 encoding
  ```python
  with open("output.md", "w", encoding="utf-8") as f:
      f.write(md)
  ```

**Large PDFs**

- Problem: Memory usage grows with PDF size
- Solution: Process page-by-page with pdfplumber
  ```python
  import pdfplumber

  with pdfplumber.open("large.pdf") as pdf:
      for page in pdf.pages:
          text = page.extract_text()
          # Process immediately, don't accumulate.
  ```

**Formatting Loss**

- Problem: Markdown output loses complex formatting
- Solution: Preserve structure with Markdown formatting
  ```python
  from pymupdf4llm import to_markdown

  md = to_markdown("input.pdf")
  # Add manual formatting as needed.
  md = md.replace("SECTION", "## SECTION")
  ```

## Tips and Tricks
**Get Table Extraction from PDFs**

- Use pdfplumber for precise table extraction:
  ```python
  import pdfplumber
  import pandas as pd

  with pdfplumber.open("data.pdf") as pdf:
      tables = pdf.pages[0].extract_tables()
      # Convert to DataFrame.
      df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
      print(df)
  ```

**Preserve Headings and Hierarchy**

- Marker-pdf automatically detects headings:
  ```bash
  # Output includes proper Markdown headers.
  > marker input.pdf --output output.md
  ```

**Test with Small PDF First**

- Always test conversion with sample PDF:
  ```bash
  > pymupdf4llm sample.pdf > test_output.md
  ```

**Combine Multiple Libraries**

- Use fastest library first, then refine with marker-pdf:
  ```python
  from pymupdf4llm import to_markdown
  from marker.convert import convert_single_pdf

  # Quick extraction.
  md_quick = to_markdown("input.pdf")

  # High-quality extraction for specific pages.
  result = convert_single_pdf("input.pdf", max_pages=10)
  md_quality = result.markdown
  ```

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
