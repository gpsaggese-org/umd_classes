### **ActiveCampaign**

**Title**: Analyze Email Campaign Performance Over Time with ActiveCampaign  
**Difficulty**: 1 (easy)

**Description**  
This project introduces students to working with ActiveCampaign’s API to extract email campaign data, analyze time-based trends, and visualize results using Python.

**Describe Technology**

- **ActiveCampaign**: A customer experience automation platform used for email marketing, CRM, and automation. Its API allows programmatic access to campaign metrics (e.g., open rates, click-through rates) and user data.  
- **Key Features**:  
  - Retrieve historical campaign performance data (time-stamped).  
  - Track user engagement metrics (opens, clicks, unsubscribes).  
  - Automate data extraction for time series analysis.  
    

**Describe the Project**

1. **Set Up API Access**:  
   - Create an ActiveCampaign trial account and generate API credentials.  
   - Use Python’s `requests` library or the `activecampaign` Python client to connect to the API.  
2.   
3. **Extract Time Series Data**:  
   - Fetch email campaign metrics (e.g., daily opens, clicks) for the past 30 days.  
   - Store the data in a pandas DataFrame with timestamps.  
4. **Clean and Analyze Data**:  
   - Handle missing values and outliers.  
   - Calculate trends (e.g., weekly engagement patterns) using moving averages.  
5. **Visualize Results**:  
   - Plot time series trends with `matplotlib` or `seaborn`.  
   - Use `statsmodels` to forecast future engagement (e.g., ARIMA model).

**Useful Resources**

- [ActiveCampaign API Documentation](https://developers.activecampaign.com/reference)  
- [Pandas Time Series Guide](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)  
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)


**Is it Free?**

- ActiveCampaign requires a paid account, but a 14-day free trial is available. API access is included in all plans.

**Python Libraries / Bindings**

- **activecampaign-python**: Official Python client for ActiveCampaign’s API. Install via `pip install activecampaign`.  
- **pandas**: For data manipulation and time series analysis.  
- **matplotlib/seaborn**: For visualization.  
- **statsmodels** (optional): For advanced time series modeling.  
- **requests**: For direct API calls if not using the client.
