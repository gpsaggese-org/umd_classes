- [x] msml610/lectures_source/Lesson16.1-What_Is_An_Agentic_AI.txt
- [x] msml610/lectures_source/Lesson16.2-LLM_Building_Blocks.txt
- [x] msml610/lectures_source/Lesson16.3-History_of_LLM_Agents.txt
- [x] msml610/lectures_source/Lesson16.4-LLM_Reasoning.txt
- [x] msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt
  - /slides.lint_5_at_the_time msml610/lectures_source/Lesson11.2-Probabilistic_deep_learning.txt
- [x] msml610/lectures_source/Lesson16.5-Reasoning_Memory_and_Planning.txt
- [x] msml610/lectures_source/Lesson16.6-Inference_time_techniques.txt
- [x] msml610/lectures_source/Lesson16.7-Tool_use_and_retrieval.txt

- [x] Create a Springer dir (similar to msml610)
- [x] Merge /Users/saggese/src/notes1/book.springer/springer.toc_v2.md
  into /Users/saggese/src/umd_classes2/book.springer/book_map.md
- [x] Merge ~/src/umd_classes2/book.springer/OLD 
  into /Users/saggese/src/umd_classes2/book.springer/book_map.md
- [x] Check what is already covered by the slides in msml610/lectures_source
### [x] Merge gp_scratch_29
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

### [x] Convert ./run_multiple_builds.sh into an invoke target
- Extend i create_branch_copy to work with only a subset of files / dirs

- [x] Merge `HelpersTask1273_Get_Mac_tests_to_pass_5`

- [x] `HelpersTask1273_Get_Mac_tests_to_pass_3`
  - Create tools for analyzing and helping with the unit tests
  - Improvements to pytest_failed

- [x] `HelpersTask1273_Get_Mac_tests_to_pass_4`
  - Merge in all the branches
### [x] Improve pytest_failed

- Read output from any pytest (local, docker, github)
- Make it into a script called by invoke
- Extract the failing tests
- Extract the longest tests
- Report the updated tests
...

### [x] Improve Springer proposal
- Title
  - From Data Science to Decision Science for Business

springer.Causal_Inference_for_Machine_Learning_Engineers.md
springer.changes.md
springer.proposal.2026-06-18.md
springer.proposal.md
springer.review.md
springer.template.md

### [x] Finalize TOC
- Very short intro about causality and probability
- Part 3 of [Book plan](https://docs.google.com/spreadsheets/d/1dU3crReWWLcSG8jI4jTvA4430-yMkqvdOEXEIbmktPQ/edit?gid=0#gid=0)
- Look at review

### Create branch for 1276
https://github.com/causify-ai/helpers/issues/1276

### [x] Handle the latex macros

> notes_to_pdf.py --input=msml610/lectures_source/Lesson16.2-LLM_Building_Blocks.txt --output=msml610/lectures_source/Lesson16.2-LLM_Building_Blocks.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst

- [ ] All unit tests should freeze the output of the script
- [x] Use the right idiom for the command line construction

Remove --fail_on_pandoc_warnings
Remove open by default

### IN PROGRESS: Failing tests

pytest_log dev_scripts_helpers/documentation/test/test_convert_pandoc_divved_fence.py dev_scripts_helpers/documentation/test/test_notes_to_pdf.py

dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf1::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf1::test3
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_actions::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_actions::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_edge_cases::test3
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_edge_cases::test4
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test3
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test4
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_filters::test5
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_latex_options::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_latex_options::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_output_types::test3
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_pandoc_ast::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_pandoc_ast::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_pandoc_ast::test3_ast_transform_inline_formatting_columns
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_script_generation::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_script_generation::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_toc_options::test1
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_toc_options::test2
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_toc_options::test3
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_toc_options::test4
dev_scripts_helpers/documentation/test/test_notes_to_pdf.py::Test_notes_to_pdf_typst_abbrevs::test_end_to_end

### [x] Fix pandoc/core:3.7

- my typst path used container_type = "pandoc_only", which points at the bare
  pandoc/core:3.7 image. That image isn't built/pulled locally (only
  pandoc_texlive and pandoc_latex get auto-built), so the assert fails.
  ```
  > container image pull pandoc/core:3.7
  ```

msml610/lectures_source/Lesson10.2-Causal_Discovery.txt

### [x] Make the second and 3rd level of text smaller

### [x] Fix div stuff

- [x] Add two steps of AST unit test
- [x] Add unit tests (for 1 and 2 phases)
- [ ] Add processing of AST

### [x] Fix gen_slides.py msml610/11.1

It doesn't work since it requires --slides_engine=beamer --skip_pandoc_ast_transform

> notes_to_pdf.py --input=msml610/lectures_source/Lesson11.1-Decision_Making_with_Causal_Models.txt --output=msml610/lectures/Lesson11.1-Decision_Making_with_Causal_Models.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine=beamer --skip_pandoc_ast_transform
### [x] Improve last_cmd and notify.py

/Users/saggese/src/umd_classes2/helpers_root/dev_scripts_helpers/coding_tools/last_cmd.py

### [x] Improve linters2/lint.py

- [x] IN PROGRESS: Fix the names of the tests
helpers_root/dev_scripts_helpers/documentation/test/test_check_links.py

### [x] Fix the bold colored

**\textcolor{red}{Question}**

2. preprocess_notes.py: _transform_lines() function (line 463-465) processes color commands and then:
  - Line 542: calls hmarkdo.colorize_bullet_points_in_slide() for slides
  - This function automatically colorizes specific keywords (like Question, Definition, Key idea, etc.) with red/blue colors
