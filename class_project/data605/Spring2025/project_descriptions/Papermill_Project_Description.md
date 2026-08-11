### **Papermill**

**Title**: Stream Processing of Bitcoin Data with Papermill

**Difficulty**: 2 (medium)

**Description**:  
Papermill is an open-source tool that allows users to parameterize and execute Jupyter Notebooks. It is designed for data science workflows, enabling automated execution of notebook tasks in a flexible and scalable manner. This project aims to teach students how to use Papermill for ingesting and processing real-time Bitcoin price data, focusing on the time series analysis of price changes. Students will configure notebooks to fetch and store Bitcoin data from a public API, then use Papermill to automate the running of this workflow in regular intervals, effectively creating a real-time data processing pipeline.

**Describe technology**:

- Papermill: A tool for parameterizing and executing Jupyter Notebooks. It's often used to run batch jobs in data science projects or set up repeatable and scheduled workflows for analytics tasks.  
- Key functionalities of Papermill:  
  - Parameterization: Allows you to define parameters within your notebooks, enabling the reuse of notebook templates with varying inputs.  
  - Execution: Automates the execution of notebooks, making it possible to schedule and repeatedly run them with different parameters.  
  - Input/Output: Supports managing the input and output notebook files, making it efficient to capture and store results from execution.

**Describe the project**:

- Step 1: Configure a Jupyter Notebook to fetch Bitcoin price data from a public API, such as CoinGecko, using Python libraries like `requests` or `http.client`.  
- Step 2: Implement basic data processing in the notebook, such as cleaning the data and performing initial exploratory data analysis (EDA).  
- Step 3: Introduce time series analysis within the notebook to analyze price trend patterns, like moving averages and volatility.  
- Step 4: Use Papermill to parameterize the notebook, setting parameters to adjust API request intervals and analysis time windows.  
- Step 5: Create a script using Papermill that schedules the periodic execution of the notebook with defined parameters, thereby building a near real-time updating data analysis dashboard.  
- Step 6: Explore logging and result storage features of Papermill to facilitate data persistence and track execution results.

**Useful resources**:

- [Papermill Documentation](https://papermill.readthedocs.io/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Jupyter Notebooks Introduction](https://jupyter.org/documentation)  
- [Time Series Analysis in Python](https://www.analyticsvidhya.com/blog/2018/02/time-series-forecasting-methods/)

**Is it free?**  
Yes, Papermill is an open-source tool and can be used freely. However, students need access to a Python environment, and possibly Jupyter Notebooks, which are also freely available.

**Python libraries / bindings**:

- `papermill`: The primary library for executing parameterized Jupyter Notebooks. Install via `pip install papermill`.  
- `requests`: A simple HTTP library for fetching data from web APIs. Install via `pip install requests`.  
- `pandas`: Used for data manipulation and analysis within your notebooks. Install via `pip install pandas`.  
- `matplotlib` and/or `seaborn`: Libraries for data visualization to graphically represent the results of your analysis. Install via `pip install matplotlib seaborn`.
