### **Boto3**

**Title**: Ingesting Bitcoin Prices Using Boto3

**Difficulty**: 1 (easy)

**Description**  
This project focuses on ingesting and processing real-time Bitcoin price data using Boto3, the AWS SDK for Python. Students will learn how to leverage AWS services to fetch, store, and process data using Boto3's functionalities. By the end of this project, students will have a foundational understanding of Boto3's capabilities and hands-on experience with building a simple data ingestion and processing pipeline.

**Describe technology**

- **Boto3**: Boto3 is the official AWS SDK for Python, enabling developers to interact programmatically with AWS services. It facilitates operations like creating and managing AWS resources, uploading and downloading data to/from S3, and tapping into AWS's computing power offered by services such as Lambda and EC2.  
- Boto3 provides a simple, user-friendly interface for interacting with AWS and is suitable for small tasks and automation scripts within Python.

**Describe the project**

- This project involves using Boto3 to:  
    
  - Fetch real-time Bitcoin price data from a public API, such as CoinGecko.  
  - Store the fetched data in an AWS S3 bucket for durability and easy access.  
  - Use basic Python packages, such as Pandas, to perform simple time series analysis on Bitcoin prices. Students will analyze price trends over given time intervals.


- **Steps**:  
    
  1. Set up your AWS account and configure your Python environment to use Boto3.  
  2. Write a Python script using Boto3 to periodically fetch Bitcoin price data and upload it to an S3 bucket.  
  3. Implement a script to fetch the stored data from S3 and use Pandas to perform basic time series analysis, such as calculating moving averages or identifying price spikes.  
  4. Write a report summarizing your findings and discuss any patterns or insights derived from the data.

**Useful resources**

- Boto3 Documentation: [https://boto3.amazonaws.com/v1/documentation/api/latest/index.html](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  
- AWS S3 Documentation: [https://docs.aws.amazon.com/s3/index.html](https://docs.aws.amazon.com/s3/index.html)  
- CoinGecko API Documentation: [https://www.coingecko.com/en/api](https://www.coingecko.com/en/api)  
- Pandas Documentation: [https://pandas.pydata.org/pandas-docs/stable/](https://pandas.pydata.org/pandas-docs/stable/)

**Is it free?**

- To complete this project, you will need an AWS account. AWS offers a free tier for S3, but usage beyond the free limits may incur costs.

**Python libraries / bindings**

- **Boto3**: For interacting with AWS S3, available via `pip install boto3`.  
- **Pandas**: For data manipulation and time series analysis, available via `pip install pandas`.
