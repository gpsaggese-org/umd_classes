#!/usr/bin/env python

"""
Transform lecture slides using LLM with specified rules.

Reads slides from a lesson file, applies LLM-based transformations based on
a rule prompt, and writes the transformed slides back to the file or output.

Processes slides in batches using hllm_cli._process_batches, extracting
only slide content (excluding headers and comments) and reassembling the
file structure after transformation.

Import as:

import class_scripts.for_loop_slides as csfls
"""

from __future__ import annotations

import argparse
import logging
from typing import List, Tuple

from tqdm import tqdm

import helpers.hdbg as hdbg
import helpers.hio as hio
import helpers.hllm_cli as hllmcli
import helpers.hmarkdown_slide_iterator as hmaslite
import helpers.hparser as hparser

_LOG = logging.getLogger(__name__)

_DEFAULT_MODEL = "claude-opus-4"
_DEFAULT_BATCH_MODE = "individual"
_DEFAULT_BATCH_SIZE = 1


def _read_prompt_file(rule_path: str) -> str:
    """
    Read the prompt from a rule file.

    :param rule_path: path to the rule file
    :return: content of the rule file as string
    """
    hdbg.dassert_file_exists(rule_path, "Rule file must exist")
    _LOG.info("Reading prompt from rule file: %s", rule_path)
    with open(rule_path, "r") as f:
        prompt = f.read()
    _LOG.debug("Read prompt of length %d", len(prompt))
    return prompt


def _extract_slides(
    items: List[hmaslite.SlideItem],
) -> Tuple[List[hmaslite.SlideItem], List[str]]:
    """
    Extract slides and their string content from parsed items.

    Filters items to keep only slides and extracts their text content
    for processing by the LLM.

    :param items: list of parsed slide items from the lesson file
    :return: tuple of (slide_items, slide_texts)
        - slide_items: list of slide items (for reconstruction)
        - slide_texts: list of string content for each slide
    """
    slide_items = []
    slide_texts = []
    for item in items:
        if item["type"] == "slide":
            slide_items.append(item)
            slide_content = "\n".join(item["content"])
            slide_texts.append(slide_content)
    _LOG.info("Extracted %d slides from %d items", len(slide_items), len(items))
    return slide_items, slide_texts


def _process_slides_with_llm(
    slide_texts: List[str],
    prompt: str,
    *,
    batch_size: int,
    batch_mode: str,
    model: str,
) -> List[str]:
    """
    Process slides using LLM transformation via _process_batches.

    Applies the prompt-based LLM transformation to each slide in batches
    and returns the transformed slides.

    :param slide_texts: list of slide text content to transform
    :param prompt: system prompt to guide the LLM transformation
    :param batch_size: number of slides to process in each batch
    :param batch_mode:
        - "individual": process each slide separately
        - "shared_prompt": use shared prompt for batch
        - "combined": combine slides in batch processing
    :param model: LLM model to use for transformation
    :return: list of transformed slide texts
    """
    num_batches = (len(slide_texts) + batch_size - 1) // batch_size
    _LOG.info(
        "Processing %d slides in %d batches of size %d using model %s",
        len(slide_texts),
        num_batches,
        batch_size,
        model,
    )
    progress_bar = tqdm(
        total=len(slide_texts),
        desc="Processing slides",
        unit="slide",
    )
    results, num_skipped, total_cost = hllmcli._process_batches(
        values=slide_texts,
        batch_size=batch_size,
        prompt=prompt,
        batch_mode=batch_mode,
        model=model,
        testing_functor=None,
        progress_bar_object=progress_bar,
        num_batches=num_batches,
    )
    progress_bar.close()
    _LOG.info(
        "Processed slides: %d results, %d skipped, cost $%.4f",
        len(results),
        num_skipped,
        total_cost,
    )
    return results


def _reconstruct_file(
    items: List[hmaslite.SlideItem],
    transformed_slides: List[str],
) -> str:
    """
    Reconstruct the file by replacing slide content with transformations.

    Replaces the content of slide items with the LLM-transformed text,
    keeping headers and comments unchanged.

    :param items: original parsed items from the file
    :param transformed_slides: list of transformed slide texts
    :return: reconstructed file content as string
    """
    slide_idx = 0
    for item in items:
        if item["type"] == "slide" and slide_idx < len(transformed_slides):
            item["content"] = transformed_slides[slide_idx].split("\n")
            slide_idx += 1
    reconstructed = hmaslite.reassemble_from_items(items)
    _LOG.info("Reconstructed file with %d transformed slides", slide_idx)
    return reconstructed


# #############################################################################


def _parse() -> argparse.ArgumentParser:
    """
    Parse command line arguments.

    :return: configured argument parser
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        action="store",
        required=True,
        help="Path to input lesson file to process",
    )
    parser.add_argument(
        "--output",
        action="store",
        required=False,
        default=None,
        help="Path to output file (if not specified, modify input in place)",
    )
    parser.add_argument(
        "--rule",
        action="store",
        required=True,
        help="Path to rule file containing the transformation prompt",
    )
    # TODO(gp): These could be factor out.
    parser.add_argument(
        "--batch_size",
        action="store",
        type=int,
        required=False,
        default=_DEFAULT_BATCH_SIZE,
        help=f"Number of slides per batch (default: {_DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--batch_mode",
        action="store",
        required=False,
        default=_DEFAULT_BATCH_MODE,
        choices=["individual", "shared_prompt", "combined"],
        help=f"Batch processing mode (default: {_DEFAULT_BATCH_MODE})",
    )
    parser.add_argument(
        "--model",
        action="store",
        required=False,
        default=_DEFAULT_MODEL,
        help=f"LLM model to use (default: {_DEFAULT_MODEL})",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    """
    Main execution function.

    Orchestrates the slide transformation process:
    1. Parse and validate arguments
    2. Read input lesson file
    3. Extract slides
    4. Apply LLM transformation via _process_batches
    5. Reconstruct file with transformed slides
    6. Write output to file or in place

    :param parser: configured argument parser
    """
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    hdbg.dassert_file_exists(args.input, "Input file must exist")
    hdbg.dassert_file_exists(args.rule, "Rule file must exist")
    _LOG.info("Processing input file: %s", args.input)
    _LOG.info("Using rule file: %s", args.rule)
    prompt = _read_prompt_file(args.rule)
    items = list(hmaslite.read_lesson_file(args.input))
    _LOG.debug("Read %d items from input file", len(items))
    _, slide_texts = _extract_slides(items)
    hdbg.dassert_lt(
        0,
        len(slide_texts),
        "Input file must contain at least one slide",
    )
    transformed_slides = _process_slides_with_llm(
        slide_texts=slide_texts,
        prompt=prompt,
        batch_size=args.batch_size,
        batch_mode=args.batch_mode,
        model=args.model,
    )
    hdbg.dassert_eq(
        len(transformed_slides),
        len(slide_texts),
        "Number of transformed slides must match input slides",
    )
    reconstructed = _reconstruct_file(items, transformed_slides)
    output_path = args.output if args.output else args.input
    _LOG.info("Writing output to: %s", output_path)
    hio.to_file(output_path, reconstructed)
    _LOG.info("Slide transformation completed successfully")


if __name__ == "__main__":
    _main(_parse())
