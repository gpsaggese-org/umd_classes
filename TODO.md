# #############################################################################
# High level
# #############################################################################

- There are too many failures across multiple builds
  - Do not add more code but focus on getting to a stable build
  - Disable the failing tests
  - Merge `gp_scratch_29`
  - Merge `HelpersTask1273_Get_Mac_tests_to_pass`

- [.] HelpersTask1273_Get_Mac_tests_to_pass_3
  - Create tools for analyzing and helping with the unit tests
  - Improvements to pytest_failed

- Find a workflow to make it easier to create smaller PRs
  - Instead of having lots of agents making changes to the same branch
  - Have a way to delegate to an agent to create a small PR, do the change,
    regress, review and merge
  - Always create PRs associated to each branch with a clear description
    - i git_branch_create -> i gh_create_pr --no-draft
  - Find an easy way to check which PR is still to merge, which one was merged

- Have a thread that looks for TODOs in the code (gp, ai_gp)
  - Ranks them by simplicity
  - Create a branch, PR, run tests and merge

# #############################################################################
# IN PROGRESS
# #############################################################################

helpers/test/test_amp_dev_scripts.py::Test_env1::test_get_system_signature1 Password:
Sorry, try again.
Password:

### [.] Merge gp_scratch_29
- In `umd_classes1`
- i gh_watch
- It crashes with no space on disk

```
dev_scripts_helpers/documentation/test/test_convert_pandoc_divved_fence.py::Test_end_to_end::test1 (0.84 s) FAILED
```

- Disable all the Test_notes_to_pdf1

```
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf1::test1 (2.06 s) PASSED [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test1 (128.13 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test1 (74.34 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test1 (71.27 s) FAILED                                                                   [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test2 (70.75 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test2 (70.67 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test2 (78.41 s) FAILED                                                                   [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test3 (69.69 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test3 (70.50 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test3 (79.34 s) FAILED                                                                   [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test4 (71.62 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test4 (62.83 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test4 (74.26 s) FAILED                                                                   [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test5 (2.24 s) FAILED [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test1 (6.78 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test1 (6.50 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test1 (6.55 s) FAILED                                                                   [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test2 (70.71 s) RERUN                                                                    [ 15%]
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test2 (70.89 s) RERUN                                                                    [ 15%]
```

### [.] Improve pytest_failed

- Read output from any pytest (local, docker, github)
- Make it into a script called by invoke
- Extract the failing tests
- Extract the longest tests
- Report the updated tests
...

### [.] HelpersTask1273_Get_Mac_tests_to_pass
- In `csfy1`
- [.] Get all the tests in master to pass
- [.] run.sh running

### [.] Make `dev_scripts_helpers/documentation/test/test_notes_to_pdf.py` pass
- In `umd_classes2` // gp_scratch

- [.] pytest_log dev_scripts_helpers/documentation/test/test_notes_to_pdf.py
- [.] /testing.triage_unit_tests dev_scripts_helpers/documentation/test/test_notes_to_pdf.py

### [.] Improve coverage of dev_scripts_helpers/documentation/

> pytest dev_scripts_helpers/documentation --cov=dev_scripts_helpers/documentation

- Need to check again

### [.] Improve coverage of class_scripts

### [.] Make the unit tests pass in `umd_classes`

- [x] Run `pytest_log msml610/test/test_gen_slides.py`
- [x] Run `pytest_log data605/test/test_gen_slides.py`
- [.] Run `linters2/lint.py --action pyright`
- [x] PASS `pytest_log class_scripts`
- [ ] Run `pytest_log msml610/test data605/test class_scripts`
- [ ] Do a run of all the tests in `pytest_log .` (with the 3 builds)
- [ ] Run coverage

data605/test/test_gen_slides.py::Test_Data605_Run_notes_to_pdf_py::test_tex_output msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_tex_output msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_typ_output

data605/test/test_gen_slides.py::Test_Data605_Run_notes_to_pdf_py::test_tex_pdf

Test_Msml610_Run_notes_to_pdf_py

