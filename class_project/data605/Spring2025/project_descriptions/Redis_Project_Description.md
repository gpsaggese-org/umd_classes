### **Redis**

**Title**: Real-time Bitcoin Price Analytics with Redis

**Difficulty**: 2 (medium)

**Description**  
Redis is an open-source, in-memory data structure store used as a database, cache, and message broker. It supports various data structures such as strings, lists, sets, and hashes and is known for its speed and efficiency in handling real-time data, making it a favored choice for developing scalable applications that require fast data access and processing. In this project, students will gain hands-on experience with Redis, focusing on its capabilities for ingesting and processing real-time Bitcoin price data.

**Describe technology**

- Redis is an in-memory data store that holds data in memory, allowing for rapid data access and manipulation.  
- Supports multiple data structures such as strings, lists, sets, sorted sets, and hashes.  
- Ideal for real-time analytics due to its low latency and high throughput.  
- Includes pub/sub messaging system for real-time event streaming.  
- Persistence options: Redis offers both snapshot storage (RDB) and append-only file (AOF) logs for data durability.  
- Supplementary features include data replication for high availability and clustering for scalability.

**Describe the project**  
This project involves setting up a Redis server to process real-time Bitcoin price data using a public API (e.g., CoinGecko). The project is divided into the following steps:

1. **Data Ingestion**:  
     
   - Use Python to develop a client that fetches real-time Bitcoin prices at regular intervals from the API.  
   - Utilize Redis commands to store data in appropriate data structures (e.g., lists or sorted sets) for efficient retrieval and analysis.

   

2. **Real-time Processing**:  
     
   - Implement Redis Pub/Sub to stream real-time updates to subscribed clients. This can be used for immediate data analysis and reporting.  
   - Perform basic processing like calculating moving averages or percent changes using Redis' in-memory computations.

   

3. **Time Series Analysis**:  
     
   - Use Redis for time-series data storage and processing, implementing basic time-series operations such as slicing and filtering to analyze price fluctuations.  
   - Extend the project with visual representations of the data using third-party Python libraries (like Matplotlib or Plotly) to visualize trends over time.

   

4. **Final Presentation**:  
     
   - Conclude the project with a presentation detailing your findings, the choices made during implementation, and potential real-world applications.

**Useful resources**

- [Redis Documentation](https://redis.io/documentation)  
- [Redis Python Client (redis-py) Documentation](https://pypi.org/project/redis/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, Redis is open-source and free to use. However, commercial support and hosted services offered by Redis Labs may incur costs.

**Python libraries / bindings**

- `redis`: Python client for interacting with Redis. Install using `pip install redis`.  
- `requests`: For making HTTP requests to fetch data from APIs. Install using `pip install requests`.  
- `Matplotlib` or `Plotly`: For data visualization purposes. Install using `pip install matplotlib` or `pip install plotly`.
