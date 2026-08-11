### **Spark SQL**

**Title**: Implementing Real-Time Bitcoin Price Analysis with Spark SQL  
**Difficulty**: 2 (Medium)

**Description**  
Spark SQL is a module of Apache Spark, designed for structured data processing. It allows users to run SQL queries on DataFrames and is highly advantageous for handling big data. One of its primary features is the ability to perform transformations and actions on large datasets using SQL-like syntax.

**Describe technology**

- Spark SQL enables seamless integration with Spark's core capabilities.  
- It provides API support in Python, Java, Scala, and R.  
- It leverages in-memory data processing for faster analytics.  
- Supports Hive metastore to manage metadata about tables and databases.  
- Provides a simple way to execute SQL queries using Spark’s scalable data processing engine.

**Describe the project**  
This easy-level project focuses on building a basic real-time data ingestion and processing pipeline using Spark SQL to analyze Bitcoin prices. The goal is to retrieve Bitcoin price data from a publicly available API and perform a time series analysis using Spark SQL.

- **Ingest**: Use Python to call a Bitcoin price API (e.g., CoinGecko) and ingest data in real-time.  
- **Store**: Store the incoming data in-memory using Spark DataFrames.  
- **Query**: Implement Spark SQL to perform time-series analysis.  
  - Example Queries:  
    - Calculate average price over the past week.  
    - Identify daily maximum and minimum prices.  
  - Use Spark SQL functions like `avg`, `max`, and `min` to perform these analyses easily.  
- **Visualize**: Optionally, use basic Python plotting libraries like Matplotlib or Plotly to visualize the results of your analysis.

**Useful resources**

- [Apache Spark SQL Documentation](https://spark.apache.org/sql/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Spark SQL Programming Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

**Is it free?**  
Yes, Apache Spark is open-source software, and you can deploy it locally or on a cloud provider's free tier.

**Python libraries / bindings**

- **pyspark**: The official Python library for Spark. To work with Spark SQL in Python, you'll use the `pyspark.sql` module, which allows you to interact with Spark DataFrames and execute SQL queries.  
  - Installation: `pip install pyspark`  
- **requests**: A library for making HTTP requests to call the Bitcoin price API.  
  - Installation: `pip install requests`  
- **pandas**: Optional, for intermediate data manipulation if needed.  
  - Installation: `pip install pandas`  
- **matplotlib/plotly**: Optional, for plotting the time series analysis results.  
  - Installation: `pip install matplotlib` or `pip install plotly`

By completing this project, students will gain hands-on experience with Spark SQL, as well as foundational skills in processing and analyzing real-time data using Python.
