# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: .venv (3.13.7)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # DocsGPT: Intelligent Documentation Assistant
#
# This notebook builds a complete AI-powered documentation assistant step by step.
# Each part focuses on one piece of the system and shows how the code works.
#
# | Part | What it does |
# |------|--------------|
# | 1 | Load text from three real datasets |
# | 2 | Summarise each document using DocsGPT |
# | 3 | Generate FAQs from each document |
# | 4 | Score the outputs with ROUGE and BLEU |
# | 5 | Produce summaries and FAQs in other languages |
# | 6 | Show all results in a summary table |
# | 7 | Launch an interactive Gradio UI |
#
# **Setup:**
# ```bash
# ./docker_build.sh
# ./docker_jupyter.sh
# cp .env.example .env
# # Open .env and set DOCSGPT_API_KEY=your-agent-key
# ```
#

# %%
# %load_ext autoreload
# %autoreload 2

import logging
import os
import pandas as pd

import docsgpt_utils as tdgputi

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
_LOG = logging.getLogger(__name__)

BASE_URL = tdgputi.get_base_url()
API_KEY  = tdgputi.get_api_key()

print(f"Base URL : {BASE_URL}")
print(f"API key  : {API_KEY[:10]}***  (truncated for safety)")
print("Environment ready ✓")

# %% [markdown]
# ---
#
# ## Part 1: Data Collection
#
# We load text from three sources. Each one is handled by a function in
# `docsgpt_utils.py` that fetches the data and returns plain text.
#
# - **`fetch_awesome_ml_readme()`** — downloads the raw markdown file from GitHub
#   using `requests.get()`. `parse_awesome_ml_sections()` then splits it into a
#   dict of `{section_title: body_text}` by scanning for `## ` heading lines.
#   `clean_markdown()` strips all markdown syntax (links, bullets, code blocks)
#   so we're left with plain prose the LLM can read cleanly.
#
# - **`load_stackoverflow_sample()`** — connects to HuggingFace Hub and streams
#   rows one at a time using `datasets.load_dataset(..., streaming=True)`. Only
#   the first `n_rows` rows are read — the full dataset is never downloaded.
#   `so_rows_to_text()` combines the title, body, and answer of each row into
#   one readable block of text.
#
# - **`load_pile_sample()`** — streams The Pile dataset the same way, collecting
#   rows until we have enough characters.
#
# All three functions fall back to built-in sample data if the network is
# unavailable, so the notebook always keeps running.
#

# %%
# ── 1a. Awesome Machine Learning (GitHub README) ───────────────────────────
# fetch_awesome_ml_readme() downloads the raw markdown from GitHub.
# parse_awesome_ml_sections() splits it into a dict: {section_title: body}
# clean_markdown() strips all markdown syntax → plain prose for the LLM.

print("=" * 60)
print("1a. Fetching Awesome Machine Learning README from GitHub...")

raw_md   = tdgputi.fetch_awesome_ml_readme()
sections = tdgputi.parse_awesome_ml_sections(raw_md)

print(f"    Total chars   : {len(raw_md):,}")
print(f"    Sections found: {len(sections)}")
print(f"    Section names : {list(sections.keys())[:6]} ...")

# Pick the largest content-rich section to give the LLM something meaty
content_sections = {k: v for k, v in sections.items() if len(v) > 500}
aml_title = sorted(content_sections, key=lambda k: len(content_sections[k]), reverse=True)[0]
aml_text  = tdgputi.clean_markdown(content_sections[aml_title])

print(f"    Selected      : '{aml_title}'")
print(f"    Clean text    : {len(aml_text):,} chars")
print(f"    Preview       : {aml_text[:200]}...")

# %%
# ── 1b. Stack Overflow Questions (HuggingFace Hub, streaming) ──────────────
# load_stackoverflow_sample() uses the HuggingFace `datasets` library with
# streaming=True so we never download the full dataset — just the first N rows.
#
# so_rows_to_text() combines title + body + answer into one readable document
# per question, then joins them all with --- separators.

print("1b. Loading Stack Overflow questions from HuggingFace Hub...")
print("    (uses streaming — no full download needed)")

