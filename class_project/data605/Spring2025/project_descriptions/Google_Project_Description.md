### **Google**

**Title**: Real-time Bitcoin Price Analysis using Google Cloud Functions  
**Difficulty**: 1 (easy)

**Description**:  
Google Cloud Functions is a serverless execution environment for building and connecting cloud services. With Cloud Functions, you can write simple, single-purpose functions that are attached to events emitted from your cloud infrastructure and services. By using Google Cloud Functions, you can efficiently process real-time Bitcoin price data, responding quickly to updates, without the need to manage server infrastructure.

**Describe technology**:

- **Google Cloud Functions**: Allows you to run your code in response to events without provisioning servers. Functions can be triggered by HTTP requests, Cloud Pub/Sub messages, and other Google Cloud services.  
- **Core Concepts**:  
  - **Event-driven**: Functions execute in response to triggers from supported Google Cloud services.  
  - **Auto-scaling**: Automatically scales based on the load.  
  - **Pay-per-use**: Charges based on actual usage – only pay for the time your code runs.

**Describe the project**:  
This project involves creating a simple real-time data ingestion and processing system using Google Cloud Functions to analyze Bitcoin price data.

1. **Objective**: Implement a serverless solution to ingest real-time Bitcoin prices from a public API, such as CoinAPI or CoinGecko.  
2. **Steps**:  
   - **Set Up Cloud Function**: Create a Google Cloud Function that is triggered by an HTTP request to fetch Bitcoin prices continuously.  
   - **Data Processing**: Process the incoming data to extract necessary information, such as current price, timestamp, and compare it to previous data points to find trends.  
   - **Storage**: Use Cloud Firestore or Cloud Storage to store the ingested and processed data for future analysis.  
   - **Time Series Analysis**: Perform basic time series analysis, such as calculating moving averages or identifying price spikes.  
3. **Outcome**: Gain hands-on experience in setting up real-time data processing systems using serverless architecture, understand the basics of time series analysis, and familiarize with Google Cloud Platform.

**Useful resources**:

- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Understanding Time Series Analysis](https://towardsdatascience.com/an-introduction-to-time-series-analysis-1197a97a4f85)

**Is it free?**:  
Google Cloud Functions offers a free tier, which should be sufficient for small-scale applications like this project. However, some usage may incur charges if the free-tier limits are exceeded.

**Python libraries / bindings**:

- **Requests**: To send HTTP requests and fetch data from the Bitcoin price API. Install it using `pip install requests`.  
- **google-cloud-functions**: While not a separate package, your function will be deployed and managed via the Google Cloud console or SDK.  
- **pandas**: For processing and analyzing time series data. Install using `pip install pandas`.  
- **Firestore or Google Cloud Storage client library**: For storing the data. Install using `pip install google-cloud-firestore` or `pip install google-cloud-storage` depending on the chosen storage solution.
