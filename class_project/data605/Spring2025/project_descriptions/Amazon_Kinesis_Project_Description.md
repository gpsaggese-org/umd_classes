### **Amazon Kinesis**

**Title**: Real-Time Bitcoin Price Anomaly Detection Using Amazon Kinesis  
**Difficulty**: 3 (Difficult)

**Description**  
This project involves building a real-time data pipeline to monitor Bitcoin prices, detect anomalies (e.g., sudden price spikes/drops), and trigger alerts using Amazon Kinesis. Students will stream live cryptocurrency data, process it with Kinesis, apply machine learning for anomaly detection, and visualize trends.

**Describe Technology**

- **Amazon Kinesis**: A suite for real-time data streaming and analytics.  
  1. **Kinesis Data Streams**: Ingests high-throughput Bitcoin price data from APIs.  
  2. **Kinesis Data Analytics**: Processes streaming data in real time (e.g., calculating moving averages).  
  3. **Kinesis Data Firehose**: Stores results in Amazon S3 or Redshift for historical analysis.  
  4. Use cases: Financial monitoring, algorithmic trading, fraud detection.


**Describe the Project**

1. **Stream Bitcoin Price Data**:  
   - Use Python (`ccxt` or `requests`) to fetch real-time Bitcoin prices from APIs like CoinGecko, Binance, or Coinbase.  
   - Stream data (price, volume, timestamp) to Kinesis Data Streams using `boto3`.  
2. **Real-Time Data Processing**:  
   - Use **Kinesis Data Analytics** (Apache Flink or SQL) to:  
     - Compute rolling averages and volatility metrics over 1-minute windows.  
     - Flag potential anomalies (e.g., prices deviating \>3σ from the mean).  
3. **Machine Learning Integration**:  
   - Deploy a pre-trained anomaly detection model (e.g., Isolation Forest, Autoencoder) via AWS Lambda.  
   - Trigger Lambda to score incoming data and send alerts (e.g., Amazon SNS) for severe anomalies.  
4. **Storage & Visualization**:  
   - Use Kinesis Data Firehose to archive raw and processed data in Amazon S3.  
   - Build a real-time dashboard with `plotly-dash` or AWS QuickSight to display price trends and anomalies.

**Useful Resources**

- [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Isolation Forest Anomaly Detection Tutorial](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)  
- [AWS Lambda with Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)

**Is it free?**

- Kinesis offers a limited free tier (2 shards/month). Costs scale with data volume and shard usage.

**Python Libraries / Bindings**

- `boto3` (AWS SDK) to interact with Kinesis, Lambda, and S3.  
- `ccxt` or `requests` for fetching cryptocurrency data.  
- `pandas`/`numpy` for data transformations.  
- `scikit-learn` or `tensorflow` for anomaly detection models.  
- `plotly-dash` for dashboarding.  
-
