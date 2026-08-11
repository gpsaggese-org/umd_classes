### **PyMC3**

**Title**: Real-time Bitcoin Price Analysis Using PyMC3

**Difficulty**: 3 (difficult)

**Description** Explore the advanced capabilities of PyMC3, a probabilistic programming library for Python that allows users to build complex Bayesian models quickly. Students will employ PyMC3 to perform probabilistic time series analysis on real-time Bitcoin data, incorporating Bayesian inference and time series forecasting techniques.

**Describe Technology**

- PyMC3 is a Python library for probabilistic programming focused on Bayesian statistical models.  
- It leverages advanced algorithms such as the No-U-Turn Sampler (NUTS), a variant of the Hamiltonian Monte Carlo (HMC) method, to efficiently sample from probabilistic models.  
- The library's user-friendly and expressive API makes it easy to define complex statistical models, conduct inference, and predict future outcomes using Bayesian principles.  
- The technology is particularly useful for uncertain environments where the goal is to infer unknown parameters or predict future states, making it well-suited for real-time data processing.

**Describe the Project**

- **Objective**: Develop a system to continuously ingest real-time Bitcoin price data and perform Bayesian time series analysis to forecast future price trends.  
- **Data Ingestion**: Use a basic Python package like `requests` or `websockets` to pull data from a public Bitcoin API such as CoinGecko or Binance.  
- **Data Processing**: Transform the raw JSON data to a time series format, ensuring it's ready for analysis with PyMC3.  
- **Modeling with PyMC3**:  
  - Define a probabilistic model for time series forecasting. A common choice is to use a Bayesian ARIMA model or a state-space model adapted for Bayesian inference.  
  - Use PyMC3 to perform inference on the model parameters, allowing for uncertainty quantification and robustness in forecasts.  
  - Implement real-time updating of the time series model as new Bitcoin price data is ingested.  
- **Forecasting and Analysis**: Generate probabilistic forecasts of future Bitcoin prices and visualize the results using libraries like `Matplotlib` or `Seaborn`.  
- **Outcome**: Students will gain hands-on experience with Bayesian modeling, learn to handle real-time data streams, and develop proficiency in probabilistic forecasting.

**Useful Resources**

- PyMC3 Documentation: [PyMC3 Documentation](https://docs.pymc.io/)  
- PyMC3 GitHub Repository: [PyMC3 GitHub](https://github.com/pymc-devs/pymc3)  
- CoinGecko API Documentation: [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- Basic tutorial on Bayesian time series analysis: [Time Series Analysis Blog](https://charlescopley.medium.com/conducting-time-series-bayesian-analysis-using-pymc-22269aeb208b)

**Is it Free?** 

Yes, PyMC3 is an open-source library and free to use. Data ingestion from public Bitcoin APIs like CoinGecko is generally free, although certain features or higher data request rates may require payment or registration.

**Python Libraries / Bindings**

- `pymc3`: For building and estimating Bayesian models. Install via `pip install pymc3`.  
- `requests` or `websockets`: For retrieving real-time Bitcoin price data from APIs. Install using `pip install requests` or `pip install websockets`.  
- `pandas`: For data manipulation and transformation into time series format. Install using `pip install pandas`.  
- `numpy`: For numerical computations necessary in model definitions and transformations. Install via `pip install numpy`.  
- Visualization tools like `matplotlib` or `seaborn`: For graphing real-time price and forecast results. Install using `pip install matplotlib seaborn`.
