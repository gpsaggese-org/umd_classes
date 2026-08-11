### **Petl**

**Title**: Ingesting and Processing Bitcoin Prices using Petl  
**Difficulty**: 1 (easy)

**Description**  
Petl (Python ETL) is a lightweight Python library designed for extract, transform, and load (ETL) tasks. It provides simple tools for working with data tables, which are ideal for small-scale data tasks and educational environments. Petl focuses on ease of use and flexibility, making it perfect for handling data from various sources and performing fundamental operations such as filtering, transforming, and joining datasets.

This introductory project involves using Petl to ingest real-time Bitcoin price data from a public API, such as CoinGecko, and perform simple time series analysis. By utilizing basic Python packages alongside Petl, students will learn to manipulate data and extract meaningful insights with ease.

**Describe technology**

- **Petl**:  
  - Aimed at simple ETL tasks using data tables.  
  - Offers intuitive functions for loading data from various sources, including CSV, JSON, Excel, and more.  
  - Facilitates straightforward data transformations, such as filtering, sorting, and aggregating.  
- **Core functionalities include**:  
  - Loading data with `fromcsv()`, `fromjson()`, etc.  
  - Transforming data using functions like `select()`, `cut()`, `convert()`.  
  - Storing or outputting data back to files or other formats.

**Describe the project**

- Create a Python script that uses Petl to fetch real-time Bitcoin price data from a public API.  
- Load the API data into a Petl table.  
- Transform the data to focus on key metrics such as price, time, and market capitalization.  
- Implement time series analysis to calculate simple moving averages or other metrics over specified time windows.  
- Optionally, visualize the results using a basic Python plotting library, like Matplotlib, to provide insights into Bitcoin's price trends.

**Useful resources**

- [Petl Documentation](https://petl.readthedocs.io/en/stable/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Python Requests Library Documentation](https://docs.python-requests.org/en/master/)

**Is it free?**  
Yes, Petl is an open-source library available to use for free. Access to the CoinGecko API is also free with no authentication required for basic usage.

**Python libraries / bindings**

- **Petl**: Essential for ETL tasks, installed via `pip install petl`.  
- **Requests**: Used to make HTTP requests to the Bitcoin price API, installed via `pip install requests`.  
- **Matplotlib**: Optional, for plotting time series data, installed via `pip install matplotlib`.

This project will guide students through the fundamental concepts of ETL processes with a focus on Python's Petl library, preparing them for more complex data manipulation tasks.
