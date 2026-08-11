### **AWS Athena**

* **Title**: Analyze Bitcoin price trends using AWS Athena  
* **Difficulty**: 1 (Easy)  
* **Description**  
  * **AWS Athena** is an interactive query service that makes it easy to analyze data directly in Amazon S3 using standard SQL. Athena is serverless, so there is no need to manage infrastructure, and it can query large datasets with ease. It supports data formats such as CSV, JSON, Parquet, ORC, and Avro. Athena automatically integrates with AWS Glue for data cataloging, making it a powerful tool for big data analytics.  
  * **The project** involves using AWS Athena to analyze Bitcoin price data in real time. You will first collect Bitcoin price data from a public API like CoinGecko or CryptoCompare and store it in an S3 bucket in JSON format. The next step is to create a Glue Data Catalog for this data, allowing Athena to query it. After setting up the catalog, you will write SQL queries in Athena to perform time series analysis, such as calculating moving averages or identifying price trends over specific time intervals. Finally, you will present the results of your analysis in a structured format, such as CSV or Parquet, which can be further processed or visualized. This project gives students a hands-on introduction to serverless analytics and time series analysis using SQL, making it a practical and efficient way to process large-scale data.  
* **Useful resources**  
  * **Is it free?**  
    * Athena charges based on the amount of data scanned by your queries. It’s cost-effective for smaller datasets, but be mindful of query optimization to reduce costs. AWS offers a free tier with limited usage.  
  * **Python libraries / bindings**

    * **boto3**: The official AWS SDK for Python allows you to interact with Athena and other AWS services programmatically. You can use boto3 to submit queries, retrieve results, and manage your S3 bucket. You can install it via `pip install boto3`.  
    * **pandas**: Used to process and visualize the query results from Athena in Python. It's helpful for analyzing data and generating reports. Install it via `pip install pandas`.  
    * **awswrangler**: A library that simplifies interaction with AWS services, particularly for querying Athena and working with data stored in S3. It supports data frames and integrates with pandas. Install via `pip install awswrangler`.  
    * **SQL**: The query language you will use within Athena to interact with your data. You will write SQL queries for time series analysis, filtering, and aggregating the Bitcoin price data.  
  * **References**  
    * **boto3 (AWS SDK for Python)**: [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  
    * **awswrangler**: [AWS Wrangler Documentation](https://aws-sdk-pandas.readthedocs.io/en/stable/)  
    * **AWS Athena**: [AWS Athena Documentation](https://docs.aws.amazon.com/athena/latest/ug/what-is-athena.html)  
    * **pandas**: [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
