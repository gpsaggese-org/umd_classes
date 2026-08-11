### **Ray**

**Title**: Real-time Bitcoin Data Processing with Apache Ray

**Difficulty**: 2 (Medium)

**Description**

Apache Ray is an open-source, distributed computing framework that allows you to build applications that can handle large-scale, real-time data processing tasks. With Ray, developers can more easily scale their Python workloads to utilize multiple cores and nodes, offering both simplicity and powerful abstractions for concurrent and parallel computing.

This project involves utilizing Ray to ingest real-time Bitcoin price data, process it, and perform time series analysis on the data. Students will gain hands-on experience with real-time data processing using Ray, learning to build scalable systems with a focus on distributed computing paradigms.

**Describe technology**

- **Ray Core Concepts**: Understand the key features of Apache Ray, such as its actor model for stateful computation and task parallelism. Learn about Ray's architecture, including its scheduler, distributed execution, and object store for shared-memory and communication between tasks.  
    
- **Real-time Data Processing**: Learn how Ray can handle streaming data and integrate with other data sources and systems to manage continuous data ingestion. Understand how the framework can one take advantage of the multi-core processors for improved performance.

**Describe the project**

- **Real-time Data Ingestion**: Implement a Python script using Ray to continuously ingest Bitcoin price data from an API such as CoinGecko or another public data source. Set up a mechanism for maintaining live connections and fetching fresh data in real-time.  
    
- **Data Processing and Transformation**: Use Ray's parallel processing capabilities to handle large volumes of incoming data. Apply transformations to the data, such as converting timestamps, calculating percentage changes, or filtering for specific criteria.  
    
- **Time Series Analysis**: Conduct a basic time series analysis on the ingested and processed data, such as moving averages or volatility indices. Utilize Ray's distributed nature to efficiently manage and calculate these metrics across large datasets.  
    
- **Visualization and Reporting**: Optionally, integrate visualization tools such as Matplotlib or Plotly to create real-time graphs and dashboards that display the Bitcoin prices and analysis results.

**Useful resources**

- [Ray Official Documentation](https://docs.ray.io/en/latest/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**

Yes, Apache Ray is an open-source project licensed under the Apache License 2.0, and it can be used for free. However, students may incur costs from any required cloud infrastructure or data services used during the project.

**Python libraries / bindings**

- **Ray**: Core library for distributed computing and parallel processing. It can be installed using `pip install ray`.  
    
- **Requests or HTTPx**: Used for accessing public APIs for Bitcoin data. Install via `pip install requests` or `pip install httpx`.  
    
- **Pandas**: Essential for data manipulation and analysis, especially useful in handling time series data. Install with `pip install pandas`.  
    
- **Plotly or Matplotlib**: For visualizing time series data. Install with `pip install plotly` or `pip install matplotlib`.

This project provides a practical understanding of distributed real-time data processing systems and how Ray can be leveraged to enhance Python's capabilities for time-sensitive data tasks.
