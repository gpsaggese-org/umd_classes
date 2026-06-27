# Automating Data Science with Coding AI: Table of Contents

- Audience: data scientists and ML practitioners

## Part 1: Foundations of AI-Assisted Development

### Chapter 1: the AI Coding Revolution
**Goal:** Understand how AI pair programming transforms the ML development
workflow and where AI assistance applies most effectively

- The ML Development Lifecycle
  - How the 10 steps map to a real project timeline from raw data to production
  - Where AI coding tools apply at each stage: ingestion scripts, feature
    pipelines, eval harnesses, deployment configs
  - The "80% boilerplate, 20% judgment" split: AI handles repetitive structure;
    developers own problem framing and validation logic

- The Evolution of AI Pair Programming
  - Tracing from autocomplete and linting tools to context-aware coding agents
  - Key inflection points: GitHub Copilot (2021), ChatGPT (2023), agentic CLI
    tools (2024+)
  - How the unit of AI assistance evolved: token -> function -> file -> project

- Tooling Landscape
  - IDE integrations: GitHub Copilot, Cursor, Cline/Continue, Claude Code
  - CLI agents vs. IDE plugins: autonomy levels and use cases
  - LLM-powered code review tools: CodeRabbit, Sourcery, Amazon CodeGuru
  - Choosing the right tool for your task

### Chapter 2: Prompting for Code
**Goal:** Master the patterns and techniques for communicating intent to models
so they generate precise, working code

- Communicating Intent to a Model
  - How to write effective specifications that translate fuzzy requirements into
    precise code
  - The specificity gradient: vague prompt yields vague code; precise type
    signatures and edge cases yield precise implementation

- Prompt Patterns
  - Zero-shot: describe self-contained tasks directly
  - Few-shot: supply 1–3 examples for non-obvious formats
  - Role prompts: "act as senior data engineer reviewing for performance"
  - Context injection: paste schemas, tracebacks, sample rows directly
  - Chain-of-thought: ask for step-by-step reasoning before code generation
  - Decomposition: break large tasks into atomic sub-prompts to avoid
    hallucination cascades

- Iterative Refinement Loop
  - Treat first output as a draft, not a solution
  - Run, observe, paste error, regenerate
  - How to refine until code works

### Chapter 3: Trustworthy AI Code
**Goal:** Validate AI-generated code to catch silent bugs, security
vulnerabilities, and logic errors before production

- Bug Detection and Verification
  - Static analysis combo: run `ruff`, `mypy`, `bandit` as mandatory
    post-generation steps
  - Security scanning for SQL, shell commands, and file paths: treat
    AI-generated code as untrusted input
  - Mutation testing: verify AI-written tests catch bugs by mutating the source
  - Ask the model to explain its own code line-by-line; gaps reveal correctness
    gaps

- Red-Teaming and Edge Cases
  - For data pipelines, feed adversarial inputs: nulls, empty frames, type
    mismatches
  - Confirm AI-generated code handles them without crashing or silent failure

### Chapter 4: Coding Architecture for AI
**Goal:** Design code structures that AI understands, reasons about, and
improves effectively

- Modularity and Context
  - Keep functions small enough that AI can reason about them in one context
    window
  - Large functions produce lower-quality suggestions

- Type Hints and Contracts
  - Type hints, docstrings, and contracts as the AI communication protocol
  - Well-typed function signatures are specifications the model reads and
    respects

- Naming and Organization
  - Naming conventions that help AI understand intent: prefer descriptive names
    over abbreviations
  - File and module organization: separate data loading, feature engineering,
    modeling, evaluation
  - AI edits stay scoped; changes don't cross concern boundaries

- Documentation as Specification
  - Write docstrings before implementation; use them as prompts to the AI
  - Documentation becomes a first-class artifact

### Chapter 5: Packaging Reusable Skills
**Goal:** Encode repeatable workflows as versioned, reusable skills that amplify
team productivity

- Anatomy of a Skill
  - Skill is a named, versioned prompt (or prompt + script) that encodes a
    repeatable workflow
  - A SKILL.md file with goal, inputs, steps, and output spec; optionally paired
    with shell or Python script

- Skill Libraries and Discovery
  - Organize by domain: coding, testing, data, deployment
  - Use `domain.action` naming convention for discoverability
  - Example: `coding.fix_type_hints`, `testing.reach_coverage`

- Encoding Domain Knowledge
  - CLAUDE.md files carry project-specific rules: naming conventions, forbidden
    patterns, required imports
  - AI reads them at session start

