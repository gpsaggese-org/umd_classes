# scripts/evaluate.py
"""
1. Loads the fine-tuned model from models/distilbert-ag-news/best/
2. Runs batch inference over the full test set
3. Computes accuracy, macro F1, per-class precision/recall/F1
4. Saves the below to results/:
     - classification_report.txt
     - confusion_matrix.png
     - per_class_metrics.png
     - predictions.csv
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
)
from tqdm import tqdm
import matplotlib
matplotlib.use("Agg")   # non-interactive backend — works inside Docker
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, f1_score

from config import OUTPUT_DIR, RESULTS_DIR, LABEL_NAMES, ID2LABEL, BATCH_SIZE
from utils.dataset_loader import load_ag_news, get_subsets
from utils.preprocessing import tokenize_dataset
from utils.metrics import full_report

os.makedirs(RESULTS_DIR, exist_ok=True)


# Model Loading

def load_model(model_dir: str):
    """Load fine-tuned model and tokenizer from disk."""
    best_path = os.path.join(model_dir, "best")
    load_path = best_path if os.path.isdir(best_path) else model_dir
    if not os.path.isdir(load_path):
        print(f"[evaluate] Model not found at '{load_path}'.")
        print("[evaluate] Run `python scripts/train.py` first.")
        sys.exit(1)
    print(f"[evaluate] Loading model from: {load_path}")
    tokenizer = AutoTokenizer.from_pretrained(load_path)
    model     = AutoModelForSequenceClassification.from_pretrained(load_path)
    return tokenizer, model


# ─── Batch Inference ───────────────────────────────────────────────────────────

def run_inference(model, test_ds, tokenizer, device):
    """
    Run inference on the entire test split in batches.

    Returns
    -------
    y_true : np.ndarray, shape (N,)
    y_pred : np.ndarray, shape (N,)
    """
    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")
    loader   = DataLoader(test_ds, batch_size=BATCH_SIZE * 2, collate_fn=collator)

    model.eval()
    model.to(device)

    all_preds, all_labels = [], []

    with torch.no_grad():
        for batch in tqdm(loader, desc="Evaluating"):
            labels = batch.pop("labels")
            batch  = {k: v.to(device) for k, v in batch.items()}
            logits = model(**batch).logits
            preds  = torch.argmax(logits, dim=-1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.numpy())

    return np.array(all_labels), np.array(all_preds)


# ─── Plots ─────────────────────────────────────────────────────────────────────

def plot_confusion_matrix(cm, label_names, save_path):
    """Save a styled confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=label_names, yticklabels=label_names,
        linewidths=0.5, ax=ax,
    )
    ax.set_xlabel("Predicted Label", fontsize=12, labelpad=10)
    ax.set_ylabel("True Label",      fontsize=12, labelpad=10)
    ax.set_title("Confusion Matrix — AG News Test Set", fontsize=14, pad=15)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"[evaluate] Confusion matrix saved : {save_path}")


def plot_per_class_metrics(report_str, label_names, save_path):
    """Parse sklearn report string and plot per-class bars."""
    lines = report_str.strip().split("\n")
    rows  = []
    for line in lines[2: 2 + len(label_names)]:
        parts = line.split()
        if len(parts) >= 5:
            rows.append({
                "class":     parts[0],
                "Precision": float(parts[1]),
                "Recall":    float(parts[2]),
                "F1-Score":  float(parts[3]),
            })

    if not rows:
        print("[evaluate] Could not parse report for per-class chart.")
        return

    df = pd.DataFrame(rows).set_index("class")
    ax = df.plot(kind="bar", figsize=(9, 5), colormap="Set2",
                 width=0.7, edgecolor="white")
    ax.set_title("Per-Class Metrics — AG News", fontsize=14)
    ax.set_xlabel("News Category", fontsize=11)
    ax.set_ylabel("Score",         fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right")
    ax.grid(axis="y", alpha=0.4)
    plt.xticks(rotation=0)
    plt.tight_layout()
    ax.figure.savefig(save_path, dpi=150)
    plt.close(ax.figure)
    print(f"[evaluate] Per-class chart saved  : {save_path}")


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, default=OUTPUT_DIR)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[evaluate] Device: {device}")

    # Load model.
    tokenizer, model = load_model(args.model_dir)

    # Load and tokenize test data.
    dataset   = load_ag_news()
    dataset   = get_subsets(dataset)
    tokenized = tokenize_dataset(dataset, tokenizer)
    test_ds   = tokenized["test"]

    # Run inference.
    print(f"\n[evaluate] Running inference on {len(test_ds):,} test examples...")
    y_true, y_pred = run_inference(model, test_ds, tokenizer, device)

    # ── 1. Classification report ───────────────────────────────────────────────
    report, cm = full_report(y_true, y_pred, LABEL_NAMES)
    print("\n── Classification Report ─────────────────────────────────────────")
    print(report)

    report_path = os.path.join(RESULTS_DIR, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(f"Model : {args.model_dir}\n\n")
        f.write(report)
    print(f"[evaluate] Report saved           : {report_path}")

    # ── 2. Confusion matrix ────────────────────────────────────────────────────
    cm_path = os.path.join(RESULTS_DIR, "confusion_matrix.png")
    plot_confusion_matrix(cm, LABEL_NAMES, cm_path)

    # ── 3. Per-class metrics bar chart ─────────────────────────────────────────
    pc_path = os.path.join(RESULTS_DIR, "per_class_metrics.png")
    plot_per_class_metrics(report, LABEL_NAMES, pc_path)

    # ── 4. Raw predictions CSV ─────────────────────────────────────────────────
    pred_df = pd.DataFrame({
        "true_label_id": y_true,
        "pred_label_id": y_pred,
        "true_label":    [ID2LABEL[i] for i in y_true],
        "pred_label":    [ID2LABEL[i] for i in y_pred],
        "correct":       y_true == y_pred,
    })
    csv_path = os.path.join(RESULTS_DIR, "predictions.csv")
    pred_df.to_csv(csv_path, index=False)
    print(f"[evaluate] Predictions saved      : {csv_path}")

    # ── 5. Summary ────────────────────────────────────────────────────────────
    acc = accuracy_score(y_true, y_pred)
    f1  = f1_score(y_true, y_pred, average="macro")
    print(f"\n{'='*50}")
    print(f"  Final Results")
    print(f"  Accuracy  : {acc:.4f}  ({acc*100:.2f}%)")
    print(f"  F1 Macro  : {f1:.4f}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
