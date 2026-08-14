### **Amazon RDS**

**Title**: Real-Time Bitcoin Data Processing using Amazon RDS

**Difficulty**: Medium

**Description**: Amazon RDS (Relational Database Service) is a managed SQL database service provided by Amazon Web Services. It facilitates setting up, operating, and scaling a relational database in the cloud. RDS offers support for several database engines, including MySQL, PostgreSQL, Oracle, Microsoft SQL Server, and Amazon Aurora, making it versatile for a variety of applications. In this project, students will utilize Amazon RDS to store and process real-time Bitcoin price data. The focus will be on understanding how RDS works, setting up a database instance, creating tables, and implementing a Python-based solution to ingest and analyze Bitcoin data.

**Describe technology**:

- **Amazon RDS Features**:  
    
  - Fully managed database service with automated backups, software patching, and hardware provisioning.  
  - Supports a variety of database engines.  
  - Offers scalability with the ability to adjust compute and storage capacity.  
  - Provides built-in security features, including encryption at rest and in transit.  
  - Allows for monitoring and managing database operations using AWS Management Console and AWS CLI.


- **Core Concepts**:  
    
  - **Database Instance**: The primary database environment consisting of resources needed to run a database.  
  - **Security Groups**: Controls access to the database instance.  
  - **Parameter Groups**: Allows customization of database parameters.

**Describe the project**:

- **Objective**: To ingest, store, and analyze real-time Bitcoin prices using Amazon RDS, with a focus on time series analysis.  
    
- **Steps**:  
    
  1. **Set Up an Amazon RDS Instance**:  
       
     - Create an RDS instance with a supported database engine like PostgreSQL or MySQL.  
     - Configure security and parameter groups for optimal access and performance.

     

  2. **Database Design**:  
       
     - Design schema for storing real-time Bitcoin price data.  
     - Implement tables to store raw data, processed data, and results of time series analysis.

     

  3. **Data Ingestion**:  
       
     - Utilize Python to fetch data from a Bitcoin price API (e.g., CoinGecko).  
     - Write scripts to insert real-time data into the RDS instance using Python's database connectivity libraries.

     

  4. **Time Series Analysis**:  
       
     - Implement basic time series analysis methods using Python packages such as Pandas and NumPy.  
     - Analyze trends and patterns in Bitcoin price changes over time.

     

  5. **Visualize Results**:  
       
     - Use Matplotlib or similar libraries to visualize the results of the time series analysis.  
     - Create informative charts that illustrate data trends and insights.

**Useful resources**:

- [Amazon RDS Documentation](https://aws.amazon.com/documentation/rds/)  
- [AWS Python SDK (Boto3) Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [CoinGecko API](https://www.coingecko.com/en/api)

**Is it free?**: Amazon RDS offers a free tier that allows you to run a single database instance for free, with some limitations. However, additional usage beyond the free tier may incur costs.

**Python libraries / bindings**:

- **Boto3**: The official AWS SDK for Python, used for interfacing with AWS services, including Amazon RDS (install via `pip install boto3`).  
- **psycopg2** or **PyMySQL**: Libraries for connecting to PostgreSQL or MySQL databases from Python (install via `pip install psycopg2-binary` or `pip install pymysql`).  
- **Pandas**: A powerful data manipulation and analysis library that supports time series analysis (install via `pip install pandas`).  
- **Matplotlib**: A plotting library for creating static, interactive, and animated visualizations in Python (install via `pip install matplotlib`).
