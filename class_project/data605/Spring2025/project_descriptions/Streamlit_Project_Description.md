### **Streamlit**

**Title**: Real-Time Bitcoin Price Monitoring with Streamlit

**Difficulty**: 3 (difficult)

**Description**: This project focuses on building an interactive dashboard to monitor real-time Bitcoin prices using Streamlit, a popular Python library for creating web applications with minimal effort. Streamlit is incredibly useful for data scientists looking to quickly develop and deploy web-based data applications without needing advanced web development skills. The project's main challenge is ingesting, processing, and visualizing real-time data with an emphasis on time series analysis. Students will be required to use Python to fetch live Bitcoin data from an API, process this data to identify trends and patterns, and present the insights using an interactive Streamlit interface.

**Describe technology**:

- **Streamlit**: A powerful open-source app framework in Python, Streamlit turns Python data scripts into shareable web apps. It's particularly suited for data science applications because it allows for the quick development of interactive dashboards and visualizations without requiring HTML, CSS, or JavaScript.  
  - Key features include:  
    - **Easy-to-use APIs**: Create complex UIs with simple Python scripts.  
    - **Instant updates**: Modify the Python code, and the Streamlit app updates in real-time.  
    - **Data-driven components**: Integrate tables, charts, and plots with minimal boilerplate code.  
    - **Seamless integration**: Leverage existing Python libraries for data visualization like Matplotlib, Plotly, and Altair.

**Describe the project**:

- **Objective**: Develop a real-time dashboard application to monitor Bitcoin prices and analyze time series data using Streamlit.  
- **Implementation steps**:  
  1. **Data Ingestion**: Use Python to fetch live data from a Bitcoin price API such as CoinGecko or Alpha Vantage.  
  2. **Data Processing**: Preprocess the raw data for use in visualizations; this includes time series transformation, calculating moving averages, and detecting anomalies.  
  3. **Time Series Analysis**: Implement techniques for forecasting and identifying patterns. Utilize libraries such as Prophet or statsmodels to perform these analyses.  
  4. **Building the App**:  
     - Design the Streamlit interface to display current prices, historical trends, and prediction models.  
     - Add interactive widgets like sliders, dropdowns, and buttons to filter data by time periods, view different metrics, and customize visualizations.  
  5. **Visualizations**: Develop dynamic charts (using libraries like Plotly or Matplotlib) integrated within Streamlit to visualize the processed data and analysis results.  
- **Outcome**: By completing the project, students will gain experience in creating interactive applications that monitor real-time data, enhancing their skills in data science, Python programming, and web app development.

**Useful resources**:

- [Streamlit Documentation](https://docs.streamlit.io/library/get-started)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Prophet Documentation](https://facebook.github.io/prophet/docs/quick_start.html)  
- [Statsmodels Documentation](https://www.statsmodels.org/stable/index.html)

**Is it free?**

- **Yes**: Streamlit is open-source and free to use for developing applications. For deploying apps, Streamlit Cloud offers a free tier with some limitations.

**Python libraries / bindings**:

- **Streamlit**: (Install with `pip install streamlit`) \- Core framework for building interactive web apps.  
- **Requests**: (Install with `pip install requests`) \- Used to fetch data from APIs.  
- **Pandas**: (Install with `pip install pandas`) \- Essential for data manipulation and analysis.  
- **Plotly/Matplotlib/Altair**: (Install with `pip install plotly`, `matplotlib`, or `altair`) \- For creating interactive visualizations.  
- **Prophet/Statsmodels**: (Install with `pip install prophet` or `statsmodels`) \- To conduct time series analysis and forecasting.
