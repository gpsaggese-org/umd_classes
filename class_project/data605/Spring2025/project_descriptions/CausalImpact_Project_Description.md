### **CausalImpact**

Title: Analyze Bitcoin Price Impact with CausalImpact

Difficulty: 1 (easy)

Description: CausalImpact is an open-source Python library that allows users to perform causal inference on time series data. It was initially developed by Google and provides a straightforward way to evaluate the effect of an intervention on a time series. This project will guide students through applying CausalImpact to analyze the impact of a major event (e.g., a government ban or a significant legal announcement) on Bitcoin prices. Over the course of a week, students will learn the basics of causal inference, how to frame a hypothesis, and apply CausalImpact to test their hypothesis using real-time Bitcoin price data.

**Describe technology:**

- CausalImpact: This library helps estimate the causal effect of a predictive event on time series data using a Bayesian structural time-series model.  
- It is particularly useful for cases where controlled experiments or randomized trials are not feasible.  
- Students will learn to set up and interpret the model which will ultimately enable them to investigate whether a suspected event has had a significant impact on Bitcoin prices.

**Describe the project:**

- The project will involve using an API like CoinGecko or CryptoCompare to collect real-time Bitcoin price data.  
- Identify a significant event that could plausibly impact Bitcoin's market behavior (e.g., a major regulatory announcement).  
- Use Python basic libraries to ingest and process this data for a specific time window before and after the event.  
- Apply the CausalImpact library to the prepared dataset to assess the impact of the chosen event.  
- Students will interpret the results, visualize the causal impact using graphical tools (like matplotlib), and prepare a brief report of their findings.

**Useful resources:**

- [CausalImpact Documentation](https://pypi.org/project/causalimpact/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api/documentation)  
- [CryptoCompare API](https://min-api.cryptocompare.com/documentation)  
- [Time Series Analysis Books and Tutorials](https://www.analyticsvidhya.com/blog/2018/02/time-series-forecasting-methods/)

**Is it free?**

- Yes, CausalImpact is an open-source library and free to use.  
- Collecting Bitcoin price data is free with limitations regarding the number of API calls, depending on the service provider.

**Python libraries / bindings:**

- `CausalImpact`: For causal inference on time series data (can be installed via pip: `pip install causalimpact`).  
- `pandas`: For data ingestion and preliminary data manipulation (install via pip: `pip install pandas`).  
- `requests`: For using APIs to fetch real-time Bitcoin data (install via pip: `pip install requests`).  
- `matplotlib`: For creating visual plots of data and results (install via pip: `pip install matplotlib`).
