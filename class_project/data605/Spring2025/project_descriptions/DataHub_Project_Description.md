### **DataHub**

**Title**: Real-time Bitcoin Data Processing with DataHub

**Difficulty**: Easy

**Description**  
DataHub is an open-source platform that helps users to discover, understand, and collaborate on datasets. It's built to handle metadata management, making it easier to manage large data ecosystems by facilitating dataset lineages, versioning, and collaborative data efforts. Through this project, students will learn the basic concepts of DataHub, including how to set up and manage a simple data lineage and metadata management process.

**Describe technology**

- DataHub offers features like easy dataset discovery, data lineage tracking, and metadata storage, which make it ideal for handling datasets in real-time environments.  
- Students will get familiar with DataHub's basic concepts, including ingesting metadata and managing data flows through a centralized platform.  
- Understand how DataHub supports integration with third-party data platforms and tools using its Python-friendly API.

**Describe the project**

- **Objective**: Implement a real-time data ingestion and processing system for Bitcoin price data utilizing DataHub for metadata management.  
- Students will initially set up a basic DataHub environment, enabling them to create a metadata catalog for their datasets and interactions.  
- Use a public API like CoinGecko to fetch real-time Bitcoin prices.  
- Implement a script in Python to continuously ingest these prices and update the DataHub metadata catalog accordingly.  
- Carry out time series analysis on the ingested Bitcoin data to identify trends, visualize price changes, and store these analyses within DataHub to facilitate easy access and collaboration.  
- The project reinforces key concepts of data ingestion, real-time data processing, and metadata management.

**Useful resources**

- [DataHub Official Documentation](https://datahubproject.io/docs/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Introduction to Time Series Analysis with Python](https://towardsdatascience.com/introduction-to-time-series-analysis-using-python-3eca768058b4)

**Is it free?**  
Yes, DataHub is open-source and free to use. However, if you require cloud infrastructure to deploy it, there might be associated costs.

**Python libraries / bindings**

- DataHub’s Python Client: Use for interfacing with DataHub to catalog your data.  
- `requests` library: For handling API requests to fetch real-time Bitcoin data.  
- `pandas`: For easy manipulation and analysis of the time series data.  
- `matplotlib` or `seaborn`: For data visualization to facilitate time series trend analysis.
