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
# # Chap 1

# %% [markdown]
# # Chap 2: Introducing Dask

# %% [markdown]
# ## Hello Dask

# %%
# #!curl https://www.kaggle.com/datasets/new-york-city/nyc-parking-tickets?resource=download&select=Parking_Violations_Issued_-_Fiscal_Year_2017.csv

# %%
# !ls

# %%
# !wc -l Parking_Violations_Issued_-_Fiscal_Year_2017.csv

# !head -10000 Parking_Violations_Issued_-_Fiscal_Year_2017.csv >Parking_Violations_Issued_-_Fiscal_Year_2017.small.csv

# !wc -l Parking_Violations_Issued_-_Fiscal_Year_2017.small.csv

# %%
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

# file_name = "Parking_Violations_Issued_-_Fiscal_Year_2017.csv"
file_name = "Parking_Violations_Issued_-_Fiscal_Year_2017.small.csv"

df = dd.read_csv(
    file_name,
    dtype={"House Number": "object", "Time First Observed": "object"},
)
df

# %%
missing_values = df.isnull().sum()
missing_values

# %%
missing_count = (missing_values / df.index.size) * 100
missing_count

# %%
with ProgressBar():
    missing_count_pct = missing_count.compute()
missing_count_pct

# %%
# This is a pd.Series.
columns_to_drop = missing_count_pct[missing_count_pct > 60].index
print(columns_to_drop)
with ProgressBar():
    df_dropped = df.drop(columns_to_drop, axis=1).persist()

# df_dropped is a Dask object.
df_dropped

# %% [markdown]
# ## Visualizing DAGs

# %%
import dask.delayed as delayed
from dask.diagnostics import ProgressBar


def inc(i):
    return i + 1


x = delayed(inc)(1)
y = delayed(inc)(2)


def add(x, y):
    return x + y


z = delayed(add)(x, y)
print("dask=", z.compute())
print("correct=", 1 + 1 + 2 + 1)
z.visualize()

# %%
data = [1, 5, 8, 10]


def add_two(x):
    return x + 2


step1 = [delayed(add_two)(i) for i in data]
total = delayed(sum)(step1)
print("dask=", total.compute())
print("correct=", 1 + 2 + 5 + 2 + 8 + 2 + 10 + 2)
total.visualize()

# %%
data = [1, 5, 8, 10]


def add_two(x):
    return x + 2


step1 = [delayed(add_two)(i) for i in data]


def multiply_four(x):
    return x * 4


step2 = [delayed(multiply_four)(j) for j in step1]
total = delayed(sum)(step2)
print("dask=", total.compute())
print("correct=", (1 + 2) * 4 + (5 + 2) * 4 + (8 + 2) * 4 + (10 + 2) * 4)
total.visualize()

# %%
print("total=", total.compute())
print("data=", data)
# Sum data again value by value.
data2 = [delayed(sum_two_numbers)(k, total) for k in data]
# Accumulate.
total2 = delayed(sum)(data2)
print("dask=", total2.compute())
print("correct=", 128 * 4 + 1 + 5 + 8 + 10)
total2.visualize()

# %%
total_persisted = total.persist()
total_persisted.visualize()

# %% [markdown]
# ##

# %%
df.visualize()

# %%
missing_values.visualize()

# %%
missing_count.visualize()

# %% [markdown]
# ## Task scheduling

# %% [markdown]
# # Introducing Dask DataFrames

# %% [markdown]
# ## Why use DataFrames?
#
# From https://github.com/jcdaniel91/data-science-python-dask/blob/master/Chapter%203.ipynb

# %%
import pandas as pd
import dask.dataframe as dd

# Creating all the data as lists
person_IDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
person_last_names = [
    "Smith",
    "Williams",
    "Williams",
    "Jackson",
    "Johnson",
    "Smith",
    "Anderson",
    "Christiansen",
    "Carter",
    "Davidson",
]
person_first_names = [
    "John",
    "Bill",
    "Jane",
    "Cathy",
    "Stuart",
    "James",
    "Felicity",
    "Liam",
    "Nancy",
    "Christina",
]
person_DOBs = [
    "1982-10-06",
    "1990-07-04",
    "1989-05-06",
    "1974-01-24",
    "1995-06-05",
    "1984-04-16",
    "1976-09-15",
    "1992-10-02",
    "1986-02-05",
    "1993-08-11",
]

