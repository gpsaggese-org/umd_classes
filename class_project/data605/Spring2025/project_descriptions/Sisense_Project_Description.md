### **Sisense**

**Title**: Real-Time Bitcoin Analytics with Sisense

**Difficulty**: 3 (difficult)

**Description**  
This project involves setting up a real-time data ingestion and analytics system for Bitcoin using Sisense, an advanced analytics platform. Students will focus on implementing an architecture that consumes live Bitcoin data from public APIs and transforms it into actionable insights using Sisense's robust data visualization and analytics features. The project requires integrating Sisense with Python for data manipulation and conducting a time series analysis to predict Bitcoin price trends.

**Describe technology**  
Sisense is a powerful business intelligence (BI) tool designed to handle and analyze large datasets with ease. It provides end-to-end solutions for data preparation, analysis, and visualization. Key features include:

- Seamless integration with various data sources, including APIs for real-time data streaming.  
- Robust data preparation tools to clean and transform raw data.  
- Advanced analytics capabilities to handle complex data relationships and calculations.  
- Customizable dashboards and visualizations for data storytelling and insight sharing.  
- Extensible through REST APIs and SDKs for further customization and integration with other tools.

**Describe the project**  
The project is divided into several critical phases:

1. **Data Ingestion**:  
     
   - Set up a connection to a real-time Bitcoin price API, such as CoinGecko, using a Python script.  
   - Capture this data constantly and prepare it to be fed into Sisense.

   

2. **Data Integration and Preparation**:  
     
   - Use Sisense's data preparation tools to clean and structure the raw Bitcoin data.  
   - Create relationships between datasets to enrich the data for more comprehensive analysis.

   

3. **Time Series Analysis**:  
     
   - Perform a time series analysis on the historical Bitcoin price data using Python’s `pandas` and `statsmodels` libraries.  
   - Build predictive models to forecast future Bitcoin prices.

   

4. **Visualization and Insights**:  
     
   - Design dashboards in Sisense to visualize current Bitcoin prices, historical trends, and future predictions.  
   - Implement features for users to interactively explore data, such as filtering by date ranges and comparing forecasted prices to historical data.

This project provides experience in integrating Sisense with real-time data systems, performing time series analysis, and creating insightful BI dashboards.

**Useful resources**

- [Sisense Documentation](https://docs.sisense.com/main/Home.htm)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [Statsmodels Documentation](https://www.statsmodels.org/stable/index.html)

**Is it free?**  
Sisense offers a free trial, but typically requires a paid subscription for ongoing use. Check with Sisense for academic pricing or special educational access programs.

**Python libraries / bindings**

- **Requests**: To interact with and fetch data from Bitcoin APIs. Install it using `pip install requests`.  
- **Pandas**: For data manipulation and preparation tasks. Install it using `pip install pandas`.  
- **Statsmodels**: For performing advanced statistical analyses, including time series forecasting. Install it using `pip install statsmodels`.  
- **Sisense REST API**: To automate processes or extend functionality within Sisense using Python.
