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
# This notebook covers how NULLs are handled and the results of different types of queries in presence of NULLs. Recall that NULL is a special value used when we don't know the value of an attribute, which may be because the value is missing, it is inapplicable, or it is hidden. It is usually a bad idea to assign any specific meaning to the NULL value, but you should know how the query answers are affected.
#
# **NOTE:** NULLs are displayed as "None" by Jupyter, whereas `psql` just shows an empty space.

# %%
# %load_ext sql
# %sql postgresql://postgres:postgres@localhost/university
# %config SqlMagic.style = '_DEPRECATED_DEFAULT'

# %%
## Let's create a simple table, with a few NULL values in it
# %sql drop table if exists R;
# %sql create table R (i int, j int);
# %sql insert into R values(10, 10), (10, 20), (10, null), (null, 20), (null, 30), (20, null);
# %sql select * from R;

# %% [markdown]
# Result of any arithmetic or similar operation involving NULL is NULL. So: 10 + NULL = NULL, 10 * NULL = NULL, and so on.

# %%
# %sql select i * 10 from R;

# %% [markdown]
# On the other hand, the result of a boolean operation involving a NULL is an **UNKNOWN**, which is another special value used by SQL. So the result of: NULL = 10 is an UNKNOWN.
#
# Consider a joint predicate: (NULL = 10) or (10 = 10). The first part evaluates to an UNKNOWN, whereas the second part evaluates to a TRUE. In this case, the joint predicate evaluates to a TRUE -- because whichever value UNKNOWN might take (TRUE or FALSE), the result of the joint predicate will always be TRUE.

# %% [markdown]
# Similarly: UNKNOWN OR FALSE = UNKNOWN, because the result depends on what is the actual value of the first part.
# UNKNOWN and TRUE = UNKNOWN.
# UNKNOWN and FALSE = FALSE.
#
# You can try out similar queries as above to see this. Note that: Jupyter also prints out an UNKNOWN as a None.
#
# UNKNOWNs are carried through the evaluation as long as possible, but are finally evaluated to False when it is time to output the results.
#
# The first query below shows the results of applying a predicate "j = 10" to R. The second query does the actual selection and as you can see, only the tuples that satisfy are returned.

# %%
# %sql select *, j = 10 from R;

# %%
# %sql select * from R where j = 10;

# %% [markdown]
# SQL has constructs: "is null", "is not null", "is unknown", "is not unknown" to handle NULLs more properly. Note that: i = NULL will always be unknown, even if i is NULL.

# %%
# %sql select * from R where j = NULL;

# %%
# %sql select * from R where j is NULL;

# %% [markdown]
# The above constructs are useful for queries like the following.

# %%
# %sql select * from R where (j = 10) or (j is null);

# %% [markdown]
# ### Aggregates
# Behavior of SQL for aggregates is somewhat complicated. Generally speaking NULLs are ignored during aggregation, but there are exceptions. Below we run some natural queries on the above table.

# %%
# %sql select count(*) from R;

# %%
## count(*) counts everything. Whereas count(i) will ignore NULLs.
# %sql select count(i) from R;

# %%
## The below shows that even if a row contains only NULLs, it is still counted in count(*).
# %sql drop table if exists S;
# %sql create table S (i int, j int);
# %sql insert into S values (null, null), (10, null);
# %sql select count(*) from S;

# %%
## sum() will also ignore NULLs and just sum up the values that are not null;
# %sql select sum(i) from R;

# %%
## avg() will also ignore NULLs.
# %sql select avg(i) from R;

# %% [markdown]
# ### Group-by Aggregates
#
# The following shows how sum works with a group by. As you can see, a single group for the value of NULL is created, and the result sum is only NULL if all the tuples with that value of i have j = null (i.e., i = 20).

# %%
# %sql select i, sum(j) from R group by i;

# %% [markdown]
# This can get somewhat counterintuitive. Let's see what happens if we do count(*) instead. As you can see, all rows are counted.

# %%
# %sql select i, count(*) from R group by i;

# %% [markdown]
# Now let's see what happens if we do an AVG.

# %%
# %sql select i, avg(j) from R group by i;

# %% [markdown]
# ### Joins
# If you think of joins as cross-product followed by a selection, then most of what we discussed so far just applied directly. NULLs in the join columns are basically ignored since any predicate involving them return false.
#
# **NOTE**: This is independent of outerjoins, which add tuples with nulls to the output.

# %%
# %sql select * from R, S where R.i = S.i;

# %% [markdown]
# However, you can use "is null" or "is unknown" if you want to include specific tuples in the output.

# %%
# %sql select * from R, S where R.i = S.i or R.i is null or S.i is null;

# %%
