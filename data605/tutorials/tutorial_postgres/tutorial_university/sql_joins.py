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
# Joins are a fundamental operation in relational databases because they allow us to correlate and combine information across multiple tables.
#
# In this notebook, we will see some examples of different types of joins.

# %%
# %load_ext sql
# %sql postgresql://postgres:postgres@localhost/university

# %% [markdown]
# # Create small example

# %%
# %load_ext sql
# %config SqlMagic.style = '_DEPRECATED_DEFAULT'
# %sql postgresql://postgres:postgres@localhost/university

# %%
# %sql drop table if exists R1;
# %sql drop table if exists R2;
# %sql drop table if exists R3;

# %sql create table R1 (A varchar(10), B int);
# %sql insert into R1 values('alpha', 10), ('beta', 20), ('gamma', 20), ('rho', 30), ('psi', 50);

# %sql create table R2 (B int, C varchar(10));
# %sql insert into R2 values (10, 'one'), (20, 'two'), (40, 'three');

# %sql create table R3 (C varchar(10), D varchar(10));
# %sql insert into R3 values ('one', 'alpha'), ('two', 'beta');

# %%
# %sql SELECT * FROM R1;

# %%
# %sql SELECT * FROM R2;

# %%
# %sql SELECT * FROM R3;

# %% [markdown]
# ## Cartesian Product (Cross-product)
# This is the most basic way to combine tuples across two tables.
#
# Every tuple in one relation is concatenated with every tuple from the other relation, so the result contains m * n tuples, where m and n are the number of tuples in the two relations.
#
# You almost never want to do cross product by itself, although there are some use cases.
#
# Trying to do a cross-product with three relations will result in an every larger relation (see example below).

# %%
# %sql SELECT * FROM R1, R2;

# %%
# %sql SELECT * FROM R1, R2, R3;

# %% [markdown]
# ## Standard Joins (Theta Joins)
# The standard way to do joins is by adding a selection predicate to the above queries.
#
# The predicate can pretty much be anything you want, although "equality" joins are most common.

# %% language="sql"
# -- Join R1 and R2 with the same value on B.
# SELECT *
#     FROM R1, R2
#     WHERE R1.B = R2.B;

# %% language="sql"
# -- Join R1, R2, R3, with the same values for B and C.
# SELECT *
#     FROM R1, R2, R3
#     WHERE R1.B = R2.B
#         AND R2.C = R3.C;

# %% language="sql"
# SELECT *
#     FROM R1, R2
#     WHERE R1.B < R2.B;

# %% language="sql"
# SELECT *
#     FROM R1, R2
#     WHERE R1.B + R2.B = 40;

# %% [markdown]
# ## Inner Join
# The following is an alternate way to write a join query, using the keyword "inner join"
# The only reason to use it is stylistic.
#
# As we will see below, this style of writing queries is *essential* for outer-joins, and writing inner joins in this fashion may make things look similar.

# %% language="sql"
# SELECT *
#     FROM R1 INNER JOIN R2
#     ON R1.B = R2.B;

# %% language="sql"
# SELECT *
#     FROM (R1 INNER JOIN R2 on R1.B = R2.B)
#         INNER JOIN R3 ON R2.C = R3.C;

# %% [markdown]
# ## Natural Joins
# A natural join is a type of inner join where the join condition is inferred by identifying common attributes in the two relations, and doing an equality on them.
#
# Because they can lead to unexpected results if you are not careful.
#
# **Note**: Unlike other types of joins, a natural join removes the extra occurrence of the join attribute (e.g., "b" below).

# %% language="sql"
# SELECT *
#     FROM R1 NATURAL JOIN R2;

# %% language="sql"
# SELECT *
#     FROM R1 NATURAL JOIN R2
#         NATURAL JOIN R3;

# %% [markdown]
# ## Outer joins
# In many cases, there is a need to keep all the tuples from one (or both) of the relations in the output, even if there is no match. Outer joins are used for that purpose.
#
# E.g., if I am doing a join between "department" and "instructor" on dept_name. Even if a department does not have any instructor, I might want the tuple to be present in the result output.
#
# There are three types of outerjoins -- left, right, and full.
#
# The left outer join is shown below: any tuple from the left relation that did not have a corresponding tuple in the right relation, is added to the output with "NULLs" in the columns from the right relation (in this case, the tuple "rho 30" which did not appear in the join results above -- attribute b_1 and c which came from R2 are set to NULL).

# %% language="sql"
# SELECT *
#     FROM R1 LEFT OUTER JOIN R2
#         ON R1.B = R2.B;

# %% [markdown]
# **Right outer join** does the opposite, whereas a **full outer join** includes tuples from both relations that don't match.

# %% language="sql"
# SELECT *
#     FROM R1 RIGHT OUTER JOIN R2
#         ON R1.B = R2.B;

# %% language="sql"
# SELECT *
#     FROM R1 FULL OUTER JOIN R2
#         ON R1.B = R2.B;

# %% language="sql"
# SELECT *
#     FROM (R1 FULL OUTER JOIN R2
#               ON R1.B = R2.B)
#         FULL OUTER JOIN R3
#             ON R2.C = R3.C;

# %% [markdown]
# ## Semi-joins
# Semi-join is not an explicit SQL keyword, but is a common Relational Algebra Operation (and has its own symbol). R1 semi-join R2 is simply the R1 tuples that have a match in R2. The output does not include any attributes from R2.
#
# The way to do this in SQL is through a subquery. As you can see, the tuple "rho, 30" does not appear because it does not have a match in R2.

# %%
# %sql select * from R1 where R1.B in (select B from R2)

# %% [markdown]
# ## Anti-join
# Anti-join is the opposite concept -- it includes tuples from the left relation which DO NOT have a match in the right relation. So in this case, it will only include the "rho, 30" tuple.
#
# Note that: R1 semi-join R2 and R1 anti-join R2 form a disjoint partition of R1.

# %%
# %sql select * from R1 where R1.B not in (select B from R2)

# %%

# %%
