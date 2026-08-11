### **Pygrametl**

**Title**: Building a Bitcoin Real-time ETL Pipeline with Pygrametl  
**Difficulty**: 1 (easy)

**Description**  
In this project, students will learn how to use Pygrametl, a lightweight library designed for ETL purposes in Python, to ingest and process real-time Bitcoin price data. Pygrametl is particularly suitable for this project due to its ability to seamlessly integrate with a variety of data sources and destinations, making it a great tool for handling ETL tasks with Python. The objective of this project is to use Pygrametl to extract Bitcoin price data from a public API, transform the data into a desired format for time series analysis, and load it into a local database for storage and further exploration.

**Describe technology**

- **Pygrametl** is a Python library specifically tailored for ETL processes. It simplifies the task of integrating data from various sources while providing basic functionalities to perform data cleaning, transformation, and loading operations.  
- Originally intended for smaller-scale ETL tasks, its flexibility and ease of use make it a suitable choice for educational purposes and for projects that do not require heavy-duty data processing tools.  
- Pygrametl supports various databases and can be easily configured to interact with different types of data, without requiring extensive knowledge in complex ETL frameworks.

**Describe the project**

- **Objective**: Create a simple Pygrametl-based pipeline to ingest, transform, and load Bitcoin price data for time series analysis.  
- **Steps**:  
  1. **Data Ingestion**: Use a public API like CoinGecko to fetch real-time Bitcoin price data.  
  2. **Data Transformation**: Clean the data to remove any unnecessary fields and perform operations such as converting timestamps to a desired format.  
  3. **Data Loading**: Store the processed data into a local SQLite database to maintain historical records for time series analysis.  
  4. **Time Series Analysis**: Perform basic analysis on the stored data, such as plotting price trends over time or calculating moving averages.  
- **Expected Outcome**: Students will successfully learn to set up a simple ETL pipeline using Pygrametl, gain hands-on experience with real-time data processing, and apply basic time series analysis techniques.

**Useful resources**

- [Pygrametl Documentation](http://pygrametl.org/index.html)  
- [SQLite Documentation](https://www.sqlite.org/docs.html)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Python datetime module](https://docs.python.org/3/library/datetime.html) 

**Is it free?**  
Yes, Pygrametl is an open-source library and can be freely used for educational and personal projects. All tools needed for this project, including SQLite and Python, are also free.

**Python libraries / bindings**

- **Pygrametl**: The primary library used for building the ETL pipeline. Install using `pip install pygrametl`.  
- **Requests**: A library for making HTTP requests, used to fetch data from the API. Install using `pip install requests`.  
- **SQLite**: No installation is needed as it is included in the Python standard library.  
- **Matplotlib**: For plotting and visualizing time series data. Install using `pip install matplotlib`.  
- **Pandas** (optional): Can be used for additional data manipulation and transformation tasks. Install using `pip install pandas`.

Through this project, students will develop a foundational understanding of ETL processes using Pygrametl and gain practical experience with real-time data ingestion and time series analysis.
