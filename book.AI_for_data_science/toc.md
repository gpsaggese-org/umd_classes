# Table of Contents: AI for Data Science

## Chapter 1: Problem Definition

- Translating Business Questions into ML Problems
- Defining Success Metrics and KPIs
- Understanding Constraints (Time, Budget, Data, Compute)
- Scoping the Solution and Managing Expectations
- Framing the Problem: Classification, Regression, Clustering, or Other

**Python Packages:** (Conceptual, no code packages required)

## Chapter 2: Data Collection

- Data Sources and Storage Systems
- APIs, Databases, and Query Optimization
- Sensor Data and Real-Time Streams
- Third-Party Data and External Datasets
- Data Governance and Privacy Considerations
- Building Data Pipelines

**Python Packages:** `pandas`, `sqlalchemy`, `psycopg2`, `pymongo`, `requests`, `aiohttp`, `pyspark`, `kafka-python`, `boto3`, `google-cloud-storage`

## Chapter 3: Data Cleaning & Preprocessing

- Identifying and Handling Missing Values
- Detecting and Removing Duplicates
- Outlier Detection and Treatment
- Standardizing Data Formats and Encoding
- Handling Categorical and Text Data
- Normalization and Scaling Techniques

**Python Packages:** `pandas`, `numpy`, `scikit-learn`, `missingno`, `outlier-utils`, `pyjanitor`, `fancyimpute`

## Chapter 4: Exploratory Data Analysis (EDA)

- Univariate Analysis and Distributions
- Bivariate and Multivariate Relationships
- Correlation and Covariance Analysis
- Visual Storytelling and Interpretation
- Hypothesis Formation and Statistical Testing
- Identifying Patterns, Anomalies, and Insights

**Python Packages:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `scipy`, `statsmodels`, `pandas-profiling`, `sweetviz`

## Chapter 5: Feature Engineering & Selection

- Creating New Features from Existing Data
- Encoding Categorical Variables
- Handling Time Series and Temporal Features
- Dimensionality Reduction Techniques
- Feature Scaling and Normalization
- Feature Selection Methods and Importance

**Python Packages:** `pandas`, `numpy`, `scikit-learn`, `featuretools`, `category-encoders`, `tsfresh`, `optuna`, `shap`

## Chapter 6: Data Splitting

- Train, Validation, and Test Set Strategy
- Cross-Validation Techniques
- Stratified and Time-Series Splits
- Class Imbalance and Sampling Strategies
- Avoiding Data Leakage
- Setting Up Evaluation Pipelines

**Python Packages:** `scikit-learn`, `imbalanced-learn`, `numpy`, `pandas`, `stratification-tools`

## Chapter 7: Model Selection & Training

- Understanding Algorithm Families
- Baseline Models and Benchmarking
- Hyperparameter Tuning and Grid Search
- Regularization and Preventing Overfitting
- Ensemble Methods and Stacking
- Training Workflows and Reproducibility

**Python Packages:** `scikit-learn`, `xgboost`, `lightgbm`, `catboost`, `tensorflow`, `torch`, `optuna`, `hyperopt`, `ray-tune`, `wandb`

## Chapter 8: Model Evaluation

- Classification Metrics (Accuracy, Precision, Recall, F1)
- Regression Metrics (RMSE, MAE, R²)
- Ranking and Recommendation Metrics (AUC, NDCG)
- Business-Oriented Metrics and ROI
- Ablation Studies and Feature Importance
- Error Analysis and Model Debugging

**Python Packages:** `scikit-learn`, `numpy`, `pandas`, `matplotlib`, `seaborn`, `shap`, `lime`, `eli5`

## Chapter 9: Deployment

- Model Packaging and Containerization
- API Development for Model Serving
- Batch Inference and Scheduled Jobs
- Embedded and Edge Deployment
- A/B Testing and Canary Releases
- Version Control and Model Registry

**Python Packages:** `fastapi`, `flask`, `gunicorn`, `mlflow`, `kubeflow`, `seldon-core`, `ray-serve`, `bentoml`, `docker`, `onnx`

## Chapter 10: Monitoring & Maintenance

- Production Performance Tracking
- Data Drift and Concept Drift Detection
- Model Retraining Strategies
- Incident Response and Debugging
- Continuous Improvement and Feedback Loops
- Stakeholder Reporting and Governance

**Python Packages:** `mlflow`, `evidently`, `whylabs`, `prometheus-client`, `airflow`, `dbt`, `grafana-api`, `pandas`, `numpy`

## AI

Cross-cutting benefits:
- Code completion & boilerplate generation (60-80% dev time savings)
- Documentation generation (docstrings, README sections)
- Bug detection via code review (pre-commit analysis)
- Explanation of complex concepts and error messages
- Reproducibility tracking (parameter logging, experiment versioning)

- The Evolution of AI Pair Programming — Tracing the path from autocomplete and
  linting tools to today's context-aware coding agents, and what that trajectory
  suggests about where development workflows are headed.
- Prompting for Code: Communicating Intent to a Model — How to write effective
  specifications and prompts that translate fuzzy human requirements into
  precise, working code, including patterns for iterative refinement.
- Trust, Verification, and the New Code Review — How developers should validate
  AI-generated code, the risks of silent bugs or security vulnerabilities, and
  how review practices need to adapt when a machine writes the first draft.
- Agentic Workflows: From Snippets to Autonomous Tasks — Examining tools that
  don't just suggest code but plan, execute, and self-correct across a whole
  codebase — what changes when AI can run commands, write files, and iterate on
  its own.
- The Changing Role of the Developer — What skills become more or less valuable
  when AI handles routine implementation: system design, taste, debugging
  intuition, and the judgment calls that remain distinctly human.

- Architecture of coding
- Unit testing
- Documentation
