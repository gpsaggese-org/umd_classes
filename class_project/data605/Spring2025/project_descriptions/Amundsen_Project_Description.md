### **Amundsen**

**Title**: Implementing Bitcoin Price Alert System using Amundsen

**Difficulty**: 1 (easy)

**Description**  
Amundsen is an open-source data discovery and metadata engine introduced by Lyft. It helps data scientists, analysts, and engineers increase productivity by making the data they need easy to find, understand, and trust. This project focuses on leveraging Amundsen to catalog and discover Bitcoin price data and using basic Python packages to explore real-time data analysis tasks.

**Describe technology**

- Amundsen is built on top of various components like Apache Atlas for metadata storage, Elasticsearch for search, and Neo4j for graph data stored.  
- It provides an intuitive user interface for data users to search for datasets, explore associated metadata, and understand lineage and usage.  
- Key features include data discovery via search, lineage view to understand data dependencies, and a profiler for table quality and freshness.

**Describe the project**

- This project aims to establish a Bitcoin Price Alert System using Amundsen and basic Python packages.  
- First, students will ingest Bitcoin price data from a public API like CoinGecko and store it in a database such as SQLite.  
- They will then configure Amundsen to catalog the ingested data, making it easily searchable and discoverable.  
- Students will create a simple Python program to monitor real-time price changes using the ingested data and trigger alerts for significant price movements, using the Amundsen catalog to track data quality and freshness.  
- Finally, students will visualize time series data and explore historical price trends to understand long-term patterns.

**Useful resources**

- [Amundsen GitHub Repository](https://github.com/amundsen-io/amundsen)

**Is it free?**   
Yes, Amundsen is open-source and free to use.

**Python libraries / bindings**

- Amundsen Libraries: Client libraries to interact with Amundsen components for metadata and data cataloging tasks.  
- Requests: For pulling real-time data from APIs like CoinGecko.  
- SQLite3: For storing and managing ingested data.  
- Pandas: For data manipulation and analysis.  
- Matplotlib or Plotly: For visualizing time series data and patterns.