so_rows = tdgputi.load_stackoverflow_sample(n_rows=10)
so_text = tdgputi.so_rows_to_text(so_rows)

print(f"\n    Rows loaded   : {len(so_rows)}")
print(f"    Combined chars: {len(so_text):,}")
print(f"    First question: {so_rows[0]['title']}")
print(f"    First answer  : {so_rows[0]['answer'][:100]}...")

# %%
# ── 1c. The Pile — uncopyrighted subset (HuggingFace Hub, streaming) ───────
# The Pile is a large-scale dataset of diverse text. We use the uncopyrighted
# subset for safety. Again we stream just enough characters rather than
# downloading the whole thing.

print("1c. Streaming a sample from The Pile (uncopyrighted subset)...")

pile_text = tdgputi.load_pile_sample(n_chars=8000)

print(f"    Collected : {len(pile_text):,} chars")
print(f"    Preview   : {pile_text[:200]}...")

# ── Package everything into a named dict for the rest of the notebook ───────
SOURCE_TEXTS = {
    "Awesome ML":    aml_text,
    "Stack Overflow": so_text,
    "The Pile":       pile_text,
}

print("\n📦 All datasets ready:")
for label, text in SOURCE_TEXTS.items():
    print(f"   • {label}: {len(text):,} chars")

# %% [markdown]
# ---
#
# ## Part 2: Text Summarisation
#
# `summarize_document()` takes a block of text and sends it to DocsGPT to
# get a summary. Here is what happens inside the function:
#
# 1. `truncate_text()` cuts the text to 4000 characters so it fits in the prompt
# 2. The text is placed inside a prompt string that instructs DocsGPT to
#    summarise it in a certain number of words
# 3. That prompt is sent to `POST /api/answer` via `query_docsgpt()`
# 4. The `"answer"` field from the JSON response is returned as the summary
#
# The loop below runs this for each of the three datasets and stores the
# results in a `summaries` dict keyed by dataset name.
#

# %%
# ── Summarise each dataset source ──────────────────────────────────────────
# summarize_document() builds the prompt, calls POST /api/answer, and returns
# the 'answer' field from the JSON response.

summaries: dict = {}

for label, text in SOURCE_TEXTS.items():
    print(f"\n{'='*60}")
    print(f"📄 Summarising: {label}  ({len(text):,} chars → truncated to 4000)")

    truncated = tdgputi.truncate_text(text, max_chars=4000)

    summary = tdgputi.summarize_document(
        truncated,
        API_KEY,
        BASE_URL,
        max_words=200,
        source_label=label,
    )
    summaries[label] = summary
    word_count = len(summary.split())
    print(f"\n✅ Summary ({word_count} words):")
    print(summary)

print(f"\n\n🎉 All {len(summaries)} summaries generated!")

# %% [markdown]
# ---
#
# ## Part 3: FAQ Generation
#
# `generate_faqs()` works the same way as summarisation — it embeds the
# document text in a prompt and sends it to `POST /api/answer`. The prompt
# instructs DocsGPT to format the output as:
#
# ```
# Q: <question>
# A: <answer>
# ```
#
# Once the response comes back, `parse_faqs()` processes the raw text:
# 1. Splits the text on `Q:` markers using `re.split()`
# 2. For each block, extracts the question with a `re.search()` for `Q: ...`
#    and the answer with a search for `A: ...`
# 3. Returns a list of `{"question": ..., "answer": ...}` dicts
#
# `print_faqs()` then formats and prints each pair.
#

# %%
# ── Generate FAQs for each dataset source ─────────────────────────────────
# generate_faqs() sends a structured prompt to /api/answer requesting
# exactly n_questions FAQs in Q:/A: format, then calls parse_faqs() on the result.

all_faqs: dict = {}

for label, text in SOURCE_TEXTS.items():
    print(f"\n{'='*60}")
    print(f"❓ Generating FAQs: {label}")

    truncated = tdgputi.truncate_text(text, max_chars=4000)

    faqs = tdgputi.generate_faqs(
        truncated,
        API_KEY,
        BASE_URL,
        n_questions=4,
        source_label=label,
    )
    all_faqs[label] = faqs

    print(f"\n✅ Generated {len(faqs)} FAQs:")
    tdgputi.print_faqs(faqs)

