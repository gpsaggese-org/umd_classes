#!/usr/bin/env python
"""
Generate project descriptions from a Google Sheet and save them to a Markdown
file. This script also creates Github links for the project files and adds them
back to the Google Sheet. Set the OPENAI_API_KEY using export before running
script.

> generate_class_project_description.py \
    -v INFO
"""

import argparse
import logging
import pathlib
import time
from collections import defaultdict
from typing import Any, Optional

import pandas as pd

import helpers_root.helpers.hdbg as hdbg
import helpers_root.helpers.hgoogle_drive_api as hgofiapi
import helpers_root.helpers.hio as hio
import helpers_root.helpers.hopenai as hopenai
import helpers_root.helpers.hparser as hparser

_LOG = logging.getLogger(__name__)

# TODO(ai_gp): Use prompt.txt

DEFAULT_MARKDOWN_PATH = "./class_project_instructions/Projects"
# The maximum number of projects.
# Set the value to None to disable the limit.
DEFAULT_MAX_PROJECTS = None


def _build_prompt(project_name: str) -> str:
    if False:
        # Potential (v3) prompt if needed to use.
        # Change False to True to use it.
        if not previous_descriptions:
            return (
                f"Write a professional and detailed project description"
                f"for a data project titled '{project_name}'. "
                f"Indicate the difficulty level: '1/2/3, and include objectives, "
                f"technologies used, and expected outcomes."
                f"Make sure it is different from the following:\n{previous_descriptions}\n"
                f"Only focus on the new idea."
            )
        else:
            previous_descriptions = "\n- " + "\n- ".join(previous_descriptions)
            return (
                f"Write a professional and detailed project description"
                f"for a data project titled '{project_name}'. "
                f"Indicate the difficulty level: '1/2/3, and include objectives, "
                f"technologies used, and expected outcomes."
                f"Make sure it is different from the following:\n{previous_descriptions}\n"
                f"Only focus on the new idea."
            )
        # Will use more tokens, but might help produce a better result.
    elif False:
        # v1 (Original) prompt.
        # Change False to True to use it.
        if not previous_descriptions:
            return f"Generate a project description for '{project_name}',"
            f"with difficulty level: 1/2/3."
        else:
            previous_descriptions = "\n- " + "\n- ".join(previous_descriptions)
            return (
                f"Generate a project description for '{project_name}',"
                f"with difficulty level: 1/2/3."
                f"Make sure it is completely different from the following:\n{previous_descriptions}\n"
                f"Only focus on the new idea."
            )
    else:
        # v2: Added by Aayush as an improvement to optimize tokens
        # while conveying the same information.
        # Short, to the point and concise. Saves the most tokens while achieving similar results.
        # if not previous_descriptions:
        #     return f"Technology: {project_name}."
        # else:
        #     previous_descriptions = "\n- " + "\n- ".join(previous_descriptions)
        # return (
        #     f"Technology: {project_name}."
        #     f"Do NOT repeat the following idea:"
        #     f"{previous_descriptions}\n"
        #     f"Only focus on the new idea."
        #     f"Create a **completely new project** that differs clearly in all three aspects:\n"
        #     f"1. the domain or application (e.g., use a different target problem),"
        #     f"2. the data source (e.g., webscraping, APIs,ready datasets),"
        #     f"3. the ML task (e.g., clustering, regression, classification, forecasting, anomaly detection, etc.)."
        #     f"Also change the difficulty by 1 from the previous project (i.e., make it one level easier or harder).\n"
        #     f"Match the style and format of the GLOBAL PROMPT strictly."
        # )
        return (
            f"Tool: {project_name}.\n"
            f"Generate three new and distinct graduate-level data science project ideas using this tool.\n"
            f"Each project must have a unique difficulty level (1-easy, 2-medium, 3-hard)."
            f"Do NOT use A/B testing anywhere in the projects."
        )


def _generate_project_description(project_name: str) -> Any:
    """
    Generate a project description. Depending on the value in No of Projects
    columns, this will generate N number of projects for each tool, each
    different from the other.

    :param project_name: the name of the project
    :param difficulty: the difficulty level of the project
    :return: the project description
    """
    prompt = _build_prompt(project_name)
    project_desc = hopenai.get_completion(
        prompt,
        system_prompt=GLOBAL_PROMPT,
        model="gpt-4o-mini",
        cache_mode="FALLBACK",
        temperature=0.5,
        max_tokens=1200,
        print_cost=True,
    )
    return project_desc


def create_markdown_file(
    df: pd.DataFrame,
    markdown_folder_path: str,
    max_projects: Optional[int],
    *,
    sleep_sec: float = 1.5,
) -> pd.DataFrame:
    """
    Create a markdown file with the project descriptions using helpers.hio.

    :param df: the dataframe containing the project descriptions
    :param markdown_path: the path to the markdown file
    :param max_projects: limit to the rows processed
    :param sleep_sec: amount of time to sleep between rows
    """
    file_githublinks_df = pd.DataFrame(columns=["Tool", "URL"])
    rows = df.head(max_projects) if max_projects is not None else df
    # temps = [0.3,0.45,0.6]
    pathlib.Path(markdown_folder_path).mkdir(parents=True, exist_ok=True)
    # rows = rows[rows['Tool'].isin(['BoTorch','Polars','Apache Arrow (PyArrow)','apache-tvm','Keras Tuner','tsfresh','Whisper Large V3','CausalInference','CausalML'])]
    # rows = rows[rows['Tool'].isin(['Caffe'])]
    for _, row in rows.iterrows():
        content = ""
        project_name = row["Tool"]
        description = _generate_project_description(project_name)
        content = f"{description}\n\n"
        # content += f"######################## END ###############################\n\n"
        file_name = f"{project_name}_Project_Description.md"
        markdown_path = pathlib.Path(markdown_folder_path) / file_name
        # if markdown_path.exists():
        #     _LOG.info(
        #         "File already exists, skipping generation: %s", markdown_path
        #     )

        # else:
        hio.to_file(str(markdown_path), content)
        _LOG.info("Generated Markdown File: %s", file_name)
        github_url = f"{DEFAULT_FILE_GITHUB_LINK}{file_name}"
        file_githublinks_df.loc[len(file_githublinks_df)] = [
            project_name,
            github_url,
        ]
        # Letting it wait for a while before triggering another request
        time.sleep(sleep_sec)
    return file_githublinks_df


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--markdown_folder_path",
        default=DEFAULT_MARKDOWN_PATH,
        help="Output Projects folder",
    )
    parser.add_argument(
        "--max_projects",
        type=int,
        default=DEFAULT_MAX_PROJECTS,
        help="Limit rows processed (None = all).",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    # Expand user/relative paths to absolute ones early to avoid surprises.
    secret_path = str(pathlib.Path(args.secret_path).expanduser().resolve())
    markdown_folder_path = str(
        pathlib.Path(args.markdown_folder_path).expanduser().resolve()
    )
    _LOG.info("Reading sheet %s", args.sheet_url)
    sheet_df = _read_google_sheet(args.sheet_url, args.tab_name, secret_path)
    file_githublinks_df = create_markdown_file(
        sheet_df,
        markdown_folder_path,
        args.max_projects,
    )
    _LOG.info("Done: %s", markdown_folder_path)
    _LOG.info("Adding GitHub links to Project files to Google sheet")
    # _write_google_sheet(
    # file_githublinks_df, args.sheet_url, 'MSML610 Project Github Links', secret_path
    # )


if __name__ == "__main__":
    _main(_parse())
