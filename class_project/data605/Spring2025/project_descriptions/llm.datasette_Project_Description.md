### **llm.datasette**

**Title**: Real-Time Bitcoin Data Processing with Datasette

**Difficulty**: 2 (medium, it should take around 10 days to complete)

**Description**: Datasette is an open-source tool designed for exploring and publishing data, especially useful for working with structured datasets. It's built to make it easy to visualize and query data from SQLite databases. In this project, you will learn how to use Datasette to ingest and process real-time Bitcoin pricing data. The main objectives are to set up an SQLite database to store the incoming data, visualize the data trends, and perform time series analysis. This project allows students to interact with data in a more dynamic and exploratory fashion, leveraging the easy-to-use yet powerful capabilities of Datasette.

**Describe technology**:

- **Datasette**: An open-source tool specifically designed for publishing and exploring data from SQLite databases over the web.  
- Provides a web interface for querying and visualizing data, making it accessible to users without requiring advanced technical skills.  
- Excellent for building publicly accessible databases with strong support for custom plugins and queries.  
- Supports live-updating datasets, making it suitable for real-time data analysis and exploration.

**Describe the project**:

- **Objective**: To develop a real-time data processing system to ingest Bitcoin pricing data and perform basic time series analysis using Datasette.  
- **Data Ingestion**: Use a public API like CoinGecko to fetch real-time Bitcoin price data and store it in an SQLite database.  
- **Database Setup**: Configure Datasette to connect to SQLite, creating a live-updating database that continuously ingests data.  
- **Visualization**: Utilize Datasette's web interface to build interactive dashboards for visualizing trends in Bitcoin prices over time.  
- **Time Series Analysis**: Implement basic time series analysis on the data, such as calculating moving averages and detecting price anomalies.

**Useful resources**:

- [Datasette Documentation](https://docs.datasette.io/)  
- [CoinGecko API Documentation](https://coingecko.com/en/api/documentation)  
- [SQLite Documentation](https://sqlite.org/docs.html)  
- [Time Series Analysis in Python](https://www.analyticsvidhya.com/blog/2021/07/time-series-forecasting-in-python/)

**Is it free?**: Yes, Datasette is open-source and free to use. However, hosting on a cloud service for production may incur costs.

**Python libraries / bindings**:

- **Datasette**: Installable via pip with `pip install datasette`. Provides a platform for exploring and publishing data using SQLite databases.  
- **Requests**: For making HTTP requests to fetch data from the CoinGecko API. `pip install requests` is needed.  
- **SQLite**: Built-in Python library for database interaction. No external installation is required.  
- **Pandas**: Helpful for manipulating and analyzing time series data. Install using `pip install pandas`.  
- **Schedule**: For scheduling regular updates of Bitcoin pricing data. Installable via `pip install schedule`.
