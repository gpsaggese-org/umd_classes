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
# %load_ext sql
# %sql postgresql://postgres:postgres@localhost

# %% [markdown]
# # Create a DB.

# %% language="sql"
# SELECT datname
#     FROM pg_database;

# %%
# !createdb seven_dbs

# %% [markdown]
# Print DBs.

# %% language="sql"
# SELECT datname
#     FROM pg_database;

# %% language="sql"
# -- Print available tables.
# SELECT table_schema, table_name
#     FROM information_schema.tables
#     WHERE table_type = 'BASE TABLE' AND
#     table_schema NOT IN ('pg_catalog', 'information_schema', 'priv');

# %% [markdown]
# # Create table `countries`.

# %% language="sql"
# DROP TABLE countries;
# -- Create table `countries`.
# CREATE TABLE countries (
#     country_code CHAR(2) PRIMARY KEY,
#     country_name TEXT UNIQUE)

# %% language="sql"
# -- Print the schema of this table.
# SELECT * FROM Information_schema.Columns
#     WHERE table_name = 'countries';

# %% run_control={"marked": true} language="sql"
# INSERT INTO countries (country_code, country_name)
#     VALUES
#     ('us','United States'),
#     ('mx','Mexico'),
#     ('au','Australia'),
#     ('gb','United Kingdom'),
#     ('de','Germany'),
#     ('ll','Loompaland');

# %% language="sql"
# SELECT * FROM countries;

# %% language="sql"
# -- Try to insert a duplicate.
# INSERT INTO countries
#     VALUES ('uk','United Kingdom');

# %% language="sql"
# DELETE FROM countries
#     WHERE country_code = 'll';
# SELECT * FROM countries;

# %% [markdown]
# # Create table `cities`.

# %% language="sql"
# DROP TABLE cities;
# -- Add a `cities` table.
# CREATE TABLE cities (
#     -- No nulls in name.
#     name text NOT NULL,
#     -- No empty strings.
#     postal_code VARCHAR(9) CHECK (postal_code <> ''),
#     -- Foreign key.
#     country_code CHAR(2) REFERENCES countries,
#     -- Compound key.
#     PRIMARY KEY (country_code, postal_code)
# );

# %% language="sql"
# -- Errors out because of referential integrity.
# INSERT INTO cities
#     VALUES ('Toronto', 'M4C1B5', 'ca');

# %% language="sql"
# -- Valid insert (but the zip code is wrong).
# INSERT INTO cities
#     VALUES ('Portland', '87200', 'us');
# SELECT * FROM cities;

# %% language="sql"
# -- Update the value in a relationship.
# UPDATE cities
#     SET postal_code = '97206'
#     WHERE name = 'Portland';
# SELECT * FROM cities;

# %% [markdown]
# ## Join reads

# %% language="sql"
# SELECT * FROM cities;

# %% language="sql"
# SELECT * FROM countries;

# %% language="sql"
# -- Show all the info from cities and the country name.
# SELECT cities.*, countries.country_name
#     FROM cities
#     INNER JOIN countries
#     ON cities.country_code = countries.country_code;

# %% language="sql"
# DROP TABLE venues;
# --
# CREATE TABLE venues (
#     --
#     venue_id SERIAL PRIMARY KEY,
#     name VARCHAR(255) UNIQUE,
#     street_address TEXT,
#     -- 2 values with one default.
#     type char(7) CHECK (type IN ('public', 'private')) DEFAULT 'public',
#     postal_code VARCHAR(9),
#     country_code CHAR(2),
#     -- The foreign key is compound.
#     FOREIGN KEY (country_code, postal_code)
#         REFERENCES cities (country_code, postal_code) MATCH FULL
# );

# %% language="sql"
# INSERT INTO venues (name, postal_code, country_code)
#     VALUES ('Crystal Ballroom', '97206', 'us');

# %% language="sql"
# SELECT * FROM venues;

# %% language="sql"
# -- Insert and return row.
# INSERT INTO venues (name, postal_code, country_code)
#     VALUES ('Voodoo Doughnut', '97206', 'us')
#     -- Return the inserted value.
#     RETURNING *;

# %% language="sql"
# -- Join venue and state.
# SELECT v.venue_id, v.name, v.postal_code, c.name
#     FROM venues v
#     INNER JOIN cities c
#     ON v.postal_code=c.postal_code AND v.country_code=c.country_code;

# %% [markdown]
# ## Outer joins.

# %% language="sql"
# DROP TABLE events;
# CREATE TABLE events (
#     event_id SERIAL PRIMARY KEY,
#     title VARCHAR(255),
#     starts TIMESTAMP,
#     ends TIMESTAMP,
#     venue_id INTEGER REFERENCES venues
# );

# %% language="sql"
# INSERT INTO events (title, starts, ends, venue_id)
#     VALUES
#     ('Fight club', '2018-02-15 17:30:00', '2018-02-15 19:30:00', 2),
#     ('April Fools day', '2018-04-01 00:00:00', '2018-04-01 23:59:00', NULL),
#     ('Christmas day', '2018-02-15 19:30:00', '2018-12-25 23:59:00', NULL)
#     RETURNING *
# ;

# %% language="sql"
# SELECT * FROM events;

# %% language="sql"
# -- Outer join but venues have NULL value so they don't show up.
# SELECT e.title, v.name
#     FROM events e
#     JOIN venues v
#     ON e.venue_id = v.venue_id;

# %% language="sql"
# -- Left outer join.
# SELECT e.title, v.name
#     FROM events e
#     LEFT JOIN venues v
#     ON e.venue_id = v.venue_id;

# %% [markdown]
# ## Indexing.

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#

# %%

# %% language="sql"
#

# %% language="sql"
#

# %% language="sql"
#