3. The coloring happens here in preprocess_notes.py lines 524-560 via the _colorize_bullets() helper function which wraps hmarkdo.colorize_bullet_points_in_slide()

### [x] The title of a slide is not showing up

### [x] Fix blue verbatim

### IN PROGRESS: [ ] Fix div stuff

./dev_scripts_helpers/documentation/convert_pandoc_divved_fence.py

./helpers_root/dev_scripts_helpers/documentation/test/test_convert_pandoc_divved_fence.py

Not good that we need to call pandoc from inside the filter, better to use a
filter (and leave the two steps pandoc as a way to debug)

sided_blocks_filter.py

pandoc two_blocks.md \
    --template=./helpers_root/dev_scripts_helpers/documentation/pandoc_touying.typ \
    --from=markdown \
    --to=typst \
    --filter=./sided_blocks_filter.py \
    --output=two_blocks_output.typ && \
  typst compile two_blocks_output.typ two_blocks_output.pdf

Input

# Two Side-by-Side Blocks

::: columns
:::: {.column width=55%}
## Block A

This is the first block.

- Point A
- Point B
- Point C
::::

:::: {.column width=45%}
## Block 2

This is the second block.

- Point X
- Point Y
- Point Z
::::
:::

Output

= Two Side-by-Side Blocks
<two-side-by-side-blocks>
#grid(
  columns: (55fr, 45fr),
  gutter: 1em,
  rect(fill: rgb("#f0f0f0"), inset: 1em)[
=== Block A

This is the first block.

- Point A
- Point B
- Point C
  ],  rect(fill: rgb("#e0e0e0"), inset: 1em)[
=== Block 2

This is the second block.

- Point X
- Point Y
- Point Z
  ],
)
### [x] Tutorials for Explainable ML
- Follow tutorials/README.md

/notebook.create_api_intro shap https://shap.readthedocs.io/ and save it in tutorials/ml_explainability/ml_explainability.01.API.shap.ipynb

Start with a single model end-to-end
(linear model)

Show local explanation

Show global explanation

### [x] Improve Manning proposal after review

- [x] Remove the last part
  ```
  > vimdiff \
    manning.Causal_Probabilistic_Machine_Learning/manning.proposal_v1.toc.md
    manning.Causal_Probabilistic_Machine_Learning/manning.proposal_v3.toc.md
  ```
  and keep only first 2 parts of [Book plan](https://docs.google.com/spreadsheets/d/1dU3crReWWLcSG8jI4jTvA4430-yMkqvdOEXEIbmktPQ/edit?gid=0#gid=0)

  ```
  > vi /Users/saggese/src/notes1/book.manning.Causal_Probabilistic_Machine_Learning/{manning.proposal_v3.toc.md,manning.template.md,manning.changes_after_review.md}
  ```

- [x] Change Chap 1
  - Explain small data
  - Systems with low signal to noise ratio
  - Explainability, actionability

/Users/saggese/src/notes1
> ls -1 book.manning.Causal_Probabilistic_Machine_Learning/
manning.changes_after_review.md
manning.proposal_v1.md
manning.proposal_v1.toc.md
manning.proposal_v2.md
manning.proposal_v2.toc.md
manning.proposal_v3.toc.md
manning.reviews_v1.md
manning.template.md

### [x] Expand the TOC

- The 
book_proposals/manning.Causal_Probabilistic_Machine_Learning/manning.proposal_v3.toc.md
      using
      /Users/saggese/src/umd_classes2/book.Causal_Probabilistic_ML/book_toc.md

| Ch     | Manning Proposal                    | Book TOC (Lecture Source)             | Gap                                                                                                                                                                                                                               |
| ------ | ----------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1**  | Prediction→Decision pipelines       | Lesson08.1: good coverage            | Book TOC adds "Causal AI in Business" (workflow, explainability) not in Manning                                                                                                                                                   |
| **2**  | Bayesian Networks                   | Lesson06.1 + 06.2: strong coverage   | Well aligned                                                                                                                                                                                                                      |
| **3**  | Causal DAGs & Structural Models     | Lesson08.3 (Do-Calculus only)         | **Major gap**: Manning has SCMs, mediators/moderators/confounders/colliders, building DAGs from domain knowledge. Book TOC only has intervention/counterfactuals/adjustment/do-calculus (which is actually Manning Ch 5 material) |
| **4**  | Causal Models→Code (PyMC)           | Lesson07.1-07.5: very deep           | Book TOC much richer: adds Bayesian Model Comparison (07.5) not in Manning. Manning lacks model comparison entirely                                                                                                               |
| **5**  | Interventions & Adjustments         | Lesson08.3 (same source as Ch 3)      | **Duplicate**: Book TOC maps identical Lesson08.3 content to both Ch 3 and Ch 5                                                                                                                                                   |
| **6**  | Causal Identification & Estimation  | Lesson08.4: extensive                | Book TOC much broader: metalearners, geo/switchback experiments, non-compliance/instruments. Manning has case study + sensitivity analysis not in lectures                                                                        |
| **7**  | Explainability & Causal Attribution | **Missing entirely**                  | **No lecture source mapped** for SHAP, LIME, DiCE, causal attribution                                                                                                                                                             |
| **8**  | Causal Inference for Time Series    | Lesson10 + 10.1: deep                | Book TOC includes full time series foundations (ARMA, ARCH, modern approaches) that Manning assumes as prerequisite                                                                                                               |
| **9**  | A/B Testing & Experimentation       | Lesson09.3 (Multi-Armed Bandits only) | **Thin**: Missing A/B test design, switchbacks, sequential decision-making from Manning                                                                                                                                           |
| **10** | Causal Discovery                    | Lesson10.2: good match               | Well aligned                                                                                                                                                                                                                      |