```
pytest msml610/test

msml610/test/test_gen_slides.py::Test_Msml610_Run_gen_slides_py::test_gen_slides_first_lesson
msml610/test/test_gen_slides.py::Test_Msml610_Run_gen_slides_py::test_render_all_lessons
msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_notes_to_pdf_md
msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_notes_to_pdf_tex
```

- [x] IN PROGRESS Save tex and typ files for all the lessons
  - [x] pytest_log msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_tex_output
  - [x] pytest_log msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_typ_output
- [x] Make all the lessons compile to latex
  - [x] pytest_log msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_typ_pdf
  - [x] pytest_log msml610/test/test_gen_slides.py::Test_Msml610_Run_notes_to_pdf_py::test_tex_pdf

### [.] Read Academic Articles

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

### [ ] From Data To Decisions
/Users/saggese/src/notes1/book.Springer.From_Data_to_Decision_Science/springer.proposal_v2.toc.md
/Users/saggese/src/notes1/book.Springer.From_Data_to_Decision_Science/springer.saggese.full_proposal_v2.md
/Users/saggese/src/umd_classes2/book.From_Data_To_Decisions/book_map.md
/Users/saggese/src/umd_classes2/book.From_Data_To_Decisions/book_toc.md

- [x] Merge /Users/saggese/src/notes1/book.Springer.From_Data_to_Decision_Science/springer.toc_v2.md
  into /Users/saggese/src/umd_classes2/book.From_Data_To_Decisions/book_map.md
- [ ] Merge ~/src/umd_classes2/book.From_Data_To_Decisions/OLD 
  into /Users/saggese/src/umd_classes2/book.From_Data_To_Decisions/book_map.md

- [ ] Check what is already covered by the slides in msml610/lectures_source

### [.] Create and review slides for Agentic AI

- TOC is at `/Users/saggese/src/notes1/book.AI_For_Data_Science/agentic_ai_toc.md`
  - `Execute /Users/saggese/src/notes1/book_proposals/prompt.from_toc_to_slides.md`

- [x] msml610/lectures_source/Lesson16.1-What_Is_An_Agentic_AI.txt
- [x] msml610/lectures_source/Lesson16.2-LLM_Building_Blocks.txt
- [x] msml610/lectures_source/Lesson16.3-History_of_LLM_Agents.txt
- [x] msml610/lectures_source/Lesson16.4-LLM_Reasoning.txt
- [x] msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt
  - /slides.lint_5_at_the_time msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt
- [x] msml610/lectures_source/Lesson16.5-Reasoning_Memory_and_Planning.txt
- [x] msml610/lectures_source/Lesson16.6-Inference_time_techniques.txt
- [x] msml610/lectures_source/Lesson16.7-Tool_use_and_retrieval.txt
- [.] msml610/lectures_source/Lesson16.8
- [ ] msml610/lectures_source/Lesson16.9
- [ ] msml610/lectures_source/Lesson16.10
- [ ] msml610/lectures_source/Lesson16.11
  > gen_slides.py msml610/16.5 --slides_engine typst --daemon
  > gen_slides.py msml610/16.4 --slides_engine typst --no_fail_on_warnings

# #############################################################################
# BACKLOG
# #############################################################################

# Work on slides

- LLM
  - Kaparthy's LLM
  - https://github.com/karpathy/nanochat
  - https://github.com/karpathy/nanoGPT
  - https://github.com/karpathy/micrograd
  - https://karpathy.ai/
- AutoEDA
- IN PROGRESS: Topics from Berkeley class
- AlphaEvolve
- Monte Carlo search
- Kaparthy's AutoResearch
- https://www.manning.com/books/build-a-large-language-model-from-scratch
- https://www.manning.com/books/build-a-reasoning-model-from-scratch
- https://aman.ai/primers/ai/top-30-papers/
  - https://arc.net/folder/D0472A20-9C20-4D3F-B145-D2865C0A9FEE

- Add references to papers
- Add more / better pictures
- Summary

## Causal Probabilistic ML
book.Causal_Probabilistic_ML/book_map.md

## AI for Data Science
book.AI_for_data_science/book_map.md

