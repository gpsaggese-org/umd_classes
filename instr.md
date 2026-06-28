# AST Transform: Divved Columns to Typst Grid

## Purpose
Write a Python script that transforms pandoc AST JSON, converting `Div` elements with `columns` class (multi-column layouts) into raw typst `#grid()` blocks.

## Invocation
```bash
/helpers_root/dev_scripts_helpers/documentation/convert_pandoc_divved_fence.py -i <input.json> -o <output.json>
```

## Input/Output

### Input Format
- Pandoc AST JSON (from `pandoc input.md -t json`)
- Structure: `{"pandoc-api-version": [...], "meta": {...}, "blocks": [...]}`
- Contains `Div` elements with `classes: ["columns"]`

### Output Format
- Modified pandoc AST JSON (same structure as input)
- All `Div` with class `columns` replaced with `RawBlock` containing typst `#grid()`
- All other elements unchanged
- Valid for: `pandoc ast.json -f json -t typst -o out.typ`

## Transformation Rules

### 1. **Detect Columns Container**
AST Pattern to match:
```python
elem["t"] == "Div" and "columns" in elem["c"][0][1]
```

Structure:
- `elem["c"][0]` = `[id, classes, attrs]`
- `elem["c"][0][1]` = classes list
- `elem["c"][1]` = children blocks (array)

### 2. **Extract Column Divs**
For each child in `elem["c"][1]`:
- Match: `child["t"] == "Div"` AND `"column"` in `child["c"][0][1]`
- Extract width: `child["c"][0][2]` (attrs array)
  - Format: `[["width", "55%"], ...]`
  - Parse: get value from matching `["width", value]` tuple
  - Fallback: default to `"1fr"` if missing

### 3. **Recursively Convert Column Content**
For each column `Div`:
- Extract: `child["c"][1]` (content blocks array)
- Process each block recursively:
  - Convert inline elements (Str, Space, Emph, Strong, RawInline, Image, Math, etc.)
  - Convert block elements (Para, BulletList, OrderedList, Table, CodeBlock, RawBlock, etc.)
  - Preserve structure and formatting exactly

### 4. **Generate Typst Grid Code**
Build typst block as string:
```typst
#grid(
  columns: (width1, width2, ...),
  gutter: 0.5em,
  [
    <rendered left column content>
  ],
  [
    <rendered right column content>
  ]
)
```

**Generation rules:**
- Columns tuple: `(55%, 45%)` or `(1fr, 1fr, 1fr)` etc.
- Gutter: always `0.5em`
- Each column wrapped in `[...]` brackets
- Content rendered as valid typst (use pandoc's typst writer logic or implement rendering)

### 5. **Replacement**
Replace original `Div` with:
```python
{
  "t": "RawBlock",
  "c": ["typst", "<grid typst code string>"]
}
```

## Implementation Structure

### Module: `convert_ast_columns.py`

**Functions:**

1. **`load_ast(filepath: str) -> dict`**
   - Read JSON file, parse, return dict

2. **`save_ast(ast: dict, filepath: str) -> None`**
   - Serialize dict to JSON, write to file

3. **`is_columns_container(elem: dict) -> bool`**
   - Return True if elem is Div with `"columns"` class
   - Handle edge cases: wrong type, missing fields

4. **`extract_columns(container: dict) -> list[tuple[str, list]]`**
   - Input: `Div` with class `columns`
   - Output: `[(width1, blocks1), (width2, blocks2), ...]`
   - width: str like `"55%"`, `"45%"`
   - blocks: list of AST block elements

5. **`render_blocks_to_typst(blocks: list) -> str`**
   - Convert list of AST blocks to typst code string
   - Use pandoc internally OR implement rendering:
     - Para → paragraph text
     - BulletList → bullet points
     - Image → `#image(path, ...)`
     - RawBlock(typst, ...) → pass through raw code
     - Etc. (comprehensive coverage)

6. **`format_grid_code(widths: list[str], columns_typst: list[str]) -> str`**
   - Build the `#grid(...)` string
   - Input: widths like `["55%", "45%"]`, column content strings
   - Output: complete typst code block

7. **`transform_div(elem: dict) -> dict`**
   - If columns container: transform to RawBlock
   - Else: return unchanged (but recursively process children)
   - Recursive: process nested Divs

8. **`transform_ast(ast: dict) -> dict`**
   - Top-level entry: walk blocks array
   - For each block, call `transform_div` recursively
   - Handle deep nesting (divs within divs)
   - Return modified AST

### Edge Cases to Handle

1. **Width formats:**
   - `"55%"` → typst `55%` ✓
   - `"1fr"` → typst `1fr` ✓
   - Missing width → default `"1fr"`
   - Non-standard format → error or warning

2. **Column count:**
   - 2 columns (most common)
   - 3+ columns (same logic, extend tuple)
   - 1 column (treat as no-op or wrap in grid with 100%)

3. **Content types:**
   - Empty column → render as empty block `[]`
   - Nested divs inside column → recurse
   - RawBlock(typst, ...) inside column → preserve as-is
   - Math, Image, Code → render correctly

4. **Malformed AST:**
   - Missing `c` key → skip/warn
   - Div without classes → skip
   - Column without width → default to `1fr`

5. **Special characters:**
   - Typst special chars in content → escape if needed
   - Quotes, backslashes, brackets → careful with string building

## Code Organization

## Testing

### Unit Tests
- Test `is_columns_container()` with valid/invalid inputs
- Test `extract_columns()` with various widths
- Test `render_blocks_to_typst()` with each block type
- Test `transform_ast()` with nested structures
- Test edge cases: empty columns, missing attrs, 3+ columns

### Integration Tests
- Load actual AST from `msml610/lectures/tmp.notes_to_pdf.render_image2.txt.ast.json`
- Transform "Taxonomy of Explainability Methods" slide
- Verify output AST is valid JSON
- Verify output can be compiled: `pandoc output.json -f json -t typst -o out.typ`
- Verify output typst compiles: `typst compile out.typ`

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

- When implementing notebooks follow the instructions in
  - `.claude/skills/notebook.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is
