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

