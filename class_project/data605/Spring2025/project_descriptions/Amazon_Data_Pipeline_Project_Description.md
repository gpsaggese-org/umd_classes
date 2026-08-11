### **Amazon Data Pipeline**

**Title**: Real-Time Bitcoin Data Processing with Amazon Data Pipeline

**Difficulty**: Medium

**Description**  
Amazon Data Pipeline is a web service that assists in automating the movement and transformation of data. With its easy-to-use interface, you can define a data processing workflow or pipeline that involves multiple stages, handling tasks like scheduling, dependency tracking, retry policies, and more. For data scientists and engineers, it provides the tools necessary to create data-driven workflows at scale.

**Describe technology**

- **Purpose and Functionality**: Amazon Data Pipeline is used to manage the flow of data between compute and storage services inside and outside of AWS. It orchestrates and automates the data-driven workflows and handles complex scheduling and dependency management.  
- **Key Components**:  
  - **Pipeline Definition**: The JSON specification to define the inputs, outputs, and activity logic.  
  - **Tasks**: Units of work performed during execution.  
  - **Schedules and Preconditions**: Define timing and dependencies for task execution.  
  - **Resources**: AWS resources like EC2 instances or S3 buckets involved in the pipeline.

**Describe the project**  
In this project, students will build a data pipeline to ingest real-time Bitcoin price data, process it to perform basic time series analysis, and store the results for further analysis.

- **Steps**:  
  - **Data Ingestion**: Use Amazon Data Pipeline to fetch Bitcoin prices from a public API, such as CoinGecko, at regular intervals.  
  - **Data Storage**: Store the ingested data in an AWS S3 bucket as a CSV or JSON file for easy access.  
  - **Data Processing**: Write a Python script using basic libraries such as Pandas and NumPy to perform time series analysis. This can involve calculating moving averages or identifying price trends over specific periods.  
  - **Data Transformation**: Use Amazon Data Pipeline to run the Python script on an EC2 instance, process the data, and store the results back in S3.  
  - **Schedule and Automate**: Set up the pipeline to run the data collection and processing activities on a regular schedule.

**Useful resources**

- [Amazon Data Pipeline Documentation](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/what-is-datapipeline.html)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/what-is-s3.html)  
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)  
- [NumPy Documentation](https://numpy.org/doc/)

**Is it free?**  
Amazon Data Pipeline is a managed service. While AWS offers a free tier that includes limited access to many of its services, usage of Data Pipeline incurs costs after the free-tier limits. Always check the latest pricing on the AWS Pricing page.

**Python libraries / bindings**

- **boto3**: The AWS SDK for Python, used to interact with AWS services programmatically, including managing the data pipeline. Install using `pip install boto3`.  
- **Pandas**: A library providing data manipulation and analysis tools for Python. Used here for time series analysis. Install using `pip install pandas`.  
- **NumPy**: A package for scientific computing with Python, helpful for performing mathematical functions used in time series analysis. Install using `pip install numpy`.
