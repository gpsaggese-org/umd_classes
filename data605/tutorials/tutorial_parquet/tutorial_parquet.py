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
# Show Parquet / Pyarrow API.

# %% [markdown]
# ## Imports

# %%
import os
import random

import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq


# %%
def get_df(num_days: int = 15) -> pd.DataFrame:
    """
    Create Pandas random data, like:

    ```
                idx instr  val1  val2
    2000-01-01    0     A    99    30
    2000-01-02    0     A    54    46
    2000-01-03    0     A    85    86
    ```
    """
    instruments = "A B C D E".split()
    start_idx = pd.Timestamp("2000-01-01")
    end_idx = start_idx + pd.Timedelta(days=num_days - 1)
    df_idx = pd.date_range(start_idx, end_idx, freq="1D")
    # print(df_idx)
    random.seed(1000)
    df = []
    for idx, inst in enumerate(instruments):
        df_tmp = pd.DataFrame(
            {
                "idx": idx,
                "instr": inst,
                "val1": [random.randint(0, 100) for k in range(len(df_idx))],
                "val2": [random.randint(0, 100) for k in range(len(df_idx))],
            },
            index=df_idx,
        )
        # print(df_tmp)
        df.append(df_tmp)
    df = pd.concat(df)
    return df


get_df()


# %%
def df_to_str(df: pd.DataFrame) -> str:
    txt = ""
    txt += "# df=\n%s" % df.head(3)
    txt += "\n...\n"
    # Remove first line with index.
    txt += "\n".join(str(df.tail(3)).split("\n")[1:])
    txt += "\n# df.shape=\n%s" % str(df.shape)
    txt += "\n# df.dtypes=\n%s" % str(df.dtypes)
    return txt


# %% [markdown]
# # Save and load all data in one file

# %%
df = get_df()
print(df_to_str(df))

# %%
df.to_csv("df.csv")

# !ls -lh df.csv

# %%
# Transform a Pandas df into a Python Arrow object.
table = pa.Table.from_pandas(df)

print("# table=\n%s" % table)

# %%
# Save.
file_name = "df_in_one_file.pq"
pq.write_table(table, file_name)

# !ls -lh df_in_one_file.pq

# %%
# Load.
df2 = pq.read_table(file_name)

# Convert to Pandas: types are conserved.
df2 = df2.to_pandas()
print(df_to_str(df2))

# %% [markdown]
# ## Scalability

# %%
for num_rows in (15, 100, 1000, 10000):
    print("# num_rows=", num_rows)
    #
    df = get_df(num_rows)
    df.to_csv("df_tmp.csv")
    # !ls -lh df_tmp.csv
    #
    df.to_csv("df_tmp.csv.gz")
    # !ls -lh df.csv.gz
    #
    file_name = "df_tmp_in_one_file.pq"
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_name)
    # !ls -lh df_in_one_file.pq

# %% [markdown]
# ## Read a subset of columns

# %%
# Load only two columns.
df2 = pq.read_table(file_name, columns=["idx", "val1"])
# print(df2)

df2 = df2.to_pandas()
print(df_to_str(df2))

# %% [markdown]
# # Partitioned dataset
#
# from https://arrow.apache.org/docs/python/dataset.html#reading-partitioned-data
#
# - A dataset can exploit a nested structure, where the sub-dir names hold information about which subset of the data is stored in that dir
# - E.g., "hive" partitioning scheme "key=vale" dir names

# %%
df = get_df()
# display(df)
print(df_to_str(df))

# %%
# Clean up dir.
base = "."
dir_name = os.path.join(base, "pq_partitioned1")
os.system("rm -rf %s" % dir_name)

# Save data in a partitioned ways using `idx` as partitioning key.
table = pa.Table.from_pandas(df)
pq.write_to_dataset(table, dir_name, partition_cols=["idx"])

# !find {dir_name}

# %%
# Read data back.
dataset = ds.dataset(dir_name, format="parquet", partitioning="hive")
print("\n".join(dataset.files))

# %%
# Read everything.
df2 = dataset.to_table().to_pandas()

print(df_to_str(df2))

