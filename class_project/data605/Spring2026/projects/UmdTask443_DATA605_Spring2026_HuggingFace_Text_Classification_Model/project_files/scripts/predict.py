# scripts/predict.py
"""
COMMIT 2 — Inference
======================
Run the fine-tuned model on custom text input.

Usage
-----
    python scripts/predict.py --text "Apple reports record iPhone sales"
    python scripts/predict.py --file articles.txt    # one article per line
    python scripts/predict.py                        # interactive mode
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config import OUTPUT_DIR, MAX_LENGTH, ID2LABEL
from utils.preprocessing import clean_text


def load_model(model_dir: str):
    """
    Load a fine-tuned model and tokenizer from disk.
    Falls back to the HuggingFace hub if local path not found.
    """
    best_path = os.path.join(model_dir, "best")
    load_path = best_path if os.path.isdir(best_path) else model_dir

    if not os.path.isdir(load_path):
        print(f"[predict] ⚠️  Model not found at '{load_path}'.")
        print("[predict] Please run `python scripts/train.py` first.")
        sys.exit(1)

    print(f"[predict] Loading model from: {load_path}")
    tokenizer = AutoTokenizer.from_pretrained(load_path)
    model = AutoModelForSequenceClassification.from_pretrained(load_path)
    model.eval()
    return tokenizer, model


def predict(texts, tokenizer, model, device="cpu"):
    """
    Predict category labels for a list of texts.

    Returns
    -------
    results : list of dict
        Each dict has 'text', 'label', 'confidence', 'all_scores'
    """
    cleaned = [clean_text(t) for t in texts]
    inputs = tokenizer(
        cleaned,
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()

    results = []
    for text, prob_row in zip(texts, probs):
        pred_id = prob_row.argmax()
        results.append({
            "text": text[:120] + "..." if len(text) > 120 else text,
            "label": ID2LABEL[pred_id],
            "confidence": round(float(prob_row[pred_id]) * 100, 2),
            "all_scores": {ID2LABEL[i]: round(float(p) * 100, 2) for i, p in enumerate(prob_row)},
        })
    return results


def display_results(results):
    for i, r in enumerate(results, 1):
        print(f"\n── Result {i} {'─'*45}")
        print(f"  Text       : {r['text']}")
        print(f"  Prediction : {r['label']}  ({r['confidence']}% confidence)")
        print(f"  All scores :")
        for label, score in sorted(r["all_scores"].items(), key=lambda x: -x[1]):
            bar = "▓" * int(score // 5)
            print(f"    {label:<12} {score:>6.2f}%  {bar}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default=None, help="Article text to classify.")
    parser.add_argument("--file", type=str, default=None, help="Path to a text file (one article per line).")
    parser.add_argument("--model_dir", type=str, default=OUTPUT_DIR, help="Directory of the fine-tuned model.")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer, model = load_model(args.model_dir)
    model = model.to(device)

    if args.text:
        texts = [args.text]
    elif args.file:
        with open(args.file) as f:
            texts = [line.strip() for line in f if line.strip()]
    else:
        print("[predict] Interactive mode — type an article and press Enter (Ctrl+C to quit).")
        texts = []
        while True:
            try:
                t = input("\n📰 Article: ").strip()
                if t:
                    results = predict([t], tokenizer, model, device)
                    display_results(results)
            except KeyboardInterrupt:
                print("\nBye!")
                break
        return

    results = predict(texts, tokenizer, model, device)
    display_results(results)


if __name__ == "__main__":
    main()