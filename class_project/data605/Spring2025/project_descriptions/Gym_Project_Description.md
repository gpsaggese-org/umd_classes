### **Gym**

**Title**: Real-time Bitcoin Analytics with Apache Kafka

**Difficulty**: 1 (easy)

**Description** This project introduces students to Apache Kafka, a distributed streaming platform that is used for building real-time data pipelines and streaming applications. Students will learn how to utilize Kafka's capabilities to ingest Bitcoin price data in real-time and perform basic processing. The project will emphasize understanding Kafka's core components, such as topics, producers, consumers, and brokers. Additionally, the project will focus on using basic Python packages for data handling and analysis.

**Describe technology**

- **Apache Kafka**: An open-source stream-processing software platform developed by LinkedIn and donated to the Apache Software Foundation. Kafka is designed to handle live data feeds, providing a robust messaging system with high throughput, reliability, and low latency.  
  - **Core Components**:  
    - *Topics*: Categories to which records are published.  
    - *Producers*: Send data to topics.  
    - *Consumers*: Subscribe to topics to receive data.  
    - *Brokers*: Servers handling data transfers.  
- The focus will be on understanding and implementing the necessary components to handle real-time data flow efficiently.

**Describe the project**

- **Objective**: Create an application that continuously ingests real-time Bitcoin prices using Apache Kafka and performs basic time series analysis, such as calculating simple moving averages.  
- **Steps**:  
  1. **Kafka Setup**: Set up a local Kafka environment using Docker and configure the necessary components to start ingesting data.  
  2. **Data Ingestion**: Use a Python script to act as a Kafka producer, fetching real-time Bitcoin price data from a public API (e.g., CoinGecko) and sending it to a Kafka topic.  
  3. **Data Consumer**: Develop a Kafka consumer in Python using basic packages like `kafka-python` to read from the Kafka topic.  
  4. **Data Processing**: Implement basic time series analysis, such as calculating moving averages, using Pandas.  
  5. **Visualization**: (Optional) Visualize the processed data using Python libraries like Matplotlib or Plotly.  
- The project will help students gain hands-on experience in setting up a simple real-time data ingestion and processing pipeline.

**Useful resources**

- [Apache Kafka Quickstart Guide](https://kafka.apache.org/quickstart)  
- [CoinGecko API](https://www.coingecko.com/en/api/documentation)  
- [Kafka-Python Documentation](https://kafka-python.readthedocs.io/en/master/)  
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

**Is it free?** Yes, Apache Kafka is free and open-source. The CoinGecko API is also free for simple use cases.

**Python libraries / bindings**

- `kafka-python`: A Python client for Apache Kafka. Install using `pip install kafka-python`.  
- `requests`: For fetching data from the Bitcoin price API. Install using `pip install requests`.  
- `pandas`: To perform time series analysis. Install using `pip install pandas`.  
- `matplotlib` or `plotly`: Optional for data visualization. Install using `pip install matplotlib` or `pip install plotly`.
