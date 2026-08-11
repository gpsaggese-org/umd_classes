### **MLflow Computational framework**

**Title**: Real-time Bitcoin Data Processing with MLflow  
**Difficulty**: 1 (easy)

**Description**  
This project is designed to give you a hands-on introduction to MLflow, an open-source platform to manage the machine learning lifecycle, which includes experimentation, reproducibility, and deployment. By the end of this project, you will have set up a simple real-time data processing pipeline for Bitcoin prices and explored basic MLflow functionalities to document and manage your work effectively.

**Describe technology**

- **MLflow** is a tool that helps manage the machine learning lifecycle, encompassing four key functions:  
  - **Tracking experiments** to record and compare parameters and results (MLflow Tracking).  
  - **Packaging code** into reproducible runs using Conda and Docker (MLflow Projects).  
  - **Managing and deploying models** from various ML libraries (MLflow Models).  
  - **Creating REST APIs** for the deployed models for easy access (Model Registry).

**Describe the project**

- **Objective**: Implement a real-time data ingestion pipeline for Bitcoin prices and apply basic time series analysis in Python, using MLflow to track the experiment and results.  
- **Steps**:  
  1. **Data Collection**: Use a public API like CoinGecko to ingest real-time Bitcoin data every few minutes.  
  2. **Data Processing**: Write a basic Python script to clean and prepare the collected data for analysis.  
  3. **Time Series Analysis**: Implement a simple moving average algorithm to analyze Bitcoin price trends.  
  4. **MLflow Integration**: Use MLflow to:  
     - Track the parameters and metrics of your analysis, such as time interval and average price.  
     - Log the versions of the software packages used in your project.  
     - Document and save the results for future reference or comparison.  
  5. **Visualization**: Optional step to visualize the time series analysis using a library like Matplotlib.

**Useful resources**

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Python's Requests Library Documentation](https://docs.python-requests.org/en/latest/)

**Is it free?**  
Yes, MLflow is open-source and can be used for free. CoinGecko provides free access to its API with rate limits.

**Python libraries / bindings**

- **MLflow**: Install MLflow using `pip install mlflow`.  
- **Requests**: For API calls, use Python's requests library, installable via `pip install requests`.  
- **Pandas**: For data manipulation, use Pandas via `pip install pandas`.  
- **Matplotlib**: For optional data visualization, install via `pip install matplotlib`.
