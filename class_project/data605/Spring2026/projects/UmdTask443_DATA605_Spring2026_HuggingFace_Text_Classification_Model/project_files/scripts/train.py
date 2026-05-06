"""
What this script does

1. Loads AG News dataset and applies the preprocessing pipeline.
2. Instantiates a pre-trained DistilBERT model with a classification head
   (AutoModelForSequenceClassification).
3. Configures HuggingFace Trainer with TrainingArguments.
4. Saves the best checkpoint(model)
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformers import (
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
import torch

from config import (
    DEFAULT_MODEL, OUTPUT_DIR, EPOCHS, BATCH_SIZE,
    LEARNING_RATE, WEIGHT_DECAY, WARMUP_STEPS,
    NUM_LABELS, LABEL_NAMES, ID2LABEL, LABEL2ID, SEED,
)
from utils.dataset_loader import load_ag_news, get_subsets
from utils.preprocessing import get_tokenizer, tokenize_dataset
from utils.metrics import compute_metrics


def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune a transformer for news classification.")
    parser.add_argument(
        "--model", type=str, default=DEFAULT_MODEL,
        help="HuggingFace model checkpoint to fine-tune."
    )
    parser.add_argument(
        "--output_dir", type=str, default=None,
        help="Where to save the fine-tuned model. Defaults to config OUTPUT_DIR."
    )
    parser.add_argument(
        "--epochs", type=int, default=EPOCHS,
        help="Number of training epochs."
    )
    parser.add_argument(
        "--batch_size", type=int, default=BATCH_SIZE,
        help="Per-device batch size."
    )
    parser.add_argument(
        "--lr", type=float, default=LEARNING_RATE,
        help="Peak learning rate."
    )
    return parser.parse_args()


def build_model(model_name: str):
    """
    Load a pre-trained transformer model with a sequence classification head.
    """
    print(f"\n[train] Loading model: {model_name}")
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=NUM_LABELS,
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )
    total_params = sum(p.numel() for p in model.parameters())
    trainable   = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[train] Total params    : {total_params:,}")
    print(f"[train] Trainable params: {trainable:,}")
    return model


def build_training_args(output_dir: str, epochs: int, batch_size: int, lr: float):
    """
    Configure HuggingFace TrainingArguments.

    - evaluation_strategy = "epoch"  → evaluate on val set after every epoch
    - load_best_model_at_end = True  → restore best checkpoint after training
    - metric_for_best_model = "f1_macro"
    """
    use_fp16 = torch.cuda.is_available()
    return TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size * 2,
        learning_rate=lr,
        weight_decay=WEIGHT_DECAY,
        warmup_steps=WARMUP_STEPS,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        logging_dir=os.path.join(output_dir, "logs"),
        logging_steps=100,
        seed=SEED,
        fp16=use_fp16,
        report_to="none",
    )


def main():
    args = parse_args()
    model_name = args.model
    out_dir    = args.output_dir or OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    #Load & preprocess data
    dataset   = load_ag_news()
    dataset   = get_subsets(dataset)
    tokenizer = get_tokenizer(model_name)
    tokenized = tokenize_dataset(dataset, tokenizer)

    train_ds = tokenized["train"]
    eval_ds  = tokenized["validation"]

    #Build model
    model = build_model(model_name)

    #Configure training
    training_args = build_training_args(out_dir, args.epochs, args.batch_size, args.lr)

    # DataCollatorWithPadding pads each batch to its longest sequence
    # (more efficient than global max_length padding)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    #Train
    trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    processing_class=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

    print(f"\n[train] Starting fine-tuning — {args.epochs} epoch(s)...")
    trainer.train()

    # ── Step 5: Save best model ─────────────────────────────────────────────────
    best_path = os.path.join(out_dir, "best")
    trainer.save_model(best_path)
    tokenizer.save_pretrained(best_path)
    print(f"\n[train] Best model saved to: {best_path}")

    # Save training metrics summary
    metrics_path = os.path.join(out_dir, "train_results.txt")
    with open(metrics_path, "w") as f:
        f.write(f"Model: {model_name}\n")
        f.write(f"Epochs: {args.epochs}\n")
        f.write(f"Batch size: {args.batch_size}\n")
        f.write(f"Learning rate: {args.lr}\n\n")
        for log in trainer.state.log_history:
            f.write(str(log) + "\n")
    print(f"[train] Training log saved to: {metrics_path}")


if __name__ == "__main__":
    main()