### **Qlik Sense**

**Title**: Real-time Bitcoin Price Analysis Using Qlik Sense

**Difficulty**: 3 (difficult)

**Description**: Qlik Sense is a powerful business intelligence and data visualization tool that allows users to create interactive reports and dashboards. It enables rapid insights through a robust associative data model and advanced analytics capabilities. In this project, students will learn to integrate Qlik Sense with real-time data streams, specifically focusing on ingesting and visualizing Bitcoin price data. The project will involve creating a real-time dashboard in Qlik Sense that showcases price trends, volatility, and predictive analytics by implementing a time series analysis using Qlik Sense's advanced analytical functions and Python.

**Describe technology**:

- Qlik Sense is designed for self-service analytics that simplifies data and derives meaningful insights, utilizing a drag-and-drop interface and powerful AI-driven features.  
- It uses an associative data model to link data from multiple sources, providing a unique advantage in data analysis.  
- Through its open APIs, Qlik Sense supports integrating analytics with custom applications, including Python scripts, to extend its capabilities.

**Describe the project**:

- **Step 1**: Set up a real-time data feed using Python to pull Bitcoin price data from a public API (e.g., CoinGecko) at regular intervals.  
- **Step 2**: Use Qlik Sense's data connector capabilities to ingest this data continuously, ensuring that the data is seamless and real-time through scheduled batch updates.  
- **Step 3**: Create a Qlik Sense dashboard that initially shows real-time Bitcoin price charts and other basic metrics like 24-hour high and low prices.  
- **Step 4**: Implement time series analysis on the data using Qlik Sense's analytical capabilities and integrate Python for advanced statistical modeling, like trend forecasting or volatility analysis.  
- **Step 5**: Extend the dashboard to allow for interactive exploration, letting users filter by time intervals, compare historical data, and visualize predictive analytics results.

**Useful resources**:

- [Qlik Sense Official Documentation](https://help.qlik.com/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**: 

Qlik Sense offers a free trial version, which provides access to basic features necessary for completing this project. This free tier has limitations on data size and storage but is sufficient for academic and small-scale projects.

**Python libraries / bindings**:

- `requests`: For making HTTP requests to obtain the Bitcoin pricing data from the public API. Install with `pip install requests`.  
- `pandas`: For handling and manipulating the data before integrating with Qlik Sense. Install with `pip install pandas`.  
- `Qlik-Py-Tools`: A set of Python scripts that can be used to build advanced analytics capabilities directly within Qlik Sense, enabling deeper integrations. This can be configured to run as a service in the background.

This project aims to deepen students' understanding of Qlik Sense's functionalities and the integration of Python for dynamic data analysis and visualization in a complex real-world scenario involving real-time data.
