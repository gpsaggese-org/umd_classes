### **Amazon QuickSight**

**Title**: Real-time Bitcoin Analytics with Amazon QuickSight

**Difficulty**: 1 (easy)

**Description** Amazon QuickSight is a business analytics service that enables you to deliver insights to everyone in your organization. As a fast, cloud-powered BI service, it allows you to easily create and publish interactive dashboards that include machine learning insights. This project involves using Amazon QuickSight to visualize real-time Bitcoin price data.

**Describe Technology**

- **Overview**: Amazon QuickSight is a scalable, serverless BI service that integrates with other AWS services to offer interactive data visualization and insights. It features an easy-to-use interface and various visualization options, such as line graphs, pie charts, and geographical maps.  
- **Data Integration and Preparation**: Users can connect QuickSight to a variety of data sources, including AWS Data Lakes, S3, Athena, and RDS. QuickSight offers capabilities for data transformation and preparation through features like SPICE (Super-fast, Parallel In-memory Calculation Engine) for faster analytics performance.  
- **Analytics and Visualization**: QuickSight supports machine learning insights, anomaly detection, and forecasts within its visualizations, helping users derive deeper insights directly from their data.

**Describe the Project**

- **Objective**: Create a real-time analytics dashboard to visualize Bitcoin price data using Amazon QuickSight.  
- **Data Source**: Fetch real-time Bitcoin price data from a public API, such as CoinGecko.  
- **Data Storage**: Store the gathered data in an AWS S3 Bucket, which will serve as the data source for QuickSight.  
- **Data Visualization**: Use Amazon QuickSight to connect to the S3 bucket, and set up data visualizations like time series line charts to display price changes over time.  
- **Analysis and Insights**: Leverage QuickSight’s built-in analytics capabilities to add anomaly detection and forecast the future price of Bitcoin based on historical data. This allows for deeper insights and an interactive experience.  
- **Expected Outcomes**: A functioning QuickSight dashboard that automatically updates with real-time data and displays meaningful insights and trends regarding Bitcoin prices over time.

**Useful Resources**

- [Amazon QuickSight Documentation](https://docs.aws.amazon.com/quicksight/index.html)  
- [QuickSight Learning Path](https://aws.amazon.com/training/path-analytics/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api/documentation)

**Is it Free?** Amazon QuickSight offers a free trial, but there are costs associated with its continued use after the trial period. Additional AWS costs may apply for S3 storage and other services used.

**Python Libraries / Bindings**

- **Boto3**: To interact with AWS services and manage S3 for data storage.  
  - Install using `pip install boto3`.  
  - [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  
- **Requests**: For fetching data from APIs, such as CoinGecko.  
  - Install using `pip install requests`.
