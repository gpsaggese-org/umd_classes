# Automating Data Science with Coding AI

## 0: Coding AI

### The ML Development Lifecycle
- How the 10 steps in this book map to a real project timeline, from raw data
  to production model
- Where AI coding tools apply at each stage:
  - generating ingestion scripts
  - scaffolding feature pipelines
  - writing eval harnesses
  - drafting deployment configs
- The "80% boilerplate, 20% judgment" split: AI handles repetitive structure,
  developers own problem framing and validation logic
- Cumulative time savings compound across the pipeline — small wins per step
  add up to days recovered per project

### The Evolution of AI Pair Programming
- Tracing the path from autocomplete and linting tools to today's context-aware
  coding agents, and what that trajectory suggests about where development
  workflows are headed
- Code completion & boilerplate generation (60-80% dev time savings)
- Key inflection points: GitHub Copilot (2021), ChatGPT code interpreter (2023),
  agentic CLI tools (2024–) — each shifted the unit of AI assistance from
  token → function → file → project

### Tooling Landscape
- IDE integrations: GitHub Copilot (inline completion), Cursor (repo-aware
  chat), Cline/Continue (open-source, self-hosted), Claude Code (CLI agent)
- CLI agents vs. IDE plugins: CLI agents run commands, edit files across the
  repo, and iterate autonomously; plugins operate within an open file
- LLM-powered code review tools: CodeRabbit, Sourcery, Amazon CodeGuru
- Comparison axes: context window size, autonomy level, cost per token, latency,
  privacy/data-residency requirements
- Choosing the right tool: inline suggestion for boilerplate, chat for
  exploration, CLI agent for multi-file refactors and end-to-end tasks

### Prompting for Code
- Communicating Intent to a Model
- How to write effective specifications and prompts that translate fuzzy human
  requirements into precise, working code, including patterns for iterative
  refinement
- **Prompt patterns:**
  - Zero-shot: describe the task directly when it is self-contained
  - Few-shot: supply 1–3 input/output examples for non-obvious formats
  - Role prompts: "act as senior data engineer reviewing for performance issues"
  - Context injection: paste error tracebacks, table schemas, or sample rows
    directly into the prompt — models reason better with concrete data
  - Chain-of-thought: ask the model to reason step-by-step before writing code,
    especially for algorithmic or mathematical problems
  - Decomposition: break large tasks into atomic sub-prompts and compose the
    outputs; avoids hallucination cascades in long generations
- Iterative refinement loop: generate → run → paste error → regenerate; treat
  the first output as a draft, not a solution
- Specificity gradient: vague prompt → vague code; precise type signatures,
  expected behavior, and edge cases in the prompt → precise implementation

### Trust, Verification, and the New Code Review
- How developers should validate AI-generated code, the risks of silent bugs or
  security vulnerabilities, and how review practices need to adapt when a machine
  writes the first draft
- Bug detection via code review (pre-commit analysis)
- Documentation generation (docstrings, README sections)
- Explanation of complex concepts and error messages
- **Concrete verification techniques:**
  - Static analysis + AI review combo: run `ruff`, `mypy`, `bandit` as a
    mandatory post-generation step before reading the diff
  - Security scanning: treat AI-generated SQL, shell commands, and file paths as
    untrusted input; run `semgrep` or `bandit` automatically
  - Mutation testing: verify AI-written tests actually catch bugs by mutating
    the source and checking test failures
  - Ask the model to explain its own code ("explain this function line by line")
    — gaps in explanation reveal gaps in correctness
  - Red-teaming: for data pipelines, feed adversarial inputs (nulls, empty
    frames, type mismatches) and confirm AI-generated code handles them

### Architecture of Code
- Modularity: keep functions small enough that AI can reason about them in a
  single context window; large functions produce lower-quality suggestions
- Type hints, docstrings, and contracts as AI communication protocol — a
  well-typed function signature is a specification the model reads and respects
- When to factor code vs. keep it inline: factor when a block is reused or
  independently testable; inline when factoring adds indirection with no gain
