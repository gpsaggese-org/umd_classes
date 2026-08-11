### **Pika**

**Title**: Real-Time Bitcoin Data Ingestion with Pika

**Difficulty**: 1 (easy)

**Description**:  
Pika is a robust Python client library for interacting with RabbitMQ, a widely-used message broker that facilitates efficient message queuing and handling across distributed systems. Pika provides a straightforward, user-friendly interface to connect, publish, and consume messages within RabbitMQ, making it an excellent tool for implementing real-time data ingestion and processing systems. In this project, students will explore Pika's basic functionalities, leading to the development of a time series analysis on Bitcoin price data.

**Describe technology**:

- **Core Concept**: Pika is a pure Python implementation for connecting with RabbitMQ, which supports advanced message queuing protocol (AMQP).  
- **Basic Operations**: Students will learn how to establish a channel, declare a queue, and perform basic publishing and consuming of messages.  
- **Use Cases**: Primarily used in applications that require asynchronous message processing, load balancing, and implementing task queues.  
- **Example**: Students will explore a Pika-based example to publish and consume simple text messages using a RabbitMQ instance.

**Describe the project**:

- **Objective**: Develop a basic real-time data ingestion system using Pika to handle Bitcoin price data.  
- **Step 1**: Set up RabbitMQ locally or use a cloud-based RabbitMQ service.  
- **Step 2**: Create a producer script in Python using Pika to fetch Bitcoin price data from a public API such as CoinGecko and publish it to a RabbitMQ queue at regular intervals.  
- **Step 3**: Develop a consumer script that retrieves data from the queue and stores it in a local database using a simple Python database library like SQLite.  
- **Step 4**: Implement basic time series analysis, such as time plotting or moving average calculations, with the ingested data using libraries like Matplotlib and NumPy.  
- **Learning Outcome**: Understand the foundations of working with message brokers and real-time data systems, and gain practical experience in processing financial data.

**Useful resources**:

- [Pika GitHub Repository](https://github.com/pika/pika)  
- [RabbitMQ Official Website](https://www.rabbitmq.com/)  
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, Pika is an open-source library, and RabbitMQ is available as open-source software. A local RabbitMQ setup can be done for free, while a cloud-based RabbitMQ service may involve costs depending on the provider.

**Python libraries / bindings**:

- **Pika**: Python client library for RabbitMQ, used for establishing connection and message queue handling. Install using `pip install pika`.  
- **SQLite**: Python built-in library for lightweight database management.  
- **Matplotlib**: Visualization library for plotting time series data, installable via `pip install matplotlib`.  
- **NumPy**: Essential library for numerical computations, installable via `pip install numpy`.
