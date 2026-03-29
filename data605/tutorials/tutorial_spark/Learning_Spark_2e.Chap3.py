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
# In Python
# Create an RDD of tuples (name, age)
dataRDD = sc.parallelize(
    [("Brooke", 20), ("Denny", 31), ("Jules", 30), ("TD", 35), ("Brooke", 25)]
)
print(dataRDD)
# Use map and reduceByKey transformations with their lambda
# expressions to aggregate and then compute average
agesRDD = (
    dataRDD.map(lambda x: (x[0], (x[1], 1)))
    .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
    .map(lambda x: (x[0], x[1][0] / x[1][1]))
)

# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

# Create a DataFrame using SparkSession
spark = SparkSession.builder.appName("AuthorsAges").getOrCreate()
# Create a DataFrame
data_df = spark.createDataFrame(
    [("Brooke", 20), ("Denny", 31), ("Jules", 30), ("TD", 35), ("Brooke", 25)],
    ["name", "age"],
)
# Group the same names together, aggregate their ages, and compute an average
avg_df = data_df.groupBy("name").agg(avg("age"))
# Show the results of the final execution
avg_df.show()
