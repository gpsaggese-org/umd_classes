### **Snowflake**

**Title**: Real-time Bitcoin Data Analysis with Snowflake

**Difficulty**: 2 (medium)

**Description**:  
This project explores using Snowflake, a cloud-based data warehousing service, to ingest, process, and analyze real-time Bitcoin price data. Snowflake's scalable architecture and robust SQL capabilities make it an excellent choice for handling big data and performing complex queries. The project will introduce students to Snowflake's core functionalities, including its data loading mechanisms, seamless integration with cloud storage, and advanced querying features. This will be paired with Python packages for auxiliary data processing tasks.

**Describe technology**:

- **Snowflake**: A cloud data platform that offers data warehousing, SQL analytics, and data integration services. Its key features include an architecture that separates storage and compute for scalability, support for structured and semi-structured data, and extensive data sharing capabilities.  
- **Core Concepts**:  
  - Warehouses: Resources for computation that allow for flexibility in scaling.  
  - Databases and Schemas: Organizational units for storing data.  
  - Tables and Views: Structures for managing data access and queries.  
  - Snowpipe: A continuous data ingestion service for loading data in near real-time.

**Describe the project**:

- **Objective**: Implement a system using Snowflake to ingest, store, and perform time-series analysis on Bitcoin price data.  
- **Steps**:  
  1. **Data Ingestion**:  
     - Use the Snowpipe service to set up a continuous ingestion pipeline.  
     - Pull Bitcoin price data from a public API, such as CoinGecko.  
     - Store the JSON data in cloud storage (e.g., AWS S3, Google Cloud Storage).  
  2. **Data Processing**:  
     - Load the data into Snowflake tables for further analysis.  
     - Transform raw data into a structured table format using SQL operations within Snowflake.  
  3. **Time-Series Analysis**:  
     - Use Snowflake's SQL capabilities to perform basic time-series analyses, such as moving averages and trendline computations.  
  4. **Visualization**:  
     - Export processed data to a Python environment for visualization using libraries like Matplotlib or Seaborn.  
- **Outcome**: Students will gain experience in setting up a real-time data pipeline and applying time-series analysis using Snowflake and Python.

**Useful resources**:

- Snowflake Documentation: [docs.snowflake.com](https://docs.snowflake.com)  
- CoinGecko API Documentation: [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- Python Matplotlib Documentation: [matplotlib.org](https://matplotlib.org)  
- Python Seaborn Documentation: [seaborn.pydata.org](https://seaborn.pydata.org)

**Is it free?**:  
Snowflake offers a free trial with credits that can be used to explore its services, but students will need to be careful to manage resources to avoid any additional charges. Access to cloud storage may also incur additional costs.

**Python libraries / bindings**:

- **snowflake-connector-python**: Python connector to perform standard database operations in Snowflake. Install with `pip install snowflake-connector-python`.  
- **requests**: Library for making HTTP requests to retrieve Bitcoin price data from APIs. Install with `pip install requests`.  
- **matplotlib**: Used for creating static, animated, and interactive visualizations in Python. Install with `pip install matplotlib`.  
- **pandas**: A library for data manipulation and analysis, ideal for preprocessing and cleaning data. Install with `pip install pandas`.

Through this project, students will have the opportunity to integrate cloud-based data warehousing with real-time data ingestion and gain hands-on experience with Snowflake's advanced capabilities for data analysis.
