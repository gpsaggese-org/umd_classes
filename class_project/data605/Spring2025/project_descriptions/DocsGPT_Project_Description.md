### **DocsGPT**

**Title**: Real-Time Bitcoin Data Q\&A Bot with DocsGPT  
**Difficulty**: 1 (medium)

**Describe technology**  
DocsGPT is an open-source AI tool designed to generate or retrieve documentation answers using natural language. It leverages language models (like GPT) to understand user queries and provide context-aware responses from documentation sources. Key features:

- Integration with custom datasets (e.g., CSV, text files).  
- Natural language processing for querying structured data.  
- Simple API or local deployment for small-scale projects.

**Describe the project**  
Build a CLI tool that ingests real-time Bitcoin price data (from CoinGecko API) and uses DocsGPT to answer time series-related questions. The project steps:

-   
1. **Data Ingestion**: Fetch Bitcoin prices every 5 minutes and store them in a CSV file with timestamps.  
2. **Time Series Processing**: Calculate basic metrics (e.g., hourly average, daily volatility) using pandas.  
3. **DocsGPT Setup**: Train DocsGPT on the Bitcoin dataset to understand fields like `timestamp`, `price`, and `volatility`.  
4. **Q\&A Interface**: Create a CLI where users ask questions like:  
   - "What was the highest price in the last 6 hours?"  
   - "When did the price drop by more than 2% today?"  
     DocsGPT processes the query, retrieves data, and 

**Useful resources**

- DocsGPT GitHub: [https://github.com/arc53/DocsGPT](https://github.com/arc53/DocsGPT)  
- CoinGecko API: [https://www.coingecko.com/en/api](https://www.coingecko.com/en/api)  
- Pandas time series guide: [https://pandas.pydata.org/docs/user\_guide/timeseries.html](https://pandas.pydata.org/docs/user_guide/timeseries.html)

**Is it free?**  
Yes. DocsGPT is open-source, and CoinGecko’s free tier supports up to 50 calls/minute.

**Python libraries / bindings**

- requests: Fetch Bitcoin data from CoinGecko API.  
  - pandas: Process time series data and calculate metrics.  
  - langchain (optional): Simplify DocsGPT integration for local LLM workflows.  
  - python-dotenv: Manage API keys (if using cloud-based LLMs).  
  - returns a plain-English answer.
