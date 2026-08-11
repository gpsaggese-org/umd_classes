### **Amazon ElasticSearch/OpenSearch**

**Title**: Bitcoin Price Trend Analysis and News Correlation with AWS OpenSearch  
**Difficulty**: 2 (Medium)

**Description**:  
Students will build a system to analyze Bitcoin price trends using AWS OpenSearch for time series analysis **and** incorporate semantic search/RAG techniques to correlate price anomalies with cryptocurrency news articles.  
**Describe Technology**:

- **AWS OpenSearch Service**: Validated for time series use cases via:  
  - Native support for `date_histogram` aggregations and time-based indexing.  
  - Built-in [Anomaly Detection](https://opensearch.org/docs/latest/monitoring-plugins/ad/index/) for automated pattern recognition.  
  - Hybrid use case: Combines time series analysis (price data) with RAG/semantic search (news articles).

**Describe the Project**:

1. **Time Series Pipeline**:  
   - Use Python to fetch real-time Bitcoin price data (e.g., CoinGecko API) and ingest into OpenSearch with timestamped indices.  
   - Perform time series aggregations (e.g., volatility analysis, moving averages) using OpenSearch DSL.  
2. **RAG Integration**:  
   - Scrape/news-API Bitcoin-related articles (e.g., Reddit, CryptoNews) and index them in OpenSearch.  
   - Use OpenSearch's semantic search to retrieve news snippets during priAmazon DynamoDB ce spikes/drops detected via anomaly analysis.  
3. **Correlation Analysis**:  
   - Build a dashboard showing Bitcoin price trends \+ annotated news events (e.g., "Regulation announcement → 12% price drop").

   

**Useful Resources**:

- OpenSearch [Time Series Documentation](https://opensearch.org/docs/latest/search-plugins/timeseries/)  
- AWS Guide: [Combining Time Series and Text Data](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/time-series.html)  
- [Bitcoin Historical Data API](https://www.coingecko.com/en/api)


**Is it free?**:  
AWS Free Tier covers small-scale testing. News APIs may have free tiers (e.g., Reddit API).

**Python Libraries / Bindings**:

- Core: `opensearch-py`, `pandas`, `requests`  
- Data: `coingecko-api` (Python wrapper), `beautifulsoup4` (news scraping)  
- Visualization: `matplotlib`, OpenSearch Dashboards
