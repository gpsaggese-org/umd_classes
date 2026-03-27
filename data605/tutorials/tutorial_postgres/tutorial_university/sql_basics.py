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
# The following commands load the requiste modules.
# **NOTE: If there is a warning, it doesn't seem to affect things.**

# %load_ext sql
# %sql postgresql://postgres:postgres@localhost/university

# %config SqlMagic.style = '_DEPRECATED_DEFAULT'

# %% [markdown]
# We can now run SQL commands using `magic` commands, which is an extensibility mechanism provided by Jupyter.
#
# - `%sql` is for single-line commands
# - `%%sql` allows multi-line SQL commands

# %% [markdown]
# # University Database
# Below we will use the University database from the class textbook. The University Dataset is the same as the one discussed in the book, and contains randomly populated information about students, courses, and instructors in a university.
#
# You should follow the rest of the Notebook along with the appropriate sections in the book.
# Each section in the notebook is tagged with the corresponding section in the book.
#
# The schema diagram for the database is as follows:
# <center><img src="https://github.com/umddb/cmsc424-fall2015/raw/master/postgresql-setup/university.png" width=800px></center>

# %% [markdown]
# One drawback of this way of accessing the database is that we can only run valid SQL -- the commands like `\d` provided by `psql` are not available to us.
#
# Instead, we will need to query the system catalog (metadata) directly
# - The first command below is equivalent to `\d`
# - The second one is similar to `\d instructor`.

# %% language="sql"
# -- Print all the tables.
# SELECT table_schema, table_name FROM information_schema.tables
#     WHERE table_type = 'BASE TABLE' AND
#     table_schema NOT IN ('pg_catalog', 'information_schema', 'priv');

# %% [markdown]
# You can see that there are:
# - some tables that describe objects (e.g., `student`, `course`, `time_slot`, `classroom`, `instructor`); and
# - other tables that describe "relationships" between objects (e.g., `takes`)
#
# - `department`: info about department
# - `course`: info about courses
# - `instructor`: info about instructors
# - `takes`: binds student with taken courses
# - `section`: binds courses with time and location
# - `student`: info about students
# - `advisor`: binds students and instructors
# - `time_slot`: schedule of each time slot
# - `classroom`: info about the classrooms
# - `teaches`: binds instructors with classes
# - `prereq`: relationship between courses

# %% language="sql"
# -- Print schema for instructor.
# SELECT column_name, data_type
#     FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'instructor';

# %% language="sql"
# --SELECT * FROM takes LIMIT 4;
# --SELECT * FROM student LIMIT 4;
# --SELECT * FROM section LIMIT 4;
# --SELECT * FROM course LIMIT 4;
# --SELECT * FROM department LIMIT 4;
# --SELECT * FROM advisor LIMIT 4;
# --SELECT * FROM time_slot LIMIT 4;
# --SELECT * FROM classroom LIMIT 4;
# --SELECT * FROM teaches LIMIT 4;
# --SELECT * FROM prereq LIMIT 4;
# SELECT * FROM instructor LIMIT 4;

# %% language="sql"
# -- Print table instructor.
# SELECT * FROM instructor;

# %% [markdown]
# ## Creating schema
#
# You can take a look at the `DDL.sql` file to see how the tables we are using are created. We won't try to run those commands here since they will only give errors.

# %%
# !cat DDL.sql

# %% [markdown]
# ## Populating data

# %% [markdown]
# The DB is populated with one of the scripts
# - smallRelationsInsertFile.sql
# - largeRelationsInsertFile.sql

# %%
# !cat smallRelationsInsertFile.sql

# %% language="sql"
# -- Test connection showing one table.
# SELECT * FROM takes;

# %% language="sql"
# -- Find the names of all instructors.

# %% [markdown]
# # (3.2) SQL Data definition

# %% language="sql"
# -- Delete the relation.
# DROP TABLE IF EXISTS department_tmp;
# -- Create a relation.
# CREATE TABLE department_tmp (
#     dept_name varchar(20),
#     building varchar(15),
#     -- 12 digits, 2 digits after decimal point.
#     budget numeric(12, 2),
#     PRIMARY KEY (dept_name)
# );

# %% language="sql"
# -- Empty relation.
# DELETE FROM department_tmp;
# -- Insert.
# INSERT INTO department_tmp VALUES ('Packard', '101', '500');
# SELECT * FROM department_tmp;

# %% language="sql"
# -- Empty relation.
# DELETE FROM department_tmp;

