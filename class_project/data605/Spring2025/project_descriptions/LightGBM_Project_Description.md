### **LightGBM**

**Title**: Real-Time Bitcoin Price Analysis using LightGBM

**Difficulty**: 2 (medium)

**Description**  
LightGBM is a highly efficient and scalable gradient boosting framework developed by Microsoft, optimized for speed and accuracy. It is especially effective for training models on large datasets because it uses a histogram-based approach that reduces memory usage and improves training speed. LightGBM's key features include support for categorical features natively, improved accuracy, and faster training. In this project, students will leverage LightGBM to create a real-time prediction system for Bitcoin prices. Using basic Python packages, students will construct a pipeline for ingesting live Bitcoin price data, perform necessary processing, and implement a time-series prediction model to forecast future price movements.

**Describe Technology**

- LightGBM is a gradient boosting framework that uses tree-based learning algorithms.  
- It is designed for distributed systems and excels in handling large datasets.  
- Supports efficient parallel and GPU learning, which accelerates the training process.  
- Natively supports categorical features, which can lead to better model performance without preprocessing.  
- LightGBM is known for its accuracy while maintaining computational efficiency.

**Describe the Project**

- **Data Ingestion**: Set up an environment to ingest real-time Bitcoin price data from a public API such as CoinGecko. Use Python libraries like requests or websocket-client to continuously fetch data every few minutes.  
- **Data Processing**: Preprocess the fetched Bitcoin data to extract relevant features for time-series analysis. This may include engineering time-based features (e.g., rolling averages, time lags).  
- **Model Implementation**: Implement a LightGBM model to perform time-series forecasting. The goal is to predict the next-minute Bitcoin price based on historical data.  
- **Model Evaluation**: Split data into training and test sets. Use evaluation metrics suitable for time-series data, such as Root Mean Square Error (RMSE) or Mean Absolute Error (MAE), to evaluate the model's performance.  
- **Real-Time Prediction**: Integrate the trained model into the data ingestion pipeline to make real-time price predictions and log the results for further analysis.  
- **Visualization**: Utilize a Python data visualization library like matplotlib or seaborn to plot actual vs. predicted Bitcoin prices over time to visually assess the model performance.

**Useful Resources**

- [LightGBM Documentation](https://lightgbm.readthedocs.io/)  
- [Python requests library documentation](https://pypi.org/project/requests/)  
- [WebSocket client for Python](https://pypi.org/project/websocket-client/)  
- [CoinGecko API](https://www.coingecko.com/en/api)  
- [Matplotlib documentation](https://matplotlib.org/stable/contents.html)

**Is it free?**  
Yes, LightGBM and the other Python libraries used (requests, websocket-client, matplotlib) are   
open-source and free to use.

**Python Libraries / Bindings**

- **LightGBM**: The primary library for implementing the gradient boosting model. Install via `pip install lightgbm`.  
- **Requests**: Used for making HTTP requests to retrieve Bitcoin price data from an API. Install via `pip install requests`.  
- **Websocket-client**: For establishing real-time connections to fetch Bitcoin data without polling. Install via `pip install websocket-client`.  
- **Matplotlib/Seaborn**: For visualizing actual vs. predicted Bitcoin prices. Install via `pip install matplotlib seaborn`.