# Storing the data in a Pandas DataFrame
people_pandas_df = pd.DataFrame(
    {
        "Person ID": person_IDs,
        "Last Name": person_last_names,
        "First Name": person_first_names,
        "Date of Birth": person_DOBs,
    },
    columns=["Person ID", "Last Name", "First Name", "Date of Birth"],
)
display(people_pandas_df)


# %%
# Converting the Pandas DataFrame to a Dask DataFrame
people_dask_df = dd.from_pandas(people_pandas_df, npartitions=2)
print("# people_dask_df=\n%s" % people_dask_df)
print("# divisions=", people_dask_df.divisions)
print("# npartitions=", people_dask_df.npartitions)

# map_partitions() applies a function to each partition.
print(
    "# elements per partition=\n%s"
    % people_dask_df.map_partitions(len).compute()
)

# %%
# Filter.
people_filtered = people_dask_df[people_dask_df["Last Name"] != "Williams"]
print(
    "# partitions before=\n%s"
    % people_filtered.map_partitions(lambda x: len(x)).compute()
)
display(people_filtered.compute())

# Repartitioning.
people_filtered_reduced = people_filtered.repartition(npartitions=1)
print(
    "# partitions after=\n%s"
    % people_filtered_reduced.map_partitions(lambda x: len(x)).compute()
)

# %% [markdown]
# # Reading data from text files

# %%
# !ls Parking*

# %%
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

data_types = {
    "House Number": "object",
    "Time First Observed": "object",
}

fy14 = dd.read_csv(
    "Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv",
    dtype=data_types,
)
fy15 = dd.read_csv(
    "Parking_Violations_Issued_-_Fiscal_Year_2015.csv", dtype=data_types
)
fy16 = dd.read_csv(
    "Parking_Violations_Issued_-_Fiscal_Year_2016.csv", dtype=data_types
)
fy17 = dd.read_csv(
    "Parking_Violations_Issued_-_Fiscal_Year_2017.csv", dtype=data_types
)
fy17

# %%
df = pd.read_csv("Parking_Violations_Issued_-_Fiscal_Year_2017.csv", nrows=10)
df.columns
# re

# %%
# Problems with the column types.
# | House Number        | object | float64  |
# | Time First Observed | object | float64
fy17.head(5)

# %%
# Reading columns is quick.
fy17.columns

# %%
# Find common columns.
from functools import reduce

columns = [
    set(fy14.columns),
    set(fy15.columns),
    set(fy16.columns),
    set(fy17.columns),
]
common_columns = list(reduce(lambda a, i: a.intersection(i), columns))
common_columns

# %%
fy17[common_columns].head()

# %%
# There are issues with the schema.
# Issuer Squad
# Unregistered Vehicle?
# Violation Description
# Violation Legal Code
# Violation Post Code
# fy14[common_columns].head()

# %%
import numpy as np
import pandas as pd
import pprint

dtype_dict = dict([x, str] for x in common_columns)
# print("dtype_dict=", pprint.pformat(dtype_dict))

# Read data with no schema.
fy14 = dd.read_csv(
    "Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv",
    dtype=dtype_dict,
)
fy14_df = fy14[common_columns].head(10000)

# %%
fy14_df.columns

# %%
print(fy14_df["Unregistered Vehicle?"].unique())

# %%
with ProgressBar():
    fy14["Vehicle Year"].unique().head(10)

