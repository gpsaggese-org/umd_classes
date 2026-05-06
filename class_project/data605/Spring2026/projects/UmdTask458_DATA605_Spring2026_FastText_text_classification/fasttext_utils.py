"""
fasttext_utils.py

Utility functions for FastText text classification project.
Provides reusable functions for data preprocessing, model training,
evaluation, and visualization.
"""
import re
import time
import fasttext
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix


def clean_text(text):
    """
    Clean and normalize text for FastText training.
    
    Removes special characters, converts to lowercase, and strips
    extra whitespace to produce consistent input for the model.
    
    Args:
        text (str): Raw input text.
    
    Returns:
        str: Cleaned and normalized text.
    """
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def prepare_fasttext_data(data, filename):
    """
    Convert sklearn dataset to FastText supervised format and save to file.
    
    FastText expects one sample per line in the format:
    __label__<category> <text>
    
    Args:
        data: sklearn Bunch object with .data and .target attributes.
        filename (str): Output file path.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for text, label in zip(data.data, data.target):
            clean = clean_text(text)
            category = data.target_names[label].replace(' ', '_')
            f.write(f"__label__{category} {clean}\n")
    print(f"Saved {len(data.data)} samples to {filename}")


def train_fasttext_model(train_path, epoch=25, lr=0.5, word_ngrams=2, min_count=1, verbose=0):
    """
    Train a supervised FastText classification model.
    
    Args:
        train_path (str): Path to FastText-formatted training file.
        epoch (int): Number of training epochs.
        lr (float): Learning rate.
        word_ngrams (int): Maximum word n-gram size.
        min_count (int): Minimum word frequency threshold.
        verbose (int): Verbosity level.
    
    Returns:
        tuple: (model, training_time_seconds)
    """
    start = time.time()
    model = fasttext.train_supervised(
        input=train_path,
        epoch=epoch,
        lr=lr,
        wordNgrams=word_ngrams,
        minCount=min_count,
        verbose=verbose
    )
    elapsed = time.time() - start
    return model, elapsed


def evaluate_model(model, test_path):
    """
    Evaluate a FastText model and return precision, recall, and F1.
    
    Args:
        model: Trained FastText model.
        test_path (str): Path to FastText-formatted test file.
    
    Returns:
        dict: Dictionary with precision, recall, and f1 scores.
    """
    results = model.test(test_path)
    f1 = 2 * results[1] * results[2] / (results[1] + results[2])
    return {
        "samples": results[0],
        "precision": round(results[1], 4),
        "recall": round(results[2], 4),
        "f1": round(f1, 4)
    }


def get_predictions(model, texts, clean_fn):
    """
    Generate predicted labels for a list of texts.
    
    Args:
        model: Trained FastText model.
        texts (list): List of raw text strings.
        clean_fn (callable): Text cleaning function.
    
    Returns:
        list: Predicted category labels.
    """
    predicted = []
    for text in texts:
        clean = clean_fn(text)
        labels, _ = model.predict(clean)
        label = labels[0].replace('__label__', '').replace('_', '.')
        predicted.append(label)
    return predicted


def plot_confusion_matrix(true_labels, predicted_labels, category_names, title, save_path, cmap='Blues'):
    """
    Plot and save a confusion matrix heatmap.
    
    Args:
        true_labels (list): Ground truth labels.
        predicted_labels (list): Model predicted labels.
        category_names (list): List of category names.
        title (str): Plot title.
        save_path (str): File path to save the figure.
        cmap (str): Colormap for the heatmap.
    """
    cm = confusion_matrix(true_labels, predicted_labels, labels=category_names)
    plt.figure(figsize=(16, 14))
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap,
                xticklabels=category_names,
                yticklabels=category_names)
    plt.title(title, fontsize=14)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Confusion matrix saved to {save_path}")


def plot_tuning_results(results_list, save_path):
    """
    Plot hyperparameter tuning results as a bar chart.
    
    Args:
        results_list (list): List of dicts with tuning results.
        save_path (str): File path to save the figure.
    """
    labels = [f"e={r['epoch']},lr={r['lr']},ng={r['wordNgrams']}" for r in results_list]
    f1_scores = [r['f1'] for r in results_list]
    colors = ['#F44336', '#2196F3', '#4CAF50', '#FF9800', '#9C27B0']

    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, f1_scores, color=colors[:len(labels)])
    plt.title('FastText Hyperparameter Tuning Results', fontsize=14)
    plt.xlabel('Configuration', fontsize=12)
    plt.ylabel('F1 Score', fontsize=12)
    plt.ylim(0, 0.8)
    for bar, score in zip(bars, f1_scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{score:.4f}', ha='center', fontsize=10)
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Tuning plot saved to {save_path}")


def plot_model_comparison(model_names, f1_scores, train_times, save_path):
    """
    Plot F1 score and training time comparison across models.
    
    Args:
        model_names (list): List of model name strings.
        f1_scores (list): F1 scores for each model.
        train_times (list): Training times in seconds for each model.
        save_path (str): File path to save the figure.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors = ['#F44336', '#4CAF50', '#2196F3']

    bars1 = ax1.bar(model_names, f1_scores, color=colors[:len(model_names)])
    ax1.set_title('F1 Score Comparison', fontsize=14)
    ax1.set_ylabel('F1 Score', fontsize=12)
    ax1.set_ylim(0, 0.8)
    for bar, score in zip(bars1, f1_scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{score:.4f}', ha='center', fontsize=11)

    bars2 = ax2.bar(model_names[:len(train_times)], train_times, color=colors[:len(train_times)])
    ax2.set_title('Training Time Comparison (seconds)', fontsize=14)
    ax2.set_ylabel('Time (seconds)', fontsize=12)
    for bar, t in zip(bars2, train_times):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{t:.2f}s', ha='center', fontsize=11)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Comparison plot saved to {save_path}")