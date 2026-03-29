# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
# # Movie Database Example
#
# This notebook mirrors the Movie example from the lecture: schema creation, inserts, typical queries, views, and examples of updates/deletes.

# %%
# Setup for running SQL cells in Colab
# Run this cell first in Colab. It installs ipython-sql and connects to a local SQLite database.
# In Colab, you may need to restart the runtime once after installation, but usually this works in one go.
# !pip install -q ipython-sql sqlalchemy
# %load_ext sql
# Create a local sqlite database file so the data persists within the Colab session
# %sql sqlite:///relational_db.sqlite


# %% [markdown]
# ## Schema creation (movie, movieStar, movieExec, starsIn, studio)
#
# Create the tables and insert sample data for exercises.

# %% language="sql"
# CREATE TABLE IF NOT EXISTS Studio (
#     name TEXT PRIMARY KEY,
#     address TEXT,
#     presC INTEGER
# );
#
# CREATE TABLE IF NOT EXISTS MovieExec (
#     name TEXT,
#     address TEXT,
#     certno INTEGER PRIMARY KEY,
#     netWorth INTEGER
# );
#
# CREATE TABLE IF NOT EXISTS Movie (
#     title TEXT,
#     year INTEGER,
#     length INTEGER,
#     inColor INTEGER,
#     studioName TEXT,
#     producerC INTEGER,
#     PRIMARY KEY(title, year),
#     FOREIGN KEY(producerC) REFERENCES MovieExec(certno),
#     FOREIGN KEY(studioName) REFERENCES Studio(name)
# );
#
# CREATE TABLE IF NOT EXISTS MovieStar (
#     name TEXT PRIMARY KEY,
#     address TEXT,
#     gender TEXT,
#     birthdate TEXT
# );
#
# CREATE TABLE IF NOT EXISTS StarsIn (
#     movieTitle TEXT,
#     movieYear INTEGER,
#     starName TEXT
# );
#

# %% language="sql"
# -- Insert sample Studios and execs
# INSERT OR IGNORE INTO Studio VALUES ('disney','Disney Address', 111);
# INSERT OR IGNORE INTO Studio VALUES ('warner','Warner Address', 112);
#
# INSERT OR IGNORE INTO MovieExec VALUES ('Exec A','Some Address',111,200000);
# INSERT OR IGNORE INTO MovieExec VALUES ('Exec B','Other Address',112,90000);
#
# -- Movies & stars
# INSERT OR IGNORE INTO Movie VALUES ('King Kong', 2005, 187, 1, 'disney', 111);
# INSERT OR IGNORE INTO Movie VALUES ('Short Story', 2014, 12, 0, 'indie', 112);
# INSERT OR IGNORE INTO MovieStar VALUES ('Naomi Watts','Unknown','F','1971-09-28');
# INSERT OR IGNORE INTO MovieStar VALUES ('Actor X','Addr','M','1980-05-05');
# INSERT OR IGNORE INTO StarsIn VALUES ('King Kong',2005,'Naomi Watts');
#

# %% [markdown]
# ## Example queries
#
# - Movies produced by Disney in 1990 (none in sample):
# ```sql
# SELECT title, year FROM Movie WHERE studioName = 'disney' AND year = 1990;
# ```
# - Distinct titles and ordering, group-by examples, set operations, and outer joins are demonstrated below.

# %% language="sql"
# SELECT DISTINCT title FROM Movie ORDER BY title;

# %% language="sql"
# SELECT year, AVG(length) AS avg_length FROM Movie GROUP BY year;
#

# %% language="sql"
# -- Find movie(s) with maximum length
# SELECT title, year FROM Movie WHERE length = (SELECT MAX(length) FROM Movie);
#

# %% [markdown]
# ## Views
#
# Create a view for Disney movies (example).

# %% language="sql"
# CREATE VIEW IF NOT EXISTS DisneyMovies AS
# SELECT * FROM Movie WHERE studioName = 'disney';
#

# %% language="sql"
# SELECT * FROM DisneyMovies;

# %% [markdown]
# ## Transactions note
#
# SQLite supports transactions (`BEGIN`, `COMMIT`, `ROLLBACK`). In Colab, the SQL magic executes statements in a transaction context per cell; for multi-statement transaction control use explicit `BEGIN`/`COMMIT`.