# %%
# Correct schema.
dtypes = {
    "Date First Observed": str,
    "Days Parking In Effect    ": str,
    "Double Parking Violation": str,
    "Feet From Curb": np.float32,
    "From Hours In Effect": str,
    "House Number": str,
    "Hydrant Violation": str,
    "Intersecting Street": str,
    "Issue Date": str,
    "Issuer Code": np.float32,
    "Issuer Command": str,
    "Issuer Precinct": np.float32,
    "Issuer Squad": str,
    "Issuing Agency": str,
    "Law Section": np.float32,
    "Meter Number": str,
    "No Standing or Stopping Violation": str,
    "Plate ID": str,
    "Plate Type": str,
    "Registration State": str,
    "Street Code1": np.uint32,
    "Street Code2": np.uint32,
    "Street Code3": np.uint32,
    "Street Name": str,
    "Sub Division": str,
    "Summons Number": np.uint32,
    "Time First Observed": str,
    "To Hours In Effect": str,
    "Unregistered Vehicle?": str,
    "Vehicle Body Type": str,
    "Vehicle Color": str,
    "Vehicle Expiration Date": str,
    "Vehicle Make": str,
    "Vehicle Year": np.float32,
    "Violation Code": np.uint16,
    "Violation County": str,
    "Violation Description": str,
    "Violation In Front Of Or Opposite": str,
    "Violation Legal Code": str,
    "Violation Location": str,
    "Violation Post Code": str,
    "Violation Precinct": np.float32,
    "Violation Time": str,
}

# Read data with no schema.
fy14 = dd.read_csv(
    "Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv",
    dtype=dtypes,
    usecols=common_columns,
)

# %% [markdown]
# # Cleaning and trasforming DataFrames
#
# https://github.com/jcdaniel91/data-science-python-dask/blob/master/Chapter%205.ipynb

# %% [markdown]
# ##

# %%
# !ls

# %%
# nyc_data_raw = fy14
# Read data with no schema.
nyc_data_raw = dd.read_csv(
    #'Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv',
    "Parking_Violations_Issued_-_Fiscal_Year_2017.small.csv",
    dtype=dtypes,
    usecols=common_columns,
)
# 391,311,954
# 429,957
with ProgressBar():
    print("num_rows=", nyc_data_raw.size.compute())

# Requesting a single column and getting back a pd.Series.
with ProgressBar():
    display(fy14["Plate ID"].head())

# %%
# Requesting a list of columns and getting back a pd.DataFrame.
with ProgressBar():
    display(fy14[["Plate ID", "Registration State"]].head())

# %%
# Keep all but a column.
display(nyc_data_raw.drop("Violation Code", axis=1).head())

# %%
# Renaming columns.
display(nyc_data_raw)
nyc_data_renamed = nyc_data_raw.rename(columns={"Plate ID": "License Plate"})
display(nyc_data_renamed)

# %%
# Get a slice of rows by index.
with ProgressBar():
    display(nyc_data_raw.loc[100:200].head(100))

# %% [markdown]
# ## Dealing with missing values

# %%
# When we apply head(1000) we materialize a DataFrame.
# missing_values = nyc_data_raw.head(1000).isnull().sum()

# When we do .loc we keep the data in Dask.
missing_values = nyc_data_raw.loc[:1000].isnull().sum()
num_rows = nyc_data_raw.loc[:1000].index.size

with ProgressBar():
    pct_missing = (missing_values / num_rows) * 100
    pct_missing = pct_missing.compute()

pct_missing

# %%
# missing_values.index.size.compute()
# nyc_data_raw.loc[:1000].isnull().compute()

# %%
# All partitions are read and filtered.
missing_values = nyc_data_raw.loc[:1000].isnull().sum()
missing_values.visualize()

# %%
# Drop columns that have more than 50% missing values.
columns_to_drop = list(pct_missing[pct_missing >= 50].index)
print(columns_to_drop)

nyc_data_clean_stage1 = nyc_data_raw.drop(columns_to_drop, axis=1)

# %%
# Impute missing values to the most common.
with ProgressBar():
    count_of_vehicle_colors = (
        nyc_data_clean_stage1["Vehicle Color"].value_counts().compute()
    )
    print("count_of_vehicle_colors\n%s" % count_of_vehicle_colors)
    most_common_color = count_of_vehicle_colors.sort_values(
        ascending=False
    ).index[0]
    print("most_common_color=", most_common_color)

# %%
# Fill nans.
nyc_data_clean_stage2 = nyc_data_clean_stage1.fillna(
    {"Vehicle Color": most_common_color}
)
print(nyc_data_clean_stage2)

