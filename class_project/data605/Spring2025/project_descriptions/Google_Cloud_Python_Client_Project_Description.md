### **Google Cloud Python Client**

**Title**: Ingest bitcoin prices using Google Cloud Python Client

**Difficulty**: 1 (easy)

**Description**  
In this project, students will explore the Google Cloud Python Client, a library designed to simplify interactions with Google Cloud Services. This project aims to provide hands-on experience in ingesting and processing real-time Bitcoin price data using Google Cloud Pub/Sub and Google Cloud Functions. The project is suitable for students with basic Python skills and an interest in cloud-based data processing solutions.

**Describe technology**  
The Google Cloud Python Client is a set of Python libraries that provide access to Google Cloud Services in a simple and efficient manner. For this project, the primary focus will be on Google Cloud Pub/Sub for real-time data ingestion and Google Cloud Functions for creating serverless functions to process data. Pub/Sub is a messaging service that allows for asynchronous data streaming, while Cloud Functions offers a lightweight, event-driven compute solution.

**Describe the project**  
The project involves:

- Setting up a Pub/Sub topic in Google Cloud to receive Bitcoin price data from a public API (e.g., CoinGecko).  
- Creating a Python-based Cloud Function to subscribe to the Pub/Sub topic, process incoming messages, and perform simple transformations, such as filtering data by time intervals or converting prices into different currencies.  
- Storing the processed data in Google Cloud Storage for subsequent analysis and time series visualization.  
- Optionally, students can use basic Python visualization libraries (e.g., Matplotlib) to create time series charts of Bitcoin price trends over time.

This straightforward project will be completed in about one week and provides practical exposure to Google Cloud services and real-time data processing workflows.

**Useful resources**

- [Google Cloud Python Client Documentation](https://googleapis.dev/python/google-api-core/latest/index.html)  
- [Getting Started with Google Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/quickstarts)  
- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)

**Is it free?**  
Google Cloud offers a free tier with limited usage, including Pub/Sub and Cloud Functions. Students can use this for the project, but they should be aware of usage limits to avoid incurring charges.

**Python libraries / bindings**

- `google-cloud-pubsub`: This library is essential for interacting with Pub/Sub topics and subscriptions. Install it using `pip install google-cloud-pubsub`.  
- `google-cloud-functions`: Though Cloud Functions are managed on GCP, students will write their serverless functions in Python. Understanding this service will be key to integrating the solution.  
- Basic Python packages such as `requests` for fetching data from APIs and `matplotlib` for data visualization.
