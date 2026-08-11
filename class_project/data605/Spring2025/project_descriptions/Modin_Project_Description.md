### **Modin**

**Title**: Process Real-Time Bitcoin Data with Modin

**Difficulty**: 1 (easy)

**Description**  
Modin is a parallel DataFrame library compatible with pandas that accelerates data processing by making use of all available CPU cores. It maintains full compatibility with pandas, allowing for a seamless transition of existing pandas code to take advantage of Modin's improved performance. Modin provides substantial speedup in data processing tasks, making it an excellent choice for handling large datasets or processing data in real-time without having to change existing code dramatically.

**Describe technology**

- Modin parallelizes operations on pandas DataFrames by distributing the computation across all available CPU cores, thus speeding up the data processing.  
- It supports a majority of pandas APIs without requiring changes to the existing pandas codebase.  
- Modin can be integrated with Dask or Ray as backends for parallel processing, thus providing scalability beyond a single machine.

**Describe the project**

- **Objective**: Implement a real-time data processing pipeline using Modin to conduct time series analysis on Bitcoin price data obtained from a public API (e.g., CoinGecko).  
- **Steps**:  
  1. Fetch real-time Bitcoin price data from a chosen API using basic Python libraries (e.g., `requests`).  
  2. Initialize a Modin DataFrame to ingest and preprocess the data. This can include data cleaning and transformation into a time series format.  
  3. Perform basic time series analysis using Modin, such as calculating moving averages, price variances, and detecting patterns over time.  
  4. Visualize the results using a compatible library (e.g., matplotlib) to plot time series trends.  
  5. Conclude with a simple report summarizing findings from the analysis.

**Useful resources**

- [Official Modin Documentation](https://modin.readthedocs.io/en/latest/)  
- [Getting Started with Modin](https://modin.readthedocs.io/en/latest/getting_started/index.html)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, both Modin and the CoinGecko API are free to use, with the latter having limitations on the number of requests you can make within a certain period.

**Python libraries / bindings**

- **Modin**: Core library to accelerate DataFrame operations, compatible with pandas. Install via `pip install modin[dask]` or `pip install modin[ray]` depending on the chosen backend or `pip install modin[all]`.  
- **Requests**: To fetch real-time Bitcoin data: `pip install requests`.  
- **Matplotlib**: To visualize the analyzed data: `pip install matplotlib`.
