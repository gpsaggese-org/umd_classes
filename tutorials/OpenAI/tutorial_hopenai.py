# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Import

# %%
# #!pip install openai


# %%
# %load_ext autoreload
# %autoreload 2

# %%
import logging

import hopenai
import snippets
import helpers.hdbg as hdbg

hdbg.init_logger()

hdbg.set_logger_verbosity(logging.INFO)

# %%
import os

os.environ["OPENAI_API_KEY"] = ""

# %%
if False:
    # Force reloading a module.
    import hopenai
    from importlib import reload

    reload(hopenai)

# %% [markdown]
# # Chat

# %%
hopenai.get_completion("hello")

# %% [markdown]
# # Eval prompt

# %%
function_tag = "code_snippets2"
transform_tag = "remove_docstring"
prompt_tag = "docstring"
in_outs = snippets.eval_prompt(function_tag, transform_tag, prompt_tag)

print(snippets.in_outs_to_str(in_outs))

# %%
snippets.in_out_to_files(in_outs)

# %% [markdown]
# # Assistant

# %%
system = """You are a proficient Python coder and write English very well.
Given the Python code passed below, improve or add comments to the code.
Each comment should be in imperative form, a full English phrase, and end with a period.
Comments must be for every logical chunk of 4 or 5 lines of Python code.
Do not comment every single line of code and especially logging statements.
"""

# There should be no empty line in the code.

user1 = snippets.get_code_snippet2()

response = hopenai.get_completion(user, system=system)

print(hopenai.response_to_txt(response))

# %% [markdown]
# ## Query using library

# %%
assistant_name = "coder_assistant"
instructions = "You are an expert Python coder. Use you knowledge base to answer questions about how to write code."

vector_store_name = "Coding style"
file_paths = ["all.coding_style.how_to_guide.md"]

assistant = hopenai.get_coding_style_assistant(
    assistant_name, instructions, vector_store_name, file_paths
)

# %%
hopenai.pprint(assistant)


# %%
# question = "What is DRY?"
question = "Should one pay the technical debt?"
messages = hopenai.get_query_assistant(assistant, question)