# %%
pct_missing

# %%
# Dropping rows with missing data.
rows_to_drop = list(pct_missing[(pct_missing > 0) & (pct_missing < 5)].index)
print("rows_to_drop=", rows_to_drop)
nyc_data_clean_stage3 = nyc_data_clean_stage2.dropna(subset=rows_to_drop)

# %%
# Imputing multiple columns with missing values.
remaining_cols_to_clean = list(
    pct_missing[(pct_missing >= 5) & (pct_missing < 50)].index
)
print("remaining_cols_to_clean=", remaining_cols_to_clean)

# %%
unknown_default_dict = dict(
    map(lambda columnName: (columnName, "Unknown"), remaining_cols_to_clean)
)
pprint.pprint(unknown_default_dict)

# %%
nyc_data_clean_stage4 = nyc_data_clean_stage3.fillna(unknown_default_dict)

with ProgressBar():
    print(nyc_data_clean_stage4.isnull().sum().compute())

nyc_data_clean_stage4.persist()

# %% [markdown]
# ## Recoding data

# %%
with ProgressBar():
    license_plate_types = (
        nyc_data_clean_stage4["Plate Type"].value_counts().compute()
    )

license_plate_types

# %%
# Replace the values not in PAS and COM with Other.
condition = nyc_data_clean_stage4["Plate Type"].isin(["PAS", "COM"])
# New series.
plate_type_masked = nyc_data_clean_stage4["Plate Type"].where(condition, "Other")
# Put the new series in the DataFrame.
nyc_data_recode_stage1 = nyc_data_clean_stage4.drop("Plate Type", axis=1)
nyc_data_recode_stage2 = nyc_data_recode_stage1.assign(
    PlateType=plate_type_masked
)
nyc_data_recode_stage3 = nyc_data_recode_stage2.rename(
    columns={"PlateType": "Plate Type"}
)

# %%
with ProgressBar():
    display(nyc_data_recode_stage3["Plate Type"].value_counts().compute())

# %%
# Put all the unique color in Other.
single_color = list(count_of_vehicle_colors[count_of_vehicle_colors == 1].index)
print("single_color=", single_color)
# Create Series.
condition = nyc_data_clean_stage4["Vehicle Color"].isin(single_color)
vehicle_color_masked = nyc_data_clean_stage4["Vehicle Color"].mask(
    condition, "Other"
)
# Update data frame.
nyc_data_recode_stage4 = nyc_data_recode_stage3.drop("Vehicle Color", axis=1)
nyc_data_recode_stage5 = nyc_data_recode_stage4.assign(
    VehicleColor=vehicle_color_masked
)
nyc_data_recode_stage6 = nyc_data_recode_stage5.rename(
    columns={"VehicleColor": "Vehicle Color"}
)

with ProgressBar():
    display(nyc_data_recode_stage6.compute())

# %% [markdown]
# ## Element wise operations

# %%
from datetime import datetime

# Create derived columns by applying functions.
issue_date_parsed = nyc_data_recode_stage6["Issue Date"].apply(
    lambda x: datetime.strptime(x, "%m/%d/%Y"), meta=datetime
)
nyc_data_derived_stage1 = nyc_data_recode_stage6.drop("Issue Date", axis=1)
nyc_data_derived_stage2 = nyc_data_derived_stage1.assign(
    IssueDate=issue_date_parsed
)
nyc_data_derived_stage3 = nyc_data_derived_stage2.rename(
    columns={"IssueDate": "Issue Date"}
)

with ProgressBar():
    display(nyc_data_derived_stage3["Issue Date"].head())

# %%
# Create a column with year + month.
issue_date_month_year = nyc_data_derived_stage3["Issue Date"].apply(
    lambda dt: dt.strftime("%Y%m"), meta=str
)
nyc_data_derived_stage4 = nyc_data_derived_stage3.assign(
    IssueMonthYear=issue_date_month_year
)
nyc_data_derived_stage5 = nyc_data_derived_stage4.rename(
    columns={"IssueMonthYear": "Citation Issued Month Year"}
)

