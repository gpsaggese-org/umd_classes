### **Dagster**

**Title**: Real-time Bitcoin Data Ingestion and Analysis with Dagster   
**Difficulty**: Medium 

Description: Dagster is an open-source data orchestration platform designed to develop, run, monitor, and maintain data processing pipelines. It is particularly useful for managing complex workflows that require several stages of transformation and different data sources. Dagster provides robust error handling, logging, and monitoring capabilities, making it a powerful tool for data scientists and engineers. Its unique approach to defining data pipelines through solid compositions allows users to modularly build and reuse components across projects.

In this project, students will set up a real-time data ingestion and processing system for Bitcoin prices using Dagster. The aim is to fetch real-time Bitcoin price data from a public API (e.g., CoinGecko or Binance), store it for historical analysis, and perform preliminary time series analysis. Students will focus on building a Dagster pipeline that continuously collects Bitcoin data, performs some initial transformations, and stores the results in a database like SQLite or a local CSV file.

- **Describe technology:**  
    
  - Understand Dagster's core elements: solids, pipelines, and resources.  
  - Learn to define and execute pipelines using Dagster's domain-specific language and Python.  
  - Explore Dagster's capabilities for handling failures, retries, and logging.  
  - Utilize Dagster's UI for monitoring and visualizing pipeline execution and debugging processes.


- **Describe the project:**  
    
  - Set up a Dagster environment and create a new repository for the project.  
  - Develop a solid for making API requests to fetch Bitcoin price data.  
  - Create a solid to process and transform the fetched data, extracting relevant features like date-time and price.  
  - Implement a storage solution using SQLite or CSV to save the processed data for historical tracking and analysis.  
  - Design a pipeline to automate the ingestion and storage process.  
  - Perform basic time series analysis on the stored Bitcoin data, such as calculating moving averages or detecting trends.  
  - Learn to schedule the pipeline to run at defined intervals to ensure continuous data ingestion.


- **Useful resources:**  
    
  - [Dagster Documentation](https://docs.dagster.io/)  
  - [Getting Started with Dagster](https://docs.dagster.io/getting-started)  
  - [CoinGecko API Documentation](https://www.coingecko.com/en/api)


- **Is it free?**  
    
  - Yes, Dagster is open-source and free to use. You might incur costs depending on how you choose to store data (e.g., cloud storage services).


- **Python libraries / bindings:**  
    
  - `Dagster`: Core libraries to set up and run data orchestrations. (Install with `pip install dagster`)  
  - `Requests`: A simple HTTP library for making API requests. (Install with `pip install requests`)  
  - `Pandas`: A powerful data manipulation library for processing data. (Install with `pip install pandas`)  
  - `SQLite`: A lightweight database accessible through Python's built-in `sqlite3` module.  
  - `Matplotlib` or `Plotly`: For visualizing historical Bitcoin trends as part of the time series analysis.
