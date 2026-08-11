### **FastAPI**

**Title**: Real-Time Bitcoin Price Analysis with FastAPI

**Difficulty**: 2 (medium difficulty)

**Description**  
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python-type hints. It allows developers to create efficient backend services quickly and intuitively, with an emphasis on performance and an easy-to-use syntax. This project focuses on utilizing FastAPI to ingest and process real-time Bitcoin price data, perform time series analysis, and provide an API for querying and visualizing these analyses.

**Describe technology**

- **Key Features**: FastAPI enhances productivity by enabling automatic generation of interactive API documentation (Swagger and ReDocs) and validations based on Python-type hints.  
- **Asynchronous Support**: FastAPI supports asynchronous programming features in Python, enhancing the I/O performance crucial for real-time data processing.  
- **Performance**: Built on Starlette for the web parts and Pydantic for the data parts, FastAPI is one of the fastest Python web frameworks.

**Describe the project**

- **Objective**: Implement a system using FastAPI to fetch real-time Bitcoin price data from a public API (e.g., CoinGecko or Binance), perform basic time series analyses (such as moving averages), and expose this data through a RESTful API.  
- **Steps**:  
  1. **Setting up FastAPI**: Create a FastAPI application that has endpoints for fetching, storing, and serving processed Bitcoin price data.  
  2. **Data Ingestion**: Use FastAPI to continuously fetch Bitcoin price data at regular intervals and store it in memory or a lightweight database like SQLite.  
  3. **Processing**: Implement basic time series analysis techniques to evaluate trends in the data, such as calculating moving averages or identifying patterns.  
  4. **Exposing Data**: Use FastAPI's capabilities to build RESTful endpoints, allowing users to query processed data and view the analyses in a structured format.  
  5. **Visualization**: Optionally, incorporate simple data visualization (e.g., using Plotly or Matplotlib for graphs) to enhance the API output.

**Useful resources**

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Asyncio for Python (Async programming guide)](https://docs.python.org/3/library/asyncio.html)  
- [Pydantic (Data validation and settings management)](https://pydantic-docs.helpmanual.io/)

**Is it free?**  
Yes, FastAPI is an open-source framework and is free to use. CoinGecko API also provides free access with rate limits for public data.

**Python libraries / bindings**

- **FastAPI**: Used to create the API service. Install using `pip install fastapi`.  
- **Uvicorn**: An ASGI server needed to run FastAPI applications. Install using `pip install uvicorn`.  
- **HTTPX or AIOHTTP**: For making asynchronous HTTP requests to fetch Bitcoin prices. Install using `pip install httpx` or `pip install aiohttp`.  
- **SQLite (built-in Python library)**: For lightweight storage of time-series data.  
- **Pandas**: Utilized for data manipulation and time series analysis. Install using `pip install pandas`.  
- **Plotly or Matplotlib**: For optional data visualization. Install using `pip install plotly` or `pip install matplotlib`.
