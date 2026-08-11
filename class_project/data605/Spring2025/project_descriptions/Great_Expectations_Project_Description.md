### **Great Expectations**

Title: Monitoring Bitcoin Prices Using Great Expectations

Difficulty: Medium (2=medium difficulty)

**Description**

Great Expectations is an open-source data validation and documentation framework that helps ensure data quality through automated testing and data profiling. With Great Expectations, data teams can create expectations for their data, validate it against these expectations, and generate detailed data documentation. This framework seamlessly integrates into Python data workflows and can be used to ensure the integrity of both batch and real-time data. This project will involve using Great Expectations to validate and monitor real-time Bitcoin price data from a public API.

**Describe technology**

- **Core Concepts**: Understand how Great Expectations empowers users to define, validate, and document data expectations directly in Python scripts. It provides a framework for writing portable, reusable, and shared data validation tests that help maintain data quality.  
- **Key Features**:  
  - **Expectations**: Specify what the data should look like or behave, such as acceptable ranges or expected distributions.  
  - **Validation**: Automatically test data against the expectations.  
  - **Data Documentation**: Generate human-readable documents detailing expectations of datasets and their validation status.  
- **Integration**: Great Expectations can be integrated with various Python data tools and backend storage options to support comprehensive data validation workflows.

**Describe the project**

In this project, students will leverage Great Expectations to implement a real-time monitoring system for Bitcoin price data:

1. **Data Ingestion**: Use Python to set up ingestion of real-time Bitcoin data from a public API like CoinGecko.  
2. **Expectation Suite**: Develop a suite of data expectations targeting key aspects such as:  
   - Expected price range to flag prices that exceed predefined thresholds.  
   - Time intervals to ensure the data is regularly updated and retrieved.  
3. **Validation Workflow**: Implement a validation pipeline to continuously check ingested data against the expectation suite.  
4. **Documentation and Alerts**: Use Great Expectations to create comprehensive data documentation and set up alerts for expectation failures, providing early warnings for potential data issues.  
5. **Time Series Analysis**: Integrate time series analysis to predict Bitcoin price trends or sudden volatility changes, using data validated by Great Expectations as reliable inputs for analysis.

**Useful Resources**

- [Great Expectations Documentation](https://docs.greatexpectations.io/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- Online tutorials and guides for setting up Great Expectations with real-time data.

**Is it free?**

Yes, Great Expectations is open-source and free to use. However, data source APIs like CoinGecko may have usage limits or require an API key.

**Python libraries / bindings**

To implement this project, the following Python libraries are essential:

- **Great Expectations**: Install via `pip install great_expectations`. This library will be used to create, validate, and document data expectations.  
- **Requests or httpx**: Libraries for making HTTP requests to the Bitcoin price API. Install via `pip install requests` or `pip install httpx`.  
- **Pandas**: For handling and processing data frames, if necessary in the workflow. Install via `pip install pandas`.  
- **Matplotlib or Seaborn**: Optional libraries for visualizing data trends or time series analysis. Install via `pip install matplotlib seaborn`.

This project gives students practical experience with data validation and monitoring, using Python and Great Expectations to ensure real-time data integrity while working with time-series data analysis.
