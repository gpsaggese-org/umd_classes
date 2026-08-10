### **Apache Hadoop**

**Title**: Real-time Bitcoin Data Processing with Apache Hadoop

**Difficulty**: 1 (easy)

**Description**  
Apache Hadoop is an open-source software framework used for distributed storage and processing of large datasets across clusters of computers using simple programming models. It is designed to scale up from a single server to thousands of machines, with a high degree of fault tolerance.

In this project, students will explore the fundamental concepts of Apache Hadoop, including its core components such as Hadoop Distributed File System (HDFS) and MapReduce. The aim is to use Hadoop to ingest real-time Bitcoin price data and perform basic time series analysis using Python.

**Describe technology**

- **Hadoop Distributed File System (HDFS)**: A distributed file system that provides high-throughput access to application data.  
- **MapReduce**: A programming model for large-scale data processing, consisting of Map (transform data) and Reduce (aggregate data) tasks.  
- **YARN**: Yet Another Resource Negotiator, which handles resource management and job scheduling in Hadoop clusters.  
- **Hadoop Ecosystem**: Complements include tools like Hive (data warehousing) and Pig (scripting for data transformation).

**Describe the project**

- **Objective**: Ingest and process Bitcoin price data using Apache Hadoop, and conduct a basic time series analysis.  
- **Step 1**: Set up a small Hadoop cluster using Apache Hadoop on local machines or in a cloud-based environment.  
- **Step 2**: Use a public API, such as CoinGecko, to periodically fetch real-time Bitcoin price data and store it in HDFS.  
- **Step 3**: Implement a MapReduce job using Python to process the stored Bitcoin data. The job should perform a simple analysis, such as calculating the moving average of Bitcoin prices over specific time intervals.  
- **Step 4**: Present findings and visualizations of the time series analysis using Python plotting libraries like matplotlib or seaborn.

**Useful resources**

- [Apache Hadoop Official Documentation](https://hadoop.apache.org/docs/)  
- [Apache Hadoop Setup Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html)  
- [Intro to MapReduce on Hadoop](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)  
- [CoinGecko API Documentation](https://coingecko.com/en/api)

**Is it free?**  
Yes, Apache Hadoop is an open-source framework and free to use. Note that using cloud services may incur costs.

**Python libraries / bindings**

- **Hadoop Streaming**: A utility to create and run Map/Reduce jobs with any executable or script as the mapper and/or reducer. Use this for writing Hadoop jobs in Python.  
- **matplotlib**: A plotting library for the Python programming language to create static, interactive, and animated visualizations.  
- **requests**: A simple HTTP library for Python for making API requests to fetch Bitcoin data.

This project gives students hands-on experience with Hadoop's capabilities and the basics of working with real-time data ingestion for time series analysis.
