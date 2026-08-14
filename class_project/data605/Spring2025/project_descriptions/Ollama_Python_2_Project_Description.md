### **Ollama Python \#2**

**Title**: Real-Time Bitcoin Price Analysis and Forecasting with Ollama-Python  
**Difficulty**: 3 (difficult)  
**Description**  
**Describe technology**  
Ollama-Python is a Python library for interacting with Ollama, a framework for deploying and running large language models (LLMs) locally. Ollama simplifies running models like LLaMA, Mistral, or CodeLLaMA on your machine, enabling text generation, data analysis, and fine-tuning. It supports REST API integration and real-time inference, making it suitable for combining LLMs with data pipelines.

**Describe the project**  
This project involves building a real-time Bitcoin price analysis system that integrates Ollama-Python to generate insights and forecasts from streaming data. Students will:

1. **Ingest real-time Bitcoin price data** from a public API (e.g., CoinGecko or Binance) using Python’s `requests` or `websockets`.  
2. **Process time series data** with `pandas` to calculate metrics (e.g., moving averages, volatility) and detect anomalies.  
3. **Integrate Ollama-Python** to run an LLM (e.g., Mistral-7B) for two tasks:  
   - Generate natural language summaries of price trends (e.g., "Bitcoin surged 5% in the last hour").  
   - Forecast short-term price movements by fine-tuning the LLM on historical data.  
4. **Build a real-time dashboard** using `Plotly` or `Dash` to visualize raw data, metrics, and LLM-generated insights.  
5. **Implement a streaming pipeline** to ensure low-latency processing (e.g., using `Faust` for stream processing).

**Challenges**:

- Optimizing Ollama’s inference speed for real-time use.  
- Structuring prompts to extract meaningful insights from time series data.  
- Handling computational constraints when running LLMs alongside data pipelines.

**Useful resources**

- [Ollama-Python Documentation](https://github.com/ollama/ollama-python)  
- [CoinGecko API Guide](https://www.coingecko.com/en/api)  
- [Time Series Forecasting with Machine Learning](https://otexts.com/fpp3/) (Chapter 11\)

**Is it free?**  
Ollama is open-source and free, but running large LLMs (e.g., 7B+ parameter models) requires significant RAM/GPU resources. Students may need cloud credits for GPU instances.

**Python libraries / bindings**

- `ollama-python`: Interact with Ollama’s local API to run LLMs.  
- `pandas`/`numpy`: Time series processing.  
- `requests`/`websockets`: Fetch real-time Bitcoin data.  
- `plotly`/`dash`: Visualization dashboard.  
- `faust`/`kafka-python`: Stream processing (optional for advanced pipelines).