print(f"\n\n🎉 FAQ generation complete for all {len(all_faqs)} sources!")

# %% [markdown]
# ---
#
# ## Part 4: Evaluation — ROUGE and BLEU
#
# We score each generated summary and FAQ answer against the original source
# text to measure how well the content was captured.
#
# **`rouge_scores(hypothesis, reference)`** uses the `rouge_score` library to
# compute three variants of ROUGE:
# - **ROUGE-1**: counts how many individual words overlap
# - **ROUGE-2**: counts how many two-word pairs overlap
# - **ROUGE-L**: finds the longest matching sequence of words in order
#
# All three are F1 scores (0 to 1). A higher number means more overlap
# with the reference text.
#
# **`bleu_score(hypothesis, reference)`** uses NLTK to compute BLEU, which
# measures how precisely the generated text matches n-grams in the reference.
# It also penalises outputs that are too short.
#
# **`evaluate_all()`** runs both metrics for every dataset. It uses the first
# 500 characters of each source as the reference, scores the summary, then
# scores the first FAQ answer, and collects everything into a results dict.
#

# %%
# ── Evaluate all summaries and FAQs ────────────────────────────────────────
# evaluate_all() runs evaluate_output() for each document label.
# evaluate_output() calls rouge_scores() and bleu_score() internally.
# The reference for each document is its first 500 chars.

print("📊 Running ROUGE + BLEU evaluation...\n")

eval_results = tdgputi.evaluate_all(summaries, all_faqs, SOURCE_TEXTS)

for label, scores in eval_results.items():
    print(f"\n[{label}]")
    print(f"  Summary scores:")
    print(f"    ROUGE-1 : {scores.get('rouge1', 0):.4f}")
    print(f"    ROUGE-2 : {scores.get('rouge2', 0):.4f}")
    print(f"    ROUGE-L : {scores.get('rougeL', 0):.4f}")
    print(f"    BLEU    : {scores.get('bleu',   0):.4f}")
    if 'faq_rouge1' in scores:
        print(f"  FAQ answer scores (first FAQ):")
        print(f"    ROUGE-1 : {scores.get('faq_rouge1', 0):.4f}")
        print(f"    BLEU    : {scores.get('faq_bleu',   0):.4f}")

# %% [markdown]
# ---
#
# ## Part 5: Multi-Language Support
#
# `summarize_multilang()` and `generate_faqs_multilang()` produce output in
# any of the 9 supported languages by running translation before and after
# the DocsGPT call.
#
# **`translate_text(text, source, target)`** uses the `deep-translator`
# library which calls the Google Translate API. If the text is longer than
# 4500 characters (Google's limit per request), the function splits it on
# sentence boundaries using `re.split()`, translates each batch separately,
# then joins the results back together.
#
# The full pipeline for `summarize_multilang()` is:
# 1. If the source language is not English, translate the input text to English
# 2. Call `summarize_document()` to get an English summary from DocsGPT
# 3. If the output language is not English, translate the summary to the target
# 4. Return both the English and translated summaries in a dict
#
# `generate_faqs_multilang()` follows the same pipeline but translates each
# FAQ question and answer individually.
#

# %%
# ── Multi-language summarisation demo ──────────────────────────────────────
print("🌍 Supported languages:")
for code, name in tdgputi.list_supported_languages().items():
    print(f"   {code}: {name}")

# Use the Stack Overflow text for this demo
demo_text   = tdgputi.truncate_text(SOURCE_TEXTS["Stack Overflow"], max_chars=2000)
target_langs = ["es", "fr", "de"]

multilang_results = {}