- Composing and Versioning Skills
  - Chain skills sequentially for multi-step workflows
  - Store skills in repo under `.claude/skills/`; skills benefit from code
    review, tests, change history

## Part 2: Building ML Systems

### Chapter 6: Framing the Problem
**Goal:** Translate business questions into well-scoped ML problems with clear
success metrics

- Translating Business Questions into ML Problems
  - Moving from "we need to predict X" to a precise problem statement
  - Classification, regression, clustering, or custom objectives

- Defining Success Metrics and KPIs
  - Choosing metrics that align with business impact, not just model accuracy
  - Business-oriented metrics and ROI

- Understanding Constraints
  - Time, budget, data availability, and compute resources
  - How constraints shape problem scope

- Scoping the Solution and Managing Expectations
  - Setting realistic baselines and MVP definitions
  - When to build incrementally vs. upfront design

### Chapter 7: Data Collection and Loading
**Goal:** Design and implement robust data pipelines that ingest from diverse
sources

- Data Sources and Storage Systems
  - Databases, APIs, real-time streams, sensor data, third-party datasets
  - Evaluating data quality at the source

- Building Data Pipelines
  - Query optimization for large datasets
  - API clients and async patterns for concurrent requests
  - Streaming ingestion with Kafka or equivalent
  - Error handling and retry logic

- Data Governance and Privacy
  - Compliance requirements: GDPR, CCPA, HIPAA, and domain-specific regulations
  - Anonymization and access controls
  - Audit trails for data lineage

### Chapter 8: Cleaning and Preparing Data
**Goal:** Transform raw data into usable form through systematic cleaning and
standardization

- Identifying and Handling Missing Values
  - Detecting missingness patterns
  - Imputation strategies: deletion, mean/median, forward-fill, modeling

- Detecting and Removing Duplicates
  - Exact and fuzzy duplicates
  - Reconciling duplicate records

- Outlier Detection and Treatment
  - Statistical and domain-based outlier detection
  - Removal vs. transformation strategies

- Standardizing Data Formats and Encoding
  - Date/time normalization, timezone handling
  - Character encoding and text normalization
  - Unit conversions

- Handling Categorical and Text Data
  - Encoding categorical variables: label, one-hot, ordinal
  - Text preprocessing: tokenization, stemming, lemmatization

- Normalization and Scaling Techniques
  - StandardScaler, MinMaxScaler, and robust scaling
  - When to apply scaling and why it matters for different models

### Chapter 9: Exploratory Data Analysis
**Goal:** Develop deep understanding of data through systematic exploration and
hypothesis testing

- Univariate Analysis and Distributions
  - Summary statistics, histograms, density plots
  - Identifying skewness and kurtosis

- Bivariate and Multivariate Relationships
  - Scatter plots, joint distributions
  - Interaction effects

- Correlation and Covariance Analysis
  - Pearson, Spearman, and Kendall correlations
  - Multicollinearity and its implications

- Visual Storytelling and Interpretation
  - Designing visualizations that reveal insights
  - Annotating findings for stakeholder communication

- Hypothesis Formation and Statistical Testing
  - Formulating and testing statistical hypotheses
  - A/B testing and experimental design basics

- Identifying Patterns, Anomalies, and Insights
  - Time series patterns and seasonality
  - Anomalies that signal data quality issues or business insights

### Chapter 10: Feature Engineering
**Goal:** Transform raw data into predictive signals through creative and
systematic feature creation

- Creating New Features from Existing Data
  - Polynomial and interaction features
  - Domain-specific feature creation aligned to business logic

- Encoding Categorical Variables
  - Target encoding, frequency encoding, and other advanced techniques
  - Handling high-cardinality features

- Handling Time Series and Temporal Features
  - Lag features, rolling window statistics
  - Seasonal decomposition
  - Calendar features (day of week, holidays)

- Dimensionality Reduction Techniques
  - PCA, t-SNE, and UMAP for exploratory analysis
  - When to reduce vs. when high dimensionality is acceptable

- Feature Scaling and Normalization
  - Preprocessing pipelines that avoid data leakage

- Feature Selection Methods and Importance
  - Correlation-based selection, permutation importance, SHAP
  - Iterative selection: forward, backward, recursive elimination

## Part 3: Production ML

### Chapter 11: Splitting Data Strategically
**Goal:** Design data splits that prevent leakage and enable reliable model
evaluation

