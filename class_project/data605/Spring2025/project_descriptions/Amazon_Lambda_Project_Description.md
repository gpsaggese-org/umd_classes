### **Amazon Lambda**

Title: Real-Time Bitcoin Price Processing with Amazon Lambda

**Difficulty**: Difficult

**Description**

Amazon Lambda, commonly referred to as AWS Lambda, is a serverless computing service that allows you to run code without provisioning or managing servers. It automatically scales your applications by executing code in response to triggers from various AWS services or direct invocations. This project focuses on utilizing AWS Lambda to ingest and process real-time Bitcoin price data for time series analysis.

**Describe Technology**

- **Serverless Computing**: AWS Lambda handles all of the capacity scaling, patching, and general infrastructure maintenance, allowing developers to focus solely on code features.  
- **Event-driven Architecture**: AWS Lambda can be triggered by a variety of event sources, such as changes in a data stream, messages on a queue, or API requests.  
- **Pay-as-you-use Pricing**: With Lambda, costs are incurred based only on the number of requests and the execution time utilized.  
- **Flexible Runtime Support**: Write your lambda functions in several languages, including Python, Java, Go, and more.  
- **Integrations with AWS Services**: Lambda can natively interact with multiple other AWS services, such as S3 for storage, DynamoDB for databases, and Kinesis for real-time data streams.

**Describe the Project**

- **Objective**: Implement a real-time data ingestion and processing system to analyze Bitcoin price fluctuations using AWS Lambda.  
- **Data Source**: Use the WebSocket API from cryptocurrency exchange platforms such as Coinbase Pro or Binance to receive real-time Bitcoin price data.  
- **System Architecture**:  
  - **Data Ingestion**: Develop a Lambda function triggered by a scheduled Amazon EventBridge rule to initiate a WebSocket connection.  
  - **Data Processing**: Another Lambda function will process incoming Bitcoin price data in near real-time. This function will extract, filter, and transform the data to derive meaningful insights, such as percentage price changes over predefined time intervals.  
  - **Data Storage**: Persist transformed data in Amazon S3 in a time-series-optimized format (e.g., Parquet/JSON) for further analysis.  
  - **Time Series Analysis**: Perform basic statistical computations or visualizations directly within AWS Lambda or using additionally integrated services like AWS QuickSight.  
- **Outcome**: A functioning distributed system utilizing AWS Lambda to inform users of significant Bitcoin price trends promptly.

**Useful Resources**

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)  
- [Amazon EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/what-is-amazon-eventbridge.html)  
- [Amazon S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)  
- [AWS QuickSight Documentation](https://docs.aws.amazon.com/quicksight/latest/userguide/welcome.html)

**Is it Free?**

AWS Lambda provides a generous free tier that includes 1 million free requests and 400,000 GB-seconds of compute time per month. However, beyond these limits, charges will apply. AWS S3 and other integrated AWS services may also incur costs beyond their free tiers.

**Python Libraries / Bindings**

- **boto3**: The AWS SDK for Python, allowing interaction with AWS services including Lambda, S3, and EventBridge services.  
    
  - Installation: `pip install boto3`  
  - Documentation: [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)


- **Websockets**: Used for establishing WebSocket connections to receive live Bitcoin pricing data.  
    
  - Installation: `pip install websockets`  
  - Documentation: [Websockets Documentation](https://websockets.readthedocs.io/en/stable/)


- **Pandas**: For data manipulation and analysis, specifically useful for handling time series data.  
    
  - Installation: `pip install pandas`  
  - Documentation: [Pandas Documentation](https://pandas.pydata.org/docs/)


- **NumPy**: Provides support for large multi-dimensional arrays and matrices, and a collection of mathematical functions to operate on these arrays.  
    
  - Installation: `pip install numpy`  
  - Documentation: [NumPy Documentation](https://numpy.org/doc/stable/)