# %% language="sql"
# SELECT * FROM department_tmp;

# %% language="sql"
# -- Insert.
# INSERT INTO department_tmp VALUES ('Packard', '101', '500');
# SELECT * FROM department_tmp;

# %% language="sql"
# -- Add an attribute.
# ALTER TABLE department_tmp ADD city VARCHAR(20);
# SELECT * FROM department_tmp;

# %% language="sql"
# -- Remove an attribute.
# ALTER TABLE department_tmp DROP city;
# SELECT * FROM department_tmp;

# %% [markdown]
# ### (3.3.1) Queries on a single relation

# %% language="sql"
# -- Projection.
# SELECT name FROM instructor;

# %% language="sql"
# SELECT dept_name FROM instructor;

# %% language="sql"
# SELECT DISTINCT dept_name FROM instructor;

# %% language="sql"
# SELECT id, name, dept_name, salary FROM instructor;

# %% language="sql"
# SELECT id, name, dept_name, salary * 1.1 FROM instructor LIMIT 4;

# %% language="sql"
# SELECT name FROM instructor WHERE dept_name = 'Comp. Sci.';

# %% language="sql"
# SELECT name FROM instructor WHERE dept_name = 'Comp. Sci.' AND salary > 70000;

# %% [markdown]
# ### (3.3.2) Queries on multiple relations

# %% language="sql"
# SELECT * FROM instructor LIMIT 4;

# %% language="sql"
# SELECT * FROM department LIMIT 4;

# %% language="sql"
# -- Find the name of instructors with their dept name and dept building name.
# -- It is a join.
# SELECT name, instructor.dept_name, building
#     FROM instructor, department
#     WHERE instructor.dept_name = department.dept_name;

# %% language="sql"
# -- Cartesian product of two relations.
# SELECT * FROM instructor, teaches;

# %% language="sql"
# -- Find instructors who have taught some course and the courses they taught.
# -- Note that the duplicates are not removed.
# SELECT name, course_id
#     FROM instructor, teaches
#     WHERE instructor.ID = teaches.ID;

# %% language="sql"
# -- Removing the duplicates.
# SELECT DISTINCT name, course_id
#     FROM instructor, teaches
#     WHERE instructor.ID = teaches.ID;

# %% language="sql"
# -- Find instructors who have taught some course in the CS dept and courses they taught.
# SELECT DISTINCT name, course_id
#     FROM instructor, teaches
#     WHERE instructor.ID = teaches.ID AND
#         instructor.dept_name = 'Comp. Sci.';

# %% [markdown]
# ## (3.4) Additional basic operations

# %% language="sql"
# -- Rename in the SELECT clause.
# -- name can be confusing so we can rename it
# SELECT DISTINCT name AS instructor_name, course_id
#     FROM instructor, teaches
#     WHERE instructor.ID = teaches.ID;

# %% language="sql"
# -- Rename relations in the WHERE clause.
# SELECT DISTINCT T.name, S.course_id
#     FROM instructor AS T, teaches AS S
#     WHERE T.ID = S.ID;

# %% language="sql"
# -- Find the names of all instructors whose salary is greater than at least one instructor in the Biology dept.
# -- E.g., the minimum salary in the biology dept.
# SELECT DISTINCT T.name, T.salary
#     FROM instructor AS T, instructor AS S
#     WHERE T.salary > S.salary AND S.dept_name = 'Biology';

# %% language="sql"
# -- Regex matching.
# SELECT dept_name, building
#     FROM department
#     WHERE building like '%Wats%';

# %% language="sql"
# -- Get the name of all the fields after a join.
# SELECT DISTINCT instructor.*, teaches.*
#     FROM instructor, teaches
#     WHERE instructor.ID = teaches.ID;

# %% language="sql"
# SELECT name
#     FROM instructor
#     WHERE dept_name = 'Physics'
#     ORDER BY name;

# %% language="sql"
# -- Sorting on multiple attributes.
# SELECT * FROM instructor
#     ORDER BY salary DESC, name ASC;

# %% [markdown]
# ## (3.5) Set operations

# %% language="sql"
# SELECT * FROM course LIMIT 4;

# %% language="sql"
# SELECT * FROM section LIMIT 4;

# %% language="sql"
# -- Set of all courses taught in Fall 2009 semester.
# SELECT DISTINCT c.course_id
#     FROM course AS c, section AS s
#     WHERE s.semester = 'Fall' AND s.year = '2009'
#     ORDER BY c.course_id;

