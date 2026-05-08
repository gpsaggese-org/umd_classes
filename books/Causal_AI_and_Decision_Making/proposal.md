# Book Proposal: _From Prediction to Decision: Causal AI for Machine Learning Practitioners_

**Proposed book title:** From Prediction to Decision: Causal AI for Machine Learning
Practitioners

**Subtitle:** Building Explainable, Robust Decision Systems with Causal Reasoning and
Agents

**Author(s):** Dr. GP Saggese

**Author title(s) and affiliation(s):**

- Adjunct Professor, University of Maryland, College Park, MD
  - DATA605: Big Data Systems
  - MSML610: Advanced Machine Learning
- Founder & CTO, Causify AI (causify.ai)

**Phone number:** +1-408-431-1286

**Preferred email address(es):** gsaggese@umd.edu, gp@causify.ai

**Author nationality:** United States of America, Italy

**Date submitted:** March 2026

## About the Author

**Biography (for Amazon/back cover):**

Dr. Giacinto Paolo (GP) Saggese is an engineer, researcher, and entrepreneur with
20+ years of experience building machine learning and AI systems across academia,
research laboratories, and industry. He holds a PhD and PostDoc from the
University of Illinois at Urbana-Champaign and has worked as a research scientist
at NVIDIA, Synopsys, Teza, and Engineers' Gate. As an Adjunct Professor at the
University of Maryland, he teaches graduate courses on big data systems and
advanced machine learning, and has trained over 1,000 students in modern data
architecture and machine learning. Dr Saggese is the founder and CTO of Causify
AI, an AI-powered platform for quantitative research. Before Causify, he founded
ZeroSoft and June, two VC-backed startups, both acquired. Dr Saggese has
published more than 40 papers on machine learning, and data systems design, and
holds 4 US patents.

**LinkedIn profile:** linkedin.com/in/gpsaggese

**Public speaking samples:**

