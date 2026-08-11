### [**Bonobo**](?tab=t.0#bookmark=id.lwsyvf35wbjj)

**Title**: Real-time Bitcoin Data Processing Using Bonobo

**Difficulty**: 2 (Medium)

**Description**:  
Bonobo is a lightweight, easy-to-use ETL (Extract, Transform, Load) framework for Python, enabling you to create simple but effective data pipelines. Designed with simplicity and extensibility in mind, Bonobo offers a versatile toolkit for anyone looking to process and analyze data. In this project, students will gain hands-on experience by implementing a real-time data processing system to ingest Bitcoin price data from a live API and perform time series analysis on this data.

**Describe Technology**:

- Bonobo is a data ETL framework in Python that emphasizes ease of use and flexibility.  
- It allows you to define your ETL processes using simple, reusable Python functions.  
- Bonobo introduces the concept of graphs to configure and execute data workflows.  
- The framework supports a variety of data sources, including APIs, databases, and files.  
- Bonobo pipelines are executed in parallel, allowing for efficient real-time data processing.

**Describe the Project**:

- **Goal**: Ingest Bitcoin price data from a public API (such as CoinGecko) and carry out basic time series analysis using Bonobo.  
    
- **Steps**:  
    
  1. **Ingest Data**: Set up Bonobo to regularly fetch Bitcoin price data from a live API.  
  2. **Transform Data**: Parse and clean the JSON response to extract necessary fields such as timestamp, price, and volume.  
  3. **Load Data**: Store the cleaned data into a suitable file format (e.g., CSV) or a lightweight database (e.g., SQLite) for further analysis.  
  4. **Analyze Data**: Implement basic time series analysis methods such as moving averages, trend detection, and volatility analysis using standard Python libraries.  
  5. **Visualize Results**: Use a Python plotting library (e.g., Matplotlib or Seaborn) to visualize the Bitcoin price trends and analysis results.


- **Outcome**: Students will understand the capabilities of Bonobo and how to handle real-time data pipelines efficiently. They will also gain experience in time series analysis, crucial for financial data applications.

**Useful Resources**:

- [Bonobo Documentation](https://bonobo.readthedocs.io/en/latest/)  
- [CoinGecko API Reference](https://coingecko.com/en/api)  
- [Basic Time Series Analysis in Python](https://towardsdatascience.com/basic-time-series-manipulation-with-pandas-4432afee64ea)

**Is it free?**:

- Yes, Bonobo is an open-source framework and free to use. Most public Bitcoin data APIs, such as CoinGecko, offer free access with limitations based on usage.

**Python Libraries / Bindings**:

- **Bonobo**: Install using `pip install bonobo` to create ETL pipelines quickly.  
- **Requests**: For interacting with the Bitcoin price API, install with `pip install requests`.  
- **Pandas**: Utilize for data manipulation and simple time series operations, install with `pip install pandas`.  
- **Matplotlib/Seaborn**: Use these libraries for visualizing data, install with `pip install matplotlib seaborn`.

By completing this project, students will acquire essential skills in using Bonobo for ETL processes and performing basic time series analysis, which are critical for handling big data systems in real-world scenarios.
