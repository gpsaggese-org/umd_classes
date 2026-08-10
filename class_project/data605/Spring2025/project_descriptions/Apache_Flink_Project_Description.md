### **Apache Flink**

**Title**: Ingest and Analyze Bitcoin Prices Using Apache Flink  
**Difficulty**: Medium (2)

**Description**  
Apache Flink is an open-source stream processing framework for distributed, high-performing, always-available, and accurate data streaming applications. It is designed to process unbounded data streams with low latency and guarantees exactly-once state consistency. Flink's powerful and flexible windowing mechanism allows real-time data processing, making it a strong fit for financial market applications like analyzing cryptocurrency price movements.

**Describe technology**

- Apache Flink is a stream processing framework that supports real-time processing of data streams.  
- It offers features such as event time processing, batch processing, and stateful computations.  
- Built-in support for complex event processing (CEP), allowing users to detect patterns in data streams.  
- Integrates with various data sources and sinks like Apache Kafka, Kinesis, Elasticsearch, and more.  
- Flink's high throughput and low latency make it suitable for complex analytical tasks.

**Describe the project**  
The project focuses on creating a Flink job to ingest and process real-time Bitcoin price data from a public API such as CoinGecko or Binance. Students will:

- Set up an Apache Flink environment locally or via a cloud service supporting Flink.  
- Develop a Flink streaming job to consume bitcoin price data from an API.  
- Implement time windowing to perform real-time time series analysis on Bitcoin price data, such as calculating moving averages or identifying price trends.  
- Use Python with Apache Flink's PyFlink API for crafting the streaming job logic.  
- Explore Flink's state management abilities to track and update the state of Bitcoin prices over time.  
- Optionally, integrate the project with a visualization tool like Grafana for real-time data visualization and analysis results.

**Useful resources**

- [Official Apache Flink Documentation](https://flink.apache.org/)  
- [PyFlink API Documentation](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/python/getting-started/)  
- [Real-time stream processing with PyFlink](https://flink.apache.org/news/2020/05/21/news-flink-python.html)

**Is it free?**  
Yes, Apache Flink is open-source software available under the Apache License 2.0, which is free to use and modify. However, associated costs might arise if using a cloud service to run Flink jobs.

**Python libraries / bindings**

- **PyFlink**: The Python API for Apache Flink. It provides bindings for developing Flink jobs using Python and is essential for this project. You can install PyFlink via `pip install apache-flink`.  
- **Requests**: Helps in making HTTP requests to access the Bitcoin price API. Install it using `pip install requests`.  
- **Matplotlib/Plotly** (optional): For data visualization, you might want to use libraries like Matplotlib or Plotly. Install via `pip install matplotlib` or `pip install plotly`.
