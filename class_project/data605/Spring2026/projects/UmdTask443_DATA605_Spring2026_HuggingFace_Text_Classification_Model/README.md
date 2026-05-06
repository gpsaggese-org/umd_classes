# HuggingFace News Article Classification

## Description

This project builds an end-to-end News Article Classification Pipeline using HuggingFace Transformers. Given a raw news article, the system fine-tunes transformer models (DistilBERT, BERT, RoBERTa) on the AG News dataset for 4-class topic classification and serves predictions through a command-line inference interface.

The entire pipeline — data loading, preprocessing, training, evaluation, and inference — runs inside Docker, requiring no local Python environment setup beyond Docker Desktop.

**Authors**: @riyaapuri @stupatel17
**Assigned to**: @riyaapuri @stupatel17 @protocorn @gpsaggese

**Project Specs**: https://github.com/gpsaggese/gpsaggese.github.io/blob/master/class_project/data605/Spring2026/projects_descriptions/HuggingFace_Project_Description.md

---

## Table of Contents

- [Architecture](#architecture)
- [Stack](#stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Pipeline Steps](#pipeline-steps)
- [Outputs](#outputs)
- [Release Notes](#release-notes)

---

## Architecture

```
Raw News Article
       │
       ▼
┌─────────────────┐
│  dataset_loader │  Loads AG News from HuggingFace Hub
│                 │  Splits into train / validation / test
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  preprocessing  │  Cleans text (HTML, URLs, whitespace)
│                 │  Tokenizes with AutoTokenizer (max 128 tokens)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    train.py     │  Fine-tunes DistilBERT / BERT / RoBERTa
│                 │  Saves best checkpoint by macro-F1
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   evaluate.py   │  Batch inference on test set
│                 │  Outputs report, confusion matrix, CSV
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   predict.py    │  Single article / file / interactive inference
│                 │  Returns label + per-class confidence scores
└─────────────────┘
```

**Docker layer**: All steps above run inside a single container. The project directory is volume-mounted at `/app` so code edits are reflected immediately without rebuilding. HuggingFace model downloads are persisted in a named Docker volume (`hf_cache`) so models are not re-downloaded across runs.

---

## Stack

| Layer | Library |
|---|---|
| Modeling & Tokenization | HuggingFace Transformers, Datasets |
| Training Backend | PyTorch, Accelerate |
| Evaluation | Scikit-learn |
| Hyperparameter Tuning | Optuna |
| Serving | FastAPI *(upcoming)* |
| Dashboard | Streamlit *(upcoming)* |
| Containerization | Docker |

---

## Project Structure

```
project_root/
│
├── project_files/
│   ├── config.py                  # All constants and hyperparameters
│   ├── requirements.txt           # Python dependencies
│   │
│   ├── scripts/
│   │   ├── train.py               # Fine-tuning script
│   │   ├── evaluate.py            # Evaluation + result export
│   │   └── predict.py             # Inference script
│   │
│   └── utils/
│       ├── dataset_loader.py      # Data loading and inspection
│       ├── preprocessing.py       # Text cleaning and tokenization
│       └── metrics.py             # Metric callbacks and report utilities
│
├── models/                        # Saved model checkpoints (generated)
│   └── distilbert-ag-news/
│       └── best/                  # Best checkpoint by macro-F1
│
├── results/                       # Evaluation outputs (generated)
│   ├── classification_report.txt
│   ├── confusion_matrix.png
│   ├── per_class_metrics.png
│   └── predictions.csv
│
├── Dockerfile                     # ML-ready container image
├── docker_name.sh                 # Image name configuration
├── docker_utils.sh                # Shared helper functions
├── run.sh                         # Unified pipeline wrapper
├── docker_build.sh                # Build the Docker image
├── docker_dataloader.sh           # Run dataset_loader.py
├── docker_train.sh                # Run train.py
├── docker_evaluate.sh             # Run evaluate.py
├── docker_predict.sh              # Run predict.py
├── docker_bash.sh                 # Open interactive shell
├── docker_jupyter.sh              # Launch Jupyter Lab
├── docker_clean.sh                # Remove image and cache
├── run_jupyter.sh                 # Jupyter startup (runs inside container)
├── version.sh                     # Package version logger (runs at build)
├── bashrc                         # Shell config copied into image
└── etc_sudoers                    # Sudo config copied into image
```

---

## Prerequisites

**Docker Desktop** is the only requirement. No local Python installation is needed.

| OS | Instructions |
|---|---|
| macOS | Download from https://www.docker.com/products/docker-desktop and install |
| Windows | Install Docker Desktop; WSL2 will be enabled automatically |
| Linux | Install Docker Engine via your package manager (`apt`, `dnf`, etc.) |

Verify Docker is working before proceeding:

```bash
docker --version
docker run hello-world
```

---

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd <repository-root>

# 2. Build the Docker image (one-time, ~5 minutes)
./docker_build.sh
```

The build installs all Python dependencies from `project_files/requirements.txt` into the image. You only need to rebuild if `requirements.txt` or the `Dockerfile` changes.

To force a clean rebuild (re-downloads all packages):

```bash
./docker_build.sh --no-cache
```

---

## Usage

### Full Pipeline

Run the entire pipeline — data loading, training, evaluation, and prediction — in a single command:

```bash
./run.sh
```

With options:

```bash
# Swap the model backbone
./run.sh --model bert-base-uncased

# Override training hyperparameters
./run.sh --model roberta-base --epochs 5 --batch_size 32 --lr 3e-5

# Set a custom prediction article
./run.sh --text "Federal Reserve raises interest rates for the third time this year"

# Skip the Docker build step if the image already exists
./run.sh --skip-build --text "Apple reports record iPhone sales"
```

### Individual Steps

Each pipeline step can also be run independently:

```bash
# Inspect the dataset (label distribution, sample articles)
./docker_dataloader.sh

# Fine-tune the model
./docker_train.sh
./docker_train.sh --model bert-base-uncased --epochs 3

# Evaluate the trained model
./docker_evaluate.sh
./docker_evaluate.sh --model_dir models/bert-ag-news

# Run inference
./docker_predict.sh --text "NASA launches a new satellite into orbit"
./docker_predict.sh --file /app/project_files/articles.txt
./docker_predict.sh                                           # interactive mode

# Open a shell inside the container for debugging
./docker_bash.sh

# Launch Jupyter Lab at http://localhost:8888/lab
./docker_jupyter.sh
JUPYTER_PORT=8889 ./docker_jupyter.sh                         # custom port

# Remove the Docker image
./docker_clean.sh
./docker_clean.sh --volumes                                   # also clears HF model cache
```

---

## Configuration

All tunable parameters live in `project_files/config.py`. Edit this file to change any default without modifying the scripts.

| Parameter | Default | Description |
|---|---|---|
| `DEFAULT_MODEL` | `distilbert-base-uncased` | Backbone used when no `--model` flag is passed |
| `BERT_MODEL` | `bert-base-uncased` | BERT checkpoint name for reference |
| `ROBERTA_MODEL` | `roberta-base` | RoBERTa checkpoint name for reference |
| `EPOCHS` | `3` | Number of training epochs |
| `BATCH_SIZE` | `16` | Per-device training batch size |
| `LEARNING_RATE` | `2e-5` | Peak learning rate |
| `WEIGHT_DECAY` | `0.01` | L2 regularization strength |
| `WARMUP_STEPS` | `500` | Linear LR warmup steps |
| `MAX_LENGTH` | `128` | Max tokens per article |
| `TRAIN_SUBSET` | `None` | Set to an integer to use a smaller training slice |
| `EVAL_SUBSET` | `None` | Set to an integer to use a smaller test slice |
| `OUTPUT_DIR` | `models/distilbert-ag-news` | Where the trained checkpoint is saved |
| `RESULTS_DIR` | `results` | Where evaluation outputs are saved |
| `SEED` | `42` | Random seed for reproducibility |

---

## Pipeline Steps

### Step 1 — Dataset Loading (`utils/dataset_loader.py`)

Loads the [AG News](https://huggingface.co/datasets/ag_news) dataset from the HuggingFace Hub. AG News contains 120,000 training and 7,600 test articles across four categories:

| ID | Category |
|---|---|
| 0 | World |
| 1 | Sports |
| 2 | Business |
| 3 | Sci/Tech |

Key functions:

- `load_ag_news()` — downloads the dataset from the HuggingFace Hub.
- `get_subsets()` — optionally samples a smaller slice for faster iteration, controlled by `TRAIN_SUBSET` and `EVAL_SUBSET` in `config.py`.
- `summarize_dataset()` — prints per-label counts to the terminal.
- `get_sample_articles()` — prints random raw examples for spot-checking before training.

A validation split (90/10 from train) is created at load time since AG News does not provide one by default. This ensures the test set remains fully unseen during model selection.

---

### Step 2 — Preprocessing (`utils/preprocessing.py`)

Three-stage pipeline applied before tokenization:

**Clean** (`clean_text()`): Removes HTML entities (`&amp;`, `&#34;`), URLs, and collapses excess whitespace. Punctuation and casing are preserved for the tokenizer.

**Tokenize** (`make_tokenize_fn()`): Returns a closure for use with `dataset.map()`. Applies `padding="max_length"` and `truncation=True` at `MAX_LENGTH=128` tokens using `AutoTokenizer`.

**Format** (`tokenize_dataset()`): Runs batched tokenization across the full `DatasetDict` and sets PyTorch tensor format on `input_ids`, `attention_mask`, and `label`.

---

### Step 3 — Training (`scripts/train.py`)

Fine-tunes a transformer model on the preprocessed dataset using HuggingFace `Trainer`.

**Model**: `AutoModelForSequenceClassification` adds a dropout layer and a linear projection (`hidden_size → 4 labels`) on top of the pre-trained backbone. Only the classification head is randomly initialized; transformer weights come from the HuggingFace checkpoint.

**Training decisions**:
- All transformer layers are trainable (full fine-tune, not frozen).
- Linear learning rate warmup over 500 steps avoids large early gradient updates.
- Weight decay regularization prevents overfitting.
- Evaluation runs after every epoch; the best checkpoint is selected by macro-F1.
- `fp16` mixed-precision is enabled automatically when CUDA is available.

**CLI flags**:

```bash
python scripts/train.py --model bert-base-uncased --epochs 5 --batch_size 32 --lr 3e-5
```

**Outputs** (written to `models/<model-name>/`):
- `best/` — best checkpoint (model weights + tokenizer).
- `train_results.txt` — per-epoch training log.

---

### Step 4 — Evaluation (`scripts/evaluate.py`)

Runs batch inference on the full test set and saves four outputs to `results/`:

| Output file | Contents |
|---|---|
| `classification_report.txt` | Per-class precision, recall, F1, and support |
| `confusion_matrix.png` | Heatmap of true vs predicted labels |
| `per_class_metrics.png` | Grouped bar chart of precision, recall, and F1 per category |
| `predictions.csv` | Row-level predictions with true label, predicted label, and a correct/incorrect flag |

Uses `matplotlib.use("Agg")` so plots render inside Docker without a display.

**CLI flags**:

```bash
python scripts/evaluate.py --model_dir models/bert-ag-news
```

---

### Step 5 — Inference (`scripts/predict.py`)

Loads a saved checkpoint and classifies articles in three modes:

**Single article**:
```bash
./docker_predict.sh --text "Apple reports record iPhone sales in Q3"
```

**File** (one article per line):
```bash
./docker_predict.sh --file /app/project_files/articles.txt
```

**Interactive** (type articles one at a time, `Ctrl+C` to quit):
```bash
./docker_predict.sh
```

Example output:
```
── Result 1 ─────────────────────────────────────────────
  Text       : Apple reports record iPhone sales in Q3...
  Prediction : Business  (94.21% confidence)
  All scores :
    Business      94.21%  ██████████████████
    Sci/Tech       3.87%
    World          1.12%
    Sports         0.80%
```

---

## Outputs

All outputs are written to the host machine via the Docker volume mount and persist after the container exits.

| Path | Contents | Generated by |
|---|---|---|
| `models/<name>/best/` | Fine-tuned model weights and tokenizer | `train.py` |
| `models/<name>/train_results.txt` | Per-epoch training log | `train.py` |
| `results/classification_report.txt` | Full sklearn classification report | `evaluate.py` |
| `results/confusion_matrix.png` | Confusion matrix heatmap | `evaluate.py` |
| `results/per_class_metrics.png` | Per-class metric bar chart | `evaluate.py` |
| `results/predictions.csv` | Row-level test set predictions | `evaluate.py` |

---

## Release Notes

### Release v1.0
Initial data and preprocessing pipeline.

- `config.py` — central configuration for all constants and hyperparameters.
- `utils/dataset_loader.py` — AG News loading, subsetting, and dataset inspection.
- `utils/preprocessing.py` — text cleaning, tokenization, and dataset formatting.
- `utils/metrics.py` — Trainer callback (`compute_metrics`) and sklearn report utility (`full_report`).
- `requirements.txt` — full dependency list.

### Release v2.0
Model training, inference, and Docker integration.

- **New**: `scripts/train.py` — end-to-end fine-tuning with HuggingFace Trainer.
- **New**: `scripts/predict.py` — three-mode inference (single article, file, interactive).
- **New**: `run.sh` — unified pipeline wrapper with CLI flags forwarded to each step.
- **New**: `Dockerfile`, `docker_utils.sh`, `docker_name.sh`, `docker_build.sh`, `docker_train.sh`, `docker_predict.sh`, `docker_dataloader.sh`, `docker_bash.sh`, `docker_jupyter.sh`, `docker_clean.sh`, `run_jupyter.sh`, `version.sh` — full standalone Docker integration.
- **Modified**: `config.py` — added `BERT_MODEL`, `ROBERTA_MODEL`, and `RESULTS_DIR`.
- **Modified**: `utils/dataset_loader.py` — added 90/10 validation split from the training set since AG News has no default validation split.
- **Modified**: `utils/preprocessing.py` — fixed `sys.path` insert for subdirectory execution.
- **Modified**: `requirements.txt` — moved from project root into `project_files/`; root-level duplicate removed.
- **Modified**: `Dockerfile` — upgraded from bare template to full ML image; added system packages required by PyTorch and scikit-learn; configured HuggingFace cache volume.

### Release v3.0
Model evaluation and result export.

- **New**: `scripts/evaluate.py` — batch inference on the test set, exports classification report, confusion matrix, per-class metric chart, and predictions CSV.
- **New**: `docker_evaluate.sh` — runs `evaluate.py` inside the container; results written to `./results/` on the host.
- **Modified**: `run.sh` — evaluation added as step 4; prediction moved to step 5; step counters updated.
- **Modified**: `utils/metrics.py` — removed `import evaluate` (HuggingFace library) to resolve a circular import. When running `scripts/evaluate.py`, Python adds `scripts/` to `sys.path` automatically, causing `import evaluate` inside `metrics.py` to resolve to `scripts/evaluate.py` instead of the HuggingFace package. Fixed by replacing the single usage with `accuracy_score` from sklearn, which produces identical results with no behaviour change.