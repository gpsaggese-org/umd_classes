### **Flask**

**Title**: Real-Time Bitcoin Monitoring with Flask

**Difficulty**: 2 (medium difficulty)

**Description**  
This project entails creating a web application using Flask, a lightweight web framework for Python, to ingest and process real-time Bitcoin data. Flask is known for its simplicity and flexibility, making it an ideal choice for creating web applications and APIs. The project focuses on using Flask to develop a real-time data processing solution where students fetch, display, and analyze Bitcoin price data. Through this project, students will gain hands-on experience in building a web application and performing basic time series analysis using Python libraries.

**Describe technology**

- **Flask**: Flask is a micro web framework written in Python. It is designed to be straightforward and easy to use, allowing developers to quickly create web applications or APIs. Flask provides essential functionalities such as routing, request handling, and templating but leaves out complexities of larger frameworks, promoting modular and adaptable development.  
  - Example functionalities:  
    - **Routing**: Define URL routes to handle client requests.  
    - **Templating**: Use Jinja2 to render dynamic HTML pages.  
    - **Request Handling**: Manage HTTP methods like GET and POST.

**Describe the project**

- The goal is to develop a Flask-based web application that:  
  1. **Ingests Real-Time Bitcoin Data**: Set up a routine using Flask's task scheduling (e.g., with APScheduler) to fetch live Bitcoin price data from a public API like CoinGecko or CryptoCompare at regular intervals.  
  2. **Data Storage**: Store the fetched data in a local database (such as SQLite) to manage and query historical prices.  
  3. **Data Display**: Create a simple web interface to display real-time Bitcoin price charts and allow users to query past data.  
  4. **Time Series Analysis**: Implement basic time series analysis functionalities within Flask, such as computing moving averages or identifying trends in Bitcoin prices over time.  
  5. **API Integration**: Optionally, expose an API endpoint using Flask that returns processed data (e.g., average price over a specified period) to external clients.

**Useful resources**

- [Flask Documentation](https://flask.palletsprojects.com/en/latest/)  
- [Real Python Flask Tutorial](https://realpython.com/tutorials/flask/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [CryptoCompare API Documentation](https://min-api.cryptocompare.com/documentation)

**Is it free?**  
Yes, Flask is an open-source framework and free to use. Public APIs like CoinGecko offer free tiers, although they may have rate limits.

**Python libraries / bindings**

- **Flask**: Main framework for building the web application.  
- **Requests**: To handle HTTP requests to fetch Bitcoin data. Install via `pip install requests`.  
- **SQLite3**: Built-in Python library for database operations.  
- **Matplotlib/Plotly**: For plotting Bitcoin price data. Install via `pip install matplotlib` or `pip install plotly`.  
- **pandas**: For data manipulation and basic time series analysis. Install via `pip install pandas`.  
- **APScheduler**: For scheduling periodic tasks within the Flask app. Install via `pip install apscheduler`.
