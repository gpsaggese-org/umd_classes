### **Celery**

**Title**: Real-Time Bitcoin Data Processing with Celery

**Difficulty**: Medium

**Description**  
Celery is an open-source distributed task queue library for Python. It is designed to handle asynchronous tasks and process them in the background. Celery is particularly useful for scheduling and executing tasks in a distributed manner, thus facilitating real-time data processing in Python applications. This project employs Celery to ingest and process real-time Bitcoin price data to perform time series analysis.

**Describe technology**

- Celery allows developers to define tasks that can be executed asynchronously. These tasks can be processed in parallel across multiple worker servers, making it highly scalable.  
- A key feature of Celery is task scheduling, which allows recurring tasks to be automatically executed at specified intervals.  
- Celery requires a message broker (such as RabbitMQ or Redis) to send and receive task messages, which facilitates communication between producers (task issuers) and consumers (workers executing tasks).

**Describe the project**

- The goal of this project is to develop a pipeline that periodically fetches Bitcoin price data from a public API (e.g., CoinDesk or CoinGecko) using Celery.  
- Set up a Celery task to retrieve Bitcoin price data every minute and schedule it to run continuously.  
- Implement a task pipeline where the fetched data is pre-processed, such as cleaning or converting to a different format, and stored in a time-series database (like InfluxDB).  
- Analyze the processed time series data to identify trends, calculate moving averages, and detect anomalies in Bitcoin prices over time.  
- The project will be implemented using basic Python packages for tasks that extend beyond Celery, such as APIs requests or data analysis.

**Useful resources**

- [Celery Documentation](https://docs.celeryproject.org/en/stable/)  
- [CoinDesk Bitcoin Price Index API](https://www.coindesk.com/coindesk-api)  
- [CoinGecko API Documentation](https://coingecko.com/en/api)  
- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/v2.0/)

**Is it free?**  
Yes, Celery is an open-source project released under the BSD License. Using public APIs from data providers like CoinDesk or CoinGecko is typically free but may have usage limitations or require email registration for an API key.

**Python libraries / bindings**

- **Celery**: Install with `pip install celery` to set up the asynchronous task queue.  
- **requests**: For making HTTP requests to fetch Bitcoin prices (install via `pip install requests`).  
- **pandas**: For time series data manipulation and analysis (install via `pip install pandas`).  
- **InfluxDB Client**: Python client to interact with an InfluxDB time-series database (install via `pip install influxdb`).  
- **Message Broker**: Choose between Redis (install via `pip install redis`) or RabbitMQ (requires separate installation) as a message broker to facilitate task management.
