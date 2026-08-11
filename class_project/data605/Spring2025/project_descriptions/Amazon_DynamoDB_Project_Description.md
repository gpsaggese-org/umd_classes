### **Amazon DynamoDB**

**Title**: Real-Time Bitcoin Data Processing with Amazon DynamoDB  
**Difficulty**: 

**Description**  
Amazon DynamoDB is a fully managed NoSQL database service provided by Amazon Web Services (AWS). It's designed to provide consistent, single-digit millisecond latency at any scale, making it well-suited for applications requiring a reliable, fast, and scalable database. In this project, students will leverage Amazon DynamoDB to ingest, store, and analyze real-time Bitcoin price data. This medium-difficulty project will take approximately ten days to complete, offering students hands-on experience with setting up a DynamoDB table, ingesting data using a real-time streaming service, and performing basic time series analysis on the data.

**Describe technology**

- **NoSQL Database**: Amazon DynamoDB is a key-value and document database optimized for speed and scalability.  
- **Managed Service**: No need for provisioning, patching, or operating hardware. Offers automatic scaling and built-in security.  
- **Streams**: DynamoDB Streams provide an ordered flow of changes to the table, enabling real-time data replication and event-driven processing.  
- **Integrations**: Easily integrate with AWS Lambda for serverless compute possibilities or Amazon Kinesis for streaming analytics.

**Describe the project**

- **Objective**: Create a real-time data ingestion system for Bitcoin price tracking, storing the data in DynamoDB, and performing initial time series analysis.  
- **Setup DynamoDB Table**: Create a DynamoDB table designed to hold Bitcoin price data, structured with a primary key of timestamp and additional attributes for price and metadata.  
- **Data Ingestion**: Utilize a Python script to fetch Bitcoin price data from a public API, such as CoinGecko, and insert this data into the DynamoDB table in real-time.  
- **Real-time Processing**: Implement DynamoDB Streams to detect and analyze changes in the stored data; use AWS Lambda to trigger instant computations, such as calculating moving averages or detecting price anomalies.  
- **Time Series Analysis**: Using data stored in DynamoDB, perform a basic time series analysis such as identifying trends or creating visualizations that help understand price movements over time.  
- **Final Output**: Compile insights into a report or presentation that showcases data processing steps, findings from time series analysis, and suggestions for further exploration.

**Useful resources**

- [Amazon DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/index.html)  
- [DynamoDB Streams Overview](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)  
- [AWS Lambda FAQs](https://aws.amazon.com/lambda/faqs/)  
- [Python Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

**Is it free?**  
You need to create an AWS account. DynamoDB offers a free tier that includes 25 GB of storage and enough read/write capacity for small to medium workloads. However, exceeding this tier or using additional services will incur charges.

**Python libraries / bindings**

- **boto3**: The official AWS SDK for Python. Install it via `pip install boto3`. Use boto3 to interact with DynamoDB and manage database operations programmatically.  
- **AWS Lambda with Python**: For writing serverless functions to process real-time data events. AWS provides guidance and support for setting up Lambda functions in Python.  
- **Requests**: A simple HTTP library for Python, used to fetch real-time Bitcoin data from public APIs. Install it via `pip install requests`.