- Train, Validation, and Test Set Strategy
  - The purpose of each split and typical proportions
  - Holdout strategies for different data regimes

- Cross-Validation Techniques
  - K-fold cross-validation and leave-one-out
  - When each approach is appropriate

- Stratified and Time-Series Splits
  - Maintaining class distribution in stratified splits
  - Forward-looking splits for time series data

- Class Imbalance and Sampling Strategies
  - Oversampling, undersampling, and synthetic data generation
  - Cost-sensitive learning approaches

- Avoiding Data Leakage
  - Common leakage patterns and how to detect them
  - Ensuring each split is independent

### Chapter 12: Model Selection and Training
**Goal:** Build, train, and tune models that generalize well to unseen data

- Understanding Algorithm Families
  - Linear models, tree-based models, neural networks, and specialized
    architectures
  - Algorithm properties: interpretability, scalability, sample efficiency

- Baseline Models and Benchmarking
  - Establishing simple baselines for performance comparison
  - When to use simple models vs. complex ones

- Hyperparameter Tuning and Grid Search
  - Grid search, random search, and Bayesian optimization
  - Cross-validation-based tuning

- Regularization and Preventing Overfitting
  - L1/L2 regularization, dropout, early stopping
  - Monitoring train/validation divergence

- Ensemble Methods and Stacking
  - Bagging, boosting, and voting
  - When ensembles improve beyond individual models

- Training Workflows and Reproducibility
  - Logging hyperparameters, random seeds, and data versions
  - Experiment versioning with MLflow, Weights & Biases
  - Reproducible environments with pinned dependencies

### Chapter 13: Model Evaluation and Debugging
**Goal:** Rigorously evaluate model performance and diagnose failure modes

- Classification Metrics
  - Accuracy, precision, recall, F1, ROC-AUC
  - Choosing metrics aligned to business goals

- Regression Metrics
  - RMSE, MAE, R², mean absolute percentage error
  - Interpreting residuals

- Ranking and Recommendation Metrics
  - AUC, NDCG, MAP
  - Relevance metrics for recommendation systems

- Business-Oriented Metrics and ROI
  - Converting model predictions to business impact
  - Cost-benefit analysis of prediction errors

- Ablation Studies and Feature Importance
  - Understanding which features drive predictions
  - SHAP values, permutation importance, and coefficient analysis

- Error Analysis and Model Debugging
  - Categorizing prediction errors by type
  - Finding patterns in failures
  - Iterating on problem framing or feature engineering

### Chapter 14: Deployment
**Goal:** Move trained models to production with robust serving and version
control

- Model Packaging and Containerization
  - Saving model artifacts and dependencies
  - Docker containerization for deployment

- API Development for Model Serving
  - Building REST APIs with FastAPI or Flask
  - Latency and throughput considerations
  - Input validation and error handling

- Batch Inference and Scheduled Jobs
  - Computing predictions over large datasets offline
  - Scheduling with Airflow or equivalent
  - Managing compute costs

- Embedded and Edge Deployment
  - Mobile and on-device models
  - Model compression and quantization
  - Hardware constraints and optimization

- A/B Testing and Canary Releases
  - Gradual rollout strategies
  - Measuring business impact before full deployment
  - Rollback procedures

- Version Control and Model Registry
  - Tracking model lineage: code, data, hyperparameters, artifacts
  - Model registries: MLflow, Hugging Face Model Hub
  - Versioning for reproducibility and rollback

### Chapter 15: Monitoring and Evolution
**Goal:** Maintain model performance in production and continuously improve as
data changes

- Production Performance Tracking
  - Instrumentation for latency, throughput, error rates
  - Real-time dashboards and alerting

- Data Drift and Concept Drift Detection
  - Monitoring input distributions for shifts
  - Detecting when model assumptions break down
  - Automated alerts and response triggers

- Model Retraining Strategies
  - Scheduling retraining: on-demand, periodic, or drift-triggered
  - Incremental learning vs. from-scratch retraining
  - Online learning for streaming data

- Incident Response and Debugging
  - Rapid diagnosis when model performance degrades
  - Root cause analysis: data quality, code bugs, distribution shift
  - Communication with stakeholders

- Continuous Improvement and Feedback Loops
  - Collecting ground truth labels from predictions in production
  - Iterating on features, models, and problem framing
  - Cost-benefit analysis of improvements

- Stakeholder Reporting and Governance
  - Translating model metrics to business impact
  - Compliance and regulatory reporting
  - Documentation for audits and governance
