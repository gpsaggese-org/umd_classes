# Project Limitations and Future Improvements

This document enumerates every place where our project scope does not fully match the literal text of the DATA605 project description, along with the reason and what we deliver instead. It also lists future improvements we identified but did not implement in the current iteration.

The document is intentionally explicit so that graders, TAs, and future team members can see where we chose to scope down and why.

---

## Part 1: Limitations

### 1. Debt Type Coverage

**What the README asks for.** Classification of four debt types: code complexity, outdated patterns, architectural violations, and performance bottlenecks.

**What we deliver.** Three-way classification into BUG, CODE_SMELL, VULNERABILITY (SonarQube's native categories).

**Why the difference.** The Technical Debt Dataset stores issues tagged with SonarQube's TYPE column, not the four categories the README names. Our parallel work (Track A in the teammate brief) addresses this by using SonarQube's SYSTEM_TAGS to produce a richer multi-category classifier. The README's four categories are a subset of the tag space SonarQube actually uses in production, so using the tag space directly gives a more faithful representation of debt than forcing a four-category mapping.

**What we concede in the notebook.** The primary pipeline uses the three-way SonarQube native classification. A parallel multi-tag classifier is under development and will be integrated in a follow-up iteration.

---

### 2. Impact Regression Targets

**What the README asks for.** Regression models that predict impact on team velocity, bug frequency, and development time.

**What we deliver.** Fault-inducing commit prediction, which addresses bug frequency. AUC 0.88 on training split, top-10 hit rate of 80% on held-out commons-io.

**Why the difference.**
- Team velocity in the software engineering sense (story points per sprint) requires sprint-level data the TD Dataset does not have. A commits-per-week proxy would be heavily confounded by team size and project phase, which we also do not have.
- Development time could be approximated as time between fault introduction and fault fixing, but this data is sparse in SZZ_FAULT_INDUCING_COMMITS and the proxy would be noisy.

**What we concede in the notebook.** Velocity and development time are named as future work. Bug frequency is what we deliver.

---

### 3. Test Coverage and Backward Compatibility Validation

**What the README asks for.** Autonomous agents that perform refactoring while maintaining test coverage and backward compatibility.

**What we deliver.** The agent generates refactorings. Validation uses three proxies: Java syntactic validity via javalang parser, exact match against CodeXGLUE ground-truth fixes when available, and BLEU score against ground truth. For real commons-io issues without ground truth, validation reduces to syntactic validity only.

**Why the difference.** Running actual JUnit test suites on refactored Apache Java code requires a full Java build environment (Maven, specific JDK versions, dependency resolution), per-project test suite execution, and correctly applying a small refactoring to the full file context. This is incompatible with the DATA605 requirement that the notebook run end-to-end via "Kernel > Restart & Run All" on a CPU-only MacBook Air inside Docker.

**What we concede in the notebook.** Test-based validation is explicitly named as future work. CodeXGLUE ground-truth match is substituted as the primary quality signal because it represents the fix a real developer actually committed, which is a stronger signal than tests passing in many cases.

---

### 4. Feedback Loop on Refactoring Outcomes

**What the README Tasks section asks for.** A feedback loop that tracks predicted versus actual impact of refactorings to improve model accuracy over time.

**What we deliver.** Nothing directly. The agent is single-shot.

**Why the difference.** Implementing this requires applying generated refactorings to the actual Apache Java codebase, running the codebase's test suite (same blocker as Limitation 3), tracking the refactoring across subsequent commits to measure whether the bug-prone signal went down, and retraining the impact predictor periodically with this feedback. Each step carries its own dependencies that exceed the scope of a single tutorial notebook.

**What we concede in the notebook.** Identified as the most substantial future work direction.

---

### 5. Repository Scale

**What the README Tasks section asks for.** Extraction of code metrics from 1,000+ open-source repositories.

**What we deliver.** Analysis across 31 pre-analyzed Apache projects from the Technical Debt Dataset V2. A parallel effort (Track B in the teammate brief) adds fresh SonarQube Community Build analysis on 5-10 additional Java projects.

**Why the difference.** Running SonarQube on 1,000 arbitrary repositories would require weeks of compute and manual QA. The Technical Debt Dataset represents the standard scale used in published work on technical debt research.

**What we concede in the notebook.** Scale is constrained by the chosen data source. The 31-project corpus matches the scale of peer-reviewed work in this area, and our parallel extraction effort on additional projects is documented as scope expansion.

---

### 6. Cross-Project Generalization of Fault Prediction

**What we initially observed.** The fault-inducing predictor trained on 30 projects scored AUC 0.88 on a random train-test split of those 30 projects, but with the original snapshot-only features it scored near-random on held-out commons-io. This is the classic cross-project generalization problem in defect prediction literature.

**How we addressed it.** Added churn features (files changed, lines added, lines removed, derived churn ratio) based on published work showing code change volume predicts faults better than static complexity alone. With churn features, the top-10 most likely fault-inducing commits in held-out commons-io match actual fault-inducing commits 80% of the time.

**What remains.** Precision at the default 0.5 threshold on commons-io is 0.48, with recall 0.63. The model is stronger as a ranker (for prioritization) than as a binary classifier. We use the probability score for ranking in Section 5, which is what the downstream pipeline actually needs.

**What we concede in the notebook.** The model is positioned as a ranker, not a binary classifier. Cross-project transfer is explicitly discussed as a known challenge in the field.

---

### 7. Agent Throughput

**What the notebook demonstrates.** The agent processes one candidate at a time in roughly 30 seconds per inference on CPU.

**What the agent cannot do today.** Process multiple candidates in a single notebook run. When we tried to process 5 samples back to back, the second sample triggered an out-of-memory kill inside the Docker container (Colima's default memory budget).

**Why the difference.** Each inference allocates activation buffers for Qwen-Coder-0.5B. Without batching or more container memory, the allocations accumulate past the container's ceiling.

**What we concede in the notebook.** The pipeline demo runs the agent on one prioritized candidate. Batching or multi-call runs are identified as future work that would require either increased container memory, gradient checkpointing, or true batched inference.

---

### 8. Exact-Match Generation Rate

**What the notebook shows.** The agent produces valid Java in 99% of cases and achieves high BLEU against ground truth. Exact match against the developer's actual fix is rare, under 1% at the 0.5B model size.

**Why.** This is the known behavior of code-generation LLMs at this size. The benchmark (Section 7) confirms Qwen-Coder-0.5B gets 0.6% exact match on 1000 CodeXGLUE pairs; the winning 3B model gets 7.9%. Research consistently shows exact match rates on CodeXGLUE are historically low across all model families at this scale.

**What we concede in the notebook.** Exact match is not a realistic headline metric at this scale. BLEU, syntactic validity, and confidence tiering are reported instead. The benchmark's full leaderboard gives the honest picture of what can be achieved with different model choices.

---

### 9. Language Scope

**What the README implies.** A broadly applicable system ("across codebases").

**What we deliver.** A pipeline that operates on Java specifically, since the TD Dataset is Java-only and CodeXGLUE is Java-only. The API notebook uses Python for pedagogical clarity, the Example notebook uses Java for the pipeline demo.

**Why the difference.** The quantification and prioritization stages depend on the TD Dataset (Java). The benchmark corpus is Java. Extending to other languages would require either a multi-language dataset or rebuilding the feature pipeline from raw static analysis on a non-Java codebase.

**What we concede in the notebook.** The pipeline is language-agnostic in structure but Java-specific in implementation. Python, C, or JavaScript would need different static analysis tools but the ML and agent layers would remain.

---

### 10. Static Analysis Data Extraction vs Integration

**What the README asks for.** Extract code metrics from 1,000+ repos using static analysis tools.

**What we deliver in the primary pipeline.** Metrics from the Technical Debt Dataset's 31 projects.

**What we deliver in parallel work (Track B).** Fresh SonarQube Community Build analysis on 5-10 additional Java projects, exported to disk and committed to the repository for future use.

**Why the extracted data is not integrated into the primary pipeline.** The Technical Debt Dataset used SonarQube accessed in May 2019 (version 7.7-7.8 era). Current SonarQube (version 10.x) uses an expanded ruleset that flags more issues per commit than the 2019-era ruleset. Directly concatenating new-analysis data with TD Dataset data would introduce rule-version drift that would confound model training. Integrating the new data properly requires either (a) reproducing the exact 2019 SonarQube environment, which is non-trivial, or (b) building a rule-version normalization layer, which is a research question in its own right. We chose to preserve the new data for future integration work rather than introduce noise into our current models.

**What we concede in the notebook.** The extraction task is fulfilled. The integration is documented as future work with a specific technical path forward.

---

### 11. Clean-Commit Coverage in Training Data

**What the fault predictor sees during training.** Every commit that has a SONAR_MEASURES row. 86% of those are labeled "not fault-inducing," which effectively makes them clean commits by our measurement criterion.

**What the training data does not include.** Commits in the project history that never got a SONAR_MEASURES row. These might be pure refactorings, documentation changes, or other non-code changes that did not trigger a new SonarQube analysis.

**Why this matters.** Our model predicts fault likelihood conditional on "a commit we can measure." Commits that SonarQube never ran on are invisible to us. For the pipeline this is fine because we are always scoring measurable commits. For research claims about the full commit stream, it is a real sampling bias.

**What we concede in the notebook.** Fault prediction is a conditional model, not a universal one.

### 12. Java Parser Limitation
Stage 4 metric computation uses javalang, which does not handle some Java 8+ features such as array constructor references (e.g., boolean[]::new). On commons-lang3, this causes 3 of 259 files to be skipped during metric aggregation. Fix: migrate metric computation to tree-sitter-java, which supports modern Java syntax fully. Verified that tree-sitter installs cleanly in the container; the migration is approximately 100-150 lines in production/lib/metrics.py. Deferred until after end-to-end pipeline is working.



---

## Part 2: Future Improvements

These are identified but not implemented in the current iteration. They are grouped by effort.

### High-value, low-effort (a few hours each)

**Expand SONAR_MEASURES feature set.** We tried adding 11 extra columns (violation counts, quality ratings, debt ratios, coupling metrics) to the fault predictor. Result: AUC barely moved (0.884 to 0.886), top-10 match dropped slightly (8 to 7), top-50 improved (30 to 36). Mixed. We reverted to the baseline. A more careful feature selection or interaction study might recover more signal. Worth revisiting with proper hyperparameter search.

**Multi-label rule-tag classifier.** Track A in the teammate brief delivers this. If executed well, it becomes an enhancement candidate for the primary pipeline.

### High-value, medium-effort (1-3 days each)

**REFACTORING_MINER integration.** The TD Dataset has a 362K-row REFACTORING_MINER table we never touch. Each row tells us "in commit X, someone did refactoring of type Y" (Extract Method, Rename Variable, Change Attribute Type, etc.). For fault prediction, this is strong signal: refactoring commits tend to fix bugs; heavy-churn non-refactoring commits tend to cause them. Adding binary "did any refactoring happen" or type-specific counts would likely improve both the fault predictor and the prioritization impact score.

**Time-aware cross-project validation.** Current fault predictor uses a random 80/20 split. A more honest evaluation uses temporal splits: train on commits through year X, test on year X+1. This matches how the model would actually be used.

**Agent batching.** Refactor the agent's inference loop to enable multi-candidate processing. Currently OOMs on second call. Fix would require either preallocating memory for multiple calls or using PyTorch's gradient checkpointing. Makes the Section 4 prioritization list actually feed through the agent.

### High-value, high-effort (3-7 days each)

**Fresh SonarQube extraction expansion.** Track B in the teammate brief delivers 5-10 new projects. A full-scale extension to 50+ new projects would take longer but would meaningfully approach the "1,000+" target.

**Test-coverage validation framework.** Set up Maven + JUnit in a Docker container. Pipeline: checkout commons-io at commit X, apply a proposed refactoring as a diff, run tests, report pass/fail. Unlocks real validation of agent outputs. Deliverable would be a separate tool that the Example notebook could optionally call for a subset of test cases.

**Feedback loop prototype.** Logging framework that tracks agent recommendations and outcomes. Simple version: log every agent call and whether the user accepted or rejected it. Analysis: compute agreement rates, identify systematically-bad recommendations, use that to retrain the priority model. Addresses README task bullet 6 directly.

### Speculative, long-effort (1-2 weeks each)

**Apache-repo-aware agent.** Currently the agent takes a Java method as input with no file context. A deeper version would fetch the actual source file around the flagged line from commons-io's git history, include that context in the prompt, and produce a fix that actually respects the surrounding code. Requires building a git-checkout-and-parse pipeline. Turns the CodeXGLUE demo into a production-quality system.

**Multi-language extension.** Add Python via radon + ast. Same pipeline, different static analysis tool. Demonstrates the architecture is language-agnostic in practice, not just in principle.

**Feedback-augmented model training.** Full closed loop: agent suggests, developer accepts/rejects, label gets written back, model retrains on accumulated data. Research-paper-level scope.

---

## Summary Table of Limitations

| Item | What README asks | What we deliver | Status |
|------|------------------|-----------------|--------|
| Debt categories | 4 named types | SonarQube's 3 types (multi-tag classifier in parallel) | Primary pipeline concedes; parallel work addresses |
| Impact regression | Velocity, bugs, dev time | Bugs only | Concedes velocity/dev-time |
| Test-coverage validation | Run test suites | CodeXGLUE ground-truth match | Future work |
| Feedback loop | Yes | No | Future work |
| Repository scale | 1,000+ | 31 + 5-10 from parallel work | Partial |
| Cross-project generalization | Implicit | Churn features address it | Strengthens the work |
| Agent throughput | Implicit | One candidate per run | Future work |
| Exact match rate | Implicit | <1% (consistent with literature) | Framed via benchmark |
| Language scope | Broad | Java-specific | Explained in intro |
| Static analysis extraction | 1,000+ repos | Extract + preserve approach | Partial, documented |
| Clean-commit coverage | Implicit | Conditional on SonarQube coverage | Documented |

---

## How this document gets used

- **In the notebook's Synthesis section:** each row becomes one or two sentences.
- **In the README.md:** summary table reproduced, pointing here for detail.
- **In the video:** verbally walked through in the limitations segment.
- **If a grader asks "did you consider X":** the answer is here.

The goal is not to hide these tradeoffs. It is to state them up front so the reader understands what was chosen and why.
