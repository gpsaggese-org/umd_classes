### **Altair**

**Title**: Interactive Bitcoin Market Dashboard with Vega-Altair

**Difficulty**: Difficult

**Description**  
Create a real-time interactive visualization system for Bitcoin market data using Vega-Altair's declarative visualization capabilities. The project combines live data streaming with complex financial visualizations, implementing a self-updating dashboard that shows price trends, volatility heatmaps, and on-chain metrics through declarative JSON specifications.

**Describe Technology**

- **Vega-Altair**: Declarative visualization library that:  
  1. Creates interactive charts through concise Python syntax  
  2. Supports complex visual encodings (e.g., layered charts, interactive selections)  
  3. Generates Vega-Lite specifications for web-native rendering  
  4. Enables client-side interactivity without callback functions  
  5. Integrates with Jupyter and web frameworks through JSON output

**Describe the Project**

1. **Real-Time Visualization Pipeline**:  
   - Ingest WebSocket data from Coinbase Pro/Binance  
   - Implement windowed transforms for:  
     - 15-minute candlestick aggregates  
     - Relative Strength Index (RSI) calculations  
     - Miner reserve vs price correlation  
   - Use Altair's `transform_*` methods instead of pre-processing

2. **Advanced Visual Features**:  
   - Create a layered chart with:  
     - Price line (primary axis)  
     - Volume bars (secondary axis)  
     - Bollinger Band confidence intervals  
   - Add interactive elements:  
     - Brush selection for time range focus  
     - Crosshair tooltip with multiple axis values  
     - Legend-driven series toggling  
-   
3. **Dashboard System**:  
   - Build a 3-panel view using Altair's `hconcat`/`vconcat`:  
     1. Time series with technical indicators  
     2. Volatility surface heatmap (time vs window size)  
     3. Mempool transaction size distribution  
   - Implement shared selections across panels  
-   
2. **Deployment Architecture**:  
   - Serve visualizations through FastAPI/Starlette with:  
     - Server-sent events for real-time updates  
     - Vega-Embed for web rendering  
     - Persistent view states through URL parameters  
   - Create a monitoring system that:  
     - Detects chart rendering errors  
     - Auto-adjusts bin sizes based on data density

   

**Useful Resources**

- [Vega-Altair Documentation](https://altair-viz.github.io)  
- [Vega-Altair Interactive Examples](https://github.com/altair-viz/altair_notebooks)  
- [Cryptocurrency Market Data Best Practices](https://www.kaiko.com/insights)


**Is it free?**  
Yes \- Vega-Altair is open-source (BSD-3). Exchange APIs have rate-limited free tiers.

**Python Libraries / Bindings**

- `altair`: Core visualization engine  
- `websockets`/`aiohttp`: Real-time data ingestion  
- `pandas`: Windowed transformations  
- `fastapi`/`starlette`: Dashboard serving  
- `jinja2`: Template rendering for web views
