### **Amazon Aurora**

**Title**: Analyzing Bitcoin Trends with Amazon Aurora

**Difficulty**: Easy

**Description**  
Amazon Aurora is a fully managed relational database engine provided by Amazon Web Services (AWS), compatible with both MySQL and PostgreSQL databases. It combines the speed and availability of high-end commercial databases with the simplicity and cost-effectiveness of open-source databases. This project involves using Amazon Aurora to store, manage, and analyze Bitcoin price data as part of a real-time data system. The project will provide hands-on experience in setting up a database in Amazon Aurora, ingesting Bitcoin data, and performing basic time series analysis in Python.

**Describe technology**

- Amazon Aurora is designed for mission-critical workloads and delivers an enhanced performance and availability.  
- Offers built-in automation for high availability with recovery features and up to 15 low-latency read replicas.  
- Provides self-healing storage, which automatically scales up to 128 terabytes per database instance.  
- Easily integrates with other AWS services like Lambda, S3, and more for seamless data processing and analysis.

**Describe the project**

- Students will begin by setting up an Amazon Aurora database instance with MySQL compatibility.  
- Using the Python `requests` package, students will write a simple script to fetch real-time Bitcoin price data from an API like CoinGecko.  
- The script will then insert the fetched data into a table within the Amazon Aurora database.  
- Perform time series analysis by querying this data, such as calculating the average daily price and identifying trends over specific periods.  
- Visualization of the data trends can be achieved using Python libraries like Matplotlib or Seaborn.

**Useful resources**

- [Amazon Aurora Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Welcome.html)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [AWS Python Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

**Is it free?**  
You need to create an AWS account. Amazon Aurora offers a free tier, which includes 750 hours of usage per month for a limited time, enabling students to explore Aurora without incurring costs, within certain limitations.

**Python libraries / bindings**

- **Boto3**: The official Amazon Web Services (AWS) SDK for Python, which will be used to interact with and manage your Amazon Aurora instance. You can install it using `pip install boto3`.  
- **MySQL Connector/Python**: For connecting to the Aurora MySQL database. Install it using `pip install mysql-connector-python`.  
- **Requests**: A simple HTTP library in Python to fetch data from APIs (e.g., CoinGecko) with `pip install requests`.  
- **Matplotlib/Seaborn**: For visualization purposes. They can be installed using `pip install matplotlib seaborn`.
