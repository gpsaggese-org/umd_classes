### **Polars**

**Title**: Analyze Bitcoin Prices with Polars in Real-Time

**Difficulty**: 1 (easy)

**Description**  
Polars is a fast DataFrame library implemented in Rust for Python, known for its speed and ability to handle large datasets efficiently. This project will involve using Polars to ingest real-time Bitcoin price data and perform basic time series analysis. Students will gain experience with Polars' core functionalities, including DataFrame manipulation, querying, and aggregation. The goal is to demonstrate how to use Polars for efficient data processing, especially for time-sensitive financial data.

**Describe technology**

- **Polars** is a DataFrame library designed for high-performance, parallel processing of data.  
- Built using Rust but offers Python bindings, ensuring both speed and ease of use.  
- Supports both eager and lazy evaluation, providing flexibility for various data processing needs.  
- Efficiently handles large datasets and complex operations like grouping, joining, and aggregating with minimal memory usage.  
- Known to outperform traditional pandas for large datasets due to its parallel processing capabilities.

**Describe the project**

- **Objective**: Use Polars to ingest real-time Bitcoin price data from an API (e.g., CoinGecko).  
- **Step 1**: Set up a function to fetch Bitcoin price data from the API every few minutes.  
- **Step 2**: Use Polars to create a DataFrame and store the fetched data.  
- **Step 3**: Implement basic time series analysis methods such as calculating moving averages and price change over time.  
- **Step 4**: Visualize the insights using simple plotting libraries like Matplotlib.  
- **Outcome**: Students will understand how to ingest and process real-time data effectively using Polars and gain insights into the dynamic nature of Bitcoin price movements.

**Useful resources**

- [Polars Official Documentation](https://docs.pola.rs)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Polars GitHub Repository](https://github.com/pola-rs/polars)

**Is it free?**  
Yes, Polars is an open-source library and free to use. Access to the CoinGecko API is also free for basic usage.

**Python libraries / bindings**

- **Polars**: The main Python library for this project, used for data manipulation and analysis.  
- **Requests**: To seamlessly retrieve data from APIs.  
- **Matplotlib**: For plotting and visualizing the analyzed Bitcoin price data.  
- **Datetime**: Useful for handling dates and times, essential in time series analysis.
