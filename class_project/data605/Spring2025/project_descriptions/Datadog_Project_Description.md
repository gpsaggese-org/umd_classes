### **Datadog**

**Title**: Analyze Bitcoin Time Series Data with Datadog

**Difficulty**: Medium 

**Description**  
This project aims to leverage Datadog as a monitoring and analytics platform to ingest and process real-time bitcoin price data. Datadog provides observability services that integrate seamlessly with various data sources. Through this project, students will get hands-on experience with Datadog, learning how to set up data pipelines, monitor performance, and conduct real-time analytics. This will involve setting up data ingestion from a public API, visualizing time-series data, and performing basic trend analysis using Python.

**Describe Technology**  
Datadog is a monitoring and analytics platform for developers, IT operation teams, and business users in the cloud age. It offers a comprehensive view of real-time data from various sources, allowing users to monitor servers, databases, tools, and services through a unified platform. Key features include:

- Customizable dashboards for visualization.  
- Built-in support for monitoring time-series data.  
- Alerts based on real-time data insights.  
- Seamless integration with various data sources and services.

**Describe the Project**  
The focus of this project is to employ Datadog for real-time monitoring and analysis of Bitcoin price data. The steps include:

1. **Data Ingestion**: Use an API like CoinGecko to fetch real-time Bitcoin price data and send it to Datadog for monitoring.  
2. **Datadog Setup**: Create a new Datadog account if not already existing. Configure a new custom event in Datadog to receive price data in real-time.  
3. **Dashboards and Visualization**:  
   - Create a real-time dashboard to visualize Bitcoin price fluctuations.  
   - Configure alerts to notify when the price crosses certain thresholds.  
4. **Time Series Analysis**: Utilize Datadog’s built-in tools to perform basic time series analysis.  
   - Implement moving average calculations to smooth out price data.  
   - Analyze trends and volatility over a set period.  
5. **Python Integration**: Write Python scripts to automate data fetching and transmission to Datadog.  
6. **Reporting and Optimization**: Present findings through automatically generated reports and optimize data ingestion for performance.

**Useful Resources**

- [Datadog Documentation](https://docs.datadoghq.com/)  
- [CoinGecko API Documentation](https://coingecko.com/en/api)  
- [Python Requests Library](https://requests.readthedocs.io/)

**Is it Free?**  
Datadog offers a 14-day free trial for new users. However, a paid subscription is required for continued use beyond the trial period with full features.

**Python Libraries / Bindings**

- **Requests**: A comprehensive HTTP library for Python that allows you to send HTTP requests for fetching API data. Install it using `pip install requests`.  
- **Datadog API Client**: Datadog provides a Python client to interact with their API for sending data and managing resources. Install with `pip install datadog`.  
- **Pandas (optional)**: For additional data manipulation and analysis in Python, install using `pip install pandas`.
