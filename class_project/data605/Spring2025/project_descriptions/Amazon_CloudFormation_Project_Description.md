### **Amazon CloudFormation**

**Title**: Real-Time Bitcoin Price Analysis Pipeline with AWS CloudFormation  
**Difficulty**: 3 (Difficult)

**Description**  
This project challenges students to build an automated AWS pipeline for ingesting, processing, and analyzing real-time Bitcoin price data using AWS CloudFormation. The pipeline includes machine learning integration for price trend prediction and alerting.

**Describe Technology**

- **AWS CloudFormation**: Infrastructure-as-Code (IaC) service for deploying complex architectures.  
- **AWS Services**:  
  - **Kinesis Data Streams**: Real-time Bitcoin price ingestion  
  - **SageMaker**: ML model training/predictions  
  - **Lambda (Python)**: Data processing and alert logic  
  - **CloudWatch**: Monitoring and triggers  
- **Key Features**:  
  - End-to-end automation of financial data pipeline  
  - ML integration for predictive analytics  
  - Real-time alerting system


**Describe the Project:**

1. **Design the Infrastructure**:  
   - Create a CloudFormation template to deploy:  
     - Kinesis stream for live price data ingestion  
     - Lambda functions for data cleaning/transformation  
     - SageMaker endpoint for LSTM/Prophet price predictions  
     - S3 buckets for raw data and model artifacts  
     - SNS topic for price alert notifications

   

2. **Implement Python Logic**:  
   - Build a Python scraper to feed live Bitcoin prices to Kinesis (CoinGecko API)  
   - Develop Lambda functions to:  
     - Calculate moving averages/RSI indicators  
     - Train/update ML models using historical data  
     - Compare predictions vs actual prices  
   - Create CloudWatch-triggered retraining workflow

   

3. **Advanced Features**:  
   - Implement anomaly detection for sudden price swings  
   - Deploy automated trading signals (e.g., "BUY/SELL" alerts via SNS)  
   - Optimize costs using spot instances for SageMaker training  
     

**Useful Resources**

- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [AWS SageMaker Python SDK](https://sagemaker.readthedocs.io/)  
- [Time Series Forecasting with TensorFlow](https://www.tensorflow.org/tutorials/structured_data/time_series)


**Is it Free?**

- CloudFormation is free, but Kinesis/SageMaker/Lambda incur costs. Free tier limits apply.  
- CoinGecko API: Free plan (50 calls/min)


**Python Libraries / Bindings**

- **boto3**: AWS service interactions  
- **yfinance/pycoingecko**: Bitcoin price data fetching  
- **tensorflow/pytorch**: ML model development  
- **pandas-ta**: Technical indicator calculations  
- **fastapi** (optional): Prediction endpoint