# %%
# Load a subset of rows of the data.
df2 = dataset.to_table(filter=ds.field("idx") == 1).to_pandas()
display(df2)
# Note that type of partitioning key sometimes is slightly changed.
print(df_to_str(df2))

# %%
df2 = dataset.to_table(filter=ds.field("idx") < 3).to_pandas()
display(df2)
print(df_to_str(df2))

# %% [markdown]
# ## Add year-month partitions

# %%
df = get_df(num_days=100)
df["year"] = df.index.year
df["month"] = df.index.month

print(df_to_str(df))

# %%
# Convert to Pyarrow.
table = pa.Table.from_pandas(df)
# print("table=\n%s" % table)

# Clean up dir.
base = "."
dir_name = os.path.join(base, "pq_partitioned2")
os.system("rm -rf %s" % dir_name)

# Save it using 3 partitioning keys.
pq.write_to_dataset(table, dir_name, partition_cols=["idx", "year", "month"])

# Show data structure.
# !find $dir_name

# %%
# !ls $dir_name/idx=0/year=2000/month=1

# %%
# Read data back.
dataset = ds.dataset(dir_name, format="parquet", partitioning="hive")

# Read only one tile back.
df2 = dataset.to_table(filter=ds.field("idx") == 2).to_pandas()
print(df_to_str(df2))

# %% [markdown]
# ## Partition manually

# %%
# We could scan manually the df and create the dirs manually.
base = "."
dir_name = os.path.join(base, "pq_partitioned4")
os.system("rm -rf %s" % dir_name)

# Extract the schema.
schemas = []
schema = pa.Table.from_pandas(df).schema
print(schema)

# grouped = df.groupby(lambda x: x.day)
group_by_idx = df.groupby("idx")
for idx, df_tmp in group_by_idx:
    print("idx=%s -> df.shape=%s" % (idx, str(df_tmp.shape)))
    #
    group_by_year = df_tmp.groupby(lambda x: x.year)
    for year, df_tmp2 in group_by_year:
        print("year=%s -> df.shape=%s" % (year, str(df_tmp2.shape)))
        #
        group_by_month = df_tmp2.groupby(lambda x: x.month)
        for month, df_tmp3 in group_by_month:
            print("month=%s -> df.shape=%s" % (month, str(df_tmp3.shape)))
            # file_name = "df_in_one_file.pq"
            # pq.write_table(table, file_name)
            # /app/data/idx=0/year=2000/month=1/02e3265d515e4fb88ebe1a72a405fc05.parquet
            subdir_name = os.path.join(
                dir_name, f"idx={idx}", f"year={year}", f"month={month}"
            )
            table = pa.Table.from_pandas(df_tmp3, schema=schema)
            schemas.append(table.schema)
            # print(df_tmp3)
            # print(table.schema)
            #             pq.write_to_dataset(table,
            #                     subdir_name, schema=schema)
            file_name = os.path.join(subdir_name, "df_out.pq")
            # hio.create_enclosing_dir(file_name)
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            pq.write_table(table, file_name)

# %%
# !find $dir_name

# %%
# #!ls $dir_name/idx=0/year=2000/month=1

# %%
# Read data back.
# https://github.com/dask/dask/issues/4194
# src_dir = f"{dir_name}/idx=0/year=2000/month=1"
src_dir = f"{dir_name}/idx=0/year=2000"
dataset = ds.dataset(src_dir, format="parquet", partitioning="hive")

df2 = dataset.to_table().to_pandas()
# print(df_to_str(df2))
print("\n".join(dataset.files))

# %% [markdown]
# ## Partition manually

# %%
from pyarrow.dataset import DirectoryPartitioning

partitioning = DirectoryPartitioning(
    pa.schema([("year", pa.int16()), ("month", pa.int8()), ("day", pa.int8())])
)
print(partitioning.parse("/2009/11/3"))

# partitioning.discover()

# %%
# !ls /data

# %%
dir_name = "/app/data"

# Read data back.
dataset = ds.dataset(dir_name, format="parquet", partitioning="hive")

print("\n".join(dataset.files))

# %%
# Read everything.
df2 = dataset.to_table().to_pandas()

print(df_to_str(df2))

# %%
print(df2["instr"].unique())
print(df2.index)
