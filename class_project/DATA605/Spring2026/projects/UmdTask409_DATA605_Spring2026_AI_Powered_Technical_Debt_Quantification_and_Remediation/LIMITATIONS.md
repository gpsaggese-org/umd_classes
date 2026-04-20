# Project Limitations and Scope Decisions

This document enumerates every place where our project scope does not fully match the literal text of the DATA605 project description, along with the reason and what we deliver instead. It exists to make our tradeoffs explicit rather than hidden in notebook prose.

---

## 1. Debt Type Coverage

**What the README asks for.** Classification of four debt types: code complexity, outdated dependencies, architectural violations, and performance bottlenecks.

**What we deliver.** Three-way classification into BUG, CODE_SMELL, VULNERABILITY (SonarQube's native categories).

**Why the difference.** The Technical Debt Dataset stores issues tagged with SonarQube's TYPE column, not the four categories the README names. Mapping to the README's categories would require:
- For complexity, architectural, and performance: rebuilding the label set from the RULE column and SonarQube's rule tags. Doable but adds a data engineering layer we did not scope for.
- For outdated dependencies: this data does not exist in the TD Dataset. SonarQube for Java does not flag dependency version staleness at the rule level. Would require parsing pom.xml files across commit history.

**What we concede in the notebook.** Outdated dependencies is explicitly out of scope. A future extension would map SonarQube rule categories to the four README buckets.

---

## 2. Impact Regression Targets

**What the README asks for.** Regression models that predict impact on team velocity, bug frequency, and development time.

**What we deliver.** Fault-inducing commit prediction, which addresses bug frequency. AUC 0.88 on training split, top-10 hit rate of 80% on held-out commons-io.

**Why the difference.**
- Team velocity in the software engineering sense (story points per sprint) requires sprint-level data the TD Dataset does not have. A commits-per-week proxy would be heavily confounded by team size and project phase, which we also do not have.
- Development time could be approximated as time between fault introduction and fault fixing, but this data is sparse in SZZ_FAULT_INDUCING_COMMITS and the proxy would be noisy.

**What we concede in the notebook.** Velocity and development time are named as future work. Bug frequency is what we deliver.

---

## 3. Test Coverage and Backward Compatibility Validation

**What the README asks for.** Autonomous agents that perform refactoring while maintaining test coverage and backward compatibility.

**What we deliver.** The agent generates refactorings. Validation uses three proxies: Java syntactic validity via javalang parser, exact match against CodeXGLUE ground-truth fixes when available, and BLEU score against ground truth. For real commons-io issues without ground truth, validation reduces to syntactic validity only.

**Why the difference.** Running actual JUnit test suites on refactored Apache Java code requires:
- A full Java build environment (Maven, specific JDK versions, dependency resolution)
- Per-project test suite execution, which can take minutes per run
- Correctly applying a small refactoring to the full file context, compiling the project, and running tests without side effects

This is incompatible with the DATA605 requirement that the notebook run end-to-end via "Kernel > Restart & Run All" on a CPU-only MacBook Air inside Docker.

**What we concede in the notebook.** Test-based validation is explicitly named as future work. CodeXGLUE ground-truth match is substituted as the primary quality signal because it represents the fix a real developer actually committed, which is a stronger signal than tests passing in many cases.

---

## 4. Feedback Loop on Refactoring Outcomes

**What the README Tasks section asks for.** A feedback loop that tracks predicted versus actual impact of refactorings to improve model accuracy over time.

**What we deliver.** Nothing directly. The agent is single-shot.

**Why the difference.** Implementing this requires:
- Applying generated refactorings to the actual Apache Java codebase
- Running the codebase's test suite (same blocker as Limitation 3)
- Tracking the refactoring across subsequent commits to measure whether the bug-prone signal went down
- Retraining the impact predictor periodically with this feedback

Each step carries its own dependencies that exceed the scope of a single tutorial notebook. The literature (Tornhill et al. 2025 ACE paper) also lists this kind of feedback loop as future work rather than delivering it.

**What we concede in the notebook.** Identified as the most substantial future work direction.

---

## 5. Repository Scale

**What the README Tasks section asks for.** Extraction of code metrics from 1,000+ open-source repositories.

**What we deliver.** Analysis across 31 pre-analyzed Apache projects from the Technical Debt Dataset V2.

**Why the difference.** Running SonarQube and Ptidej on 1,000 arbitrary repositories would require weeks of compute and manual QA. The Technical Debt Dataset (Lenarduzzi et al. 2019) represents the standard scale used in the published literature. The 2024 systematic review (Ajibode et al.) found most published TD studies use between 5 and 50 projects.

**What we concede in the notebook.** Scale is constrained by the chosen data source. The 31-project corpus matches the scale of peer-reviewed work in this area.

---

## 6. Multi-Project Generalization of Fault Prediction

**What we initially observed.** The fault-inducing predictor trained on 30 projects scored AUC 0.88 on a random train-test split of those 30 projects, but with the original snapshot-only features it scored near-random on held-out commons-io. This is the classic cross-project generalization problem (Zimmermann et al. 2009).

**How we addressed it.** Added churn features (files changed, lines added, lines removed, derived churn ratio) based on Mockus and Votta (2000) and Nagappan and Ball (2005). With churn features, the top-10 most likely fault-inducing commits in held-out commons-io match actual fault-inducing commits 80% of the time.

**What remains.** Precision at the default 0.5 threshold on commons-io is 0.48, with recall 0.63. The model is stronger as a ranker (for prioritization) than as a binary classifier. We use the probability score for ranking in Section 5, which is what the downstream pipeline actually needs.

**What we concede in the notebook.** The model is positioned as a ranker, not a binary classifier. Cross-project transfer is explicitly discussed as a known challenge in the field.

---

## 7. Agent Throughput

**What the notebook demonstrates.** The agent processes one candidate at a time in roughly 30 seconds per inference on CPU.

**What the agent cannot do today.** Process multiple candidates in a single notebook run. When we tried to process 5 samples back to back, the second sample triggered an out-of-memory kill inside the Docker container (Colima's default memory budget).

**Why the difference.** Each inference allocates activation buffers for Qwen-Coder-0.5B. Without batching or more container memory, the allocations accumulate past the container's ceiling.

**What we concede in the notebook.** The pipeline demo runs the agent on one prioritized candidate. Batching or multi-call runs are identified as future work that would require either increased container memory, gradient checkpointing, or true batched inference.

---

## 8. Exact-Match Generation Rate

**What the notebook shows.** The agent produces valid Java in 99% of cases and achieves high BLEU against ground truth. Exact match against the developer's actual fix is rare, under 1% at the 0.5B model size.

**Why.** This is the known behavior of code-generation LLMs at this size. The benchmark (Section 7) confirms Qwen-Coder-0.5B gets 0.6% exact match on 1000 CodeXGLUE pairs; the winning 3B model gets 7.9%. The literature (Tufano et al. 2019) shows exact match rates on CodeXGLUE are historically low across all model families.

**What we concede in the notebook.** Exact match is not a realistic headline metric at this scale. BLEU, syntactic validity, and confidence tiering are reported instead. The benchmark's full leaderboard gives the honest picture of what can be achieved with different model choices.

---

## 9. Language Scope

**What the README implies.** A broadly applicable system ("across codebases").

**What we deliver.** A pipeline that operates on Java specifically, since the TD Dataset is Java-only and CodeXGLUE is Java-only. The API notebook uses Python for pedagogical clarity, the Example notebook uses Java for the pipeline demo.

**Why the difference.** The quantification and prioritization stages depend on the TD Dataset (Java). The benchmark corpus is Java. Extending to other languages would require either a multi-language dataset or rebuilding the feature pipeline from raw static analysis on a non-Java codebase.

**What we concede in the notebook.** The pipeline is language-agnostic in structure but Java-specific in implementation. Python, C, or JavaScript would need different static analysis tools (radon, cppcheck, ESLint respectively) but the ML and agent layers would remain.

---

## Summary Table

| Item | What README asks | What we deliver | Impact on notebook |
|------|------------------|-----------------|---------------------|
| Debt categories | 4 named types | SonarQube's 3 types (no outdated deps) | Named as limitation |
| Impact regression | Velocity, bugs, dev time | Bugs only | Named as limitation |
| Test-coverage validation | Run test suites | CodeXGLUE ground-truth match | Named as future work |
| Feedback loop | Yes | No | Named as future work |
| Repository scale | 1,000+ | 31 (TD Dataset) | Explained via literature |
| Cross-project generalization | Implicit | Churn features fix it | Strengthens the work |
| Agent throughput | Implicit | One candidate per run | Named as future work |
| Exact match rate | Implicit | <1% (consistent with literature) | Framed via benchmark |
| Language scope | Broad | Java-specific | Explained in intro |

---

## How this list is used

When writing Section 8 of the Example notebook ("Synthesis and Limitations"), each row above becomes one or two sentences. The list is also useful for the README.md, the video script, and any questions from the grader or TA that start with "did you consider...".

The goal is not to hide these tradeoffs. It is to state them up front so the reader understands what was chosen and why.
