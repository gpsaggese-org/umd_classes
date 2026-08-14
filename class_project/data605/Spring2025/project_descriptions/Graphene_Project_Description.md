### **Graphene**

**Title**: Analyzing Bitcoin Trends with Graphene

**Difficulty**: 1 (Easy)

**Description**  
This project involves using Graphene, a lightweight and powerful Python framework, to handle and analyze real-time Bitcoin price data. Students will learn about fundamental aspects of Graphene and apply this knowledge to ingest, process, and analyze time-series data related to Bitcoin prices. The project offers a basic introduction to Graphene and data handling in Python, suitable for those new to big data systems and time series analysis.

**Describe Technology**

- **Graphene**:  
  - Graphene is a popular framework for building GraphQL APIs in Python. It's known for its simplicity and ease of use, facilitating the creation of robust data models and query handling.  
  - Core Concepts:  
    - **Schema**: Defines the data model and operations in GraphQL.  
    - **Resolvers**: Functions that fulfill the data fetching requirements.  
    - **Queries and Mutations**: Used for data retrieval and modification, respectively.  
  - Graphene supports Python's native async features for real-time data handling.

**Describe the Project**

- Objective: Use Graphene to implement a mini-server that listens to real-time Bitcoin price updates via a public API, processes this data, and makes it available for analysis through a GraphQL interface.  
- Steps:  
  - Set up a basic Python environment with Graphene.  
  - Implement a data ingestion script to fetch real-time Bitcoin price data from a public API like CoinGecko.  
  - Define a GraphQL schema using Graphene, including types for Bitcoin data such as price, timestamp, and volume.  
  - Create resolvers that handle incoming Bitcoin price data and store it in a Python data structure (like a list or a simple database).  
  - Implement queries that allow users to perform basic time-series analysis on this data, such as retrieving price changes over a specific period or calculating average price.  
  - Test your GraphQL server locally, ensuring it appropriately responds to queries and updates in real-time data.  
- The project culminates in a demonstration of querying real-time Bitcoin price trends via GraphQL.

**Useful Resources**

- [Graphene Documentation](https://docs.graphene-python.org/en/latest/)  
- [Introduction to GraphQL](https://graphql.org/learn/)  
- [Python Requests Library](https://docs.python-requests.org/en/master/)

**Is it free?**  
Yes, Graphene is open-source and freely available. No additional software costs are associated with this project.

**Python Libraries / Bindings**

- **Graphene**: The main library to implement GraphQL APIs. Install with `pip install graphene`.  
- **Requests**: For making HTTP requests to fetch data from external APIs. Install with `pip install requests`.  
- **Asyncio**: A standard Python library for asynchronous programming, used for handling real-time data updates.

This project offers hands-on experience with Graphene and helps students develop skills in building GraphQL APIs and time-series analysis using real-world data.
