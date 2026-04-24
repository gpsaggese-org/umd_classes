"""
Re-extract Java from the raw outputs saved in the latest spike JSON,
using a fixed extractor that handles lopsided code fences.

The original extractor in ai_technical_debt_utils.py returns an empty
string when the model produces code followed only by a closing fence
(no opening fence). This script patches around that without touching
the MVP utils.
"""

import glob
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path("/data")
sys.path.insert(0, str(PROJECT_ROOT))
import ai_technical_debt_utils as utils  # noqa: E402

def _strip_leading_imports(text: str) -> str:
    """Strip leading import/package lines and blank lines."""
    lines = text.split("\n")
    while lines and (
        lines[0].strip().startswith("import ")
        or lines[0].strip().startswith("package ")
        or not lines[0].strip()
    ):
        lines.pop(0)
    return "\n".join(lines)


def extract_java_fixed(response: str) -> str:
    """Fixed version that handles asymmetric fences and leading imports."""
    text = response.strip()

    # Case 1 and 2: explicit java fence.
    if "```java" in text:
        after = text.split("```java", 1)[1]
        if "```" in after:
            inner = after.split("```", 1)[0].strip()
        else:
            inner = after.strip()
        return _strip_leading_imports(inner).strip()

    # Case 3: plain fence with no java marker.
    if text.startswith("```"):
        text = text[3:].lstrip()
    if text.rstrip().endswith("```"):
        idx = text.rstrip().rfind("```")
        text = text[:idx].rstrip()
    if text.endswith("```"):
        text = text[:-3].rstrip()

    return _strip_leading_imports(text).strip()


def reprocess(record: dict) -> dict:
    """Re-extract and re-evaluate a single record from the spike JSON."""
    raw = record.get("generated_raw") or ""
    input_code = record.get("input_code") or ""

    clean = extract_java_fixed(raw)

    # Re-validate Java syntax.
    syntax = utils.validate_java_syntax(clean)
    is_valid = syntax["is_valid"]
    syntax_err = syntax["error"]

    # Re-compute BLEU against the input (pseudo-reference).
    if input_code:
        bleu = utils.compute_bleu_against_reference(clean, input_code)
        exact = utils.is_exact_match(clean, input_code)
    else:
        bleu = None
        exact = False

    # Recompute confidence.
    confidence = utils.compute_confidence_score(is_valid, exact, bleu or 0.0)

    record["generated_clean_fixed"] = clean
    record["is_valid_java_fixed"] = is_valid
    record["syntax_error_fixed"] = syntax_err
    record["bleu_vs_input_fixed"] = bleu
    record["exact_match_vs_input_fixed"] = exact
    record["confidence_fixed"] = confidence
    return record


def main():
    path = sorted(
        glob.glob("outputs/spike_q1_Qwen_Qwen2.5-Coder-0.5B-Instruct_*.json")
    )[-1]
    print(f"Reprocessing: {path}")
    data = json.load(open(path))
    for r in data["records"]:
        reprocess(r)

    # Save a new file with _reextracted suffix.
    out_path = path.replace(".json", "_reextracted.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved reextracted: {out_path}")

    # Print new summary table.
    print("\n" + "=" * 95)
    print("SPIKE Q1 SUMMARY (after fence fix)")
    print("=" * 95)
    print(
        f"{'method':<18} {'strategy':<22} "
        f"{'orig_valid':<11} {'orig_bleu':<10} "
        f"{'fix_valid':<10} {'fix_bleu':<10} {'fix_conf':<8}"
    )
    print("-" * 95)
    for r in data["records"]:
        ob = (
            f"{r['bleu_vs_input']:.1f}"
            if r["bleu_vs_input"] is not None
            else "n/a"
        )
        fb = (
            f"{r['bleu_vs_input_fixed']:.1f}"
            if r["bleu_vs_input_fixed"] is not None
            else "n/a"
        )
        fc = (
            r["confidence_fixed"].get("level")
            if r["confidence_fixed"]
            else "n/a"
        )
        print(
            f"{r['method_name']:<18} {r['strategy']:<22} "
            f"{str(r['is_valid_java']):<11} {ob:<10} "
            f"{str(r['is_valid_java_fixed']):<10} {fb:<10} {fc:<8}"
        )
    print("=" * 95)


if __name__ == "__main__":
    main()
