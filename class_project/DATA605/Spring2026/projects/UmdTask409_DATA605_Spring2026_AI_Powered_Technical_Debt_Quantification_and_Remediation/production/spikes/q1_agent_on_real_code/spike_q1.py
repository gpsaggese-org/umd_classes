"""
Q1 Spike: does the refactoring agent generalize from CodeXGLUE's abstracted
Java (TYPE_1, VAR_1 placeholders) to real Java methods from commons-lang3?

Runs Qwen2.5-Coder-0.5B-Instruct on 5 hand-picked methods from commons-lang3
under two strategies (zero-shot and few-shot retrieval), captures outputs
and metrics, and saves a JSON log for analysis.

This is an investigation, not production code. Output lives in ./outputs/
and is gitignored.
"""

import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path so we can import from ai_technical_debt_utils.
PROJECT_ROOT = Path("/data")
sys.path.insert(0, str(PROJECT_ROOT))

import ai_technical_debt_utils as utils  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("spike_q1")


# ---------------------------------------------------------------------------
# Section A: the 5 methods we're testing.
# ---------------------------------------------------------------------------
# Each entry has:
#   name: short identifier for logging
#   class_name: which commons-lang3 class it came from
#   source_line: line where the method declaration starts
#   code: the method source as a standalone Java snippet
# We hardcode the method source so the spike is reproducible even if
# commons-lang3 changes upstream.

METHODS = [
    {
        "name": "capitalize",
        "class_name": "StringUtils",
        "source_line": 536,
        "code": """public static String capitalize(final String str) {
    if (isEmpty(str)) {
        return str;
    }
    final int firstCodepoint = str.codePointAt(0);
    final int newCodePoint = Character.toTitleCase(firstCodepoint);
    if (firstCodepoint == newCodePoint) {
        // already capitalized
        return str;
    }
    final int[] newCodePoints = str.codePoints().toArray();
    newCodePoints[0] = newCodePoint; // copy the first code point
    return new String(newCodePoints, 0, newCodePoints.length);
}""",
    },
    {
        "name": "chomp",
        "class_name": "StringUtils",
        "source_line": 682,
        "code": """public static String chomp(final String str) {
    if (isEmpty(str)) {
        return str;
    }
    if (str.length() == 1) {
        final char ch = str.charAt(0);
        if (ch == CharUtils.CR || ch == CharUtils.LF) {
            return EMPTY;
        }
        return str;
    }
    int lastIdx = str.length() - 1;
    final char last = str.charAt(lastIdx);
    if (last == CharUtils.LF) {
        if (str.charAt(lastIdx - 1) == CharUtils.CR) {
            lastIdx--;
        }
    } else if (last != CharUtils.CR) {
        lastIdx++;
    }
    return str.substring(0, lastIdx);
}""",
    },
    {
        "name": "containsAny",
        "class_name": "StringUtils",
        "source_line": 1054,
        "code": """public static boolean containsAny(final CharSequence cs, final char... searchChars) {
    if (isEmpty(cs) || ArrayUtils.isEmpty(searchChars)) {
        return false;
    }
    final int csLength = cs.length();
    final int searchLength = searchChars.length;
    final int csLast = csLength - 1;
    final int searchLast = searchLength - 1;
    for (int i = 0; i < csLength; i++) {
        final char ch = cs.charAt(i);
        for (int j = 0; j < searchLength; j++) {
            if (searchChars[j] == ch) {
                if (!Character.isHighSurrogate(ch) || j == searchLast || i < csLast && searchChars[j + 1] == cs.charAt(i + 1)) {
                    return true;
                }
            }
        }
    }
    return false;
}""",
    },
    {
        "name": "isSorted",
        "class_name": "ArrayUtils",
        "source_line": 4074,
        "code": """public static <T> boolean isSorted(final T[] array, final Comparator<T> comparator) {
    Objects.requireNonNull(comparator, "comparator");
    if (getLength(array) < 2) {
        return true;
    }
    T previous = array[0];
    final int n = array.length;
    for (int i = 1; i < n; i++) {
        final T current = array[i];
        if (comparator.compare(previous, current) > 0) {
            return false;
        }
        previous = current;
    }
    return true;
}""",
    },
    {
        "name": "indexOf_double",
        "class_name": "ArrayUtils",
        "source_line": 2832,
        "code": """public static int indexOf(final double[] array, final double valueToFind, final int startIndex) {
    if (Double.isNaN(valueToFind)) {
        return indexOfNaN(array, startIndex);
    }
    if (isEmpty(array)) {
        return INDEX_NOT_FOUND;
    }
    for (int i = max0(startIndex); i < array.length; i++) {
        if (valueToFind == array[i]) {
            return i;
        }
    }
    return INDEX_NOT_FOUND;
}""",
    },
]


# ---------------------------------------------------------------------------
# Section B: model and retrieval index loading.
# ---------------------------------------------------------------------------

