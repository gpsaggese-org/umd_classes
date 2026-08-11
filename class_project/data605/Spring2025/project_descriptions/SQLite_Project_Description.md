###   **SQLite**

**Title**: Time Series Analysis of Bitcoin Prices using SQLite

**Difficulty**: 2 (medium)

**Description**  
SQLite is a software library that provides a relational database management system. It is self-contained, serverless, and requires a minimal setup, making it ideal for embedding into other applications. It supports SQL queries, which makes it suitable for handling structured data efficiently. SQLite is used globally in both simple applications and complex systems due to its simplicity and flexibility.

**Describe technology**

- **Lightweight and Efficient**: SQLite is a compact database solution integrated into the application software, eliminating the need for a separate server process.  
- **SQL Support**: It fully supports SQL standards, enabling complex queries and data manipulation.  
- **Zero Configuration**: SQLite does not require any installation or configuration, facilitating a hassle-free setup.  
- **ACID Compliance**: Transactions in SQLite are compliant with the ACID properties, ensuring reliable and safe data manipulation even during system failures.  
- **Platform Independent**: Available across multiple operating systems without the need for extensive configuration, making it versatile for various development environments.

**Describe the project**  
In this project, students are required to build a real-time data ingestion and processing system using SQLite to analyze Bitcoin price fluctuations. The focus will be on implementing this system in Python:

1. **Data Ingestion**:  
     
   - Fetch real-time Bitcoin price data from a public API such as CoinGecko or CoinMarketCap.  
   - Store the incoming data into an SQLite database, emphasizing the use of SQL to create and manage the database schema.

   

2. **Data Processing and Analysis**:  
     
   - Query the SQLite database to extract relevant Bitcoin pricing information.  
   - Perform time series analysis, which may include calculating moving averages, rate of change, or volatility metrics.  
   - Utilize Python libraries such as Pandas to support data manipulation and Matplotlib for data visualization of price trends.

**Useful resources**

- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [SQLite Official Documentation](https://sqlite.org/docs.html)  
- [SQLite Python Tutorial](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)  
- [Pandas Time Series Tutorial](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)  
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)

**Is it free?**  
Yes, SQLite is open-source and freely available for both personal and commercial use.

**Python libraries / bindings**

- **sqlite3**: Built-in Python library that provides an interface for interacting with SQLite databases.  
- **pandas**: Library used for data manipulation and analysis; helps with loading data from SQLite and performing time series analysis.  
- **requests**: Library to handle API requests for fetching real-time Bitcoin pricing data.  
- **matplotlib**: Plotting library used to visualize the time series data and analysis results.