- [University of Maryland MSML610 Video Lectures](https://drive.google.com/drive/folders/1wdetoWxD1475S1wzFOT-ZnKNzb2EwU8b)

## 1. Overview

Most machine learning practitioners are trained to optimize prediction accuracy.
Yet prediction and decision-making are fundamentally different: a model that
predicts accurately can still recommend harmful or ineffective actions if it
ignores causality. Practitioners routinely encounter problems that prediction
alone cannot solve, such as inferring the effect of an intervention, explaining
why a model made a decision, identifying root causes of failures, or optimizing a
business decision under uncertainty.

_From Prediction to Decision_ bridges this gap. It gives data scientists, ML
engineers, and machine learning practitioners a rigorous, hands-on guide to
causal reasoning and decision-making. The book moves beyond predictive modeling
to show readers how to build explainable, robust decision systems grounded in
causal inference. It covers fundamental causal methods (DAGs, adjustment, IVs,
RCTs), estimation techniques (propensity scores, causal forests), decision-making
under uncertainty, autonomous agents that reason causally, and real-world
applications from marketing optimization to healthcare.

The book grew out of MSML610: Advanced Machine Learning, a graduate course at
the University of Maryland, and from hands-on work building causal inference
systems at Causify AI. Every chapter pairs conceptual grounding with working
code in Docker-containerized environments and real-world case studies.

## 2. Why This Book? Why Now?

### The Market Gap

Existing ML books teach prediction. Existing causal inference books are written
for econometricians and statisticians, requiring advanced mathematics. No book
currently bridges the gap: how to apply causal reasoning and decision theory
systematically to real-world ML problems, in a language practitioners
understand, with working code and case studies.

### Why Now

- **Causal reasoning has moved from academia to industry.** Companies like Uber,
  LinkedIn, and Netflix now employ causal inference at scale for decision-making.
  Practitioners need a guide to implement these methods without a PhD in
  econometrics or advanced statistics.
- **Prediction-only systems are failing.** Simpson's paradox, policy reversals,
  and distribution shift confound practitioners who rely solely on predictive
  accuracy. Causal models offer a principled alternative.
- **Explainability demands require causality.** Regulations (EU AI Act, GDPR,
  fair lending) require explaining decisions and demonstrating non-discrimination.
  Post-hoc explanation techniques are insufficient; causal reasoning is necessary.
- **LLM-powered agents need reasoning.** Large language models can execute tools
  but lack true causal reasoning. Integrating causal inference into agent
  architectures is the frontier of trustworthy AI.

## Marketing Description

_From Prediction to Decision_ shows you how to apply causal reasoning to build ML
systems that actually work in the real world. Written for practicing data
scientists and ML engineers who have encountered confounding, distribution shift,
or policy reversals, this book pairs causal theory with hands-on code and
real-world case studies. You'll learn to estimate causal effects, design
experiments, make robust decisions under uncertainty, and build autonomous agents
that reason causally. Whether you're optimizing marketing campaigns, improving
healthcare outcomes, or building trustworthy AI, you'll gain the understanding
and tools to move beyond prediction to principled decision-making.

## 3. Target Audience

**Audience Level:** Intermediate to Advanced

### Primary Audience

**Practicing data scientists and ML engineers** with 2+ years of experience who
know how to build predictive models but have encountered real-world problems
that prediction alone cannot solve: causal inference, model explainability,
fairness, or decision optimization. They understand Python, statistics, and
standard ML tools.

### Secondary Audiences

- **Quantitative analysts** in finance, marketing and other fields who use A/B
  testing and need deeper causal inference methods
- **Graduate students** in data science, statistics, or economics programs seeking
  practitioner-focused causal inference training
- **ML product managers** making decisions about model deployment and fairness
- **Researchers** in industry labs building trustworthy AI systems
- **Engineering managers** evaluating causal AI capabilities for their teams

## 4. What Readers Will Learn

By the end of this book, readers will be able to:

- Build and reason with causal directed acyclic graphs (DAGs) to model real-world
  phenomena
- Estimate causal effects from observational data using adjustment, propensity
  scores, and advanced methods
- Design and analyze A/B tests, RCTs, and other experiments with statistical rigor
- Apply causal inference to explain model predictions and identify root causes
- Make robust decisions under uncertainty using Bayesian decision theory
- Build machine learning systems that are fair, interpretable, and robust to
  distribution shift
- Construct autonomous agents that reason causally and execute interventions safely
- Validate causal assumptions and assess sensitivity to unmeasured confounding
- Apply causal methods to real problems: pricing, targeting, healthcare, operations

## 5. Competitive Analysis

| Title | Publisher | Year | ISBN | Gap This Book Fills |
| :---- | :-------- | :--- | :--- | :------------------ |
| _Book of Why_ (Pearl & Mackenzie) | Basic Books | 2018 | 978-0465097616 | Excellent theory but no practical ML code or implementation for practitioners |
| _Causal Inference: The Mixtape_ (Cunningham) | Self-published | 2021 | — | Written for economists; heavy econometric focus, not ML/data science |
| _Hands-On Machine Learning_ (Géron) | O'Reilly | 2022 | 978-1098125974 | Focuses on prediction; no causal reasoning or decision-making |
| _Interpretable Machine Learning_ (Molnar) | Self-published | 2022 | — | Post-hoc explanation only; conflates explainability with causality |
| _Designing ML Systems_ (Huyen) | O'Reilly | 2022 | 978-1098107963 | Strong MLOps framing but minimal causal inference or decision theory |
| _The Book of Statistical Proof_ (Alcock) | Cambridge | 2021 | — | Academic focus on statistics; not accessible to ML practitioners |

**Unique position:** The only title that bridges causal inference theory and
practical ML engineering, written for data scientists and ML practitioners, with
working code, real-world case studies, and decision-making frameworks throughout.

## 6. Keywords

- Causal inference for machine learning
- Decision-making under uncertainty
- Causal DAGs and structural models
- Treatment effect estimation
- Propensity scores and matching
- Causal forests and heterogeneous effects
- A/B testing and experimentation
- Explainability and fairness
- Bayesian decision theory
- Causal reasoning in AI agents
- Counterfactual reasoning
- Observational vs. experimental inference
- Sensitivity analysis and unmeasured confounding
- Causal discovery algorithms
- Real-world applications: marketing, healthcare, operations

## 7. Table of Contents

_(Estimated length: ~500 pages / ~125,000 words. 15 chapters organized into 
3 parts, plus preface and 4 appendices.)_

Each chapter contains detailed examples with supporting Jupyter notebook
showing how to apply causal AI techniques to concrete real-world problems.

### Preface

- Who this book is for
- How to use this book
- Setting up the lab environment (Docker + Python + causal inference libraries)
- What prior knowledge you need
- Conventions used

### Part I: Understanding Causality

#### Chapter 1: From Prediction Pipelines to Decision Pipelines (~35 Pages)

Why ML practitioners need to think causally.

**1.1 The Problem: When Prediction Fails** — Simpson's paradox, policy reversals,
and distribution shift. Real-world examples where accurate prediction led to 
wrong decisions.

**1.2 What ML Systems Can and Cannot Tell You** — The limits of prediction.
Optimization vs. inference vs. decision theory. The gap between correlation 
and causation.

**1.3 The Ladder of Causation** — Observational, interventional, and counterfactual
levels. What each level can answer. How to recognize which level a problem requires.

**1.4 Data Science vs. Decision Science** — Shifting mindsets from "what will happen?" 
to "what should we do?" Business context and decision frameworks.

**1.5 Tools and Tutorials** — TUTORIAL: Introduction to causal DAGs using real-world
examples (marketing, healthcare, operations).

#### Chapter 2: Bayesian Networks and Probabilistic Reasoning (~35 Pages)

Logic-based AI under uncertainty.

**2.1 Probability and Conditional Independence** — Foundations. Joint distributions,
Bayes' rule, conditional independence as a path to tractable inference.

**2.2 Bayesian Networks** — Semantics and structure. How graphs encode independence
assumptions. D-separation and the role of conditioning.

**2.3 Constructing a Bayesian Network** — Working with domain experts. Building 
directed graphs from causal assumptions.

**2.4 Exact and Approximate Inference** — Variable elimination, belief propagation.
When to use sampling methods. Computational complexity.

**2.5 Tools and Tutorials** — TUTORIAL: Implementing Bayesian Networks in PyMC.
Inference and posterior predictions.

#### Chapter 3: Causal DAGs and Structural Models (~40 Pages)

From graphs to causal reasoning.

**3.1 Causal vs. Observational Graphs** — The critical distinction. Why association
is not causation. Adding causal arrows.

**3.2 Structural Causal Models** — Equations and noise terms. From DAGs to SCMs.
Variables: observed, unobserved, endogenous, exogenous.

**3.3 Special Variable Types** — Mediators, moderators, confounders, colliders,
and collider bias. How each affects inference.

**3.4 Building Causal DAGs from Domain Knowledge** — Identifying variables,
relationships, and assumptions. When you're uncertain about structure.

**3.5 Tools and Tutorials** — TUTORIAL: Building and visualizing causal DAGs.
Working with domain experts to validate structure.

#### Chapter 4: From Causal Models to Code (~40 Pages)

Probabilistic programming and decision-making.

**4.1 Bayesian Inference in Practice** — Posterior inference using PyMC. MCMC
and variational inference. Diagnostics and convergence.

**4.2 Generalized Linear Models** — Logistic, Poisson, and survival models in
a Bayesian framework. Regularization and priors.

**4.3 Hierarchical Models** — Partial pooling and structured data. When and why
to use hierarchical structures.

**4.4 Posterior-Based Decisions** — From beliefs to actions. Decision rules and
expected utility. Sensitivity to prior assumptions.

**4.5 Tools and Tutorials** — TUTORIAL: Posterior workflows in PyMC. Model
comparison and validation.

### Part II: Estimating Causal Effects

#### Chapter 5: Interventions, Experiments, and Adjustments (~40 Pages)

From observation to causal effect estimation.

**5.1 Interventions and Counterfactuals** — What if we intervene? Causal effects
as contrasts. The do-operator.

**5.2 Randomized Controlled Trials** — Why randomization breaks confounding.
RCT design and analysis. When RCTs are not feasible.

**5.3 Observational Adjustment** — Back-door paths and confounding. The 
back-door criterion. Valid adjustment sets.

**5.4 Do-Calculus** — Complete framework. Three rules. When estimation is 
impossible. Using do-calculus to derive adjustment formulas.

**5.5 Tools and Tutorials** — TUTORIAL: Using DoWhy for causal inference. 
Refutation methods to validate assumptions.

#### Chapter 6: Causal Identification and Estimation (~45 Pages)

Practical methods for estimating effects from observational data.

**6.1 The Identification Problem** — When can we estimate causal effects?
Causal sufficiency, positivity, consistency, SUTVA.

**6.2 Classical Strategies** — Instrumental variables and natural experiments.
Regression discontinuity design. Difference-in-differences.

**6.3 Matching and Propensity Scores** — Matching as adjustment. Propensity 
score methods: matching, stratification, IPW. Doubly robust estimation.

**6.4 Modern Causal Forests** — Learning heterogeneous treatment effects at scale.
S/T/X/R-learners. When to use which approach.

**6.5 Sensitivity to Unmeasured Confounding** — Rosenbaum bounds and E-values.
When estimates are robust.

**6.6 Case Study: Healthcare Treatment Effects** — Workflow: DAG → method selection
→ robustness checks. When estimates differ and why.

**6.7 Tools and Tutorials** — TUTORIAL: EconML and CausalML for effect estimation.
DoWhy for end-to-end causal analysis.

#### Chapter 7: Explainability and Causal Attribution (~40 Pages)

Explaining predictions using causal reasoning.

**7.1 Explanation vs. Causality** — Post-hoc explanation and its limits.
When explainability is sufficient and when you need causality.

**7.2 Explanation Methods** — Feature importance, SHAP, LIME. Correct interpretation
and common pitfalls.

**7.3 The Critical Gap** — Feature importance is not causality. Correlation 
masquerades as contribution. Why post-hoc explanations mislead.

**7.4 Causal Attribution** — Counterfactual explanations. Causal SHAP values.
Actionable recourse: what to change to affect outcomes.

**7.5 Decision Support** — Using explainability to identify potential causal
relationships. From "what does the model rely on?" to "what should we intervene on?"

**7.6 Tools and Tutorials** — TUTORIAL: SHAP and LIME. DiCE and DoWhy for 
causal explanations.

#### Chapter 8: Causal Inference for Time Series (~40 Pages)

Causality with temporal structure.

**8.1 Time Series vs. Cross-Sectional Causality** — Temporal causal structures.
When temporal structure helps and when it misleads.

**8.2 Granger Causality** — Definition and intuition. Assumptions and limitations.
Practical examples.

**8.3 Interrupted Time Series** — Design and estimation. ITS and regression
discontinuity. Applications.

**8.4 Difference-in-Differences** — Parallel trends assumption. Multiple time
periods. Extensions.

**8.5 Synthetic Control Methods** — Constructing counterfactuals. When synthetic
control succeeds and fails.

**8.6 Tools and Tutorials** — TUTORIAL: CausalImpact for Bayesian interrupted
time series. CausalPy for DiD and synthetic control.

#### Chapter 9: A/B Testing and Experimentation (~35 Pages)

Designing and analyzing randomized experiments.

**9.1 Randomization as Causal Identification** — Why randomization breaks
confounding. Causal graphs of experiments.

**9.2 A/B Test Design** — Power analysis and sample size. Multiple testing
corrections. Heterogeneous effects.

**9.3 Beyond Standard A/B Tests** — Switchback experiments. Multi-armed bandits.
When A/B testing fails.

**9.4 Sequential Decision-Making** — Value of information. Thompson sampling.
Bayesian optimization for experimentation.

**9.5 Tools and Tutorials** — TUTORIAL: CausalML for A/B test analysis.
CausalPy for Bayesian experiment design.

#### Chapter 10: Causal Discovery (~35 Pages)

Inferring causal structure from data.

**10.1 When Discovery Works and When It Doesn't** — Assumptions required. 
Identifiability and causal sufficiency. Practical limitations.

**10.2 Discovery vs. Domain Knowledge** — Discovery as hypothesis generation.
Using partial information to constrain search.

**10.3 Discovery Algorithms** — Constraint-based methods (PC, FCI). Score-based
methods (GES, NOTEARS). Non-Gaussian methods (LiNGAM).

**10.4 Validation and Refutation** — Why standard ML fails. Domain expert review.
When discovery should change your DAG.

**10.5 Tools and Tutorials** — TUTORIAL: causal-learn for constraint and 
score-based discovery. LiNGAM for non-Gaussian structures.

### Part III: Making Decisions with Causality

#### Chapter 11: Decision-Making with Causal Models (~40 Pages)

From inference to action.

**11.1 Prediction Is Not Enough** — Prediction pipelines vs. decision pipelines.
Causal models as the foundation for decisions.

**11.2 Foundations of Decision Theory** — Utility functions and expected utility.
Causal interventions and outcomes. Risk preferences.

**11.3 Influence Diagrams** — Adding decisions and utility nodes to causal DAGs.
Solving influence diagrams. Optimal policies.

**11.4 Bayesian Decision-Making** — Posteriors to optimal actions. Prior elicitation.
Iterative refinement of decisions.

**11.5 Uncertainty in Decisions** — Aleatoric and epistemic uncertainty.
Communicating uncertainty to stakeholders.

**11.6 Tools and Tutorials** — TUTORIAL: PyMC for causal inference and posterior-
based decisions. BoTorch for Bayesian optimization.

#### Chapter 12: Causal Reinforcement Learning (~40 Pages)

Learning robust policies from causal structure.

**12.1 Why Standard RL Fails** — MDPs assume no confounding. Distribution shift.
When RL produces brittle policies.

**12.2 Causal Dynamics Models** — Learning causal transition models. Model-based
RL with causal structure. Generalization and transfer.

**12.3 Offline RL and Confounding** — Learning from logged data. Addressing
confounding. Off-policy evaluation with causal adjustments.

**12.4 Policy Learning with Heterogeneous Effects** — Learning policies from
causal effect estimates. Counterfactual policy evaluation.

**12.5 Tools and Tutorials** — TUTORIAL: gymnasium for RL environments.
d3rlpy for offline RL with causal considerations.

#### Chapter 13: Forecasting Under Causal Intervention (~35 Pages)

Valid predictions when the world changes.

**13.1 Why Standard Forecasting Breaks** — Assumption of stationarity.
Structural breaks and regime changes. When past patterns fail.

**13.2 Causal Constraints on Forecasts** — Using causal models to validate
forecasts. Forecasting under new policies.

**13.3 Bayesian Forecasting with Causal Models** — Generating forecasts from
posterior causal models. Propagating uncertainty. Posterior predictive checks.

**13.4 Spillover Effects** — Joint distributions under intervention.
Indirect consequences. Multivariate causal forecasts.

**13.5 Tools and Tutorials** — TUTORIAL: PyMC for posterior predictive 
validation. Prophet with causal structure.

#### Chapter 14: Causal Decision Making in Practice (~40 Pages)

Real-world applications and workflows.

**14.1 From Learning to Deployment** — Bridging causal inference and business
decisions. When prediction fails: Simpson's paradox and policy reversal.

**14.2 Policy Learning and Optimization** — Learning optimal policies. Heterogeneous
effects and targeting. Uplift and personalization.

**14.3 Real-World Applications** — Marketing: targeting with causal uplift models.
Healthcare: treatment guidelines from observational data. Operations: resource
allocation. Pricing: demand under causal dynamics. HR: hiring and retention.

**14.4 Validation and Continuous Learning** — A/B testing policy recommendations.
Off-policy evaluation before deployment. Monitoring assumptions. Iterative
improvement.

**14.5 Case Studies** — End-to-end workflows from problem definition to
monitoring.

**14.6 Tools and Tutorials** — TUTORIAL: DoWhy for policy evaluation.
EconML for policy optimization and uplift.

#### Chapter 15: Causal Reasoning in AI Systems (~35 Pages)

Building trustworthy autonomous agents.

**15.1 LLMs and Causal Reasoning** — Where LLMs excel and fail. Pattern matching
vs. causal reasoning. Robustness and out-of-distribution failures.

**15.2 Enhancing LLM Reasoning** — Chain-of-thought prompting for structured
reasoning. Connecting LLMs to causal frameworks. Tool use and integration.

**15.3 Causal Agent Architectures** — Agents with explicit causal models.
Integrating causal inference into planning. Planning under causal uncertainty.

**15.4 Trustworthy AI Through Causality** — Transparency. Robustness.
Fairness. Safety.

**15.5 Tools and Tutorials** — TUTORIAL: LangChain + DoWhy for causal reasoning.
ReAct with causal structure. LlamaIndex for knowledge-grounded reasoning.

### Appendices

**Appendix A:** Lab Environment Setup — Installing Docker, Python, and causal
inference libraries on Mac, Linux, and Windows.

**Appendix B:** Causal Inference Tool Reference — Quick reference for DoWhy,
EconML, CausalML, causal-learn, LiNGAM.

**Appendix C:** Statistical Reference — Common distributions, hypothesis testing,
power analysis, and sensitivity analysis formulas.

**Appendix D:** Datasets and Case Study Data — Where to find public datasets for
causal inference. Setting up case study data in Docker.

## 8. Other Book Features

### GitHub Repository

- **Primary repository:** All code organized by chapter with Docker Compose
  configurations for reproducible lab environments
- Real-world datasets and case studies included
- Jupyter notebooks with step-by-step causal inference workflows
- Licensed under MIT for broad reusability

### O'Reilly Sandboxes

- Pre-configured Docker environments for each chapter's hands-on labs
- Causal inference libraries pre-installed (DoWhy, EconML, PyMC, causal-learn)
- Interactive Jupyter notebooks for causal reasoning tutorials
- Real-world datasets for practice and experimentation

## 9. Software Dependencies

1. **Python** — Target Python 3.11+
2. **Causal inference libraries** — DoWhy, EconML, CausalML, causal-learn, LiNGAM
3. **Probabilistic programming** — PyMC (inference, posterior workflows)
4. **ML libraries** — scikit-learn, pandas, PyTorch (as needed)
5. **Visualization** — graphviz, networkx, matplotlib, seaborn
6. **Data libraries** — numpy, scipy, statsmodels (hypothesis testing)
7. **Docker** — Docker 24+ with Docker Compose v2

## 10. Suggested Technical Reviewers

To be completed with acquisitions editor.
I have several university colleagues who I can recommend.

## 11. Sample Material

- Class repo:
  https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610
- Class slides:
  https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/lectures
- Class hands-on tutorials:
  https://github.com/gpsaggese/gpsaggese.github.io/tree/master/msml610/tutorials
- Class videos:
  https://drive.google.com/drive/folders/1wdetoWxD1475S1wzFOT-ZnKNzb2EwU8b

## 12. Production Details

| Parameter | Detail |
| :-------- | :----- |
| **Estimated length** | ~500 pages / ~125,000 words |
| **Chapter count** | 15 chapters + preface + 4 appendices |
| **Code examples** | Python throughout |
| **Lab environment** | Docker + Docker Compose (fully reproducible) |
| **Figures/diagrams** | ~100–120 (causal DAGs, decision trees, workflow diagrams) |
| **Jupyter notebooks** | Companion notebooks for each chapter with real data |
| **Case studies** | 5–8 end-to-end applications (marketing, healthcare, operations) |
| **Proposed delivery** | First draft: 12 months from contract |

## 13. Delivery Schedule

| Milestone | Target Date |
| :-------- | :---------- |
| Two draft chapters (Chapters 1–2) | Month 3 |
| Half draft manuscript (Chapters 1–7) | Month 6 |
| Full draft manuscript ready for tech review | Month 10 |
| Final manuscript incorporating tech review | Month 12 |
| Companion code and notebook finalization | Month 12.5 |

## Author Nationality Disclosure Form

I hereby declare that I am a national of the United States of America and Italy.

**Signature:** __________________________________________

**Date:** ________________________