for lang_code in target_langs:
    lang_name = tdgputi.SUPPORTED_LANGUAGES[lang_code]
    print(f"\n{'='*55}")
    print(f"🌐 Target: {lang_name} ({lang_code})")

    result = tdgputi.summarize_multilang(
        demo_text,
        API_KEY,
        source_lang="en",
        output_lang=lang_code,
        base_url=BASE_URL,
        max_words=100,
        source_label=f"so_{lang_code}",
    )
    multilang_results[lang_code] = result

    print(f"\n[English summary]")
    print(result['english_summary'])
    print(f"\n[{lang_name} translation]")
    print(result['translated_summary'])

print("\n\n✅ Multi-language summaries complete!")

# %% [markdown]
# ---
#
# ## Part 6: Results Dashboard
#
# This cell collects all the outputs generated so far — summaries, FAQ counts,
# and evaluation scores — and arranges them into a pandas DataFrame.
#
# Each row represents one dataset. The columns show the number of FAQs
# generated, a preview of the summary, and the four metric scores.
# `pd.set_option()` controls how wide the summary preview column is and how
# many decimal places the scores display.
#

# %%
# ── Results dashboard ──────────────────────────────────────────────────────
rows = []
for label in SOURCE_TEXTS:
    scores  = eval_results.get(label, {})
    n_faqs  = len(all_faqs.get(label, []))
    summary = summaries.get(label, "")
    rows.append({
        "Document":  label,
        "# FAQs":    n_faqs,
        "Summary preview": (summary[:80] + "...") if len(summary) > 80 else summary,
        "ROUGE-1":   scores.get("rouge1", 0.0),
        "ROUGE-2":   scores.get("rouge2", 0.0),
        "ROUGE-L":   scores.get("rougeL", 0.0),
        "BLEU":      scores.get("bleu",   0.0),
    })

dashboard = pd.DataFrame(rows).set_index("Document")
pd.set_option("display.max_colwidth", 85)
pd.set_option("display.float_format", "{:.4f}".format)

print("=" * 70)
print("       DocsGPT Documentation Assistant — Results Dashboard")
print("=" * 70)
print(dashboard.to_string())
print("=" * 70)

best_rouge  = dashboard["ROUGE-1"].idxmax()
best_bleu   = dashboard["BLEU"].idxmax()
print(f"\n🏆 Best ROUGE-1 : {best_rouge}  ({dashboard.loc[best_rouge, 'ROUGE-1']:.4f})")
print(f"🏆 Best BLEU    : {best_bleu}  ({dashboard.loc[best_bleu, 'BLEU']:.4f})")

# %% [markdown]
# ---
#
# ## Part 7: Gradio User Interface
#
# This cell builds an interactive web UI using Gradio. When a user clicks
# the Generate button, the `run_docsgpt_ui()` function runs:
#
# 1. Truncates the input text to 3500 characters
# 2. Calls `summarize_multilang()` to get a summary in the selected language
# 3. Calls `generate_faqs_multilang()` to get FAQs in the selected language
# 4. Calls `evaluate_output()` to compute ROUGE and BLEU scores for the summary
# 5. Returns all three results to the UI components
#
# `gr.Blocks()` defines the layout — a text input, a language dropdown, a
# slider for FAQ count, and three output areas. `submit_btn.click()` wires
# the button to the function, specifying which inputs to read and which
# outputs to update.
#
# Run the cell, then open **http://127.0.0.1:7860** in your browser.
#

# %%
# ── Gradio UI ──────────────────────────────────────────────────────────────
import gradio as gr