/Users/saggese/src/notes1/book.AI_For_Data_Science/agentic_ai_toc.md

# Downloading HN Links

```
export LINKS_GSHEET=https://docs.google.com/spreadsheets/d/1i6Z7v2TzPdftR9BQ5Ia6jrrNWvVy-pUCxZAt4A59l8M/edit?gid=2008094999#gid=2008094999

> download_link_articles.py --url "$LINKS_GSHEET" --row_idx 1
```

- To understand the structure
  ```
  > ./dev_scripts_helpers/coding_tools/build_call_graph.py --input dev_scripts_helpers/scraping/download_link_articles.py
  ```

- Create unit tests from the cache

- Run a test_generator.py with a command
  ./dev_scripts_helpers/coding_tools/build_call_graph.py --input dev_scripts_helpers/scraping/download_link_articles.py
  1) the cache gets warmed up and saved in the right position (using a command
     line switch)
  2) test code gets generated that in practice runs the command (using the proper
  command line switch)

hcacsimp.add_cache_control_arg(parser)

- Switch the order of HN and article
- Article_url is always present (even if we bookmark the url)
  - If url is not hackernews than propagate
- Check that the gsheet has all the expected columns in the expected order

- Add a mode --cache_mode TRACE_CACHE to show the behavior of the cache (e.g.,
  warning when there are cache hits), maybe different colors

# Download and process Dwakersh blogs and LexFriedman blogs

# Convert slides into book

- [x] Create a map from book.from_corr_to_decision/book_map.md

class_scripts/create_book_toc_from_slides.py --max_number 2 --max_level 2

- [x] Add comments to README

### [.] Improve Generating Book

#### The old flow
The output looks like 
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/data605/book/Lesson01.1-Intro.book_chapter.pdf

#### The new flow 
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

### [ ] Get typst slides as close as possible to latex ones

```
notes_to_pdf.py --input=msml610/lectures_source/Lesson13.1-Explainability.txt --output=msml610/lectures/Lesson13.1-Explainability.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst --no_fail_on_warnings
vi msml610/lectures/tmp.notes_to_pdf.render_image2.txt msml610/lectures/tmp.notes_to_pdf.render_image2.typ
```

### [ ] Improve unit testing

```
> pytest dev_scripts_helpers/documentation/test/
```

- [ ] Do test runs and which is disabled?
- [ ] What is the coverage?
- [ ] What is not tested?

- [ ] Check CsfyIssue8889

dev_scripts_helpers/documentation/test/test_notes_to_pdf.py   85     12      8      2    83%
dev_scripts_helpers/documentation/preprocess_notes.py        349     78    140     19    77%
dev_scripts_helpers/documentation/render_images.py           381    174    142      9    53%

dev_scripts_helpers/dockerize/lib_pandoc.py                  110     40     20      3    59%
dev_scripts_helpers/dockerize/lib_prettier.py                124     15     34      6    84%

helpers/hmarkdown.py                                          13      0      0      0   100%
helpers/hmarkdown_bullets.py                                  93     81     44      0     9%
helpers/hmarkdown_coloring.py                                108     59     38      5    41%
helpers/hmarkdown_comments.py                                 28      9     10      3    63%
helpers/hmarkdown_div_blocks.py                               54     23     24      4    55%
helpers/hmarkdown_fenced_blocks.py                            55      0     14      1    99%
helpers/hmarkdown_filtering.py                                68     56      8      0    16%
helpers/hmarkdown_formatting.py                              335    259     84      1    19%
helpers/hmarkdown_headers.py                                 330    156    144     18    50%
helpers/hmarkdown_rules.py                                   104     86     42      0    12%
helpers/hmarkdown_select.py                                  251    112     92     14    54%
helpers/hmarkdown_slides.py                                   90     24     30      5    69%
helpers/hmarkdown_tables.py                                   48     31     14      1    32%
helpers/hmarkdown_toc.py                                      92     24     26      8    68%

- [ ] Extract lib_notes_to_pdf.py

./dev_scripts_helpers/documentation/notes_to_pdf.py

### Improve lint_txt.py

