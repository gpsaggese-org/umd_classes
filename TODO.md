# Work on slides

book.Causal_Probabilistic_ML/book_map.md

# Convert slides into book

- [x] Create a map from book.from_corr_to_decision/book_map.md

class_scripts/create_book_toc_from_slides.py --max_number 2 --max_level 2

- [x] Add comments to README

## The old flow
The output looks like 
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/data605/book/Lesson01.1-Intro.book_chapter.pdf

## The new flow 

- The style is like:
  > vi helpers_root/dev_scripts_helpers/typst/aima_style.typ
  ```
  > typst compile --root . helpers_root/dev_scripts_helpers/typst/aima_style_example.typ && open helpers_root/dev_scripts_helpers/typst/aima_style_example.pdf
  ```

- TODO(gp): Improve the figure handling

- Generate the text from the slides
  ```
  export FILE=Lesson08.1-Causal_AI_intro
  claude> /model sonnet
  claude> Execute /Users/saggese/src/notes1/book_proposals/prompt.slides_to_text.txt on msml610/lectures_source/${FILE}.txt
  ```

- Render with
  ```
  > ./msml610/book/render_chapter.sh msml610/book/$FILE
  ```
  which is equivalent to:
  ```
  > render_images.py -i msml610/book/$FILE.typ
  > typst compile --root . msml610/book/$FILE.typ
  > open msml610/book/$FILE.pdf
  ```

- TODO(gp): Improve the prompt

- TODO(gp): create some scripts similar `./class_scripts/gen_book_chapter.py` and
  `./class_scripts/generate_book_chapter.py` to run the prompt

# HelperTask1276: Port slides flow to typst
https://github.com/causify-ai/helpers/issues/1276

- [x] Implement TODOs
- [x] Add pictures of screen with ./dev_scripts_helpers/system_tools/capture_iterm_command.py --command "(cd ~/src/umd_classes2/helpers_root; clear; glow TODO.convert_slides_into_book.md)" --output_file screenshot1.png
- [x] Refresh the README.blog.md
- [x] Convert to Python dev_scripts_helpers/documentation/open_md.sh
- [x] Test dev_scripts_helpers/documentation/open_md.sh
- [x] Finish website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md

## Get typst slides as close as possible to latex ones

```
> notes_to_pdf.py --input=msml610/lectures_source/Lesson13.1-Explainability.txt --output=msml610/lectures/Lesson13.1-Explainability.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst --no_fail_on_warnings
> vi msml610/lectures/tmp.notes_to_pdf.render_image2.txt msml610/lectures/tmp.notes_to_pdf.render_image2.typ
```

### Create branch for 1276
https://github.com/causify-ai/helpers/issues/1276

### IN PROGRESS: [ ] Improve unit testing

```
> pytest dev_scripts_helpers/documentation/test/
```

- [ ] Do test runs and which is disabled?
- [ ] What is the coverage?
- [ ] What is not tested?

- [ ] IN PROGRESS: Fix the names of the tests
helpers_root/dev_scripts_helpers/documentation/test/test_check_links.py

- [ ] Check CsfyIssue8889

dev_scripts_helpers/documentation/test/test_notes_to_pdf.py                                                                               85     12      8      2    83%
dev_scripts_helpers/documentation/preprocess_notes.py                                                                                    349     78    140     19    77%
dev_scripts_helpers/documentation/render_images.py                                                                                       381    174    142      9    53%

dev_scripts_helpers/dockerize/lib_pandoc.py                                                                                              110     40     20      3    59%
dev_scripts_helpers/dockerize/lib_prettier.py                                                                                            124     15     34      6    84%

helpers/hmarkdown.py                                                                                                                      13      0      0      0   100%
helpers/hmarkdown_bullets.py                                                                                                              93     81     44      0     9%
helpers/hmarkdown_coloring.py                                                                                                            108     59     38      5    41%
helpers/hmarkdown_comments.py                                                                                                             28      9     10      3    63%
helpers/hmarkdown_div_blocks.py                                                                                                           54     23     24      4    55%
helpers/hmarkdown_fenced_blocks.py                                                                                                        55      0     14      1    99%
helpers/hmarkdown_filtering.py                                                                                                            68     56      8      0    16%
helpers/hmarkdown_formatting.py                                                                                                          335    259     84      1    19%
helpers/hmarkdown_headers.py                                                                                                             330    156    144     18    50%
helpers/hmarkdown_rules.py                                                                                                               104     86     42      0    12%
helpers/hmarkdown_select.py                                                                                                              251    112     92     14    54%
helpers/hmarkdown_slides.py                                                                                                               90     24     30      5    69%
helpers/hmarkdown_tables.py                                                                                                               48     31     14      1    32%
helpers/hmarkdown_toc.py                                                                                                                  92     24     26      8    68%

