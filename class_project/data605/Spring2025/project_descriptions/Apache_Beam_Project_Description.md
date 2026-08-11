### **Apache Beam**

**Title**: Real-Time Bitcoin Price Analysis Using Apache Beam  
**Difficulty**: 1 (Easy)

**Description**  
This project involves utilizing Apache Beam for ingesting and processing real-time Bitcoin price data. Apache Beam is a unified model for defining both batch and streaming data-parallel processing pipelines. As part of this beginner project, students will gather real-time Bitcoin data from a public API and perform basic time series analysis using Python.

**Describe technology**

- Apache Beam: An open-source unified programming model to define and execute data processing pipelines, including ETL and batch/streaming.  
- It abstracts away the details of the execution engines, enabling decoupling of logic and execution.  
- Focus is on simplicity and ease of use, making it suitable for introducing new users to big data systems.

**Describe the project**

- Set up an environment to run Apache Beam locally using the Python SDK.  
- Use Python scripts to fetch real-time Bitcoin price data from an open-source API like CoinGecko.  
- Construct an Apache Beam pipeline to stream and process the Bitcoin data. This includes steps like:  
  - Fetching data every minute.  
  - Extracting relevant fields such as timestamp and price.  
  - Performing basic calculations to analyze price trends over a specific time window (e.g., compute average price over 10-minute intervals).  
- Output the processed data to a local file system, Google Cloud Storage, or any other supported storage backend.  
- Visualize the trend using a simple plot in Python.

**Useful resources**

- [Apache Beam Documentation](https://beam.apache.org/documentation/)  
- [Apache Beam Python SDK Quickstart](https://beam.apache.org/get-started/quickstart-py/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)

**Is it free?**  
Yes, Apache Beam is open-source and free to use. However, operational costs might incur if you choose to deploy the pipeline on a cloud data processing service such as Google Cloud Dataflow.

**Python libraries / bindings**

- `apache-beam`: Install via `pip install apache-beam`. It provides the necessary tools to define and execute Beam data processing pipelines in Python.  
- `requests`: Utility library for making HTTP requests to fetch Bitcoin price data from the API (install via `pip install requests`).  
- `matplotlib` or `seaborn`: For creating simple plots to visualize the processed time series data (install via `pip install matplotlib` or `seaborn`).
