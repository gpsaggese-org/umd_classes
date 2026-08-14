# utils/preprocessing.py
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformers import AutoTokenizer
from config import DEFAULT_MODEL, MAX_LENGTH


# Text Cleaning

def clean_text(text: str) -> str:
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove HTML entities
    text = re.sub(r"&[a-zA-Z]+;|&#\d+;", " ", text)
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    return text.strip()


# Tokenizer Setup

def get_tokenizer(model_name: str = DEFAULT_MODEL):
    """
    Load a HuggingFace AutoTokenizer
    Parameters: model_name [HuggingFace model hub ID (like 'distilbert-base-uncased')]
    Returns: PreTrainedTokenizer
    """
    print(f"[preprocessing] Loading tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer


# Tokenization Pipeline

def make_tokenize_fn(tokenizer, max_length: int = MAX_LENGTH):
    # Creates dataset.map() -> ready tokenizer that cleans text, pads/truncates to max_length,
    # Returns input_ids, attention_mask (token_type_ids for BERT).
    def tokenize_fn(examples):
        # Clean all texts in the batch
        cleaned = [clean_text(t) for t in examples["text"]]
        # Tokenize
        encoded = tokenizer(
            cleaned,
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )
        return encoded

    return tokenize_fn


def tokenize_dataset(dataset, tokenizer, max_length: int = MAX_LENGTH):

    #Apply tokenization to an entire HuggingFace DatasetDict.
    #Returns a tokenized_dataset : DatasetDict
    print(f"[preprocessing] Tokenizing dataset (max_length={max_length})...")
    tokenize_fn = make_tokenize_fn(tokenizer, max_length)

    tokenized = dataset.map(
        tokenize_fn,
        batched=True,
        desc="Tokenizing",
        remove_columns=["text"],   # keep 'label', add token columns
    )

    # Set output format for PyTorch
    tokenized.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
    print("[preprocessing] Tokenization complete.")
    return tokenized


# Quick test

if __name__ == "__main__":
    sample = "  NASA launches <b>new</b> satellite &amp; rover into orbit.  https://nasa.gov  "
    print("Raw   :", repr(sample))
    print("Clean :", repr(clean_text(sample)))

    tok = get_tokenizer()
    fn = make_tokenize_fn(tok)
    result = fn({"text": [sample]})
    print("Tokens:", result["input_ids"])
