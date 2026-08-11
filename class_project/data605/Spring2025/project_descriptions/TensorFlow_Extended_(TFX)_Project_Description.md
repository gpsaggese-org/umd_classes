### **TensorFlow Extended (TFX)**

**Title**: Real-Time Bitcoin Data Processing using TensorFlow Extended (TFX)

**Difficulty**: 2 (medium difficulty, should take around 10 days to complete)

**Description**  
TensorFlow Extended (TFX) is an end-to-end platform for deploying production machine learning (ML) pipelines. It provides a cohesive set of tools that enable the integration and management of various ML components, facilitating seamless data ingestion, validation, transformation, and model training/serving. TFX is uniquely tailored to handle large-scale data processing in a robust and efficient manner. This project focuses on using TFX to ingest and process real-time Bitcoin price data for time series analysis, with the aim of creating a streamlined ML pipeline.

**Describe Technology**

- **Data Ingestion**: TFX Pipeline uses components like `ExampleGen` to ingest data; it can handle streaming data and batch inputs.  
- **Data Validation**: The `SchemaGen` and `ExampleValidator` components help in validating the incoming data schema and identifying anomalies.  
- **Data Transformation**: Using `Transform` component, TFX applies feature transformations (e.g., scaling, encoding) necessary for ML model training.  
- **Training and Serving**: `Trainer` and `Pusher` components allow model training using TensorFlow and deployment in a serving environment.  
- **Scalability and Robustness**: Built on TensorFlow, TFX is optimized for high-performance processing and scalability across large datasets.

**Describe the Project**  
The project will involve setting up a TFX pipeline to handle real-time Bitcoin price data to perform time series analysis. Here are the key steps:

- **Set Up Data Ingestion**: Use public APIs (such as CoinGecko or CryptoCompare) to fetch real-time Bitcoin price data and ingest it using TFX's `ExampleGen`.  
- **Data Validation**: Utilize `SchemaGen` to establish a data schema and `ExampleValidator` to ensure data quality by detecting anomalies or inconsistencies.  
- **Data Transformation**: Implement transformations required for time series data, like normalizing prices and creating lag features, using the `Transform` component.  
- **Model Training**: Use a simple TensorFlow LSTM model to forecast Bitcoin price trends and train it using the `Trainer` component.  
- **Model Deployment**: Deploy the trained model using the `Pusher` component for real-time predictions.

Through this project, students will gain practical experience in building and managing ML pipelines using TFX, focusing on the challenges of real-time data processing and analysis.

**Useful Resources**

- TensorFlow TFX Documentation: [TFX Documentation](https://www.tensorflow.org/tfx)  
- Official TensorFlow Guide: [TensorFlow Documentation](https://www.tensorflow.org/guide)  
- Data API References (CoinGecko): [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it Free?**  
Yes, TFX is an open-source framework available under the Apache 2.0 license. While Python libraries used in the project are free, note that data APIs may impose rate limits or require subscriptions for extensive usage.

**Python Libraries / Bindings**

- **TensorFlow Extended (TFX)**: The core library for creating and deploying ML pipelines.  
- **TensorFlow**: Required for model training and data processing.  
- **Pandas**: For preliminary data manipulation before ingestion into TFX.  
- **Requests/HTTP Libraries**: To interact with Bitcoin price data APIs.  
- **NumPy**: For handling numerical computations in data transformation.

This project will not only enable students to familiarize themselves with TFX but also provide practical insights into real-time data processing and ML model deployment workflows.
