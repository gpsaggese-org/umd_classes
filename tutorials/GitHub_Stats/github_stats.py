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

# %%
# %load_ext autoreload
# %autoreload 2

import logging

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
import helpers.github_utils as hgitutil

# %% [markdown]
# # GitHub PR Statistics
#
# Demonstrate how to use `helpers.github_utils` to:
# - Connect to the GitHub API
# - Count open PRs broken down by author and draft/ready status
# - Count closed PRs over a specified time period broken down by author

# %% [markdown]
# ## Configuration
#
# Set the target repository and optional date range for closed PR filtering.

# %%
# Target repository in "owner/repo" format.
REPO_NAME = "causify-ai/helpers"
# Optional date range for closed PR stats (set to None to include all time).
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

# %% [markdown]
# ## Connect to GitHub API

# %%
# Authenticate using the GITHUB_ACCESS_TOKEN environment variable.
gh_api = hgitutil.GitHubAPI()
client = gh_api.get_client()
_LOG.info("Connected to GitHub API.")

# %% [markdown]
# ## Fetch Repository

# %%
repo_obj = client.get_repo(REPO_NAME)
_LOG.info("Fetched repository: %s", REPO_NAME)

# %% [markdown]
# ## Open PR Statistics
#
# Count and display all open PRs broken down by author and draft/ready status.

# %%
_LOG.info("Fetching open PRs...")
open_stats = hgitutil.count_open_prs_by_author(repo_obj)
hgitutil.print_open_pr_stats(open_stats)

# %% [markdown]
# ## Closed PR Statistics
#
# Count and display closed PRs in the specified date range, broken down by author.

# %%
period = hgitutil.utc_period(START_DATE, END_DATE)
_LOG.info("Fetching closed PRs for period %s to %s...", START_DATE, END_DATE)
closed_stats = hgitutil.count_closed_prs_by_author(repo_obj, period=period)
hgitutil.print_closed_pr_stats(closed_stats, period=period)

# %% [markdown]
# ## Closed PR Statistics (All Time)
#
# Count and display closed PRs across all time, broken down by author.

# %%
_LOG.info("Fetching closed PRs for all time...")
closed_stats_all = hgitutil.count_closed_prs_by_author(repo_obj)
hgitutil.print_closed_pr_stats(closed_stats_all)

# %% [markdown]
# ## Close Connection

# %%
gh_api.close_connection()
_LOG.info("Connection closed.")
