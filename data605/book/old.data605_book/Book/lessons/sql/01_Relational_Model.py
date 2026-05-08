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
#     display_name: Python 3
#     name: python3
# ---

# %% [markdown] id="3c1f84a5"
# # Relational Model (UMD DATA605)
#
# This notebook presents the **relational model** concepts extracted from the lecture PDF: definitions, primary & foreign keys, and simple examples executed with SQLite in Colab.

# %% id="e3cec637"
# Setup for running SQL cells in Colab
# Run this cell first in Colab. It installs ipython-sql and connects to a local SQLite database.
# In Colab, you may need to restart the runtime once after installation, but usually this works in one go.
# !pip install -q ipython-sql sqlalchemy
# %load_ext sql
# Create a local sqlite database file so the data persists within the Colab session
# %sql sqlite:///relational_db.sqlite

# %% [markdown] id="20c56244"
# ## Relational Model: Overview
#
# - Introduced by Ted Codd.
# - A relational DB consists of a collection of tables (relations).
# - Each table has a schema and rows (tuples).
#
# ### UML / Schema diagrams
#
# Insert the UML diagram(s) referenced in the slides below (placeholder):
#
# ![UML Diagram: University DB](# "Insert UML diagram of University DB here")
#
# > Replace the placeholder above with an image file using Colab file upload or a URL.

# %% [markdown] id="34140dfe"
# ## Primary Key and Foreign Key examples
#
# We will create three simple tables: `department`, `instructor`, and `course`. The `instructor` table uses `id` as primary key and references `department` via `dept_name` (a foreign key).

# %% id="0e11a543" language="sql"
# -- Create tables: department, instructor, course
# CREATE TABLE IF NOT EXISTS department (
#     dept_name TEXT PRIMARY KEY,
#     building TEXT,
#     budget INTEGER
# );
#
# CREATE TABLE IF NOT EXISTS instructor (
#     id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     dept_name TEXT,
#     salary INTEGER,
#     FOREIGN KEY(dept_name) REFERENCES department(dept_name)
# );
#
# CREATE TABLE IF NOT EXISTS course (
#     course_id TEXT PRIMARY KEY,
#     title TEXT,
#     dept_name TEXT,
#     credits INTEGER,
#     FOREIGN KEY(dept_name) REFERENCES department(dept_name)
# );
#

# %% id="cda1cf23" language="sql"
# -- Insert sample data into department, instructor, and course
# INSERT OR IGNORE INTO department VALUES ('Computer Science','Hampden', 500000);
# INSERT OR IGNORE INTO department VALUES ('Physics','Maxwell', 300000);
# INSERT OR IGNORE INTO department VALUES ('Music','Britten', 150000);
#
# INSERT OR IGNORE INTO instructor VALUES (1, 'Alice Smith', 'Computer Science', 90000);
# INSERT OR IGNORE INTO instructor VALUES (2, 'Bob Jones', 'Physics', 80000);
# INSERT OR IGNORE INTO instructor VALUES (3, 'Carol Lee', 'Music', 70000);
#
# INSERT OR IGNORE INTO course VALUES ('DATA-605','Big Data Systems','Computer Science',4);
# INSERT OR IGNORE INTO course VALUES ('PHYS-101','Intro Physics','Physics',3);
# INSERT OR IGNORE INTO course VALUES ('MUS-200','Advanced Music','Music',3);
#

# %% [markdown] id="e16e1900"
# ### Inspect tables

# %% id="462a38f3" language="sql"
# SELECT * FROM department;

# %% id="b5c06bf1" language="sql"
# SELECT * FROM instructor;

# %% id="71851f5f" language="sql"
# SELECT * FROM course;

# %% [markdown] id="2bab8db1"
# ## Notes
# - `PRIMARY KEY` must be unique and non-null.
# - `FOREIGN KEY` ensures referential integrity: values must match an existing primary key value in the referenced table.
# - In SQLite, foreign key enforcement is disabled by default for older versions; modern builds used in Colab enable it, but you can enable explicitly with `PRAGMA foreign_keys = ON;` if needed.

# %% id="10abe2a3" language="sql"
# PRAGMA foreign_keys = ON;