# %% language="sql"
# -- Set of all courses taught in Spring 2009 semester.
# SELECT DISTINCT c.course_id
#     FROM course AS c, section AS s
#     WHERE s.semester = 'Spring' AND s.year = '2009';

# %% language="sql"
# (SELECT DISTINCT c.course_id
#      FROM course AS c, section AS s
#      WHERE s.semester = 'Spring' AND s.year = '2009')
# UNION
# (SELECT DISTINCT c.course_id
#      FROM course AS c, section AS s
#      WHERE s.semester = 'Fall' AND s.year = '2009')

# %% language="sql"
# (SELECT DISTINCT c.course_id
#      FROM course AS c, section AS s
#      WHERE s.semester = 'Spring' AND s.year = '2009')
# INTERSECT
# (SELECT DISTINCT c.course_id
#      FROM course AS c, section AS s
#      WHERE s.semester = 'Fall' AND s.year = '2007')

# %% [markdown]
# ## (3.6) NULL values

# %% [markdown]
# ## (3.7) Aggregate functions

# %% [markdown]
# ### Count

# %% language="sql"
# SELECT * FROM instructor;

# %% language="sql"
# -- Count instructors by department.
# SELECT dept_name, count(*)
#     FROM instructor
#     GROUP BY dept_name
#     ORDER BY count;

# %% language="sql"
# -- Compute the average salary of instructors in the CS dept.
# SELECT AVG(salary) AS avg_salary
#     FROM instructor
#     WHERE dept_name = 'Comp. Sci.';

# %% language="sql"
# -- Count the elements in a table.
# SELECT COUNT(*) FROM instructor;

# %% language="sql"
# -- Count the distinct ids.
# SELECT COUNT(DISTINCT ID) FROM instructor;

# %% language="sql"
# SELECT *
#     FROM teaches
#     WHERE semester = 'Spring' and year = '2009';

# %% language="sql"
# -- COUNT() counts the number of elements in a group by.
# SELECT COUNT (DISTINCT ID)
#     FROM teaches
#     WHERE semester = 'Spring' and year = '2009';

# %% language="sql"
# SELECT COUNT (*) FROM course;

# %%
# # %%sql
# -- Distinct doesn't work with count.
# -- SELECT COUNT (DISTINCT *) FROM course;

# %% language="sql"
# -- Find the average dept in each department.
# SELECT dept_name, AVG(salary) AS avg_salary
#     FROM instructor
#     GROUP BY dept_name;

# %% language="sql"
# -- Find the number of instructors in each dept who teach a course in Spring 2007.
# SELECT dept_name, COUNT(DISTINCT instructor.ID) AS instr_count
#     FROM instructor, teaches
#     WHERE instructor.ID = teaches.ID
#         AND semester = 'Spring' AND year = 2009
#     GROUP BY dept_name;

# %% [markdown]
# ### Having

# %% language="sql"
# -- Get the department having instructors with an average salary larger than $42k.
# SELECT dept_name, AVG(salary) AS avg_salary
#     FROM instructor
#     GROUP BY dept_name
#     HAVING AVG(salary) > 42000;

# %% language="sql"
# -- Report the average total credits of students taking courses in 2009
# -- with at least 2 students.
# SELECT course_id, semester, year, sec_id, AVG(tot_cred)
#     FROM student, takes
#     WHERE student.ID = takes.ID AND year = 2009
#     GROUP BY course_id, semester, year, sec_id
#     HAVING COUNT(student.ID) >= 2;

# %% [markdown]
# ## (3.8) Nested subqueries

# %% language="sql"
# SELECT course_id FROM section WHERE semester = 'Fall' and year=2009

# %% language="sql"
# SELECT course_id FROM section WHERE semester = 'Spring' and year=2009

# %% language="sql"
# -- Find all the courses in either fall 2009 or spring 2009, using nested subquery.
# SELECT course_id
#     FROM section
#     WHERE semester = 'Fall' AND year=2009
#         OR course_id IN
#             -- Nested query.
#             (SELECT course_id FROM section
#                 WHERE semester = 'Spring' AND year=2009)

# %% language="sql"
# -- Find all the instructors that are not Mozart or Einstein.
# SELECT DISTINCT name
#     FROM instructor
#     WHERE name NOT IN ('Mozart', 'Einstein');

