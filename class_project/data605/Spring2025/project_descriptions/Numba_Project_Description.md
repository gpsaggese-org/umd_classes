### **Numba**

**Title**: Real-Time Bitcoin Price Analysis with Numba

**Difficulty**: 1 (Easy)

**Description**  
This project involves using Numba, a just-in-time compiler that translates a subset of Python and NumPy code into fast machine code, to ingest and process real-time Bitcoin price data. The task will focus on implementing basic functionalities of Numba to optimize computational parts of a Python-based time series analysis on Bitcoin prices.

**Describe Technology**

- Numba is designed to accelerate numerical Python functions, making them nearly as fast as compiled languages like C or FORTRAN.  
- Key functionalities include:  
  - Just-In-Time (JIT) Compilation: Numba compiles Python functions “just-in-time” to improve runtime performance.  
  - Easy integration with NumPy: Numba can efficiently handle NumPy operations, improving array processing speed.  
  - Parallel Computing: Supports GPU and multi-core CPUs to enable parallel computations.

**Describe the Project**

- **Objective**: Implement a real-time data processing system for Bitcoin prices with optimized performance using Numba.  
    
- **Steps**:  
    
  1. **Data Ingestion**: Use a basic Python library, like `requests`, to fetch real-time Bitcoin price data from a public API (e.g., CoinGecko).  
  2. **Optimization with Numba**: Write a function to analyze the time series data, focusing on tasks like simple moving averages or returns. Use Numba's JIT decorator to optimize these functions.  
  3. **Real-time Processing**: Implement a loop to fetch data at regular intervals and process it using the Numba-optimized functions.  
  4. **Visualization**: Use matplotlib to plot the real-time price changes and computed metrics, providing a visual insight into Bitcoin's price trends.


- **Outcome**: Students will gain experience in boosting Python performance with Numba, applying it to time-sensitive cryptocurrency data analysis.

**Useful Resources**

- [Numba Documentation](https://numba.readthedocs.io/en/stable/index.html)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Matplotlib for Data Visualization](https://matplotlib.org/)

**Is it Free?**  
Yes, Numba is an open-source Python library freely available for use. Access to cryptocurrency APIs like CoinGecko can also be used for free within certain limits.

**Python Libraries / Bindings**

- **Numba**: For optimizing numerical computations (`pip install numba`)  
- **Requests**: To fetch real-time data from APIs (`pip install requests`)  
- **NumPy**: For numerical operations (`pip install numpy`)  
- **Matplotlib**: To visualize the data (`pip install matplotlib`)
