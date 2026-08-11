### **HuggingFace \#2**

**Title**: Bitcoin Event-Driven Price Impact Analysis with Hugging Face NLP  
**Difficulty**: 2 (medium)  
**Description**  
**Describe technology**  
Hugging Face’s `transformers` library provides models for **Named Entity Recognition (NER)** and **text classification**. This project uses a pre-trained NER model (`dslim/bert-base-NER`) to detect Bitcoin-related events (e.g., regulatory changes, hacks) from news articles and measure their delayed price impact.

**Describe the project**  
This project identifies actionable Bitcoin market events from text and quantifies their multi-day price effects, avoiding overlap with sentiment-based approaches:

- **Data collection**:  
  - Scrape **long-form Bitcoin news articles** (not headlines) using `newspaper3k` (Python library).  
  - Fetch daily OHLC (Open-High-Low-Close) Bitcoin data from CoinGecko.  
- **Event extraction**:  
  - Use Hugging Face’s NER pipeline to detect entities like organizations ("SEC"), laws ("MiCA"), and technologies ("Lightning Network").  
  - Classify articles into event types using zero-shot classification (`facebook/bart-large-mnli`):  
    1. Regulatory, Technological, Market Manipulation, Adoption News.  
- **Time series engineering**:  
  - Create a binary event matrix (1=event occurred on day *t*, 0=otherwise) for each category.  
  - Calculate 3-day rolling price volatility (% change from day *t* to *t+3*).  
- **Causal inference**:  
  - Use **propensity score matching** (PSM) with `causalnex` to isolate event impacts from market noise.  
  - Quantify average price volatility increase/decrease per event type.  
- **Reporting**:  
  - Build an automated report showing "High-Impact Events" (e.g., "SEC lawsuits cause \+8% volatility").  
  - Visualize event clusters on a timeline with price overlays using `plotly`.


**Challenges**:

- Distinguishing impactful events from routine news (e.g., "Coinbase listing" vs. "Coinbase routine maintenance")  
- Handling overlapping events in time series analysis  
- Addressing survivorship bias in news scraping


**Useful resources**

- [Hugging Face Zero-Shot Classification Guide](https://huggingface.co/docs/transformers/tasks/zero_shot_classification)  
- [CausalNEX Documentation](https://causalnex.readthedocs.io/)  
- [CoinGecko OHLC API](https://www.coingecko.com/en/api/documentation)


**Is it free?**  
Yes:

- `newspaper3k` and Hugging Face models are open-source  
- CoinGecko API free tier supports daily data  
- `causalnex` is MIT-licensed


**Python libraries / bindings**

- `transformers`: NER and zero-shot classification  
- `newspaper3k`: News article scraping & NLP  
- `causalnex`: Propensity score matching  
- `pandas`/`numpy`: Time series alignment  
- `plotly`: Interactive timeline visualization  
- `requests`: API data fetching
