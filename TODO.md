# #############################################################################
# High level
# #############################################################################

- There are too many failures across multiple builds
  - Do not add more code but focus on getting to a stable build
  - Disable the failing tests
  - [x] Merge `gp_scratch_29`
  - [x] Merge `HelpersTask1273_Get_Mac_tests_to_pass`

> export CSFY_DOCKER_ENGINE="docker"; i docker_bash --stage=local -v 1.6.0;
> export CSFY_DOCKER_ENGINE="docker"; i docker_cmd --stage=local -v 1.6.0 --cmd "pytest_log dev_scripts_helpers"

> export CSFY_DOCKER_ENGINE="docker"; pytest_log dev_scripts_helpers

> export CSFY_DOCKER_ENGINE="apple"; pytest_log dev_scripts_helpers

##
- Find a workflow to make it easier to create smaller PRs
  - Instead of having lots of agents making changes to the same branch
  - Have a way to delegate to an agent to create a small PR, do the change,
    regress, review and merge
  - Always create PRs associated to each branch with a clear description
    - i git_branch_create -> i gh_create_pr --no-draft
  - Find an easy way to check which PR is still to merge, which one was merged

  - /github.split_branch_in_PRs
  - Review edit github_pr_plan.md
  - /github.create_child_pr PR2

##
- Have a thread that looks for TODOs in the code (gp, ai_gp)
  - Ranks them by simplicity
  - Create a branch, PR, run tests and merge

##

Create a script to apply a skill to a set of files

Is there anything already?

apply_cc_skill.py --skill ... or --rule ... --files ...

Do it in parallel

Fix the output

# #############################################################################
# IN PROGRESS
# #############################################################################

## pytest_failed

### [.] Improve pytest_failed.py and pytest_failed_multi_build.py

Short tests

> pytest_multi_build.py --target dev_scripts_helpers/documentation/test/test_split_text_in_chapters.py
> pytest_multi_build.py --target dev_scripts_helpers/documentation/test/
generates `tmp.pytest_multi_build.<build_name>.txt`

Run for a single build
pytest_failed.py -i tmp.pytest_multi_build.apple.txt

Run for all builds
> pytest_failed_multi_build.py
generates `tmp.pytest_failed.<build_name>.<tag>.txt` for each build
and then 
`tmp.pytest_failed_multi_build.failed_tests.txt`
`tmp.pytest_failed_multi_build.repro.sh`

./dev_scripts_helpers/testing/pytest_failed_multi_build.py ./dev_scripts_helpers/testing/pytest_failed.py ./dev_scripts_helpers/testing/pytest_multi_build.py
./dev_scripts_helpers/testing/test/test_pytest_failed_multi_build.py ./dev_scripts_helpers/testing/test/test_pytest_failed.py ./dev_scripts_helpers/testing/test/test_pytest_multi_build.py

 /pytest.triage_local_unit_tests tmp.pytest_failed_multi_build.repro.sh

Fix group

pytest_failed.py -i tmp.pytest_multi_build.apple.txt --in_build_tag ... --out_build_tag

tmp.pytest_failed_multi_build.repro.sh

pytest_failed.py -i tmp.pytest_multi_build.apple.txt --in_build_tag ... --out_build_tag

tmp.pytest_failed_multi_build.repro.sh

// Using GH
i gh_workflow_list

tmp.failure.check_if_the_linter_was_run.helperstask1273_get_mac_tests_to_pass.txt

pytest_failed.py -i tmp.failure.fast_tests.helperstask1273_get_mac_tests_to_pass.txt

```
20:17:32 - INFO  pytest_failed.py _process_single_file:227              Created 'passed_tests.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:233              Created 'failed_tests.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:239              Created 'skipped_tests.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:245              Created 'updated_tests.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:252              Created 'tests_by_duration.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:258              Created 'duration_stats.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:264              Created 'stacktraces.txt'
20:17:32 - INFO  pytest_failed.py _process_single_file:270              Created 'info.json'

################################################################################
Test Outcome Summary
################################################################################
Build                                                            | Status | Passed | Skipped | Failed | Total | Duration |
---------------------------------------------------------------- | ------ | ------ | ------- | ------ | ----- | -------- |
tmp.failure.fast_tests.helperstask1273_get_mac_tests_to_pass.txt | FAIL   | 3106   | 172     | 3      | 3281  | 263.28s  |
```