- [ ] Extract lib_notes_to_pdf.py

./dev_scripts_helpers/documentation/notes_to_pdf.py


### What tests pass on master vs local?

### Make the second and 3rd level of text smaller

### Use Latex font
https://tug.org/FontCatalogue/computermodern/ instead of DejaVu

### IN PROGRESS: [ ] Fix Latex Preamble

dev_scripts_helpers/documentation/preprocess_notes.py

- [ ] Add unit tests
- [ ] Factor out code to umd_classes

### IN PROGRESS: [ ] Fix div stuff

- [x] Add two steps of AST unit test
- [ ] Add unit tests (for 1 and 2 phases)
- [ ] Add processing of AST

### gen_slides.py msml610/11.1

It doesn't work since it requires --slides_engine=beamer --skip_pandoc_ast_transform

> notes_to_pdf.py --input=msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt --output=msml610/lectures/Lesson11.1-Decision_Making_with_Causal_Models.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine=beamer --skip_pandoc_ast_transform

### IN PROGRESS: [ ] Fix blue verbatim

### Improve tables

- [ ] Use table from let styled-table using AST transform
- [ ] Add processing of AST
- [ ] Add unit tests

### [x] Fix the bold colored

**\textcolor{red}{Question}**

2. preprocess_notes.py: _transform_lines() function (line 463-465) processes color commands and then:
  - Line 542: calls hmarkdo.colorize_bullet_points_in_slide() for slides
  - This function automatically colorizes specific keywords (like Question, Definition, Key idea, etc.) with red/blue colors
3. The coloring happens here in preprocess_notes.py lines 524-560 via the _colorize_bullets() helper function which wraps hmarkdo.colorize_bullet_points_in_slide()

### [x] The title of a slide is not showing up

### [ ] Autoscale the font to fit the slide

### [ ] Document current system
- `helpers_root/dev_scripts_helpers/documentation/README.md`
- `helpers_root/dev_scripts_helpers/documentation/notes_to_pdf.README.md`

### [ ] Document typst and slides

website/README.blog.md

website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md
- Create blog

website/docs/blog/posts/draft.in_30_mins.helpers_typesetting_system.md
-> create blog

website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.all_examples.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.hello_world.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.all_examples.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.hello_world.typ
website/docs/blog/posts/draft.how_to.latex_vs_typst_for_typsetting.md

### [ ] Extend the flow and document it
dev_scripts_helpers/documentation/notes_to_pdf.py

> notes_to_pdf.py --input=data605/lectures_source/Lesson01.1-Intro.txt --output=data605/lectures/Lesson01.1-Intro.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst

### [ ] Fix pandoc/core:3.7

- my typst path used container_type = "pandoc_only", which points at the bare
  pandoc/core:3.7 image. That image isn't built/pulled locally (only
  pandoc_texlive and pandoc_latex get auto-built), so the assert fails.
  ```
  > container image pull pandoc/core:3.7
  ```

msml610/lectures_source/Lesson10.2-Causal_Discovery.txt

### [ ] Reorg dev_scripts_helpers/documentation
- Too many files

### Rename the txt files to smd

smd = slide markdown

# Mix

### [ ] Clean up all the messy interfaces

    use_host_tools,
    dockerized_force_rebuild,
    dockerized_use_sudo,

- It's not clear how to do it, maybe pass a config?

### [ ] Update render_images.py

- [ ] Add an option to only render without commenting out the code

- [ ] Clarify what is the boilerplate for Latex and Tikz

- [ ] Improve documentation

  - `helpers_root/dev_scripts_helpers/documentation/render_images.py`
  - `helpers_root/dev_scripts_helpers/documentation/test/test_render_images.py`
  - `helpers_root/docs/tools/documentation_toolchain/all.render_images.explanation.md`

