# utils/metrics.py
"""
  - compute_metrics()  →  used as callback during HuggingFace Trainer training
  - full_report()      →  detailed sklearn classification report

These are separated from the training script to keep concerns clean and allow
the same metric logic to be reused across multiple models in Commit 4.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
import evaluate  # HuggingFace evaluate library


# Load HuggingFace accuracy metric (used inside Trainer)
_hf_accuracy = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    """
    Callback passed to HuggingFace Trainer.
    Called at the end of every evaluation step.

    Parameters
    ----------
    eval_pred : EvalPrediction
        .predictions  → raw logits, shape (N, num_labels)
        .label_ids    → true labels, shape (N,)

    Returns
    -------
    dict with keys: 'accuracy', 'f1_macro'
    """
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    acc = _hf_accuracy.compute(predictions=predictions, references=labels)["accuracy"]
    f1  = f1_score(labels, predictions, average="macro")

    return {
        "accuracy": round(acc, 4),
        "f1_macro": round(f1, 4),
    }


def full_report(y_true, y_pred, label_names):
    """
    Generate a detailed classification report and confusion matrix.

    Parameters
    ----------
    y_true      : list or np.ndarray of true label IDs
    y_pred      : list or np.ndarray of predicted label IDs
    label_names : list of str  (e.g. ['World', 'Sports', 'Business', 'Sci/Tech'])

    Returns
    -------
    report : str   (sklearn classification_report string)
    cm     : np.ndarray  (confusion matrix)
    """
    report = classification_report(y_true, y_pred, target_names=label_names, digits=4)
    cm = confusion_matrix(y_true, y_pred)
    return report, cm
