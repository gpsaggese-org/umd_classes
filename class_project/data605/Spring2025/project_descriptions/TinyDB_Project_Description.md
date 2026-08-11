### **TinyDB**

**Title**: Real-Time Bitcoin Data Analysis using TinyDB

**Difficulty**: 1 (easy)

**Description**: This project involves using TinyDB, a lightweight and simple JSON-based database for Python, to store and analyze real-time Bitcoin price data. TinyDB is an ideal choice for projects that require minimal setup, allowing students to focus on understanding data ingestion and basic analysis in a time-series context. In this project, students will fetch Bitcoin price data from a public API, store it using TinyDB, and perform basic time-series analysis to understand trends and patterns in price fluctuations.

**Describe Technology**:

- **TinyDB** is a simple, document-oriented database that runs within Python applications. It stores data as JSON documents, making it easy to set up and use for small-scale projects or during initial development stages.  
- Core functionalities include:  
  - Easy installation and setup within any Python environment as it does not require a server.  
  - Supports custom queries using traditional Python expressions.  
  - Provides modules for handling data persistence and caching.

**Describe the Project**:

- **Step 1**: Install TinyDB and required Python libraries. Use `pip install tinydb` to get started.  
- **Step 2**: Use a public API (e.g., CoinGecko) to fetch Bitcoin price data at regular intervals.  
- **Step 3**: Store the ingested data into a TinyDB database. This involves defining a schema for the data (e.g., timestamp, price) and writing functions to add new entries.  
- **Step 4**: Implement basic time-series analysis:  
  - Calculate moving averages to observe price trends over time.  
  - Visualize price changes and trends using simple plots with libraries like Matplotlib.  
- **Step 5**: Document findings and insights from the data analysis, focusing on observed trends and price fluctuations of Bitcoin over the collected dataset.

**Useful Resources**:

- TinyDB Documentation: [TinyDB Docs](https://tinydb.readthedocs.io)  
- CoinGecko API Documentation for Bitcoin data: [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- Python Plotting with Matplotlib: [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

**Is it free?**: Yes, this project is entirely free to develop and execute. TinyDB is open-source and does not require any subscription or payment. Access to public APIs for Bitcoin data is typically free but may have usage limits.

**Python Libraries / Bindings**:

- **TinyDB**: Lightweight, document-oriented database for storing Bitcoin price data.  
- **Requests**: To make HTTP requests to fetch data from the Bitcoin API. Install it using `pip install requests`.  
- **Matplotlib**: For plotting and visualizing data trends. Can be installed using `pip install matplotlib`.

This project serves as an introductory exercise in handling real-time data, building foundational skills in data ingestion, minor data persistence, and basic time-series analysis using Python.
