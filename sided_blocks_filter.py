#!/usr/bin/env python3
"""Pandoc filter to convert columns/column divs to Typst grid layout."""

import json
import sys
import re


def extract_width(kvpairs: list) -> str:
    """Extract width attribute from key-value pairs, return as Typst fraction."""
    for key, value in kvpairs:
        if key == "width":
            # Convert percentage (e.g., "55%") to Typst fraction
            match = re.match(r"(\d+)%", value)
            if match:
                percent = int(match.group(1))
                # Convert to relative fraction
                return f"{percent}fr"
    return "1fr"


def element_to_typst(elements: list) -> str:
    """Recursively convert Pandoc elements to Typst."""
    result = []

    for elem in elements:
        if isinstance(elem, dict):
            t = elem.get("t", "")
            c = elem.get("c", [])

            if t == "Header":
                level, _, content = c
                markup = "=" * (level + 1)
                text = content_to_text(content)
                result.append(f"{markup} {text}")

            elif t == "Para":
                text = content_to_text(c)
                result.append(text)

            elif t == "BulletList":
                for item in c:
                    text = content_to_text(item[0]["c"])
                    result.append(f"- {text}")

        result.append("")

    return "\n".join(result).strip()


def content_to_text(content: list) -> str:
    """Convert inline content to plain text."""
    text = []
    for item in content:
        if isinstance(item, dict):
            if item.get("t") == "Str":
                text.append(item["c"])
            elif item.get("t") == "Space":
                text.append(" ")
            elif item.get("t") == "SoftBreak" or item.get("t") == "LineBreak":
                text.append(" ")
        elif isinstance(item, str):
            text.append(item)
    return "".join(text)


def process_blocks(blocks: list) -> list:
    """Process blocks to convert columns divs to Typst grid."""
    processed = []
    i = 0

    while i < len(blocks):
        block = blocks[i]

        if isinstance(block, dict) and block.get("t") == "Div":
            attrs, content = block["c"]
            classes = attrs[1]

            # Check if this is a columns container
            if "columns" in classes:
                # Extract column children
                columns = []
                for col_block in content:
                    if isinstance(col_block, dict) and col_block.get("t") == "Div":
                        col_attrs, col_content = col_block["c"]
                        col_classes = col_attrs[1]
                        col_kvpairs = col_attrs[2]

                        if "column" in col_classes:
                            width = extract_width(col_kvpairs)
                            typst_content = element_to_typst(col_content)
                            columns.append((width, typst_content))

                # Generate Typst grid
                if columns:
                    col_widths = ", ".join(w for w, _ in columns)
                    col_rects = []

                    colors = ["#f0f0f0", "#e0e0e0", "#d0d0d0"]
                    for j, (_, col_content) in enumerate(columns):
                        color = colors[j % len(colors)]
                        rect_code = f'  rect(fill: rgb("{color}"), inset: 1em)[\n{col_content}\n  ]'
                        col_rects.append(rect_code)

                    grid_code = f"""#grid(
  columns: ({col_widths}),
  gutter: 1em,
{",".join(col_rects)},
)"""

                    processed.append({
                        "t": "RawBlock",
                        "c": ["typst", grid_code]
                    })
                    i += 1
                    continue

        processed.append(block)
        i += 1

    return processed


def main():
    """Process Pandoc JSON AST."""
    data = json.load(sys.stdin)
    blocks = data.get("blocks", [])
    data["blocks"] = process_blocks(blocks)
    json.dump(data, sys.stdout)


if __name__ == "__main__":
    main()