## Improve unit test

### [ ] Why there are two updated?
Updated:    2/3346

### [ ] pass regex
expected = "Version: ImageMagick 7.1.2-\S+ Q16-HDRI aarch64 24116 https://imagemagick.org"
self.assert_equal(..., regex=True)

### [ ] Print the files that have been updated in hunit_test.py
- Add report in files

### [ ] Automatically run git add for golden outcomes

## Breaks

### [ ] Password requested by Docker

helpers/test/test_amp_dev_scripts.py::Test_env1::test_get_system_signature1 Password:
Sorry, try again.
Password:

### [x] HelpersTask1273_Get_Mac_tests_to_pass
- In `csfy1`
- [x] Get all the tests in master to pass
- [x] run.sh running

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

## Create book to publish

### 
- Use the same flow (slides + commentary)
  > gen_lecture_commentary.py data605 01.1 (it's broken)

- Pointer to GitHub
- Pointer to Videos
- Pointer to Tutorials
- Pointer to Video Tutorial (on YouTube)

### Add counter and Google Analytics
- [.] Count download, visits, etc

### Publish on Substack
- [ ] Start with copy-paste

### Start Promoting
- Same as causify substack
- LinkedIn
- Email to my students

## Books

### [ ] From Data To Decisions
/Users/saggese/src/umd_classes2/book_springer/book_map_vXYZ.md
/Users/saggese/src/umd_classes2/book_springer/book_map_v3.md
/Users/saggese/src/umd_classes2/book_springer/book_toc.md
/Users/saggese/src/notes1/book_springer/springer.proposal_v2.toc.md
/Users/saggese/src/notes1/book_springer/springer.saggese.full_proposal_v2.md

- `Execute /Users/saggese/src/notes1/book_proposals/prompt.springer.from_toc_to_slides.md`

- [ ] Remove ###### from files
- [ ] Convert files to typst
- [ ] Compare the TOC book_springer/decision_making_categories_with_examples.md
  to AIMA
  https://docs.google.com/spreadsheets/d/1MSpnfnFz4JZXEnn_fd3QPkjtZmHhol-AJOO_kguO7Bg/edit?gid=1589123179#gid=1589123179

  - http://localhost:8888/lab/tree/git_root/book_springer/tutorials/Lesson10_01_q_learning

- [ ] Review `book_springer/lectures_source/Lesson01.01_From_Data_Science_To_Decision_Science.txt`
- [ ] Review `book_springer/lectures_source/Lesson01.02_Integrating_Causality_And_Probability_in_ML.txt`
- [ ] Review `book_springer/lectures_source/Lesson01.03_Integrating_Business_Objective_And_Real_World_Dynamics.txt`
- [ ] Review `book_springer/lectures_source/Lesson10.01_Taxonomy_of_Decision_Problems.txt`
- [ ] Review `book_springer/lectures_source/Lesson11.01_Simple_Decisions.txt`
- [ ] Review `book_springer/lectures_source/Lesson12.01_Complex_Decisions.txt`
- [ ] Review `book_springer/lectures_source/Lesson15.01_Deployment_Monitoring_And_Adaptation.txt`

### Typst flow

- [ ] Generate some chapters to see how they look like
  ```
  > export FILE=Lesson08.1-Causal_AI_intro
  claude> /model sonnet
  claude> Execute /Users/saggese/src/notes1/book_proposals/prompt.create_slides_to_latex_text.txt on msml610/lectures_source/${FILE}.txt
  ```

  render_typst.sh book_springer/book/Lesson02.01_From_Data_Science_To_Decision_Science.typ

### Latex flow
- [ ] Generate some chapters to see how they look like
  ```
  > export FILE=Lesson08.1-Causal_AI_intro
  claude> /model sonnet
  claude> Execute /Users/saggese/src/notes1/book_proposals/prompt.create_slides_to_typst_text.txt on msml610/lectures_source/${FILE}.txt
  ```

  ~/src/umd_classes2/book_springer/latex_template/book/run_latex.sh

  pandoc book_springer/book/Lesson02.01_From_Data_Science_To_Decision_Science.tex -s -o document.html --mathjax

- [ ] Remove Abstract
- [ ] Decrease one level
- [ ] Tweak prompt to fix these problems

### [.] Create and review slides for Agentic AI

- TOC is at `/Users/saggese/src/notes1/book.AI_For_Data_Science/agentic_ai_toc.md`
  - `Execute /Users/saggese/src/notes1/book_proposals/prompt.from_toc_to_slides.md`

- [.] book.Agentic_AI/lectures_source/Lesson01.08
  -> Reading the RHLF book before continuing
- [ ] book.Agentic_AI/lectures_source/Lesson01.09
- [ ] book.Agentic_AI/lectures_source/Lesson01.10
- [ ] book.Agentic_AI/lectures_source/Lesson01.11
  > gen_slides.py book.Agentic_AI/01.08 --slides_engine typst --daemon

## CS Refresher

- [ ] class_CS_refreshers/lectures_source/Lesson95.Refresher_game_theory.txt
  - http://localhost:8888/lab/tree/git_root/class_cs_refreshers/tutorials/notebooks/L95_05_game_theory.ipynb

- Tutorials
  - [ ] Show how the game is played
  - [ ] Show examples of dominant strategies

## RHLF Book

- notes/math.rlhfbook.txt
  - Chap 6

## Content Summarization

### [ ] 

- Create a script that given an input (url, pdf article, book title)
  - html_to_md.py 
  - download_academic_paper.py
- Download the PDF and cache it in Books or Papers dir
- Converts it to markdown (if necessary)
- Apply a text transform

### [.] Read Academic Articles

- [x] Add a script to download an HTML file to markdown
  
- [ ] Merge the flows if possible
./dev_scripts_helpers/documentation/summarize_chapters.py
./dev_scripts_helpers/documentation/summarize_md.py
.claude/skills/markdown.summarize/SKILL.md
  - html_to_md.py + /markdown.summarize seems to work well
  - summarize_chapters.py seems a worse version than /markdown.summarize
  - Maybe summarize_md.py allows to summarize in one shot or chapter by chapter

2023.Zanga.et.al.A_Survey_on_Causal_Discovery_Theory_and_Practice

Zanga et al, "A Survey on Causal Discovery Theory and Practice" (2023)

Also use arxiv link whenever possible

```
> download_academic_paper.py -i https://arxiv.org/pdf/2305.10032
> convert_pdf_to_md.py -i 2023.Zanga.et.al.A_Survey_on_Causal_Discovery_Theory_and_Practice.pdf
> summarize_md.py
```

/markdown.summarize
/text.explain
/text.extract_ideas

```
> download_academic_paper.py -i https://arxiv.org/pdf/1602.04938.pdf
claude> /text.extract_ideas 2016.Ribeiro_et_al.Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.pdf
> mv 2016.Ribeiro_et_al.Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.* "$PAPERS_ROOT_DIR"/2026
claude> /book.incorporate_content ~/Library/CloudStorage/GoogleDrive-saggese@gmail.com/My Drive/papers/2026/2016.Ribeiro_et_al.Why_Should_I_Trust_You_Explaining_the_Predictions_of_Any_Classifier.ideas.md
```

### [ ] Add scripts to read / cache books and papers

/Users/saggese/Library/CloudStorage/GoogleDrive-saggese@gmail.com/My Drive/books
How to find a book with a title like "The Book of Why" in /Users/saggese/Library/CloudStorage/GoogleDrive-saggese@gmail.com/My Drive/books

> echo "$PAPERS_ROOT_DIR"
/Users/saggese/Library/CloudStorage/GoogleDrive-saggese@gmail.com/My Drive/papers

download_academic_paper.py

# #############################################################################
# BACKLOG
# #############################################################################

# Work on slides

- LLM
  - Karpathy's LLM
  - https://www.youtube.com/@AndrejKarpathy
  - https://github.com/karpathy/micrograd
    - A tiny scalar-valued autograd engine and a neural net library on top of it with PyTorch-like API
    - https://www.youtube.com/watch?v=VMj-3S1tku0
  - https://github.com/karpathy/nanochat
    - The best ChatGPT that $100 can buy
  - https://github.com/karpathy/nanoGPT
    - The simplest, fastest repository for training/finetuning medium-sized GPTs.
  - MicroGPT
    - https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95
  - https://karpathy.ai/
  - https://karpathy.ai/zero-to-hero.html
  - https://github.com/karpathy/makemore
    - [.] The spelled-out intro to language modeling: building makemore 47
  - Karpathy's AutoResearch
- [ ]: AutoEDA
- [ ]: Topics from Berkeley class
- AlphaEvolve
- Monte Carlo search
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
  > export FILE=Lesson08.1-Causal_AI_intro
  claude> /model sonnet
  claude> Execute /Users/saggese/src/notes1/book_proposals/prompt.create_slides_to_typst_text.txt on msml610/lectures_source/${FILE}.txt
  claude> Execute /Users/saggese/src/notes1/book_proposals/prompt.update_slides_to_typst_text.txt on msml610/lectures_source/${FILE}.txt
  ```

- Render with
  ```
  > ./helpers_root/dev_scripts_helpers/typst/render_typst.sh msml610/book/$FILE
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

Remove hllm.py

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

### [ ] Add a test case for all the dockerized executables

Use Test_build_pandoc_container1 as a reference

- Build from scratch on slow_tests

### [ ] Remove use_sudo

- use_sudo is a property of the machine
  - Make use_sudo = None and then deduce it from the config

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

# Tutorials

## Existing
> ls -1 tutorials/
Asana
Autogen
Ax_Multi_Objective_Optimization
BambooAI
CausalML_Diabetes_Study
causalnex
crewai
data_science_packages
dowhy
FilterPy
gCastle
GitHub_Stats
GluonTS_COVID19_Prediction
gymnasium
Jupyter_Extension_Langchain
LangChain
LangChain_LangGraph
LangGraph
lime
LlamaIndex
Neo4j
OpenAI
pgmpy
project_template
Prophet
README.md
shap
TensorFlow
TorchRL_MAC
tsfresh
tutorial_data_science
tutorial_forecast_as_service
tutorial_pydanticAI

## 
numpy
torch
scipy
pandas

# Book proposals

## Manning

- Possible titles
  ```
  Probabilistic and Causal AI for Practitioners
  Causal and Probabilistic Machine Learning in Action
  ```

## Springer

## ? AI Agents for Big Data

- DATA605
- Agents stuff

## AI for Finance
- ?

## Interesting slide lectures outside of books

### ?
- Gaussian processes for continuous uncertainty: kernels, posterior inference,
  and extrapolation
- Variational inference for scalable Bayesian modeling: ELBO, amortized
  inference, and gradient estimation
- Normalizing flows: flexible density estimation for complex posterior
  approximation
- Probabilistic programming: specifying generative models in Pyro, NumPyro, and
  Stan
- Calibration and uncertainty quantification: coverage guarantees and conformal
  prediction
- Neural posterior estimation: learning to invert simulators and likelihood-free
  inference

## Advanced Topics for Time Series Predictions

- Self-Supervised and Representation Learning for Time Series
  - Contrastive learning (e.g., TS-TCC, SimCLR adaptations)
  - Predictive coding models (e.g., CPC)
  - Applications: few-shot forecasting, anomaly detection

- Hierarchical Bayesian Forecasting
  - Multi-level time series models
  - Shrinkage across groups
  - Handling partial pooling across different but related series

- Reinforcement Learning for Time Series Decision Making
  - Forecasting coupled with decision making
  - Inventory control, dynamic pricing
  - Predict-then-Optimize pipelines

- Transformers and Attention Mechanisms for Time Series
  - Temporal Fusion Transformer (TFT)
  - Informer, Autoformer, FEDformer
  - Handling long-term dependencies better than RNNs

- Energy-Based Models and Diffusion Models for Forecasting
  - Energy-based forecasting models
  - Diffusion probabilistic models adapted for sequences

- Time Series Generative Models
  - GANs for time series (e.g., TimeGAN)
  - Variational Autoencoders (VAEs) for synthetic data generation
  - Applications: simulation, data augmentation

- Long-Horizon Forecasting Challenges
  - Distribution shift over long horizons
  - Degradation of model accuracy
  - Specialized architectures: recurrent decoders, multi-resolution forecasting

- Uncertainty Quantification and Calibration
  - Prediction intervals
  - Coverage probability and reliability diagrams
  - Post-hoc calibration (e.g., temperature scaling)
