### **Pytest-mock**

**Title**: Analyzing Bitcoin Prices with Pytest-mock

**Difficulty**: 1 (easy)

**Description**  
This project focuses on using the `pytest-mock` library to facilitate testing in Python applications. `pytest-mock` enables developers to replace parts of their system under test and make assertions on how they are used. This is particularly useful for testing components that interact with external systems, such as APIs or databases.

In this project, students will build an application that ingests real-time Bitcoin price data from a public API and performs basic time series analysis. The goal is to create a test-driven development (TDD) process using `pytest-mock`, allowing students to simulate different scenarios and validate their data processing logic effectively.

**Describe technology**

- `pytest-mock` is a plugin for the pytest framework that provides powerful mocking capabilities, making it easier to write unit tests for Python applications.  
- Students will learn how to use `pytest-mock` to create mock objects which can simulate the behavior of complex systems or external dependencies.  
- The library allows tests to assert whether particular actions were performed on a mocked object, making it ideal for scenarios where real-time data changes are simulated.

**Describe the project**

- **Data Ingestion**: Set up a basic Python script to fetch real-time Bitcoin price data from a public API, such as CoinGecko or CryptoCompare.  
- **Simulate Real-time Processing**: Using simple Python scripts, simulate the ingestion of data at regular intervals.  
- **Time Series Analysis**: Implement basic operations on the ingested data such as calculating moving averages or detecting trends.  
- **Testing Using Pytest-mock**: Develop a suite of unit tests using pytest and `pytest-mock` to:  
  - Mock API responses to test how the system behaves with varying Bitcoin prices.  
  - Simulate network failures or API downtimes and verify system resilience.  
  - Ensure that time series analysis logic performs correctly by mocking various input datasets.

**Useful resources**

- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/en/latest/)  
- [pytest Official Documentation](https://docs.pytest.org/en/stable/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, both `pytest-mock` and pytest are open-source and free to use. The public APIs for Bitcoin price data typically offer free tiers, but they may have limitations on the number of requests.

**Python libraries / bindings**

- `pytest-mock`: Install via pip using `pip install pytest-mock`. It extends pytest with powerful mocking features.  
- `requests`: Used for making HTTP requests to the Bitcoin price API. Install using `pip install requests`.  
- Optionally, `pandas`: For handling time series data. Install using `pip install pandas`. This library is useful for more advanced data manipulation and analysis, aiding the processing of Bitcoin price data.
