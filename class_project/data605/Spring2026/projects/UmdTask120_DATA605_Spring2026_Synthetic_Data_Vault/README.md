# DATA605 Spring 2026: Synthetic Data Vault Privacy Classification Project

## Project Summary

This project explores how **Synthetic Data Vault (SDV)** can be used to generate synthetic tabular data for a privacy-preserving machine learning workflow.

The main idea of the project is to check whether synthetic data can preserve enough useful patterns from a real dataset to train classification models. I used the **Adult Income dataset**, generated synthetic training data using SDV, evaluated the quality of the synthetic data, and compared models trained on real data versus synthetic data.

The project is structured like a small tutorial so that someone new to SDV can understand the basic workflow and reproduce the results.

---

## Why This Project Matters

Real-world datasets often contain sensitive information, especially when they include demographic, financial, medical, or personal records. In many situations, sharing or using the original dataset directly may create privacy concerns.

Synthetic data can help by creating artificial records that follow similar statistical patterns as the real data, without directly exposing the original records. However, synthetic data should not be assumed to be useful or safe automatically. It needs to be evaluated carefully.

This project focuses on one important question:

> If we train a machine learning model on synthetic data, can it still perform well on real unseen data?

---

## Dataset

This project uses the **Adult Income dataset**, a real-world tabular dataset commonly used for classification tasks.

The dataset includes features such as:

- age
- workclass
- education
- marital status
- occupation
- relationship
- race
- sex
- capital gain
- capital loss
- hours worked per week
- native country

The target variable is income class:

- `<=50K`
- `>50K`

This makes the project a **binary classification problem**.

I selected this dataset because it contains both numerical and categorical variables, which makes it a good example for testing synthetic tabular data generation.

---

## Project Objective

The objective of this project is to build an end-to-end workflow using SDV.

The project includes:

- loading and cleaning a real dataset
- exploring the dataset through basic EDA
- generating synthetic data using SDV
- evaluating synthetic data quality using SDMetrics
- training machine learning models on real and synthetic data
- comparing model performance using classification metrics
- discussing limitations and possible improvements

The main experiment is:

> Train models on synthetic data and evaluate them on real test data.

This helps test whether the synthetic data preserves useful predictive patterns from the original dataset.

---

## Repository Structure

```text
DATA605_Spring2026_Synthetic_Data_Vault/
│
├── README.md
│   Main project documentation.
│
├── requirements.txt
│   Python libraries required to run the project.
│
├── Dockerfile
│   Docker setup for reproducible execution.
│
├── docker_build.sh
│   Script to build the Docker image.
│
├── docker_run.sh
│   Script to run the Docker container.
│
├── run_project_check.py
│   Script used by Docker to verify that important files and outputs exist.
│
├── synthetic_data_vault_utils.py
│   Helper functions for data cleaning, splitting, model evaluation, and saving results.
│
├── notebooks/
│   ├── Synthetic_Data_Vault.ipynb
│   │   Main notebook with the full project workflow.
│   │
│   └── synthetic_data_vault.API.ipynb
│       Short API-style notebook explaining the basic SDV workflow.
│
└── outputs/
    ├── model_comparison_results.csv
    │   Initial model comparison results.
    │
    └── final_model_comparison_results.csv
        Final model results including the tuning experiment.
```

---

## How to Run the Project

Create and activate a Python environment:

