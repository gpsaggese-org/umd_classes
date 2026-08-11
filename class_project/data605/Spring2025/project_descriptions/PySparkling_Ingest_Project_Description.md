### **pySparkling**

**Title**: Ingest and Process Bitcoin Prices Using PySparkling

**Difficulty**: 1 (easy)

**Description**  
PySparkling is a Python interface for using the H2O Sparkling Water platform that combines the user-friendly nature of Python with the scalable machine learning capabilities of H2O.ai and Apache Spark. It allows you to efficiently process large datasets using Spark's distributed computing capabilities while also leveraging H2O's machine learning algorithms.

**Describe technology**

- **PySparkling**: An interface to integrate H2O.ai Machine Learning with Spark, allowing distributed computations on large data volumes.  
- **Apache Spark**: An open-source, distributed processing system used for big data workloads, providing built-in modules for streaming, SQL, machine learning, and graph processing.  
- **H2O.ai**: Provides scalable machine learning algorithms, such as Gradient Boosting, Random Forest, and K-Means, which can be applied to big data problems.

**Describe the project**  
This project involves using PySparkling to ingest real-time Bitcoin price data from a public API (e.g., CoinGecko) for time series analysis. You will:

1. **Data Ingestion**:  
     
   - Utilize Python's `requests` library to set up an automated data retrieval system fetching Bitcoin price data at regular intervals.  
   - Integrate the collected data with PySpark and convert it to a format suitable for analysis.

   

2. **Data Processing**:  
     
   - Utilize PySparkling to perform basic transformations on the ingested data, such as parsing JSON data, filtering unnecessary fields, and handling missing values.

   

3. **Time Series Analysis**:  
     
   - Implement a simple time series analysis using PySparkling's machine learning functionalities, for instance, using H2O's AutoML to predict future Bitcoin prices based on historical data.

   

4. **Data Storage**:  
     
   - Store the processed data back into a storage solution like a local file system or a cloud storage service in CSV or Parquet format for future retrieval and analysis.

**Useful resources**

- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [PySparkling Documentation](https://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/pysparkling.html)  
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)  
- [H2O.ai Documentation](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/index.html)

**Is it free?**  
Yes, PySparkling is open-source and free to use. While integrating with other platforms such as cloud storage might incur costs, using local resources is entirely free.

**Python libraries / bindings**

- **PySparkling**: Used for combining Apache Spark's processing power with H2O.ai's machine learning capabilities.  
- **requests**: To fetch real-time data from Bitcoin price APIs.  
- **pandas**: For data manipulation and pre-processing.  
- **numpy**: For numerical operations and handling time series indices.

This project will give students hands-on experience with setting up a basic big data pipeline in Python using PySparkling, allowing them to gain practical skills in real-time data ingestion, processing, and analysis.