- -> lint_text.py

- Test lint_txt.py to see which tool is best (prettier, mdformat, ...)

- txt -> smd, or mds (slide markdown) 

- The transforms are:

                             preprocess: Yes
                               prettier: Yes
                            postprocess: Yes
    remove_code_block_extra_indentation: Yes
                 remove_page_separators: Yes
                     handle_empty_lines: Yes
        add_blank_lines_between_headers: Yes
     convert_asterisk_bullets_to_dashes: Yes
                remove_trailing_periods: Yes
             replace_em_dash_with_colon: Yes
             remove_markdown_formatting: -
                         frame_chapters: -
                      capitalize_header: Yes
                            refresh_toc: -
                            check_links: -

- The preprocess stage should handle everything that is not standard markdown

- prettier doesn't handle well
  - //
  - The * slides

- Add spaces between first level bullets

- Make the definitions bold and black for visibility
  - -*Definition*- for bold and color
  - **Definition** for black and color



### [ ] Improve _LOG output

```
18:05:06 common_utils.py find_lecture_file:62                Searching for files matching pattern='msml610/lectures_source/Lesson00*'
18:05:06 - INFO  common_utils.py find_lecture_file:74                   Found lecture file: msml610/lectures_source/Lesson00-Class.txt
18:05:06 common_utils.py get_source_name:92                  Source name='Lesson00-Class.txt'
```

- Remove `-` which wastes space
- Align everything
- Maybe add DEBUG?
  - Use `I`, `D`, `W`

### Use Latex font
https://tug.org/FontCatalogue/computermodern/ instead of DejaVu

### [.] Fix Latex Preamble

dev_scripts_helpers/documentation/preprocess_notes.py

- [x] Get it working
- [ ] Add unit tests
- [ ] Factor out code to umd_classes

### Update documentation

Add https://typst.app/play/ to the 

### Improve pandoc/typst tables

- Not needed since we are inlining directly the slides in Latex format
  - It might be nice to have markdown only

- [ ] Use table from let styled-table using AST transform
- [ ] Add processing of AST
- [ ] Add unit tests

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
- [ ] Render many different files at once
- [ ] Clarify what is the boilerplate for Latex and Tikz
- [x] IN PROGRESS: Fix the names of the tests
helpers_root/dev_scripts_helpers/documentation/test/test_check_links.py

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

### [ ] Add support for nitro models and reasoning in llm_cli and in cc

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

### [ ] Improve llm_compare.py

llm_compare.py --models "openrouter/openai/gpt-4o-mini,openrouter/openai/gpt-oss-120b" --benchmark summarization1 --output_dir results/

run_eval.sh

Get info about models
dev_scripts_helpers/llms/openrouter_models_table.py --models dev_scripts_helpers/llms/test_models.txt

helpers_root/dev_scripts_helpers/llms/openrouter_models_table.py --models_from_file helpers_root/dev_scripts_helpers/llms/text_models.txt

### [ ] Test lint_txt.py with new backends

lint_txt.py -i dev_scripts_helpers/ai/README.md --backend mdformat --mode uvx

Better / faster markdown formatting
test_hmarkdown_formatting.py
```
> pytest helpers/test/test_hmarkdown_formatting.py
> pytest helpers/test/test_hmarkdown_formatting.py::Test_format_md_comparison_and_performance
```

mdformat .claude/skills/slides.write/SKILL.md --number

Need to disable the protection and keep it only for prettier

Merge --backend and --mode

### [ ] Improve cost and speed accounting for hllm

### [ ] Fix annoying claude code scrolling

tmux focus-events off · add 'set -g focus-events on' to ~/.tmux.conf and reattach for focus tracking
tmux detected · scroll with PgUp/PgDn · or add 'set -g mouse on' to ~/.tmux.conf for wheel scroll

### [ ] Convert llm_transform.py to llm_cli.py
Move prompts and action into a YAML file

### [ ] Merge markdown.rules.md and text.rules.md?
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

### [x] Make file interfaces aligned
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

# ? AI Agents for Big Data

- DATA605
- Agents stuff

# AI for Finance
- ?