- Naming conventions that help AI understand intent: prefer descriptive names
  (`compute_revenue_by_cohort`) over abbreviations (`calc_rev`); AI generates
  better continuations from readable context
- File and module organization for data science repos: separate data loading,
  feature engineering, modeling, and evaluation into distinct modules so AI
  edits stay scoped and don't cross concern boundaries
- Documentation as a first-class artifact: write the docstring before the
  implementation; use it as a prompt to the AI for the function body

### Reproducibility Tracking
- Unit testing: AI-generated code should ship with AI-generated tests; prompt
  the model to write pytest cases covering happy path, edge cases, and
  error conditions in the same turn as the implementation
- Parameter logging: log every hyperparameter, random seed, and data version at
  experiment start so results can be reconstructed; use `mlflow.log_params()`
  or equivalent as a scaffold AI can fill in
- Experiment versioning: tag code commits to experiment runs; tools like MLflow,
  W&B, and DVC link artifacts to the exact code that produced them
- Reproducible environments: pin `requirements.txt` or `pyproject.toml` deps;
  AI can generate these from import lists but must be prompted to pin versions

### Agentic Workflows: From Snippets to Autonomous Tasks
- Examining tools that don't just suggest code but plan, execute, and
  self-correct across a whole codebase — what changes when AI can run commands,
  write files, and iterate on its own
- **How agents work:** read-eval-write loop — agent reads files, generates a
  plan, executes shell commands or edits, observes output, and iterates
- Tool use and function calling: agents are given tools (bash, file read/write,
  web search) as structured function calls; the model decides when and how to
  invoke them
- Multi-file refactoring: agentic tools (Claude Code, Cursor Composer, Copilot
  Workspace) can rename symbols, update imports, and restructure modules across
  a repository in a single session
- When agentic ≠ better: hallucination cascades (one bad assumption propagates
  across many files), high token cost for exploratory tasks, and risk of
  irreversible edits without human review
- Human-in-the-loop checkpoints: require explicit approval before destructive
  operations (file deletion, schema migration, force-push); treat agent output
  as a PR diff to review, not a final commit

### The Changing Role of the Developer
- What skills become more or less valuable when AI handles routine
  implementation: system design, taste, debugging intuition, and the judgment
  calls that remain distinctly human
- High-value skills post-AI: problem framing, architecture decisions, knowing
  when to stop (scope discipline), and reading AI output critically
- Skills that transfer: understanding of algorithms, data structures, and system
  behavior; you cannot catch AI errors without knowing what correct looks like
- New meta-skill: prompt engineering and agent orchestration — directing AI
  effectively is itself a learned craft with significant productivity leverage
- The taste gap: AI can write code that works but not code that fits; knowing
  what idiomatic, maintainable, and appropriately-scoped code looks like remains
  a human judgment

### Packaging Workflows in Skills
- Defining reusable prompt templates as "skills": a skill is a named,
  versioned prompt (or prompt + script) that encodes a repeatable workflow
- Skill anatomy: a SKILL.md file with goal, inputs, steps, and output spec;
  optionally paired with a shell or Python script the agent runs
- Skill libraries: organize by domain (coding, testing, data, deployment);
  name skills with `domain.action` convention (`coding.fix_type_hints`,
  `testing.reach_coverage`) for discoverability
- Encoding domain knowledge into persistent instructions: CLAUDE.md files
  (or equivalent) carry project-specific rules (naming conventions, forbidden
  patterns, required imports) that the AI reads at session start
- Composing skills into pipelines: chain skills sequentially for multi-step
  workflows (e.g., `notebook.create_outline` → `notebook.implement_outline` →
  `coding.fix_type_hints`) with outputs of one feeding inputs of the next
- Versioning and sharing: store skills in the repo under `.claude/skills/`;
  skills are code — they benefit from code review, tests, and change history

# Automating ML Steps

## 1: Problem Definition

- Translating Business Questions into ML Problems
- Defining Success Metrics and KPIs
- Understanding Constraints (Time, Budget, Data, Compute)
- Scoping the Solution and Managing Expectations
- Framing the Problem: Classification, Regression, Clustering, or Other