- [ ] Publish blog

  - `website/docs/blog/posts/draft.in_5_mins.helpers_render_images.md`

### [ ] Fix output of lint_cc.py

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
test_hmarkdown_formatting.py
```
> pytest helpers/test/test_hmarkdown_formatting.py
> pytest helpers/test/test_hmarkdown_formatting.py::Test_format_md_comparison_and_performance
```

## Improve cost and speed accounting for hllm

## Managing gsheet links

vi dev_scripts_helpers/scraping/README.link_flow.md

download_link_articles.py --url https://docs.google.com/spreadsheets/d/1i6Z7v2TzPdftR9BQ5Ia6jrrNWvVy-pUCxZAt4A59l8M/edit?gid=2008094999#gid=2008094999 --row_idx 2

llm_cli.py -p "Summarize the following text in 5 bullet points and less than 200 words" --input We_should_be_more_tired_than_the_model.hn_comments.txt --model openrouter/anthropic/claude-haiku-4.5 --lint

## Fix annoying claude code scrolling

tmux focus-events off · add 'set -g focus-events on' to ~/.tmux.conf and reattach for focus tracking
tmux detected · scroll with PgUp/PgDn · or add 'set -g mouse on' to ~/.tmux.conf for wheel scroll

## Process Academic Articles

  ```
  > download_academic_paper.py -i https://arxiv.org/pdf/2305.10032
  > convert_pdf_to_md.py -i 2023.Zanga.et.al.A_Survey_on_Causal_Discovery_Theory_and_Practice.pdf
  > summarize_md.py
  ```

  ```
  > download_academic_paper.py -i https://arxiv.org/pdf/1602.04938.pdf
  claude> /text.extract_ideas 2016.Ribeiro_et_al.Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.pdf
  > mv 2016.Ribeiro_et_al.Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.* "$PAPERS_ROOT_DIR"/2026
  claude> /book.incorporate_content ~/Library/CloudStorage/GoogleDrive-saggese@gmail.com/My Drive/papers/2026/2016.Ribeiro_et_al.Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.ideas.md
```

## Convert llm_transform.py to llm_cli.py
Move prompts and action into a YAML file

## Merge markdown. and text.
Is there any difference?

  ```
  > ls -1 -d .claude/skills/markdown* .claude/skills/text* | sort
  .claude/skills/markdown.add_summary
  .claude/skills/markdown.fix_bullet_points
  .claude/skills/markdown.reduce
  .claude/skills/markdown.rules.md
  .claude/skills/markdown.summarize
  .claude/skills/text.convert_to_latex
  .claude/skills/text.criticize
  .claude/skills/text.explain
  .claude/skills/text.extract_ideas
  .claude/skills/text.humanize
  .claude/skills/text.read_start_end
  .claude/skills/text.rules.md
  .claude/skills/text.summarize_hn_in_bullet_points
  .claude/skills/text.summarize_in_bullet_points
  .claude/skills/text.use_bullet_lists
  ```

## Improve / unify --rule, --skill, ...

- Move --skill and --topic from ./linters2/lint_cc.py to this parser hmarsele.add_rule_cli_arg(action_group)
- Merge rigrule into mdm

## Make file interfaces aligned
- Make compatible in terms of options
  ```
  i git_files
  i git_branch_diff
  linters2/lint.py
  linters2/lint_cc.py
  ```

- Add -i, --input together with files

# Book proposals

## Manning

- Possible titles
  ```
  Probabilistic and Causal AI for Practitioners
  Causal and Probabilistic Machine Learning in Action
  ```

# Springer

- Title
  - From Data Science to Decision Science for Business

## Improve Springer proposal

springer.Causal_Inference_for_Machine_Learning_Engineers.md
springer.changes.md
springer.proposal.2026-06-18.md
springer.proposal.md
springer.review.md
springer.template.md


## [ ] Finalize TOC
- Very short intro about causality and probability
- Part 3 of [Book plan](https://docs.google.com/spreadsheets/d/1dU3crReWWLcSG8jI4jTvA4430-yMkqvdOEXEIbmktPQ/edit?gid=0#gid=0)
- Look at review

# ? AI Agents for Big Data

- DATA605
- Agents stuff

# AI for Finance
- ?