def run_docsgpt_ui(document_text: str, output_language: str, n_faqs: int) -> tuple:
    """Gradio handler: summarise + generate FAQs + evaluate + translate."""
    if not document_text.strip():
        return "⚠️ Please paste a document first.", "", ""

    lang_map      = {v: k for k, v in tdgputi.list_supported_languages().items()}
    out_lang_code = lang_map.get(output_language, "en")

    try:
        truncated = tdgputi.truncate_text(document_text, max_chars=3500)

        # ── Summarisation ──────────────────────────────────────────────────
        result          = tdgputi.summarize_multilang(
            truncated, API_KEY, source_lang="en",
            output_lang=out_lang_code, base_url=BASE_URL, source_label="ui",
        )
        english_summary    = result["english_summary"]
        translated_summary = result["translated_summary"]

        summary_md = (
            f"### Summary\n{english_summary}" if out_lang_code == "en"
            else f"### English Summary\n{english_summary}\n\n### {output_language} Summary\n{translated_summary}"
        )

        # ── FAQ Generation ─────────────────────────────────────────────────
        faq_result = tdgputi.generate_faqs_multilang(
            truncated, API_KEY, source_lang="en",
            output_lang=out_lang_code, n_questions=int(n_faqs),
            base_url=BASE_URL, source_label="ui_faq",
        )
        faq_lines = [
            f"**Q{i}: {faq['question']}**\nA: {faq['answer']}"
            for i, faq in enumerate(faq_result["translated_faqs"], 1)
        ]
        faqs_md = "\n\n".join(faq_lines) or "No FAQs generated."

        # ── Evaluation ─────────────────────────────────────────────────────
        scores      = tdgputi.evaluate_output(english_summary, document_text[:500])
        scores_text = "\n".join(f"{k.upper()}: {v:.4f}" for k, v in scores.items())

        return summary_md, faqs_md, scores_text

    except Exception as exc:
        return f"❌ Error: {exc}", "", ""


# ── Build the interface ────────────────────────────────────────────────────
lang_choices = list(tdgputi.list_supported_languages().values())

EXAMPLE_TEXT = (
    "Python is a high-level, interpreted programming language known for its "
    "clear syntax and readability. It supports multiple programming paradigms "
    "including procedural, object-oriented, and functional programming. Python "
    "is widely used in data science, machine learning, web development, and "
    "automation. It was created by Guido van Rossum and first released in 1991. "
    "Python has a large standard library and a vibrant open-source ecosystem. "
    "Its package manager pip provides access to hundreds of thousands of packages."
)

with gr.Blocks(title="DocsGPT Documentation Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# 📄 DocsGPT Documentation Assistant\n"
        "Paste any technical document to get an AI-powered **summary** and **FAQs** "
        "in your chosen language — powered by **DocsGPT Cloud** (`POST /api/answer`)."
    )

    with gr.Row():
        with gr.Column(scale=3):
            doc_input = gr.Textbox(
                label="📋 Document Text",
                placeholder="Paste your technical document here...",
                lines=12, value=EXAMPLE_TEXT,
            )
        with gr.Column(scale=1):
            lang_dropdown = gr.Dropdown(
                choices=lang_choices, value="English", label="🌍 Output Language",
            )
            n_faqs_slider = gr.Slider(
                minimum=1, maximum=8, value=4, step=1, label="❓ Number of FAQs",
            )
            submit_btn = gr.Button("🚀 Generate Summary + FAQs", variant="primary", size="lg")

    with gr.Row():
        summary_out = gr.Markdown(label="Summary")

    with gr.Row():
        faqs_out = gr.Markdown(label="FAQs")

    scores_out = gr.Textbox(
        label="📊 Evaluation Scores (ROUGE + BLEU)", lines=5, interactive=False,
    )

    submit_btn.click(
        fn=run_docsgpt_ui,
        inputs=[doc_input, lang_dropdown, n_faqs_slider],
        outputs=[summary_out, faqs_out, scores_out],
    )

print("Launching Gradio app at http://127.0.0.1:7860 ...")
demo.launch(share=True)
# Set share=True to get a public URL for demos

# %% [markdown]
# ---
#
# ## What We Built
#
# | Part | Function used | API call |
# |------|---------------|----------|
# | Data Collection | `fetch_awesome_ml_readme()`, `load_stackoverflow_sample()`, `load_pile_sample()` | GitHub, HuggingFace Hub |
# | Summarisation | `summarize_document()` | `POST /api/answer` |
# | FAQ Generation | `generate_faqs()`, `parse_faqs()` | `POST /api/answer` |
# | Evaluation | `evaluate_all()` | rouge_score, nltk |
# | Multi-Language | `summarize_multilang()`, `generate_faqs_multilang()` | deep-translator + DocsGPT |
# | UI | `gr.Blocks()`, `demo.launch()` | Gradio |
#

# %% [markdown]
#
