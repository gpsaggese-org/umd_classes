### **Google Cloud Platform**

**Title**: Scalable Bitcoin Data Pipeline on Google Cloud Platform

**Difficulty**

- **Level:** 3 

**Description**

- **Technology Overview:**  
  Google Cloud Platform (GCP) offers cloud services for storage, compute, machine learning, and data analytics, including Google Pub/Sub, BigQuery, AI Platform, and Data Studio. This project leverages GCP for a scalable Bitcoin data pipeline.  
    
- **Project Details:**  
  This project involves:  
    
  - Using Google Pub/Sub to ingest real-time Bitcoin data (prices, transactions, social media sentiment).  
  - Storing and processing data in Google BigQuery for historical analysis and real-time queries.  
  - Implementing time series analysis (e.g., price forecasting) using Google AI Platform or BigQuery ML.  
  - Detecting anomalies in transaction data with machine learning models.  
  - Visualizing results in Google Data Studio with real-time dashboards.  
  - Ensuring scalability and cost-effectiveness using GCP’s managed services.


  The complexity lies in integrating multiple GCP services, handling large-scale data, and optimizing for performance and cost.

**Useful Resources**

- [Google Cloud Documentation](https://cloud.google.com/docs)  
- [Google Pub/Sub](https://cloud.google.com/pubsub/docs)  
- [Google BigQuery](https://cloud.google.com/bigquery/docs)  
- [Google AI Platform](https://cloud.google.com/ai-platform/docs)  
- [Google Data Studio](https://datastudio.google.com/)

**Is it Free?**

- **GCP:** Free tier with limited resources; additional usage incurs costs.

**Python Libraries**

- `google-cloud-pubsub`: `pip install google-cloud-pubsub`  
- `google-cloud-bigquery`: `pip install google-cloud-bigquery`  
- `google-cloud-aiplatform`: `pip install google-cloud-aiplatform`  
- `pandas`: `pip install pandas`  
- `matplotlib`: `pip install matplotlib` (local plotting if needed)
