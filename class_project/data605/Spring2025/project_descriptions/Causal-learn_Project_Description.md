### **Causal-learn**

**Title**: Bitcoin Price Causality Analysis with Causal-Learn  
**Difficulty**: 2 (Medium)

**Description**  
A project to analyze causal relationships in Bitcoin price movements and related market variables (e.g., trading volume, social sentiment) using the `causal-learn` package for time series causal inference.

**Describe technology**

- **`causal-learn`**: A Python library for causal discovery, offering algorithms like Granger causality and constraint-based methods to infer causal links in time series data.  
- Designed to work with observational/time series datasets (e.g., financial data).  
- Integrates with Python’s data stack (`pandas`, `numpy`) for preprocessing and analysis.

**Describe the project**

1. **Data Collection**:  
   - Collect Bitcoin historical data (price, trading volume) and external variables (e.g., Google Trends for "Bitcoin," S\&P 500 index) using APIs like `yfinance` or `Cryptocompare`.  
   - Example: Download hourly/daily Bitcoin price and volume data for the past 2 years.  
2. **Preprocessing**:  
   - Handle missing values, normalize data, and engineer lagged features (e.g., lagged price changes).  
3. **Causal Discovery**:  
   - Use `causal-learn`’s time-series methods to identify causal drivers of Bitcoin price changes.  
   - Example code snippet for Granger causality:  
4. **Interpretation**:  
   - Analyze which variables (e.g., trading volume, S\&P 500\) Granger-cause Bitcoin price changes.  
5. **Validation**:  
   - Validate results against known economic hypotheses (e.g., "trading volume precedes price changes").  
6. **Visualization**:  
   - Plot causal graphs and time series interactions using `matplotlib` or `seaborn`.  
7. **Optional Extension**:  
   - Incorporate sentiment analysis from social media (e.g., Reddit/Twitter) using `textblob` and test its causal impact.

**Useful resources**

- [Causal-Learn Documentation](https://causal-learn.readthedocs.io)  
- [Yahoo Finance API (`yfinance`) Tutorial](https://pypi.org/project/yfinance/)  
- [Paper: "Causal Relationships in Cryptocurrency Markets" (arXiv)](https://arxiv.org/abs/2203.12114)


**Is it free?**  
Yes. `causal-learn`, `yfinance`, and other suggested tools are open-source.

**Python libraries / bindings**

- Core: `causal-learn`  
- Data: `pandas`, `yfinance`, `numpy`  
- Visualization: `matplotlib`, `seaborn`  
- Optional: `textblob` (for sentiment analysis)  
-
