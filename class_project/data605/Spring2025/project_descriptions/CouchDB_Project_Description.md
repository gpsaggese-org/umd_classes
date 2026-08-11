### **CouchDB**

**Title**: Real-time Bitcoin Data Ingestion and Analysis using CouchDB

**Difficulty**: Easy

**Description**  
Apache CouchDB is an open-source NoSQL database that uses a document-oriented data model. CouchDB is known for its ease of use, real-time data updating capabilities, and its efficient replication protocol designed for offline-first applications. The aim of this project is to teach students how to use CouchDB for storing and processing real-time data, such as Bitcoin prices, using basic Python packages for additional processing.

**Describe technology**

- CouchDB stores data in a JSON-based, document-based model allowing complex data structures to be easily handled.  
- It uses MapReduce views and indexing, which provide powerful querying capabilities.  
- CouchDB supports multi-master setups, meaning that you can have multiple copies of your database actively synchronizing with each other.  
- It is highly scalable and has built-in support for fault-tolerance and database sync across distributed systems.

**Describe the project**

1. **Ingest Real-time Bitcoin Data**: Use the public CoinGecko API to continuously fetch Bitcoin prices.  
2. **Store Data in CouchDB**: Set up a CouchDB instance and create a database to store the data fetched from the API. Each data point (price information) will be stored as a JSON document.  
3. **Data Processing**: Use Python to access the data stored in CouchDB and perform basic time-series analysis, such as calculating moving averages or visualizing price trends over time.  
4. **Query and View Creation**: Create MapReduce views in CouchDB to filter and sort data according to specific criteria, for example, finding price trends over specific intervals.  
5. **Presentation**: Implement a simple command-line interface using Python to query the database and present the analyzed data.

**Useful resources**

- [CouchDB Official Documentation](https://docs.couchdb.org/en/stable/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Python CouchDB Library](https://pypi.org/project/CouchDB/)

**Is it free?**  
Yes, CouchDB is open-source and free to use. CoinGecko also provides free access to its API with certain rate limitations.

**Python libraries / bindings**

- CouchDB: To interact with the CouchDB instance and manage databases, you can use the CouchDB Python client: `pip install CouchDB`.  
- Requests: To fetch data from the CoinGecko API, you might want to use the Requests library to manage HTTP requests: `pip install requests`.  
- Pandas: For data processing and analysis of time-series data: `pip install pandas`.  
- Matplotlib: For visualizing data and creating graphs: `pip install matplotlib`.
