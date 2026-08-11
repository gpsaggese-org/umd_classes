### **Facebook prophet**

**Title**: Bitcoin Price Forecasting with Facebook Prophet

**Difficulty**: 3 (Difficult)

**Description**  
This project involves implementing a real-time Bitcoin price forecasting system using Facebook Prophet, a robust time-series forecasting library developed by Facebook's Core Data Science team. The aim is for students to ingest live Bitcoin price data from a public API, process it, and produce forecasts that can anticipate future price movements using machine learning models. This project requires knowledge in data science, Python programming, and time series analysis, providing students with hands-on experience in using sophisticated analytics tools to derive insights from financial data.

**Describe technology**

- **Facebook Prophet** is an open-source tool designed for time series forecasting. It is especially useful for data with daily observations that display patterns on different time scales. Prophet is known for its versatility and ease of use, making it possible for both experts and non-experts to work with time series data efficiently.  
- Core features include:  
  - **Automatic seasonality detection**: Handles yearly, weekly, and daily seasonality, including holiday effects.  
  - **Robust to missing data and shifts in the trend**: Useful for real-world data with irregularities.  
  - **Human-friendly**: Allows inclusion of holidays, custom seasonality terms, and offers extensive control over other model aspects.

**Describe the project**

- **Data Ingestion**:  
    
  - Use a public API, such as CoinDesk or CoinGecko, to continuously fetch real-time Bitcoin price data.  
  - Implement a data buffer to store the incoming data within a local or cloud-based database.


- **Data Processing**:  
    
  - Pre-process the ingested data to fill missing values, remove outliers, and format the data correctly for forecasting.  
  - Use basic Python libraries like pandas for data manipulation and cleaning.


- **Modeling**:  
    
  - Integrate Facebook Prophet to model the time-series data.  
  - Train the model using historical Bitcoin prices and include key features such as trend lines, daily/weekly/yearly seasonality.


- **Forecasting**:  
    
  - Generate future price forecasts and visualize these predictions alongside historical data using charting libraries like matplotlib or plotly.  
  - Implement a reporting module to create alerts or notifications based on significant forecast changes.


- **Evaluation**:  
    
  - Evaluate the performance of your forecasts by comparing them to actual price movements using metrics such as RMSE or MAE.

**Useful resources**

- [Facebook Prophet Documentation](https://facebook.github.io/prophet/)  
- [Kaggle Datasets for Historical Bitcoin Prices](https://www.kaggle.com/datasets)  
- [CoinDesk Developer API](https://www.coindesk.com/coindesk-api)  
- [Plotly Website](https://plotly.com/python/)

**Is it free?**  
Yes, Facebook Prophet is open source and can be used for free. The public APIs like CoinDesk or CoinGecko typically have a free tier for basic usage but may require registration to obtain an API key.

**Python libraries / bindings**

- **prophet**: Installable via `pip install prophet`, requires additional dependencies like pystan for fitting Bayesian models.  
- **pandas**: For data manipulation and cleaning tasks.  
- **matplotlib and plotly**: For data visualization and plotting results/forecasts.  
- **requests**: To handle API requests for real-time data ingestion.