**Python Packages:** (Conceptual, no code packages required)

## 2: Data Collection

- Data Sources and Storage Systems
- APIs, Databases, and Query Optimization
- Sensor Data and Real-Time Streams
- Third-Party Data and External Datasets
- Data Governance and Privacy Considerations
- Building Data Pipelines

**Python Packages:** `pandas`, `sqlalchemy`, `psycopg2`, `pymongo`, `requests`, `aiohttp`, `pyspark`, `kafka-python`, `boto3`, `google-cloud-storage`

## 3: Data Cleaning & Preprocessing

- Identifying and Handling Missing Values
- Detecting and Removing Duplicates
- Outlier Detection and Treatment
- Standardizing Data Formats and Encoding
- Handling Categorical and Text Data
- Normalization and Scaling Techniques

**Python Packages:** `pandas`, `numpy`, `scikit-learn`, `missingno`, `outlier-utils`, `pyjanitor`, `fancyimpute`

## 4: Exploratory Data Analysis (EDA)

- Univariate Analysis and Distributions
- Bivariate and Multivariate Relationships
- Correlation and Covariance Analysis
- Visual Storytelling and Interpretation
- Hypothesis Formation and Statistical Testing
- Identifying Patterns, Anomalies, and Insights

**Python Packages:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `scipy`, `statsmodels`, `pandas-profiling`, `sweetviz`

## 5: Feature Engineering & Selection

- Creating New Features from Existing Data
- Encoding Categorical Variables
- Handling Time Series and Temporal Features
- Dimensionality Reduction Techniques
- Feature Scaling and Normalization
- Feature Selection Methods and Importance

**Python Packages:** `pandas`, `numpy`, `scikit-learn`, `featuretools`, `category-encoders`, `tsfresh`, `optuna`, `shap`

## 6: Data Splitting

- Train, Validation, and Test Set Strategy
- Cross-Validation Techniques
- Stratified and Time-Series Splits
- Class Imbalance and Sampling Strategies
- Avoiding Data Leakage
- Setting Up Evaluation Pipelines

**Python Packages:** `scikit-learn`, `imbalanced-learn`, `numpy`, `pandas`, `stratification-tools`

## 7: Model Selection & Training

- Understanding Algorithm Families
- Baseline Models and Benchmarking
- Hyperparameter Tuning and Grid Search
- Regularization and Preventing Overfitting
- Ensemble Methods and Stacking
- Training Workflows and Reproducibility

**Python Packages:** `scikit-learn`, `xgboost`, `lightgbm`, `catboost`, `tensorflow`, `torch`, `optuna`, `hyperopt`, `ray-tune`, `wandb`

## 8: Model Evaluation

- Classification Metrics (Accuracy, Precision, Recall, F1)
- Regression Metrics (RMSE, MAE, R²)
- Ranking and Recommendation Metrics (AUC, NDCG)
- Business-Oriented Metrics and ROI
- Ablation Studies and Feature Importance
- Error Analysis and Model Debugging

**Python Packages:** `scikit-learn`, `numpy`, `pandas`, `matplotlib`, `seaborn`, `shap`, `lime`, `eli5`

## 9: Deployment

- Model Packaging and Containerization
- API Development for Model Serving
- Batch Inference and Scheduled Jobs
- Embedded and Edge Deployment
- A/B Testing and Canary Releases
- Version Control and Model Registry

**Python Packages:** `fastapi`, `flask`, `gunicorn`, `mlflow`, `kubeflow`, `seldon-core`, `ray-serve`, `bentoml`, `docker`, `onnx`

## 10: Monitoring & Maintenance

- Production Performance Tracking
- Data Drift and Concept Drift Detection
- Model Retraining Strategies
- Incident Response and Debugging
- Continuous Improvement and Feedback Loops
- Stakeholder Reporting and Governance

**Python Packages:** `mlflow`, `evidently`, `whylabs`, `prometheus-client`, `airflow`, `dbt`, `grafana-api`, `pandas`, `numpy`
