### **Hex.tech**

**Title**: Collaborative Bitcoin Market Analysis & Forecasting with Hex  
**Difficulty**: 2 (medium)

**Description**  
**Describe technology**  
**Hex** is a modern data workspace for analytics and collaborative data science. Key features:

- **SQL/Python/R integration**: Mix code languages in notebooks.  
- **Data app publishing**: Turn analyses into interactive dashboards.  
- **Data lineage & versioning**: Track changes and dependencies.  
- **Scheduled pipelines**: Automate data refreshes (e.g., hourly Bitcoin prices).

**Describe the project**  
Build a Hex project to analyze Bitcoin market trends, correlate them with external factors (e.g., S\&P 500, gold), and create a price forecast model. Steps:

1. **Data Ingestion**:  
   - Connect to APIs using Hex’s Python cells:  
     - Bitcoin prices (CoinGecko API).  
     - Macroeconomic data (Alpha Vantage API).  
     - Social sentiment (CryptoPanic headlines).  
   - Schedule hourly data refreshes in Hex.  
2. **Time Series Analysis**:  
   - Use SQL in Hex to calculate:  
     - 30-day volatility.  
     - Bitcoin vs. gold correlation (rolling window).  
   - Python-powered anomaly detection (e.g., sudden 5% drops).  
3. **Machine Learning**:  
   - Train a Prophet time-series model on historical data.  
   - Publish predictions as a Hex data app with sliders to adjust forecast horizons.  
4. **Collaboration**:  
   - Add commentary cells to explain market events (e.g., "ETF approval impact").  
   - Share the app with peers for live feedback.

**Useful resources**

- Hex Docs: [https://learn.hex.tech/](https://learn.hex.tech/)  
- CoinGecko API Guide: [https://www.coingecko.com/en/api](https://www.coingecko.com/en/api)  
- Prophet Forecasting: [https://facebook.github.io/prophet/docs/quick\_start.html](https://facebook.github.io/prophet/docs/quick_start.html)

**Is it free?**   
Hex offers a free tier (limited compute hours). APIs may have usage limits.

**Python libraries / bindings**

- pandas: Data manipulation.  
- prophet: Time-series forecasting.  
- requests: API calls.  
- plotly: Interactive dashboards (built into Hex).
