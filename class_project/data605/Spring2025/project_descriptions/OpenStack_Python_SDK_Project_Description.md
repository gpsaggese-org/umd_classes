### **OpenStack Python SDK**

**Title**: Ingest Bitcoin Prices using OpenStack Python SDK

**Difficulty**: 1 (easy)

**Description**  
The OpenStack Python SDK offers a comprehensive set of tools to interact with OpenStack services using Python, facilitating operations like provisioning and managing cloud resources. For this project, students will explore how to use the OpenStack Python SDK to ingest and process real-time Bitcoin price data. Through this hands-on experience, students will learn about integrating cloud services using OpenStack and basic time series data analysis in Python.

**Describe technology**

- **OpenStack Python SDK**: A Python library that simplifies the interaction with OpenStack services. It provides object-oriented APIs to work with OpenStack clouds, covering services like compute, storage, and networking.  
- **Key Features**:  
  - Manage OpenStack cloud resources programmatically.  
  - Simplifies the integration with OpenStack services using high-level Python APIs.  
  - Facilitates automation and orchestration of cloud resources.

**Describe the project**  
In this project, students will:

2. **Set up an OpenStack Environment**: Use OpenStack to set up a simple cloud environment where they can manage resources.  
3. **Data Ingestion**: Use the OpenStack Python SDK to launch a cloud instance that runs a script to fetch real-time Bitcoin prices from a public API like CoinGecko.  
4. **Data Storage**: Store the raw Bitcoin price data in an OpenStack Object Storage service (Swift) for later analysis.  
5. **Real-time Processing**: Implement a simple time series analysis using Python to calculate and visualize trends in Bitcoin pricing data.  
6. **Data Visualization**: Use a basic plotting library like Matplotlib or Seaborn to create visualizations of the Bitcoin price trends.

**Useful resources**

- [OpenStack Python SDK Documentation](https://docs.openstack.org/openstacksdk/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Matplotlib](https://matplotlib.org/stable/contents.html)  
- [Python Time Series Analysis](https://www.machinelearningplus.com/time-series/time-series-analysis-python/)

**Is it free?**  
OpenStack itself is an open-source platform and can be set up on local systems without any cost. However, if students opt to use a professional cloud service or specific OpenStack distributions, they might incur costs.

**Python libraries / bindings**

- **OpenStack SDK**: The key library to interact with OpenStack resources. Install it with `pip install openstacksdk`.  
- **Requests**: A library for making HTTP requests to fetch data from APIs. Install with `pip install requests`.  
- **Pandas**: For data manipulation and analysis, especially useful for time series data. Install with `pip install pandas`.  
- **Matplotlib**: For creating static, animated, and interactive visualizations in Python. Install with `pip install matplotlib`.
