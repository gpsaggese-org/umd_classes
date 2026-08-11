### **Django ORM**

**Title**: Real-Time Bitcoin Analysis using Django ORM

**Difficulty**: 2 

**Description**: Django ORM (Object-Relational Mapping) is a core component of the Django web framework that allows you to interact with your database, like SQL statements. It offers an intuitive and efficient way to manage database queries through Python classes and methods rather than writing raw SQL. This project involves using the Django ORM to ingest real-time Bitcoin price data from an API, store it in a database, and perform time series analysis to gain insights into price trends and volatility.

**Describe technology**:

- *Django ORM* is an integral part of Django that simplifies the communication between relational databases and Python applications through a high-level Python API.  
- It supports various database backends (e.g., PostgreSQL, MySQL, SQLite).  
- Django models represent database tables, leveraging Python classes and attributes, making it easy and intuitive to manipulate complex queries.  
- With migrations, Django ORM automatically adapts the database schema as models evolve, which ensures a smooth evolution of the database structure.  
- It offers filtering and querying capabilities through chaining methods and Pythonic syntax, providing powerful and flexible data retrieval options.

**Describe the project**:

- **Objective**: Use Django ORM to ingest, store, and analyze live Bitcoin pricing data.  
- **Data Ingestion**: Fetch real-time Bitcoin prices from a public API, such as CoinGecko, and use Django models to store the fetched data in a SQLite database.  
- **Data Processing**: Develop Django model methods or separate functions to perform basic data processing such as calculating average prices, detecting peaks, or measuring volatility over a specific period.  
- **Time Series Analysis**: Implement a simple time series analysis function or feature within the project using standard Python libraries to visualize trends, cyclic patterns, or anomalies in bitcoin prices.  
- **Deployment**: Set up a Django web application to provide users with the ability to visualize real-time Bitcoin price data and analysis directly in a web interface.

**Useful resources**:

- [Django Official Documentation](https://docs.djangoproject.com/en/stable/)  
- [Django ORM Documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/)  
- [SQLite Database](https://www.sqlite.org/index.html)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)

**Is it free?**: Yes, Django is an open-source framework, and SQLite is a free database engine. All tools mentioned in the project can be used at no charge.

**Python libraries / bindings**:

- **Django**: For using Django ORM and building the overall project structure. Install it via `pip install django`.  
- **Requests**: To fetch real-time Bitcoin data from APIs. Install it using `pip install requests`.  
- **Matplotlib or Plotly**: For creating visualizations of the time series analysis, install using `pip install matplotlib` or `pip install plotly`.  
- **Pandas**: Optional but useful for handling complex data manipulation and analysis tasks. Install it with `pip install pandas`.