with ProgressBar():
    display(nyc_data_derived_stage5["Citation Issued Month Year"].head())

# %% [markdown]
# ## Filtering and reindexing DataFrames.

# %%
# Find citations in a certain month (i.e., October).
months = ["201310", "201410", "201510", "201610", "201710"]
condition = nyc_data_derived_stage5["Citation Issued Month Year"].isin(months)
october_citations = nyc_data_derived_stage5[condition]

with ProgressBar():
    display(october_citations.head())

# %%
# Find all the citations after a specific data.
bound_date = "2016-4-25"
condition = nyc_data_derived_stage5["Issue Date"] > bound_date
citations_after_bound = nyc_data_derived_stage5[condition]

with ProgressBar():
    display(citations_after_bound.head())

# %%
# If we want to join dataframes we should index them on the same index and sort.

# %%
with ProgressBar():
    # Find a subset of the data.
    condition = (nyc_data_derived_stage5["Issue Date"] > "2014-01-01") & (
        nyc_data_derived_stage5["Issue Date"] <= "2017-12-31"
    )
    nyc_data_filtered = nyc_data_derived_stage5[condition]
    # Reindex based on the month / year.
    nyc_data_new_index = nyc_data_filtered.set_index(
        "Citation Issued Month Year"
    )

display(nyc_data_new_index.head(10))

# %%
nyc_data_new_index

# %%
# !pip install fastparquet

# %%
# Repartition on the new index.
# years = ['2014', '2015', '2016', '2017']
years = ["2014"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
divisions = [year + month for year in years for month in months]
divisions = ["201401", "201406"]
print("divisions=", divisions)

with ProgressBar():
    # ValueError: left side of old and new divisions are different
    # nyc_data_new_index.repartition(divisions=divisions)
    nyc_data_new_index.repartition(npartitions=2)
    # .to_parquet('nyc_data_date_index')#, compression='snappy')

# nyc_data_new_index = dd.read_parquet('nyc_data_date_index')

# %% [markdown]
# # Summarizing and analyzing df

# %% [markdown]
# # Visualizing df with Seaborn

# %% [markdown]
# # Working with Bags and Array

# %% [markdown]
# The format is
#
# ```
# product/productId: B001E4KFG0
# review/userId: A3SGXH7AUHU8GW
# review/profileName: delmartian
# review/helpfulness: 1/1
# review/score: 5.0
# review/time: 1303862400
# review/summary: Good Quality Dog Food
# review/text: I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product better than  most.
# ```

# %%
# !ls /data

# %%
import dask.bag as bag

raw_data = bag.read_text("/data/finefoods.txt")
raw_data

# %%
# `take()` is equivalent to `head()`.
# Each element is a line.
raw_data.take(10)

# %%
# Error since there are chars that can't be decoded with utf-8.
# raw_data.count().compute()

# %%
raw_data = bag.read_text("/data/finefoods.txt", encoding="cp1252")
raw_data.count().compute()

# %%
from dask.delayed import delayed


def get_next_part(file, start_index, span_index=0, blocksize=1000):
    # Read the next chunk.
    file.seek(start_index)
    buffer = file.read(blocksize + span_index).decode("cp1252")
    # Look for the end of the record.
    delimiter_position = buffer.find("\n\n")
    if delimiter_position == -1:
        # The delimiter is not found: try to read more data recursively.
        return get_next_part(file, start_index, span_index + blocksize)
    else:
        file.seek(start_index)
        return start_index, delimiter_position


with open("/data/finefoods.txt", "rb") as fh:
    # Get size of the file in bytes.
    size = fh.seek(0, 2) - 1
    more_data = True
    output = []
    curr_pos = next_pos = 0
    while more_data:
        # print(curr_pos, next_pos)
        if curr_pos >= size:
            # We have reached the end fo the file.
            more_data = False
        else:
            # Find the next record starting from the current position.
            curr_pos, next_pos = get_next_part(fh, curr_pos, 0)
            output.append((curr_pos, next_pos))
            # Add two position since there are two `\n`.
            curr_pos = curr_pos + next_pos + 2
