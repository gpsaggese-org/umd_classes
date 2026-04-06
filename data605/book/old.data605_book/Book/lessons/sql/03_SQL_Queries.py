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
# # SQL Queries: Joins, Subqueries, WITH, Aggregation
#
# This notebook demonstrates multi-table queries, joins (including outer joins), nested subqueries, WITH (CTE), and ranking examples using SQLite.

# %%
# Setup for running SQL cells in Colab
# Run this cell first in Colab. It installs ipython-sql and connects to a local SQLite database.
# In Colab, you may need to restart the runtime once after installation, but usually this works in one go.
# !pip install -q ipython-sql sqlalchemy
# %load_ext sql
# Create a local sqlite database file so the data persists within the Colab session
# %sql sqlite:///relational_db.sqlite

# %% [markdown]
# ## Create auxiliary tables for examples: movies, starsIn, movieExec, movieStar

# %% language="sql"
# CREATE TABLE IF NOT EXISTS movie (
#     title TEXT,
#     year INTEGER,
#     length INTEGER,
#     inColor INTEGER,
#     studioName TEXT,
#     producerC INTEGER,
#     PRIMARY KEY(title, year)
# );
#
# CREATE TABLE IF NOT EXISTS starsIn (
#     movieTitle TEXT,
#     movieYear INTEGER,
#     starName TEXT
# );
#
# CREATE TABLE IF NOT EXISTS movieExec (
#     name TEXT,
#     address TEXT,
#     certno INTEGER PRIMARY KEY,
#     netWorth INTEGER
# );
#
# CREATE TABLE IF NOT EXISTS movieStar (
#     name TEXT PRIMARY KEY,
#     address TEXT,
#     gender TEXT,
#     birthdate TEXT
# );
#

# %% language="sql"
# -- Insert sample data
# INSERT OR IGNORE INTO movie VALUES ('King Kong', 2005, 187, 1, 'disney', 111);
# INSERT OR IGNORE INTO movie VALUES ('A Short Film', 2010, 25, 0, 'indie', 112);
# INSERT OR IGNORE INTO movie VALUES ('Epic Tale', 1998, 150, 1, 'warner', 111);
#
# INSERT OR IGNORE INTO movieExec VALUES ('Exec A','Some Address',111,200000);
# INSERT OR IGNORE INTO movieExec VALUES ('Exec B','Other Address',112,90000);
#
# INSERT OR IGNORE INTO movieStar VALUES ('Naomi Watts','Unknown','F','1971-09-28');
# INSERT OR IGNORE INTO movieStar VALUES ('Actor X','Addr','M','1980-05-05');
#
# INSERT OR IGNORE INTO starsIn VALUES ('King Kong',2005,'Naomi Watts');
# INSERT OR IGNORE INTO starsIn VALUES ('Epic Tale',1998,'Actor X');
#

# %% [markdown]
# ## Multi-table join example
#
# Find movie title, year and producer name by joining `movie` and `movieExec`.

# %% language="sql"
# SELECT m.title, m.year, me.name AS producerName
# FROM movie m JOIN movieExec me ON m.producerC = me.certno;

# %% [markdown]
# ### Count stars per movie (grouping + LEFT OUTER JOIN)

# %% language="sql"
# SELECT m.title, m.year, COUNT(si.starName) AS num_stars
# FROM movie m LEFT JOIN starsIn si
#     ON m.title = si.movieTitle AND m.year = si.movieYear
# GROUP BY m.title, m.year;
#

# %% [markdown]
# ## Nested / Correlated subquery example
#
# Find movies with at most 5 stars (here we only have up to 1-2 in sample data)

# %% language="sql"
# SELECT m.title, m.year
# FROM movie m
# WHERE 5 >= (
#     SELECT COUNT(*) FROM starsIn si
#     WHERE si.movieTitle = m.title AND si.movieYear = m.year
# );
#

# %% [markdown]
# ## WITH clause (Common Table Expression) example

# %% language="sql"
# WITH avg_length AS (
#     SELECT AVG(length) AS avg_len FROM movie
# )
# SELECT title, year, length FROM movie WHERE length > (SELECT avg_len FROM avg_length);
#

# %% [markdown]
# ## Ranking example using correlated subquery
#
# Rank movies by length (1 = longest). Note: SQLite lacks a window `RANK()` prior to certain versions — this demonstrates correlated subquery ranking.

# %% language="sql"
# SELECT title, year,
#     (SELECT COUNT(*) FROM movie m2 WHERE m2.length >= m1.length) AS rank
# FROM movie m1
# ORDER BY rank;
#
