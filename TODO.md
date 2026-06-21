# Convert slides into book

- [x] Create a map from book.from_corr_to_decision/book_map.md

class_scripts/create_book_toc_from_slides.py --max_number 2 --max_level 2

- [ ] Add comments to README

## The old flow
`./class_scripts/gen_book_chapter.py`
`./class_scripts/generate_book_chapter.py`

The output looks like 
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/data605/book/Lesson01.1-Intro.book_chapter.pdf

## The new flow 

- The style is like:
  vi msml610/book/aima_style.typ

- TODO(gp): Improve the figure handling

Generate the text from the slides
```
claude> msml610/book/prompt.slides_to_text.txt
```

- TODO(gp): Improve the prompt

```
> render_images.py -i msml610/book/Lesson06.2-Using_Bayesian_Networks.typ
> typst compile --root . msml610/book/aima_style_example.typ && open msml610/book/aima_style_example.pdf
> typst compile --root . msml610/book/Lesson06.2-Using_Bayesian_Networks.typ && open msml610/book/Lesson06.2-Using_Bayesian_Networks.pdf
```
# Port documentation flow to typst

## Step 0:

- [x] Implement TODOs
- [x] Add pictures of screen with ./dev_scripts_helpers/system_tools/capture_iterm_command.py --command "(cd ~/src/umd_classes2/helpers_root; clear; glow TODO.convert_slides_into_book.md)" --output_file screenshot1.png
- [x] Refresh the README.blog.md
- [x] Convert to Python dev_scripts_helpers/documentation/open_md.sh
- [ ] Test dev_scripts_helpers/documentation/open_md.sh
- [ ] Finish website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md

## Step 1: Document current system
helpers_root/dev_scripts_helpers/documentation/README.md
helpers_root/dev_scripts_helpers/documentation/README.notes_to_pdf.md

website/docs/blog/posts/draft.in_30_mins.helpers_typesetting_system.md
-> create blog

## Step 2: Document typst and slides

website/README.blog.md

website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md
- Create blog

website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.all_examples.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.hello_world.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.all_examples.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.hello_world.typ
website/docs/blog/posts/draft.how_to.latex_vs_typst_for_typsetting.md

## Step 3: Extend the flow and document it
dev_scripts_helpers/documentation/notes_to_pdf.py

notes_to_pdf.py --input=data605/lectures_source/Lesson01.1-Intro.txt --output=data605/lectures/Lesson01.1-Intro.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst

Cause: my typst path used container_type = "pandoc_only", which points at the bare pandoc/core:3.7 image. That image isn't built/pulled locally (only pandoc_texlive and pandoc_latex get auto-built), so the assert fails.

## Step 4: Reorg dev_scripts_helpers/documentation
- Too many files

# Mix

## Fix output of lint_cc.py

Right now the output has all the verbose output from the model

```
> linters2/lint_cc.py --files class_scripts/README.md --rule='/Users/saggese/src/umd_classes2/.claude/skills/markdown.rules.md:153:## Command Formatting'
```

- [ ] Write a blog from TODO.parsing_claude_code_logs.md

- [ ] Finish the script to process

- --verbose — Shows verbose output
claude -p "your prompt" --verbose
- -d / --debug — Enables debug logging (optionally filtered)
claude -p "your prompt" -d
claude -p "your prompt" -d api,hooks  # Filter to specific categories
- --output-format stream-json with --include-partial-messages — Shows real-time streaming responses
claude -p "your prompt" --output-format stream-json --include-partial-messages

So if you want the normal printed output but with debug info attached:
claude -p "your prompt" --debug

## Add support for nitro models and reasoning in llm_cli and in cc

```
{
  "model": "openai/o3",
  "provider": {
    "sort": "throughput"
  }
}
openai/o3:nitro
```

```
    reasoning={
       "effort": "high"    }
```

## Improve llm_compare.py
llm_compare.py --models "openrouter/openai/gpt-4o-mini,openrouter/openai/gpt-oss-120b" --benchmark summarization1 --output_dir results/

run_eval.sh

Get info about models
dev_scripts_helpers/llms/openrouter_models_table.py --models dev_scripts_helpers/llms/test_models.txt

helpers_root/dev_scripts_helpers/llms/openrouter_models_table.py --models_from_file helpers_root/dev_scripts_helpers/llms/text_models.txt

## Test lint_txt.py with new backends

lint_txt.py -i dev_scripts_helpers/ai/README.md --backend mdformat --mode uvx

Better / faster markdown formatting
- test_hmarkdown_formatting.py
- pytest helpers/test/test_hmarkdown_formatting.py
- pytest helpers/test/test_hmarkdown_formatting.py::Test_format_md_comparison_and_performance

## Improve cost and speed accounting for hllm

## Managing gsheet links

vi dev_scripts_helpers/scraping/README.link_flow.md

download_link_articles.py --url https://docs.google.com/spreadsheets/d/1i6Z7v2TzPdftR9BQ5Ia6jrrNWvVy-pUCxZAt4A59l8M/edit?gid=2008094999#gid=2008094999 --row_idx 2

llm_cli.py -p "Summarize the following text in 5 bullet points and less than 200 words" --input We_should_be_more_tired_than_the_model.hn_comments.txt --model openrouter/anthropic/claude-haiku-4.5 --lint

## Fix annoying claude code scrolling

tmux focus-events off · add 'set -g focus-events on' to ~/.tmux.conf and reattach for focus tracking
tmux detected · scroll with PgUp/PgDn · or add 'set -g mouse on' to ~/.tmux.conf for wheel scroll