```bash
conda create -n sdv_project python=3.11 -y
conda activate sdv_project
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open the main notebook:

```text
notebooks/Synthetic_Data_Vault.ipynb
```

Run the notebook from top to bottom.

---

## Docker Execution

This project includes Docker files to make the project easier to reproduce.

Build the Docker image:

```bash
./docker_build.sh
```

Run the Docker image:

```bash
./docker_run.sh
```

The Docker run command executes:

```text
run_project_check.py
```

This script checks that the important project files and output results are available.

A successful Docker run ends with:

```text
Project check completed successfully.
```

---

## Methodology

The project starts by loading the Adult Income dataset and cleaning missing or inconsistent values. After cleaning, I performed basic exploratory data analysis to understand the target distribution, feature types, and general dataset structure.

The real dataset was then split into training and testing sets. This step is important because SDV was trained only on the training data, while the real test data was kept separate for final evaluation. This avoids data leakage and makes the comparison more fair.

For synthetic data generation, I used SDV’s **Gaussian Copula Synthesizer**. I selected this synthesizer because it is stable, efficient, and suitable for a tutorial-style single-table project.

After generating the synthetic data, I used **SDMetrics** to evaluate how similar the synthetic data was to the real training data. Finally, I trained classification models on real and synthetic data and evaluated all models on the same real test set.

---

## Synthetic Data Quality Results

The SDMetrics quality report produced the following results:

| Metric | Score |
|---|---:|
| Column Shapes | 90.31% |
| Column Pair Trends | 75.09% |
| Overall Quality Score | 82.70% |

The **Column Shapes** score shows that the synthetic data preserved individual column distributions fairly well. This means the generated data followed many of the same single-column patterns as the original training data.

The **Column Pair Trends** score was lower, which means relationships between pairs of columns were harder to preserve. This is important because machine learning models often rely on relationships between features, not just individual column distributions.

Overall, the synthetic data quality was reasonably strong, but not perfect.

---

## Machine Learning Results

The models were evaluated using:

- accuracy
- precision
- recall
- F1-score

All models were tested on the same real test set.

| Model | Training Data | Accuracy | Precision | Recall | F1-score |
|---|---|---:|---:|---:|---:|
| Logistic Regression | Real Data | 0.846 | 0.738 | 0.589 | 0.655 |
| Logistic Regression | Synthetic Data | 0.758 | 0.556 | 0.121 | 0.199 |
| Random Forest | Real Data | 0.854 | 0.806 | 0.540 | 0.647 |
| Random Forest | Synthetic Data | 0.753 | 1.000 | 0.001 | 0.003 |
| Tuned Random Forest | Real Data | 0.849 | 0.806 | 0.515 | 0.629 |
| Tuned Random Forest | Synthetic Data | 0.752 | 0.000 | 0.000 | 0.000 |

The models trained on real data performed better than the models trained only on synthetic data.

The Logistic Regression model trained on real data achieved an F1-score of about `0.655` for the `>50K` class. When trained on synthetic data, the F1-score dropped to about `0.199`.

The Random Forest model trained on synthetic data performed especially poorly for the `>50K` class. It mostly predicted the majority class, `<=50K`, and almost completely missed the minority class.

---

## Key Findings

The project showed that SDV was able to generate synthetic data with a good overall quality score. The synthetic data preserved many broad patterns from the original training data, especially individual column distributions.

However, the synthetic data did not fully preserve the deeper feature relationships needed for strong classification performance. This was most visible in the models trained on synthetic data, which struggled to correctly identify the minority `>50K` class.

The hyperparameter tuning experiment also did not solve this issue. This suggests that the main limitation was not only the model settings, but also the quality of the relationships preserved in the synthetic data.

---

## Limitations

This project has some limitations.

I used the Gaussian Copula Synthesizer because it is fast and stable for a tutorial-style project. More advanced synthesizers such as CTGAN or TVAE could be tested in future work.

The dataset is also imbalanced, with many more `<=50K` records than `>50K` records. This made the minority class harder to predict, especially when models were trained only on synthetic data.

The project focused mainly on machine learning utility. It did not deeply evaluate privacy risks such as membership inference or record-level disclosure risk. Because of that, the synthetic data should not automatically be treated as fully private without additional privacy testing.

---

## Future Improvements

Future work could improve this project by:

- comparing Gaussian Copula with CTGAN and TVAE
- adding privacy risk evaluation
- testing stronger imbalance-handling methods
- adding confusion matrix visualizations
- trying additional classifiers
- tuning SDV synthesizer settings
- improving minority-class representation in the synthetic data

These improvements would help better understand both the strengths and limits of synthetic data in classification workflows.

---

## Documentation Guide

This repository is organized as a tutorial-style project.

A reader can start with this `README.md` to understand the project goal, workflow, setup instructions, results, and limitations.

Then they can open:

```text
notebooks/synthetic_data_vault.API.ipynb
```

to understand the basic SDV API workflow.

After that, they can open:

```text
notebooks/Synthetic_Data_Vault.ipynb
```

to review the full project, including EDA, synthetic data generation, quality evaluation, machine learning, tuning, and interpretation.

The Docker scripts can be used to verify that the project files and outputs are present.

---


## References

This project used the following resources and documentation:

- Synthetic Data Vault. “Welcome to the SDV!” SDV Documentation.  
  https://docs.sdv.dev/sdv

- SDMetrics. “Synthetic Data Metrics.” SDMetrics Documentation.  
  https://docs.sdv.dev/sdmetrics

- UCI Machine Learning Repository. “Adult Dataset.”  
  https://archive.ics.uci.edu/dataset/2/adult

- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. “Scikit-learn: Machine Learning in Python.” *Journal of Machine Learning Research*, 12, 2825–2830, 2011.  
  https://www.jmlr.org/papers/v12/pedregosa11a.html

- SDV Developers. “Synthetic Data Vault.” GitHub Repository.  
  https://github.com/sdv-dev/SDV

---

## Conclusion

This project shows that SDV can be used to generate synthetic tabular data for privacy-preserving machine learning experiments.

The generated synthetic data had a strong overall quality score and preserved many individual column-level patterns. However, the machine learning results showed that models trained only on synthetic data did not perform as well as models trained on real data, especially for the minority `>50K` class.

Overall, SDV is useful for safe experimentation, tutorials, and early-stage modeling. At the same time, synthetic data should always be evaluated carefully before being used as a replacement for real data in serious machine learning tasks.
