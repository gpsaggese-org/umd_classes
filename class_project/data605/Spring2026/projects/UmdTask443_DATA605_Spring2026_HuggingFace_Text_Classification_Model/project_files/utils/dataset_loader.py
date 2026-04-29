#Data Loading

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets import load_dataset
import pandas as pd
from config import (
    DATASET_NAME, LABEL_NAMES, ID2LABEL,
    TRAIN_SUBSET, EVAL_SUBSET, SEED
)


def load_ag_news():

    #Load the AG News dataset from HuggingFace hub
    #Each split has columns: 'text', 'label'

    print(f"Loading '{DATASET_NAME}' from HuggingFace")
    dataset = load_dataset(DATASET_NAME)
    print(f"Train size : {len(dataset['train']):,}")
    print(f"Test size  : {len(dataset['test']):,}")
    return dataset


def get_subsets(dataset):
    if TRAIN_SUBSET:
        dataset["train"] = dataset["train"].shuffle(seed=SEED).select(range(TRAIN_SUBSET))
        print(f"Using train subset: {TRAIN_SUBSET}")
    if EVAL_SUBSET:
        dataset["test"] = dataset["test"].shuffle(seed=SEED).select(range(EVAL_SUBSET))
        print(f"Using test subset: {EVAL_SUBSET}")
    return dataset


def summarize_dataset(dataset):
    
    # Print summary
    print("\nDataset Summary:")
    for split_name, split in dataset.items():
        df = pd.DataFrame(split)
        print(f"\n  Split: {split_name}  ({len(df):,} examples)")
        counts = df["label"].value_counts().sort_index()
        for label_id, count in counts.items():
            label_name = ID2LABEL[label_id]
            bar = "█" * (count // 1000)
            print(f"    [{label_id}] {label_name:<12} {count:>6,}  {bar}")
    print("─" * 52 + "\n")


def get_sample_articles(dataset, n=3, split="train"):
    
    # Return n random sample articles with their labels
    indices = random.sample(range(len(dataset[split])), n)
    samples = dataset[split].select(indices)
    print(f"\n{n} Sample Articles from '{split}' split")
    for i, row in enumerate(samples):
        label_name = ID2LABEL[row["label"]]
        print(f"\n  [{i+1}] Label: {label_name}")
        print(f"  Text : {row['text'][:200]}...")
    print("─" * 52 + "\n")
    return samples


if __name__ == "__main__":
    dataset = load_ag_news()
    dataset = get_subsets(dataset)
    summarize_dataset(dataset)
    get_sample_articles(dataset)
