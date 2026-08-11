### **Luigi Corrected**

**Title**: Real-Time Bitcoin Price Analytics Pipeline with Luigi  
**Difficulty**: 3 (difficult)  
**Description**:  
Design a Luigi-powered pipeline to ingest, process, and analyze real-time Bitcoin price data. The project focuses on building a fault-tolerant system for time series forecasting and anomaly detection.

**Describe technology**:

- **Luigi**: A workflow management system for orchestrating complex data pipelines.  
  - **Key functionalities**:  
    - Task dependency resolution (e.g., `requires()` method for chaining tasks).  
    - Atomic output handling (e.g., `output().exists()` checks).  
    - Parallel execution (e.g., `--workers 4` flag).  
  - Example: A `FetchDataTask` class that triggers `CleanDataTask` only after successful API ingestion.

**Describe the project**:

1. **Real-time ingestion**:  
   - Stream Bitcoin price data from Coinbase Pro WebSocket API (15,000+ requests/day).  
   - Implement error handling for API rate limits and reconnection logic.  
2. **Time series processing**:  
   - Calculate 1-hour rolling volatility and ARIMA-based forecasts.  
   - Detect anomalies using Z-score thresholds (±3σ).  
3. **Pipeline orchestration**:  
   - Create 5+ interdependent Luigi tasks (e.g., Fetch→Clean→Analyze→Visualize→Alert).  
   - Implement S3/MinIO integration for storing processed data.  
4. **Monitoring**:  
   - Generate PyPlot visualizations of price trends and prediction intervals.  
   - Send email alerts for detected anomalies using SMTPLIB.

**Useful resources**:

1. [Luigi: Complex Pipelines Made Easy](https://luigi.readthedocs.io/en/stable/)  
2. [Coinbase Pro WebSocket API Docs](https://docs.pro.coinbase.com/)  
3. [Forecasting: Principles and Practice (ARIMA guide)](https://otexts.com/fpp3/arima.html)

**Is it free?**: Yes (Luigi MIT License, Coinbase API free tier)

**Python libraries / bindings**:

- Core: `luigi`, `websockets`, `numpy`  
- Analysis: `statsmodels`, `pandas`, `scikit-learn`  
- Visualization: `matplotlib`, `seaborn`  
- Storage: `boto3` (for S3), `sqlalchemy`