def load_model_and_tokenizer(model_name):
    """Load the HuggingFace causal LM and tokenizer."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    logger.info("Loading tokenizer for %s...", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    logger.info("Loading model for %s (this may take a minute)...", model_name)
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    logger.info("Model loaded in %.1fs", time.time() - t0)
    return model, tokenizer


def load_retrieval_index():
    """Load the prebuilt CodeXGLUE TF-IDF retrieval index."""
    logger.info("Loading retrieval index from cache...")
    t0 = time.time()
    index = utils.build_retrieval_index(
        cache_dir="/data/retrieval_cache",
        subset=utils.AGENT_RETRIEVAL_SUBSET,
        force_rebuild=False,
    )
    logger.info(
        "Retrieval index loaded in %.1fs (%d training pairs)",
        time.time() - t0,
        len(index["train_pairs"]),
    )
    return index


# ---------------------------------------------------------------------------
# Section C: run one method under one strategy.
# ---------------------------------------------------------------------------

def run_one(method_entry, model, tokenizer, retrieval_index, strategy):
    """Run the agent on one method under one strategy.

    strategy is either "zero_shot" or "few_shot_retrieval".
    Returns the full result dict from refactor_java_method plus metadata.
    """
    logger.info(
        "Running %s.%s with strategy=%s",
        method_entry["class_name"],
        method_entry["name"],
        strategy,
    )
    retrieval_arg = retrieval_index if strategy == "few_shot_retrieval" else None

    t0 = time.time()
    result = utils.refactor_java_method(
        buggy_code=method_entry["code"],
        model=model,
        tokenizer=tokenizer,
        retrieval_index=retrieval_arg,
        reference_code=method_entry["code"],  # use the original as pseudo-reference
        n_retrieval_examples=utils.AGENT_DEFAULT_N_RETRIEVAL_EXAMPLES,
        max_new_tokens=utils.AGENT_DEFAULT_MAX_NEW_TOKENS,
        seed=utils.AGENT_DEFAULT_SEED,
    )
    total_elapsed = time.time() - t0

    # Augment the result with our metadata for logging.
    result_record = {
        "method_name": method_entry["name"],
        "class_name": method_entry["class_name"],
        "source_line": method_entry["source_line"],
        "strategy": strategy,
        "total_elapsed_s": total_elapsed,
        "input_code": method_entry["code"],
        "generated_raw": result.get("generated_raw"),
        "generated_clean": result.get("generated_clean"),
        "is_valid_java": result.get("is_valid"),
        "syntax_error": result.get("syntax_error"),
        "bleu_vs_input": result.get("bleu"),
        "exact_match_vs_input": result.get("exact_match"),
        "confidence": result.get("confidence"),
        "strategy_used_by_agent": result.get("strategy_used"),
        "retrieved_examples_count": len(result.get("retrieved_examples", [])),
        "retrieved_similarities": [
            ex.get("similarity") for ex in result.get("retrieved_examples", [])
        ],
    }
    return result_record


# ---------------------------------------------------------------------------
# Section D: main experiment loop.
# ---------------------------------------------------------------------------

def main():
    model_name = utils.AGENT_DEFAULT_MODEL  # 0.5B from utils
    logger.info("=== Q1 spike: agent on real commons-lang3 code ===")
    logger.info("Model: %s", model_name)
    logger.info("Number of methods: %d", len(METHODS))
    logger.info("Strategies: zero_shot, few_shot_retrieval")

    model, tokenizer = load_model_and_tokenizer(model_name)
    retrieval_index = load_retrieval_index()

    all_records = []
    for method_entry in METHODS:
        for strategy in ["zero_shot", "few_shot_retrieval"]:
            record = run_one(
                method_entry, model, tokenizer, retrieval_index, strategy
            )
            all_records.append(record)

    # Save the full log to a timestamped JSON in the outputs folder.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(
        f"/data/production/spikes/q1_agent_on_real_code/outputs/"
        f"spike_q1_{model_name.replace('/', '_')}_{timestamp}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        json.dump(
            {
                "model_name": model_name,
                "timestamp": timestamp,
                "n_methods": len(METHODS),
                "records": all_records,
            },
            f,
            indent=2,
        )
    logger.info("Saved results to %s", output_path)

    # Print a summary table.
    print_summary(all_records)


def print_summary(records):
    """Print a short table of spike results."""
    print("\n" + "=" * 80)
    print("SPIKE Q1 SUMMARY")
    print("=" * 80)
    header = f"{'method':<20} {'strategy':<22} {'valid':<6} {'bleu':<7} {'time_s':<8} {'conf':<8}"
    print(header)
    print("-" * 80)
    for r in records:
        conf = r["confidence"].get("level") if r["confidence"] else "n/a"
        bleu = f"{r['bleu_vs_input']:.1f}" if r["bleu_vs_input"] is not None else "n/a"
        time_s = f"{r['total_elapsed_s']:.1f}"
        print(
            f"{r['method_name']:<20} "
            f"{r['strategy']:<22} "
            f"{str(r['is_valid_java']):<6} "
            f"{bleu:<7} "
            f"{time_s:<8} "
            f"{conf:<8}"
        )
    print("=" * 80)


if __name__ == "__main__":
    main()
