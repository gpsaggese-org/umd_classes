### **PyCaret**

**Title**: Real-Time Bitcoin Data Analysis with PyCaret

**Difficulty**: Medium (2=medium difficulty)

**Description**  
This project focuses on using PyCaret, an open-source, low-code machine learning library in Python, to perform real-time data ingestion and time series analysis of Bitcoin price data. The goal is to gain hands-on experience with PyCaret's capabilities in building and deploying machine learning models efficiently, emphasizing its application in time series forecasting.

**Describe technology**

- **PyCaret**: PyCaret simplifies machine learning tasks, including data preparation, model training, and deployment. It supports a wide range of models through a unified API and is especially valuable for quickly prototyping and testing different algorithms.  
- PyCaret provides modules tailored for various machine learning types, including classification, regression, clustering, anomaly detection, natural language processing, and time series analysis.

**Describe the project**

- **Data Ingestion**: Utilize Python packages such as `requests` to connect to a public Bitcoin price API (e.g., CoinGecko, CoinMarketCap) to fetch real-time Bitcoin data. Use `pandas` to organize the fetched data.  
- **Data Processing**: Cleanse and preprocess the acquired data using `pandas` to prepare it for analysis. This involves handling missing values, formatting timestamps, and normalizing data.  
- **Time Series Analysis with PyCaret**:  
  - Leverage PyCaret's time series module to explore different forecasting techniques.  
  - Focus on developing a model that predicts future Bitcoin prices based on real-time data.  
  - Measure the performance of various models and select the optimal one based on evaluation metrics.  
- **Deployment and Visualization**: Implement a visualization step using libraries such as `matplotlib` or `plotly` to visualize historical and predicted data. Optionally, prepare a simple dashboard showing the real-time updates of the Bitcoin price and model predictions.  
- **Results Analysis**: Document the findings, challenges faced, and insights gained from the time series analysis process.

**Useful resources**

- [PyCaret Official Documentation](https://pycaret.gitbook.io/docs)  
- [PyCaret Time Series Module](https://pycaret.gitbook.io/docs/get-started/modules)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, PyCaret is open-source and free to use. Access to some Bitcoin APIs may have free usage tiers or require registration.

**Python libraries / bindings**

- **PyCaret**: The primary library for implementing machine learning workflows, specifically time series analysis for this project.  
- **pandas**: For data manipulation and handling.  
- **requests**: To establish connections with Bitcoin APIs and ingest data.  
- **matplotlib/plotly**: For creating visualizations that represent model predictions and real-time data trends.
