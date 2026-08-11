### **SQLAlchemy**

**Title**: Real-time Bitcoin Analysis with SQLAlchemy

**Difficulty**: 2

**Description**  
Students will explore the use of SQLAlchemy for managing and accessing large datasets with the focus on real-time Bitcoin price analysis. SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) library for Python that provides a full suite of well-known enterprise-level persistence patterns, designed for efficient and high-performing database access. Know the basics of SQLAlchemy, its ORM capabilities, and how it facilitates database interactions within Python applications.

**Describe technology**

- **SQLAlchemy Core**: Offers a schema-centric SQL abstraction layer and a full suite of enterprise-level persistence patterns.  
- **Object Relational Mapper (ORM)**: Allows the definition of classes mapped to database tables; relations can be established between classes and SQL queries can be built using these objects.  
- **Engine Interface**: Manages connections to the database, supporting multiple databases (e.g., SQLite, PostgreSQL, MySQL).  
- **Session Management**: Provides a factory for creating new sessions to interact with the database, supporting transaction management and workflow control.

**Describe the project**  
This project involves creating a real-time data processing system to ingest Bitcoin prices and conduct time series analysis:

- **Data Ingestion**: Use a public API such as CoinGecko or CryptoCompare to fetch real-time Bitcoin prices. This data will be ingested at regular intervals and stored using SQLAlchemy, providing ORM capabilities for easy data manipulation.  
- **Database Modeling**: Design database schema using SQLAlchemy ORM to handle time series data efficiently. This includes defining tables for storing the Bitcoin price data and any additional metadata required for analysis.  
- **Data Processing**: Implement a data processing routine to calculate key metrics over time, such as moving averages or price volatility, utilizing Python standard libraries.  
- **Visualization**: Use a library like Matplotlib or Seaborn to visualize the Bitcoin prices and derived metrics over time, showcasing SQLAlchemy's efficacy in handling real-time data.  
- **Analysis Demonstration**: Write Python scripts using SQLAlchemy to retrieve and process the data, demonstrating real-time analysis and visualization.

**Useful resources**

- [SQLAlchemy Official Documentation](https://docs.sqlalchemy.org/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Matplotlib Official Documentation](https://matplotlib.org/stable/users/index.html)  
- [Seaborn Documentation](https://seaborn.pydata.org/)

**Is it free?**  
Yes, SQLAlchemy is open-source and free to use. You might need an API key for certain usage levels with data providers like CoinGecko or CryptoCompare, though these often offer free tiers.

**Python libraries / bindings**

- **SQLAlchemy**: Use it for database interactions with ORM features. Install via `pip install sqlalchemy`.  
- **Requests**: Use it to fetch data from the Bitcoin price API. Install with `pip install requests`.  
- **Pandas**: Use it for data manipulation and processing. Install with `pip install pandas`.  
- **Matplotlib/Seaborn**: Use it for visualizing data insights. Install with `pip install matplotlib seaborn`.
