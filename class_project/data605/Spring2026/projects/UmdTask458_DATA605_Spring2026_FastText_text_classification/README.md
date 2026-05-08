# FastText Text Classification

## What is FastText?

- FastText is an open-source library developed by Facebook AI Research for
  efficient text classification and representation.
- It allows users to create word embeddings and perform supervised learning
  tasks such as text classification with high accuracy and speed.
- FastText can handle large datasets and provides pre-trained models for various
  languages, making it accessible for multilingual applications.
- The tool supports subword information, which allows it to generate embeddings
  for out-of-vocabulary words, improving its robustness in natural language
  processing tasks.
- FastText is designed to be easy to use, with a command-line interface and
  Python bindings, making it suitable for both beginners and advanced users.


## Project Overview

This project demonstrates text classification using FastText, an open-source
library developed by Facebook AI Research. We train a model to classify news
articles from the 20 Newsgroups dataset into 20 categories, covering topics
such as politics, religion, sports, science, and technology.


## Dataset

We use the 20 Newsgroups dataset, which contains approximately 18,000 newsgroup
posts across 20 categories. The dataset is loaded directly via scikit-learn and
requires no manual download.

- Training samples: 11,314
- Test samples: 7,532
- Categories: 20

Headers, footers, and quoted text are removed to make the classification task
more realistic and challenging.

## Project Structure

    UmdTask458_DATA605_Spring2026_FastText_text_classification/
    Dockerfile                  - Docker environment setup
    requirements.txt            - Python dependencies
    fasttext_utils.py           - Utility functions for training and evaluation
    fasttext.example.ipynb      - Full project walkthrough notebook
    fasttext.API.ipynb          - FastText API usage examples
    confusion_matrix_baseline.png
    confusion_matrix_best.png
    hyperparameter_tuning.png
    model_comparison.png
    error_analysis.png
    README.md

## Setup and Installation

### Prerequisites
- Docker Desktop installed and running
- Git

Note: docker_build.sh has Windows path issues. Use docker build directly instead.
FastText is incompatible with NumPy 2.0, so numpy<2.0 is pinned in requirements.txt.

### Build the Docker Container

    docker build -t gpsaggese/umd_data605_fasttext .

### Run the Container

    docker run -it --rm -p 8888:8888 -v "C:/Users/Vaibhav Devarapalli/src/gpsaggese.github.io/class_project/data605/Spring2026/projects/UmdTask458_DATA605_Spring2026_FastText_text_classification:/home/user" gpsaggese/umd_data605_fasttext bash

### Start Jupyter

    pip install "numpy<2.0" -q && jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --notebook-dir=/home/user

Then open the token URL shown in the terminal in your browser.

## Notebooks

### fasttext.example.ipynb
The main project notebook covering:
1. Dataset loading and exploration
2. Text preprocessing for FastText format
3. Baseline model training and evaluation
4. Hyperparameter tuning across 5 configurations
5. Best model evaluation with confusion matrix and error analysis
6. Comparison with Logistic Regression + TF-IDF

### fasttext.API.ipynb
Demonstrates the FastText API including:
- Training a model from scratch
- Making single and top-k predictions
- Evaluating model performance
- Saving and loading models
- Accessing word vectors and nearest neighbors

## Results

| Model | F1 Score | Training Time |
|---|---|---|
| FastText Baseline (e=25, lr=0.5, ng=2) | 0.60 | ~5s |
| FastText Best (e=75, lr=0.5, ng=2) | 0.62 | ~8s |
| Logistic Regression + TF-IDF | 0.66 | ~19s |

FastText trains 2.5x faster than Logistic Regression while achieving
competitive accuracy. On larger datasets, FastText's speed advantage
becomes significantly more pronounced.

## Key Findings

1. Hyperparameter tuning improved F1 from 0.60 (baseline) to 0.62 (best
   configuration). Poor configuration choices such as low epoch count and
   learning rate can drop performance as low as 0.31.
2. The most common misclassifications occur between semantically similar
   categories such as talk.politics.misc and talk.politics.guns.
3. Logistic Regression + TF-IDF slightly outperforms FastText on this
   small dataset, but FastText scales significantly better to large datasets.
4. FastText is best suited for large-scale text classification where
   training speed and memory efficiency are critical.

## Dependencies

- fasttext-wheel
- scikit-learn
- numpy<2.0
- pandas
- matplotlib
- seaborn