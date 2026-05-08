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
# # LangChain API Tutorial
#
# This tutorial demonstrates how to use LangChain's core functionalities.
# LangChain is a powerful framework designed to facilitate building language model-powered applications.
# We'll explore its components, including prompt creation, chains, retrieval, and agents.

# %%
import requests

resp = requests.post(
    "http://host.docker.internal:11434/api/generate",
    json={
        "model": "gemma3",
        "prompt": "what is the e constant, euler",
        "stream": False,
    },
)
print(resp.json())