# %% language="sql"
# -- Find the dept with an average salary per instruction larger than $42k.
# -- This is an alternative query to the HAVING query.
# SELECT tmp.dept_name, tmp.avg_salary
#     FROM
#         (SELECT dept_name, AVG(salary) AS avg_salary
#           FROM instructor
#           GROUP BY dept_name) AS tmp
#     WHERE avg_salary > 42000

# %% [markdown]
# In many cases you might find it easier to create temporary tables, especially for queries involving finding "max" or "min". This also allows you to break down the full query AND makes it easier to debug. It is preferable to use the WITH construct for this purpose. The syntax AND support differs across systems, but here is the link to PostgreSQL: http://www.postgresql.org/docs/9.0/static/queries-with.html
#
# These are also called Common Table Expressions (CTEs).

# %% language="sql"
# -- Find department with the maximum budget.
# WITH max_budget(value) as (
#         SELECT MAX(budget) FROM department)
#     SELECT department.dept_name, budget
#         FROM department, max_budget
#         WHERE department.budget = max_budget.value

# %% [markdown]
# ## (3.9) Modification of the DB

# %% [markdown]
# # Other queries

# %% language="sql"
# SELECT * FROM course;

# %% language="sql"
# -- Reports the courses with titles containing Biology.
# SELECT *
#     FROM course
#     WHERE title LIKE '%Biology%';

# %% language="sql"
# -- There are two  courses. How many students are enrolled in the first one (ever)?
# SELECT *
#     FROM takes
#     WHERE course_id = 'BIO-101';

# %% language="sql"
# -- What about in Summer 2009?
# SELECT *
#     FROM takes
#     WHERE course_id = 'BIO-101' AND year = 2009 AND semester = 'Summer';

# %% [markdown]
# ### Aggregates
#

# %% language="sql"
# --  Count the number of instructors in Finance.
# SELECT COUNT(*)
#     FROM instructor WHERE dept_name = 'Finance';

# %% language="sql"
# -- Find the instructor with the maximum salary using subquery.
# SELECT *
#     FROM instructor
#     WHERE salary =
#         (SELECT MAX(salary) FROM instructor);

# %% [markdown]
# ### (3.3.2) Joins AND Cartesian Product

# %% language="sql"
# -- To find building names for all instructors, we must do a join between two relations.
# SELECT name, instructor.dept_name, building
#     FROM instructor, department
#     WHERE instructor.dept_name = department.dept_name;

# %% language="sql"
# -- Since the join here is a equality join on the common attributes in the two relations:
# SELECT name, instructor.dept_name, building
#     FROM instructor NATURAL JOIN department;

# %% language="sql"
# -- On the other hand, just doing the following (i.e., just the Cartesian Product) will lead to a large number of tuples, most
# -- of which are not meaningful.
# SELECT name, instructor.dept_name, building
#     FROM instructor, department;

# %% [markdown]
# ### Renaming using "as"

# %% language="sql"
# -- AS can be used to rename tables AND simplify queries.
# EXPLAIN
#     -- ANALYZE
#     SELECT DISTINCT T.name
#         FROM instructor AS T, instructor AS S
#         WHERE T.salary > S.salary AND S.dept_name = 'Biology';

# %% [markdown] jupyter={"outputs_hidden": true}
# **Self-joins** (WHERE two of the relations in the FROM clause are the same) are impossible without using `as`. The following query associates a course with the pre-requisite of one of its pre-requisites. There is no way to disambiguate the columns without some form of renaming.

# %% language="sql"
# EXPLAIN
#     ANALYZE
#         SELECT p1.course_id, p2.prereq_id AS pre_prereq_id
#             FROM prereq p1, prereq p2
#             WHERE p1.prereq_id = p2.course_id;

# %% [markdown]
# The small University database doesn't have any chains of this kind. You can try adding a new tuple using a new tuple. Now the query will return an answer.

# %%
# %sql insert into prereq values ('CS-101', 'PHY-101');

# %% language="sql"
# SELECT p1.course_id, p2.prereq_id AS pre_prereq_id
#     FROM prereq p1, prereq p2
#     WHERE p1.prereq_id = p2.course_id;

# %% [markdown]
# ### LIMIT
# PostgreSQL allows you to limit the number of results displayed which
# is useful for debugging etc. Here is an example.

# %%
# %sql SELECT * FROM instructor limit 2;

# %% [markdown]
# ### Try your own queries
# Feel free to use the cells below to write new queries. You can also just modify the above queries directly if you'd like.

# %%

# %%
