# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
# ---

# %% [markdown]
# # SQL Intro (DDL, DML, DQL)
#
# This notebook covers Data Definition Language (DDL), Data Manipulation Language (DML), and basic queries (SELECT, WHERE, NULL behavior, GROUP BY, HAVING).

# %%
# Setup for running SQL cells in Colab
# Run this cell first in Colab. It installs ipython-sql and connects to a local SQLite database.
# In Colab, you may need to restart the runtime once after installation, but usually this works in one go.
# !pip install -q ipython-sql sqlalchemy
# %load_ext sql
# Create a local sqlite database file so the data persists within the Colab session
# %sql sqlite:///relational_db.sqlite

# %% [markdown]
# ## CREATE TABLE (DDL) example
#
# We'll create a single `student` table to demonstrate `CREATE TABLE`, `INSERT`, `UPDATE`, and `DELETE`.

# %% language="sql"
# CREATE TABLE IF NOT EXISTS student (
#     student_id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     dept_name TEXT,
#     tot_cred INTEGER DEFAULT 0
# );
#

# %% language="sql"
# -- Insert sample students
# INSERT OR IGNORE INTO student VALUES (101, 'David Kim', 'Computer Science', 120);
# INSERT OR IGNORE INTO student VALUES (102, 'Eva Green', 'Music', 150);
# INSERT OR IGNORE INTO student VALUES (103, 'Frank Li', NULL, 30);
#

# %% [markdown]
# ### SELECT and WHERE examples

# %% language="sql"
# SELECT student_id, name, dept_name, tot_cred FROM student;

# %% language="sql"
# SELECT * FROM student WHERE tot_cred > 100;

# %% [markdown]
# ### NULL values behavior
#
# Note: comparisons with `NULL` yield UNKNOWN and rows won't be returned unless you use `IS NULL` or `IS NOT NULL`.

# %% language="sql"
# SELECT * FROM student WHERE dept_name IS NULL;

# %% [markdown]
# ### GROUP BY and HAVING
#
# Compute average credits per department and filter departments by average using HAVING.

# %% language="sql"
# SELECT dept_name, AVG(tot_cred) AS avg_credits
# FROM student
# GROUP BY dept_name
# HAVING AVG(tot_cred) > 100;
#

# %% [markdown]
# ### UPDATE and DELETE examples

# %% language="sql"
# UPDATE student SET tot_cred = tot_cred + 6 WHERE student_id = 101;

# %% language="sql"
# SELECT * FROM student WHERE student_id = 101;

# %% language="sql"
# -- Delete students with fewer than 10 credits (example)
# DELETE FROM student WHERE tot_cred < 10;

# %% language="sql"
# SELECT * FROM student;
