### **Pyllms**

**Title:** Real-Time Bitcoin Sentiment Analysis Using PyLLMs​

**Difficulty:** 2 (Medium)​

**Description:**

In this project, students will utilize PyLLMs, a minimal Python library designed to connect to various Large Language Models (LLMs), to perform real-time sentiment analysis on Bitcoin-related news articles. The project involves fetching real-time news data, processing it using LLMs accessed through PyLLMs, and determining the sentiment to assess potential impacts on Bitcoin prices. This project offers an excellent opportunity to learn about integrating LLMs into data processing pipelines using Python.​

**Describe technology:**

PyLLMs is a lightweight Python library that simplifies connections to multiple LLMs, including those from OpenAI, Anthropic, Google, and others. It offers a unified interface to interact with these models, enabling functionalities such as text completion, sentiment analysis, and more. Key features include:​

* **Multi-Model Support:** Easily switch between different LLM providers without altering the core codebase.​  
* **Benchmarking:** Built-in tools to evaluate model performance across various parameters.​  
* **Asynchronous and Streaming Support:** Facilitates efficient data processing with compatible models.​

**Describe the project:**

**Objective:** To analyze real-time Bitcoin-related news articles using LLMs accessed through PyLLMs to assess sentiment and potential impacts on Bitcoin prices.​

**Steps:**

1. **Data Ingestion:**  
   * Use a news API (such as NewsAPI) to fetch real-time news articles related to Bitcoin.​  
2. **Data Processing:**  
   * Extract relevant information from the news articles, such as headlines and content.​  
3. **Sentiment Analysis:**  
   * Utilize PyLLMs to connect to an LLM capable of performing sentiment analysis on the extracted news content.​  
4. **Impact Assessment:**  
   * Analyze the sentiment data to determine potential impacts on Bitcoin prices.​  
5. **Automation:**  
   * Set up a Python script to automate the data ingestion and analysis process at regular intervals (e.g., every hour).​

**Useful resources:**

* [PyLLMs GitHub Repository](https://github.com/kagisearch/pyllms)​  
* [NewsAPI Documentation](https://newsapi.org/docs)​

**Is it free?**

PyLLMs is an open-source library and free to use. However, accessing certain LLMs through PyLLMs may require API keys, which could have associated costs depending on the provider. Similarly, some news APIs offer free tiers with limitations, so it's essential to review their pricing structures.​

**Python libraries / bindings:**

* **PyLLMs:** Install via `pip install pyllms`.​  
* **Requests:** To make HTTP requests for fetching news data from the API (`pip install requests`).​  
* **Schedule:** To assist with running the script at regular intervals (`pip install schedule`).​

This project provides students with hands-on experience in integrating LLMs into data processing workflows using PyLLMs, focusing on real-time sentiment analysis of Bitcoin-related news.​
