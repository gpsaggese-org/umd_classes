### **Plotly \#2**

**Title**: Real-Time Bitcoin Blockchain Metrics Visualization and Time Series Analysis with Plotly  
**Difficulty**: 3 (difficult)

**Description**  
This project focuses on visualizing and analyzing Bitcoin blockchain metrics (e.g., transaction volume, block size, hash rate) in real-time using Plotly. Instead of Dash, you will use Plotly’s native interactive plotting capabilities to build a self-updating Jupyter Notebook or standalone HTML dashboard. The goal is to ingest live blockchain data, process it, and generate time series visualizations with statistical analysis.

**Describe technology**

- **Plotly**: A library for creating interactive, publication-quality graphs. It supports animations, subplots, and dynamic updates without Dash.  
- **Key Features**: Use Plotly’s `FigureWidget` for live updates in Jupyter Notebooks, or auto-refreshing HTML files with `plotly.offline`.

**Describe the project**

1. **Data Ingestion**:  
     
   - Fetch Bitcoin blockchain metrics (e.g., transaction count, hash rate) from APIs like Blockchain.com or Mempool.space.  
   - Use `requests` for REST API calls or `websockets` for streaming data.

   

2. **Data Processing**:  
     
   - Clean data with Pandas (handle missing values, resample time series).  
   - Compute rolling averages, transaction rates, and anomaly scores (Z-scores).  
   - Decompose time series into trend/seasonality/residuals using `statsmodels`.

   

3. **Visualization & Analysis**:  
     
   - **Real-Time Plots**: Use Plotly’s `FigureWidget` to create auto-updating line charts for live metrics.  
   - **Statistical Charts**: Build subplots showing decomposed time series, histograms, and correlation heatmaps.  
   - **Anomaly Highlighting**: Add annotations to flag unusual events (e.g., spikes in block size).  
   - Export visualizations as standalone HTML files with `plotly.offline.plot()`.

   

4. **Auto-Refresh Workaround**:  
     
   - Schedule periodic data fetches and plot updates using Python’s `time.sleep()` or `threading.Timer`.  
   - For Jupyter: Use `FigureWidget`’s `add_trace()` and `relayout()` to refresh plots.

**Useful resources**

- Plotly Time Series Tutorial: [https://plotly.com/python/time-series/](https://plotly.com/python/time-series/)  
- Blockchain.com API Docs: [https://www.blockchain.com/api](https://www.blockchain.com/api)  
- Statsmodels Decomposition Guide: [https://www.statsmodels.org/stable/examples/notebooks/generated/tsa\_decompose.html](https://www.statsmodels.org/stable/examples/notebooks/generated/tsa_decompose.html)

**Is it free?**  
Yes: Plotly’s open-source library and Blockchain.com’s API are free for non-commercial use.

**Python libraries / bindings**

- `plotly` (install: `pip install plotly`)  
- `pandas`, `numpy` (data processing)  
- `requests`, `websockets` (data ingestion)  
- `statsmodels` (time series decomposition)
