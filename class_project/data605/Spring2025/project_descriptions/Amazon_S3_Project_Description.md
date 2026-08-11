### **Amazon S3**

**Title**: Analyzing Real-Time Bitcoin Prices with Amazon S3

**Difficulty**: 1 (easy)

**Description**  
Amazon S3 (Simple Storage Service) is a scalable, high-speed web-based cloud storage service designed for online data and backup archiving. It is part of Amazon Web Services (AWS) and provides object storage through a web service interface. The fundamental purpose of Amazon S3 is to provide storage infrastructure on a pay-as-you-go basis, offering reliability, fast data access, and secure solutions for a wide variety of applications, including big data analytics. This project introduces students to the basic functionalities of Amazon S3, focusing on data storage, retrieval, and management through Python, with an emphasis on real-time Bitcoin data ingestion and analysis.

**Describe Technology**

- **Amazon S3 Features**:  
    
  - Secure, durable, and scalable storage solution allowing organizations to store and retrieve any volume of data anytime from anywhere.  
  - Uses REST API for easy data access and integration with other AWS services.  
  - Capable of handling large-scale data analytics tasks by integrating seamlessly with AWS services like AWS Lambda, AWS Glue, or Amazon EMR.  
  - Supports various data import methods including direct data transfers, AWS DataSync, and managed file transfers for large datasets.


- **Example Use Cases**:  
    
  - Data backup and archival  
  - Data lakes for big data analytics  
  - Static website hosting  
  - Media storage and distribution

**Describe the Project**

In this project, students will utilize Amazon S3 to implement a simple data pipeline for ingesting and analyzing real-time Bitcoin prices:

- **Objective**: Ingest real-time Bitcoin price data from a public API and store the data efficiently in Amazon S3 for future analysis.  
- **Steps**:  
  1. **Set Up Amazon S3**: Create an Amazon S3 bucket to store Bitcoin price data.  
  2. **Ingest Data**: Write a Python script to call a Bitcoin API (e.g., CoinGecko) and capture real-time price data periodically using a simple scheduling approach like time.sleep().  
  3. **Store Data**: Save the ingested data into a CSV file format and upload it to the S3 bucket. Students will use the Boto3 library to interact with S3 for uploading and accessing files.  
  4. **Analyze Data**: Implement a basic time series analysis in Python using libraries such as pandas to process the data retrieved from S3, focusing on trends or moving averages of the Bitcoin prices over time.  
  5. **Visualization**: Create basic plots to visualize the price changes using Python’s matplotlib or seaborn libraries.

**Useful Resources**

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)  
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

**Is it free?**

To use Amazon S3, you need to create an AWS account. Amazon S3 offers a free tier, which includes 5 GB of standard storage space, but it's limited to the first year of service and certain data transfer limits.

**Python Libraries / Bindings**

- **Boto3**: The AWS SDK for Python. It allows you to interact with Amazon S3 programmatically. Install it via `pip install boto3`.  
- **Pandas**: A powerful Python library for data manipulation, especially useful for time series data analysis. Install it via `pip install pandas`.  
- **Matplotlib/Seaborn**: Libraries for data visualization in Python. Matplotlib can be installed via `pip install matplotlib` and Seaborn via `pip install seaborn`.
