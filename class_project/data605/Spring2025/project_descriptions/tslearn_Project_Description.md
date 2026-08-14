### **tslearn**

**Title**: Analyze Bitcoin Prices with tslearn

**Difficulty**: 1 (easy)

**Description**  
tslearn is a Python package specifically designed for time series analysis. The library supports an array of time series data processing functionalities, such as machine learning on time series, time series clustering, classification, and regression. Key features of tslearn include tools for normalization, metrics dedicated to time series (such as Dynamic Time Warping), and an interface that synchronizes well with popular libraries such as NumPy and Scikit-learn.

In this project, students will utilize tslearn to analyze real-time Bitcoin price data. They will work on fetching the data from a public API, process it, and perform a basic time series analysis to understand trends and patterns over a specified time frame. The focus will be on demonstrating the core capabilities of tslearn using straightforward time series analysis tasks.

**Describe technology**

- **tslearn**: Provides extensive tools and functions tailored specifically for time series data handling and analysis. It offers:  
  - Various metrics and methods for time series data (e.g., DTW, Soft-DTW).  
  - Tools for time series transformations such as scaling and interpolation.  
  - Compatibility with popular machine learning libraries for enhanced analytic capabilities.  
  - Predefined datasets for quick testing and benchmarking of algorithms.

**Describe the project**

- Fetch real-time Bitcoin price data using a public API such as CoinGecko.  
- Preprocess the incoming data to handle missing values and normalize the data.  
- Apply tslearn’s functionalities to:  
  - Perform clustering based on daily or hourly price patterns, using methods like k-means or hierarchical clustering.  
  - Analyze and visualize time series patterns, identifying significant trends or anomalies.  
- Extend the project by comparing different methods of time series classification offered by tslearn and evaluating their effectiveness on Bitcoin's price volatility.  
- Students will present a simple report with visualization of their findings using libraries like Matplotlib or Seaborn, demonstrating the application of tslearn's tools in analyzing Bitcoin prices effectively.

**Useful resources**

- [tslearn Documentation](https://tslearn.readthedocs.io/en/stable/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, tslearn is an open-source library and can be freely used for academic and personal projects. Access to Bitcoin price data via public APIs like CoinGecko is typically free, but may have usage limitations or rate restrictions.

**Python libraries / bindings**

- `tslearn`: The primary library for time series analysis. Install it using `pip install tslearn`.  
- `requests`: For making HTTP requests to the Bitcoin price API.  
- `numpy`: For numerical operations and data manipulation.  
- `pandas`: For handling and processing time series data in a structured format.  
- `matplotlib` and `seaborn`: For creating data visualizations to present time series data insights.
