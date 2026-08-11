### **PyOD**

**Title**: Real-Time Bitcoin Anomaly Detection with PyOD

**Difficulty**: 2 (medium)

**Description**  
PyOD (Python Outlier Detection) is an open-source Python library that leverages a wide range of anomaly detection algorithms to identify outliers in a given dataset. In the context of data science and machine learning, anomaly detection is crucial for identifying unexpected behaviors in data—such as fraudulent activities, spikes, or anomalies in time series datasets. PyOD is particularly valuable because it supports various detection models, from classical algorithms like Isolation Forest to neural network architectures such as AutoEncoders, allowing flexible applications across different domains and datasets.

**Describe technology**

- **PyOD** is a comprehensive library for detecting outliers in multivariate data.  
- It supports more than 20 detection algorithms, facilitating extensive experimentation.  
- Allows integration with scikit-learn's pipeline and model selection tools for enhanced machine learning workflows.  
- Comes with utility functions for model evaluation, visualization, and comparison.  
- Can handle both individual data points and entire system behaviors as anomalies.

**Describe the project**  
This project involves developing a real-time bitcoin price anomaly detection system using PyOD. By integrating a publicly available Bitcoin price API, students will ingest and process real-time Bitcoin prices to identify unusual price movements (anomalies) over time. The project components are:

- **Data Ingestion**:  
  Use a simple Python script to consume live Bitcoin price data from a source like CoinGecko or Blockchain.info API.  
- **Data Storage**:  
  Temporarily store the incoming data using a lightweight in-memory database or directly aggregate it for processing.  
- **Anomaly Detection**:  
  Employ PyOD to analyze the Bitcoin price stream for anomalies. Start by applying simple algorithms, such as Z-Score or Isolation Forest, to detect price spikes or drops. Assess the effectiveness by comparing multiple PyOD models.  
- **Time Series Analysis**:  
  Extend the basic model to include time series analysis, identifying patterns over hourly or daily intervals and establishing thresholds for what constitutes "anomalous" behavior in the Bitcoin price dataset.  
- **Real-Time Alerts**:  
  Implement a basic notification system to alert users when significant anomalies are detected. This could be a command-line printout or an email notification for significant events.

**Useful resources**

- [PyOD Official Documentation](https://pyod.readthedocs.io/en/latest/)  
- [Time Series Anomaly Detection Toolkits from PyOD](https://github.com/yzhao062/pyod)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, PyOD is free and open-source. Bitcoin price APIs often have free tiers for basic usage.

**Python libraries / bindings**

- **PyOD**: For anomaly detection processes.  
- **Requests**: To make HTTP requests to the Bitcoin price API.  
- **Pandas**: For data manipulation and time series analysis.  
- **NumPy**: For numerical operations and data preparation.  
- **Scikit-learn**: For data preparation and integrating PyOD models into a machine-learning pipeline.
