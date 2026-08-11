### **TextBlob\#1**

**Title**: Bitcoin News Keyword Trend Analysis Using TextBlob  
**Difficulty**: 3 (Difficult)

**Description**  
**Describe technology**:

- **TextBlob**:  
  - A lightweight Python library for text processing.  
  - Provides tools for **noun phrase extraction**, part-of-speech tagging, and frequency analysis.  
  - Uses NLTK under the hood but simplifies complex NLP tasks.  
- **NewsAPI**:  
  - Aggregates news articles from global sources.  
  - Free tier allows keyword-based filtering (e.g., "Bitcoin," "blockchain").

**Describe the project**:  
**Objective**: Analyze Bitcoin-related news articles to identify trending keywords (e.g., "halving," "regulation," "ETF approval") and correlate their frequency with Bitcoin price movements over time.

**Tasks**:

1. **Ingest News Data**:  
   - Fetch Bitcoin-related articles using NewsAPI.  
   - Store metadata (title, description, publication date) in a DataFrame.  
2. **Keyword Extraction with TextBlob**:  
   - Use TextBlob’s `noun_phrases` method to extract key terms (e.g., "market crash," "institutional adoption").  
   - Create a frequency dictionary of terms per time window (hourly/daily).  
3. **Bitcoin Price Integration**:  
   - Fetch historical price data (e.g., from CoinGecko API).  
   - Align price changes with keyword frequency using timestamps.  
4. **Trend Correlation Analysis**:  
   - Use `pandas` to calculate **term-frequency volatility** (e.g., spikes in "regulation" mentions).  
   - Apply Granger causality tests (via `statsmodels`) to determine if keyword trends *precede* price changes.  
5. **Visualization**:  
   - Plot keyword frequency trends against price charts (e.g., "ETF approval" mentions vs. BTC price spikes).  
   - Use heatmaps to highlight correlations between specific terms and price movements.

**Useful resources**:

- [TextBlob Noun Phrase Extraction Guide](https://textblob.readthedocs.io/en/dev/quickstart.html#noun-phrase-extraction)  
- [Granger Causality in Time Series](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.grangercausalitytests.html)  
- [NewsAPI Python Client](https://newsapi.org/docs/client-libraries/python)

**Is it free?**

- TextBlob: Free and open-source.  
- NewsAPI: Free tier available (500 requests/day).  
- CoinGecko API: Free for non-commercial use.

**Python libraries / bindings**:

- `textblob` (core NLP tasks)  
- `newsapi-python` (news ingestion)  
- `pandas` (time-series alignment)  
- `statsmodels` (Granger causality tests)  
- `matplotlib`/`plotly` (interactive visualizations)
