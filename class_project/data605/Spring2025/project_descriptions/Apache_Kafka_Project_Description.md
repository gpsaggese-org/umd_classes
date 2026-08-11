### **Apache Kafka**

**Title**: Real-Time Bitcoin Price Analysis using Apache Kafka  
**Difficulty**: 1 (easy)

**Description**  
Apache Kafka is an open-source distributed event streaming platform designed to handle real-time data feeds with high throughput and low latency. It is commonly used for building real-time streaming data pipelines and applications that require data integration across different sources.

In this easy project, students will use Apache Kafka to ingest real-time Bitcoin price data from a public API and process it for a simple time series analysis. This project will be completed over one week and offers practical experience with real-time data ingestion and processing.

**Describe technology**

- **Apache Kafka**: A distributed publishing and subscribing messaging system designed to scale to handle multiple producers and consumers simultaneously.  
  - **Core components**: Topics (a stream of records), Producers (writing data to topics), Consumers (reading data from topics), Brokers (Kafka server instances), and Zookeepers (coordinate brokers).  
  - **Key features**:  
    - Reliability and fault-tolerance through distributed architecture.  
    - Scalability allowing it to manage extensive data feeds.  
    - Durability by persisting records on disk.  
    - High throughput, suitable for real-time processing.

**Describe the project**

- **Objective**: Ingest real-time Bitcoin price data and conduct a basic time series analysis using Apache Kafka and Python.  
- **Steps**:  
  1. **Setup Apache Kafka**:  
     - Install Apache Kafka on your local machine or use a managed Kafka service.  
     - Create a Kafka topic  ("bitcoin\_prices") for ingesting real-time Bitcoin price data.  
  2. **Data Ingestion**:  
     - Use a simple Python script to act as a producer, fetching real-time price data from a public Bitcoin API (such as CoinGecko) and sending it to the Kafka topic.  
  3. **Data Processing**:  
     - Create a Python consumer script to consume messages from the Kafka topic.  
     - Perform basic transformations, such as aggregating prices over fixed intervals (e.g., average price per minute).  
  4. **Time Series Analysis**:  
     - Store the aggregated data in a local file or database.  
     - Use basic Python statistical packages like Pandas to analyze the time series data, calculate metrics (e.g., moving averages), and visualize trends.

**Useful resources**

- [Apache Kafka Quickstart](https://kafka.apache.org/quickstart)  
- [CoinGecko API Documentation](https://coingecko.com/en/api)  
- [Pandas: Python Data Analysis Library](https://pandas.pydata.org/docs/)

**Is it free?**  
Yes, Apache Kafka is open-source and free to use. However, hosting Kafka might incur costs depending on the infrastructure used (e.g., cloud services).

**Python libraries / bindings**

- **Kafka-Python**: A Python client for the Apache Kafka platform `pip install kafka-python`  
- **Requests**: To fetch real-time Bitcoin data from APIs  `pip install requests`  
- **Pandas**: For data analysis and manipulation `pip install pandas`
