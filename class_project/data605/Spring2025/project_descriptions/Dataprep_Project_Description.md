### **Dataprep**

**Title**: Real-time Bitcoin Data Processing using Dataprep

**Difficulty**: Difficult

**Description**:  
This project involves implementing a system for ingesting and processing real-time Bitcoin data using Dataprep. Dataprep is a Python library designed to simplify data collection, exploration, cleaning, and visualization. It streamlines data preparation tasks, traditionally elaborate and error-prone, into straightforward processes. The main focus of this project is to demonstrate Dataprep's capabilities in handling time series analysis of Bitcoin prices in a big data context.

**Describe technology**:

- **Dataprep**: A Python library that offers modules to easily collect, explore, clean, and visualize data. Dataprep simplifies common data preparation tasks through:  
    
  - `Dataprep.eda`: A module for exploratory data analysis (EDA), enabling the quick generation of statistics, visualizations, and reports.  
  - `Dataprep.connector`: Facilitates connection to a wide variety of data sources, supporting seamless data ingestion.  
  - `Dataprep.clean`: Provides tools for cleaning and preparing data with flexible and intuitive methods.  
  - `Dataprep.feature`: (optional, based on needs) Assists in feature engineering tasks.


  Dataprep is designed to be intuitive and to integrate smoothly with commonly used data manipulation libraries like pandas.

**Describe the project**:

- **Objective**: Build a system that ingests real-time Bitcoin price data from a public API and performs time series analysis using Dataprep.  
- **Steps involved**:  
  1. **Data Ingestion**: Use the `Dataprep.connector` module to fetch real-time Bitcoin price data from a chosen public API, such as CoinGecko.  
  2. **Data Cleaning**: With the `Dataprep.clean` module, process the ingested data to handle missing values, normalize data fields, and remove inconsistencies.  
  3. **Data Exploration**: Utilize `Dataprep.eda` for exploratory data analysis to understand trends and patterns in Bitcoin price movements.  
  4. **Time Series Analysis**: Implement a time series analysis method (e.g., ARIMA) to forecast Bitcoin prices. This step involves preparing the datasets for analysis, selecting a model, and evaluating its performance.  
  5. **Visualization**: Generate insightful visualizations of historical Bitcoin prices, forecast results, and potential future trends using the visualization capabilities of `Dataprep.eda`.

**Useful resources**:

- [Dataprep Official Documentation](https://docs.dataprep.ai/index.html)  
- [Dataprep GitHub Repository](https://github.com/sfu-db/dataprep)  
- [Time Series Forecasting Methods](https://otexts.com/fpp3/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)

**Is it free?**:  
Yes, Dataprep is an open-source library that is free to use. However, using certain data source APIs, such as CoinGecko, may have rate limits or usage tier plans if heavy data usage is required.

**Python libraries / bindings**:

- `dataprep`: The primary library for data preparation tasks. Installable using `pip install -U dataprep`.  
- `pandas`: For general data manipulation and cleaning tasks. Installable with `pip install pandas`.  
- `requests`: To facilitate API calls for fetching Bitcoin data. Installable using `pip install requests`.  
- `statsmodels`: A library for performing time series analysis, such as ARIMA. Install with `pip install statsmodels`.  
- `matplotlib`/`seaborn`: For plotting and visualization of results. Install using `pip install matplotlib seaborn`.
