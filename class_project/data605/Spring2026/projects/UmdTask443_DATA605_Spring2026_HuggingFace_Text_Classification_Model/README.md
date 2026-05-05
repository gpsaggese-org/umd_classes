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

---
 
## Release v2.0

### How to run (this will be cleaned up before the final commit)

**Prerequisites:** Docker Desktop installed and running. No other local dependencies needed from this commit onwards.

```bash
# Full pipeline — build, load data, train, predict
./run.sh
 
# With a custom model and prediction text
./run.sh --model roberta-base --epochs 5 --text "Fed raises interest rates again"
 
# Skip rebuild if image already exists
./run.sh --skip-build --text "Apple reports record iPhone sales"
 
# Run individual steps
./docker_build.sh                                             # build image
./docker_dataloader.sh                                        # inspect dataset
./docker_train.sh --model bert-base-uncased --epochs 3        # fine-tune
./docker_predict.sh --text "NASA launches new satellite"      # single prediction
./docker_predict.sh                                           # interactive mode
./docker_jupyter.sh                                           # open Jupyter Lab
```
 
---
 
### New Files
 
#### `scripts/train.py`
Fine-tunes a transformer model on AG News end-to-end. Orchestrates the full training pipeline in five steps:
1. Loads and preprocesses the dataset via the `dataset_loader` and `preprocessing` utilities.
2. Instantiates `AutoModelForSequenceClassification` with a classification head (dropout + linear projection to 4 labels) on top of the pre-trained transformer backbone.
3. Configures HuggingFace `Trainer` with: linear LR warmup over 500 steps, weight decay regularization, per-epoch evaluation, and macro-F1 as the checkpoint selection metric.
4. Runs training with optional `fp16` on CUDA for speed.
5. Saves the best checkpoint to `models/<model-name>/best/` and writes a training log to `train_results.txt`.
Accepts CLI flags `--model`, `--epochs`, `--batch_size`, `--lr` so any backbone (DistilBERT, BERT, RoBERTa) can be swapped without touching code.
 
#### `scripts/predict.py`
Loads a fine-tuned checkpoint and runs inference in three modes:
- `--text` — classify a single article passed as a string.
- `--file` — classify all articles in a text file (one per line).
- Interactive — prompts for articles in a loop until `Ctrl+C`.
Outputs the predicted label, confidence percentage, and a score bar for all four classes. Falls back gracefully with a clear error if the model checkpoint is not found.
 
#### `run.sh`
Unified pipeline wrapper that runs the entire workflow in a single command. Executes four steps in order: build image → load dataset → train model → run prediction. Accepts `--skip-build` to avoid rebuilding when the image already exists, `--text` to set a custom prediction article, and all `train.py` flags (`--model`, `--epochs`, `--batch_size`, `--lr`) which are forwarded directly to the training step.
 
#### `docker_utils.sh`
Shared helper library sourced by every `docker_*.sh` script. Provides three functions: `run()` to echo and execute commands, `load_docker_vars()` to source `docker_name.sh` and print resolved image names, and `base_run_opts()` to build the standard `docker run` flags including the code volume mount and HuggingFace cache volume.
 
#### `docker_train.sh`
Runs `scripts/train.py` inside the container. Forwards all CLI arguments directly to the script, so any combination of `--model`, `--epochs`, `--batch_size`, and `--lr` works without modifying the script. The trained model is saved to `./models/` on the host via the volume mount.
 
#### `docker_predict.sh`
Runs `scripts/predict.py` inside the container. Allocates a TTY only when called with no arguments (interactive mode), allowing it to also be called non-interactively from `run.sh` without a "not a TTY" error.
 
#### `docker_dataloader.sh`
Runs `utils/dataset_loader.py` inside the container. Prints dataset size, per-label distribution, and sample articles so the data can be inspected before committing to a full training run.
 
#### `version.sh`
Executed inside the container at image build time. Prints and logs the versions of all key packages (torch, transformers, datasets, etc.) to `/install/version.log`, making the image reproducible and debuggable.
 
---
 
### Modified Files
 
#### `config.py`
Added `BERT_MODEL` and `ROBERTA_MODEL` checkpoint constants alongside the existing `DEFAULT_MODEL` (DistilBERT) so alternative backbones can be referenced by name across the codebase without hardcoding strings. `RESULTS_DIR` path added for evaluation outputs in future commits.
 
#### `utils/dataset_loader.py`
Added a validation split to test and find the best fit model before saving it. Since AGNews does not have a default validation split to ensure the final evaluation is done on unseen test data. This split (90/10 train, validation) helps us achieve that.
 
#### `utils/metrics.py`
Updated import paths to reflect the new `project_files/` directory structure. No logic changes — `compute_metrics()` and `full_report()` behave identically to v1.0.
 
#### `utils/preprocessing.py`
Fixed the `sys.path` insert to correctly locate `config.py` when the script is called from inside the `utils/` subdirectory as part of the restructured project layout.
 
#### `Dockerfile`
Updated from the bare template to a full ML image:
- Base stays `python:3.12-slim`; added system packages `git`, `build-essential`, `g++`, `libgomp1`
- `COPY` path for `requirements.txt` changed to `project_files/requirements.txt`.
- Added `ENV HF_HOME=/hf_cache` and `ENV TRANSFORMERS_CACHE=/hf_cache` so all HuggingFace model downloads survive container restarts.
- Project code is not copied into the image — it is volume-mounted at runtime, so code edits require no rebuild.
#### `docker_build.sh`
Rewritten to be fully standalone — removed the dependency on the monorepo `utils.sh` via `git rev-parse`. Sources `docker_utils.sh` instead. Enables `DOCKER_BUILDKIT=1` for faster cached layer builds. Extra args (e.g. `--no-cache`) are passed through to `docker build`.
 
#### `docker_bash.sh`
Rewritten standalone. Opens an interactive bash shell inside the container with the project directory live-mounted at `/app`. Used for manual debugging and exploration.
 
#### `docker_jupyter.sh`
Rewritten standalone. Launches Jupyter Lab in a detached container with port-forwarding (`host:8888 → container:8888`). Port can be overridden via `JUPYTER_PORT` env var.
 
#### `docker_clean.sh`
Rewritten standalone. Gains a `--volumes` flag that additionally removes the `hf_cache` named volume, wiping downloaded model weights for a full clean slate.
 
#### `run_jupyter.sh`
Simplified — removed monorepo framework calls. Retains the same Jupyter flags: `--no-browser`, `--ip=0.0.0.0`, `--allow-root`, no token/password.