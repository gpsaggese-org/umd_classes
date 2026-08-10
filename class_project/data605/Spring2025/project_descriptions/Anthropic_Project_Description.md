### **Anthropic**

**Title**: Real-Time Bitcoin Transaction Anomaly Detection with Anthropic Claude  
**Difficulty**: 3 (difficult)

**Description**  
Build an explainable AI system to detect anomalous Bitcoin transactions using Anthropic's constitutional AI models. The system will process blockchain data in real-time, provide human-readable explanations for flagged transactions, and integrate with alerting systems while maintaining auditability.

**Describe Technology**

- **Anthropic Claude**: AI system focused on:  
  - Interpretable anomaly detection through constitutional AI principles  
  - Natural language explanations for model decisions  
  - Real-time processing capabilities via API  
  - Built-in safety constraints for financial applications  
  - Support for structured data parsing through system prompts

**Describe the Project**

1. **Data Pipeline**:  
-   
  - Stream raw blockchain data from Blockchair API (1000+ tps)  
  - Preprocess transactions with PySpark:  
    - Extract features (value, fee, input/output ratios, temporal patterns)  
    - Windowed aggregation (1min/5min buckets)  
  - Handle imbalanced data (99% normal transactions) through synthetic minority oversampling  
-   
2. **Anomaly Detection**:  
-   
  - Implement two-stage detection:  
    1. Rule-based filtering (known attack patterns)  
    2. Anthropic model analysis with chain-of-thought prompting for example,:

```py
prompt = f"""Analyze this Bitcoin transaction {tx_data}. 
Consider: - Deviation from account history patterns
          - Network-wide statistical baselines
          - Common attack signatures"""
```

  - Generate natural language reports for flagged transactions

2. **Temporal Analysis**:  
   - Track anomaly rates with exponential weighted moving averages  
   - Detect coordinated attacks through cross-account pattern matching  
   - Predict future anomaly clusters using Prophet time series forecasting

3. **Operational System**:  
   - Build alert workflows with priority scoring (Slack/email/PagerDuty)  
   - Create Dash dashboard showing:  
     - Real-time transaction map  
     - Model confidence distributions  
     - Explanation audit trails  
   - Deploy on AWS EMR with auto-scaling for spike handling

**Useful Resources**

- [Anthropic Constitutional AI Paper](https://www.anthropic.com/constitutional-ai)  
- [Blockchain Analytics Toolkit](https://blockchain.com/explorer/api)  
- [Financial Anomaly Detection Patterns](https://arxiv.org/abs/2207.10418)

**Is it free?**

- Anthropic: Free trial credits available, production usage requires API payment  
- Blockchair: Free tier (1000 requests/day)  
- Apache Spark/Dash: Open-source


**Python Libraries / Bindings**

- `anthropic`: Official SDK for Claude models \- install with `pip install anthropic`  
- `pyspark`: Distributed data processing \- `pip install pyspark`  
- `dash`: Interactive dashboard \- `pip install dash`  
- `prophet`: Time series forecasting \- `pip install prophet`  
- `slack-sdk`: Alert integration \- `pip install slack-sdk`  
- `imbalanced-learn`: Handle data skew \- `pip install imbalanced-learn`
