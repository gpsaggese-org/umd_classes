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

