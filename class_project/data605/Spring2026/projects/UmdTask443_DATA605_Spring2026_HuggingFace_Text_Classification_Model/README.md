# HuggingFace Text Classification Model

## Description

HuggingFace is an open-source platform that provides ready-to-use, state-of-the-art language models along with the tools needed to fine-tune, evaluate, and deploy them for any natural language task, without needing to build models from scratch.

This project builds a News Article Classification Pipeline on top of HuggingFace. Given a raw news article, the system ingests data from public news datasets (AG News, BBC News), fine-tunes transformer models, covering BERT, DistilBERT, and RoBERTa for multi-class topic classification, and serves predictions through a live inference endpoint and dashboard.

The full stack uses HuggingFace Transformers and Datasets for tokenization and fine-tuning, PyTorch as the training backend, Scikit-learn for evaluation metrics, FastAPI for inference serving, and Streamlit for the prediction dashboard.

## Project Specs: 
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/class_project/data605/Spring2026/projects_descriptions/HuggingFace_Project_Description.md

**Authors**: @riyaapuri @stupatel17
**Assigned to**: @riyaapuri @stupatel17 @protocorn @gpsaggese

## Stack

| Layer | Library |
|---|---|
| Modeling & Tokenization | HuggingFace Transformers, Datasets |
| Training Backend | PyTorch, Accelerate |
| Evaluation | Scikit-learn, HuggingFace Evaluate |
| Hyperparameter Tuning | Optuna |
| Serving | FastAPI |
| Dashboard | Streamlit |

---

## Release v1.0 

### `config.py`
Central config for all constants — dataset name, label mappings, model checkpoints, training hyperparameters, and paths. Imported by every other module to avoid hardcoded values.

### `dataset_loader.py`
Loads AG News from the HuggingFace hub. Optionally subsets train/test splits for faster iteration. Includes `summarize_dataset()` for label-distribution stats and `get_sample_articles()` for spot-checking raw examples.

### `preprocessing.py`
Three-stage pipeline: **clean → tokenize → format**.
- `clean_text()` strips HTML entities, URLs, and excess whitespace. Punctuation and casing are intentionally preserved for the tokenizer.
- `get_tokenizer()` loads an `AutoTokenizer` for any HF checkpoint.
- `make_tokenize_fn()` returns a closure for use with `dataset.map()`, applying cleaning + tokenization with `padding="max_length"` and `truncation=True` at `MAX_LENGTH=128`.
- `tokenize_dataset()` runs batched tokenization over the full `DatasetDict` and sets torch format on the output columns (`input_ids`, `attention_mask`, `label`).

### `metrics.py`
Two evaluation utilities:
- `compute_metrics()` — Trainer callback returning `accuracy` and `f1_macro` after each eval step.
- `full_report()` — generates a detailed sklearn classification report and confusion matrix, used during final model evaluation.

### `requirements.txt`
Pins all dependencies. Key versions: `transformers>=4.35`, `torch>=2.0`, `datasets>=2.14`, `scikit-learn>=1.3`, `optuna>=3.3`.