### **pywhy**

**Title:** Real-Time Bitcoin Price and News Sentiment Analysis with PyWhy and NewsAPI​

**Difficulty:** 3 (Difficult)

**Description:** This project aims to analyze real-time Bitcoin price data alongside news sentiment to uncover potential causal relationships between media coverage and price fluctuations. Students will utilize PyWhy for causal inference and NewsAPI to fetch relevant news articles, enabling a comprehensive analysis of how external factors influence Bitcoin's market behavior.​

**Describe Technology:**

* **PyWhy:**  
  * A Python library focused on causal inference.​  
  * Provides tools to model, estimate, and validate causal relationships in data.​  
  * Supports Directed Acyclic Graph (DAG) causal modeling and other statistical methods.​  
  * Offers an intuitive API for visualizing, simulating, and analyzing causality within datasets.​  
* **NewsAPI:**  
  * A service that provides access to news articles from various sources worldwide.​  
  * Allows fetching articles based on keywords, sources, and dates.​  
  * Offers a free tier suitable for development and testing purposes.​

**Describe the Project:**

**Objective:** To analyze the impact of news sentiment on real-time Bitcoin price movements using causal inference techniques.​

**Tasks:**

1. **Data Ingestion:**  
   * Fetch real-time Bitcoin price data at regular intervals using a public API (e.g., CoinGecko).​  
   * Retrieve news articles related to Bitcoin using NewsAPI, focusing on recent publications.​  
2. **Data Preprocessing:**  
   * Clean and structure the Bitcoin price data for analysis.​  
   * Perform sentiment analysis on the fetched news articles to quantify their sentiment scores.​  
3. **Causal Modeling:**  
   * Utilize PyWhy to construct a causal model examining the relationship between news sentiment and Bitcoin price movements.​  
   * Identify potential confounding variables and adjust the model accordingly.​  
4. **Analysis and Visualization:**  
   * Conduct time series analysis to observe correlations and causal effects.​  
   * Visualize the findings using libraries like Matplotlib or Seaborn to illustrate trends and causal links.​

**Useful Resources:**

* [PyWhy](https://www.pywhy.org)  
* [NewsAPI](https://newsapi.org/)  
* [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)​

**Is it Free?**

Yes, both PyWhy and NewsAPI offer free access suitable for development and testing. NewsAPI's free tier allows for up to 100 requests per day, which should suffice for small-scale projects.  CoinGecko also provides free access to cryptocurrency data.​

**Python Libraries / Bindings:**

* `pywhy`​  
* `newsapi-python`​  
* `requests`​  
* `pandas`​  
* `nltk` (for sentiment analysis)​  
* `matplotlib` or `seaborn`​

This project offers a practical introduction to causal inference and sentiment analysis, providing students with valuable skills in analyzing the interplay between media coverage and cryptocurrency markets.​
