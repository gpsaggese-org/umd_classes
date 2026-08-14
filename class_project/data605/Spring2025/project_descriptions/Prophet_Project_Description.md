### **Prophet**

**Title:** Time Series Forecasting of Bitcoin Prices using Prophet

**Difficulty:** Medium (2)

**Description**  
Prophet is an open-source forecasting tool developed by Facebook (now Meta) designed to handle large-scale time series data with ease. It provides straightforward APIs for accurate and fast time series forecasting, particularly when dealing with data exhibiting weekly and yearly seasonality, holidays, or missing data. The core strength of Prophet is its ability to fit complex nonlinear trends with daily seasonality over various periods.

In this project, students will explore Prophet's main functionalities and their application to real-time Bitcoin price data. The use of basic Python packages alongside Prophet will be a requirement, enabling students to solidify their understanding of time series forecasting, data ingestion, and initial data processing for trend analysis.

**Describe technology**

- **Prophet**: Developed by Facebook (Meta), Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects if needed.  
- **Key features**: It is particularly robust to missing data and shifts in the trend, and typically handles outliers well. Its straightforward procedure allows for quick iterations, which is vital for students learning dynamic forecasting methods.  
- **Example functionalities**:  
  - Import and structure data for time series analysis.  
  - Fit a model using historical data and make forecasts.  
  - Plot the results, including components such as trend, weekly, and yearly seasonality.

**Describe the project**

- **Objective**: Implement a real-time data processing pipeline using Prophet to forecast Bitcoin prices.  
- **Steps**:  
  1. **Data Collection**: Use a public API (e.g., CoinGecko or Binance) to ingest real-time Bitcoin price data into a local environment. This involves setting up a script to periodically fetch data and store it in a CSV format.  
  2. **Data Preprocessing**: Use basic Python libraries (Pandas) to clean and preprocess the data. Ensure the data is formatted correctly for time series analysis with Prophet. Handle missing timestamps, any anomalies, or outliers effectively to maintain the quality of input data.  
  3. **Apply Prophet**:  
     - Load the preprocessed data into the Prophet model.  
     - Fit the model to the historical data to understand the underlying patterns and trends.  
     - Forecast future Bitcoin prices for a specified period.  
  4. **Visualization and Analysis**:  
     - Plot the forecasts and evaluate the model's performance.  
     - Analyze the impact of seasonal components and provide insights derived from the forecast results.

**Useful resources**

- [Prophet Official Documentation](https://facebook.github.io/prophet/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)

**Is it free?**  
Yes, Prophet is open-source and free to use. However, API access might be subject to limits or require subscriptions for higher usage levels. It's essential to verify the terms of use for the API chosen for data collection.

**Python libraries / bindings**

- **Prophet**: Install via pip using `pip install prophet`. This library will be used for building and evaluating the forecasting model.  
- **Pandas**: For data manipulation and preprocessing. Install via pip using `pip install pandas`.  
- **Requests**: For fetching data from public APIs. Install via pip using `pip install requests`.  
- **Matplotlib/Seaborn**: For plotting and visualizing the forecasted results. Install via pip using `pip install matplotlib seaborn`.

By the end of this project, students will gain valuable experience in handling time series data with real-world applications, enriching their understanding of data science models specifically geared for forecasting.
