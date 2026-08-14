### **Amazon Sagemaker**

**Title**: Real-Time Bitcoin Price Analysis with Amazon SageMaker

**Difficulty**: 3 (difficult)

**Description**

In this project, students will leverage Amazon SageMaker to ingest and process real-time Bitcoin price data for time series analysis. Amazon SageMaker is a fully managed service that provides every developer and data scientist with the ability to build, train, and deploy machine learning (ML) models quickly. It covers the entire ML workflow, including preparing data, building models, training and tuning them, deploying them to production, and scaling them as needed. This project involves gathering real-time Bitcoin price data from an external API, performing time series analysis, and deploying a predictive model using SageMaker.

**Describe technology**

- **Amazon SageMaker**: A comprehensive managed service that enables users to quickly create and manage machine learning models. It provides tools for data preparation, feature engineering, model training, tuning, and deployment.  
- **Notebooks**: SageMaker offers Jupyter Notebooks for data exploration and model building, integrating with data sources within AWS.  
- **Built-in Algorithms**: SageMaker includes a range of built-in algorithms optimized for speed, scale, and accuracy.  
- **Real-Time Endpoints**: Deploy models as scalable API endpoints.

**Describe the project**

- **Data Ingestion**: Utilize Python's `requests` library to fetch real-time Bitcoin price data from an API, such as CoinGecko. Use Amazon Kinesis Data Streams to manage the data ingestion pipeline for streaming data into Amazon S3.  
- **Data Storage**: Store ingested data in Amazon S3 for further processing and analysis.  
- **Data Processing**: Use SageMaker Processing Jobs with pre-loaded Jupyter Notebooks containing Pandas and NumPy for dataset cleaning and pre-processing.  
- **Time Series Analysis**: Implement a time series forecasting model using advanced built-in algorithms like DeepAR in SageMaker. Complement it with statistical methods in Python for validation.  
- **Model Training and Evaluation**: Train the model, tune hyperparameters, and evaluate accuracy using SageMaker’s built-in capabilities.  
- **Model Deployment**: Deploy the trained model as a SageMaker endpoint to predict future Bitcoin prices, demonstrating how time series forecasting can be applied to financial datasets.  
- **Visualization**: Leverage Matplotlib and Seaborn for generating visual insights into the Bitcoin price trend, including forecasting vs actual comparisons.

**Useful resources**

- [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/index.html)  
- [DeepAR Forecasting Algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html)  
- [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/kinesis/index.html)

**Is it free?**  
You need an AWS account to use Amazon SageMaker. The AWS Free Tier provides limited free monthly usage of SageMaker and Kinesis, which may be sufficient for small-scale experiments. Exceeding these limits will incur charges.

**Python libraries / bindings**

To effectively implement this project, the following Python libraries will be utilized:

- `boto3`: AWS SDK for Python, enables interaction with Amazon SageMaker, S3, and Kinesis.  
- `Pandas` and `NumPy`: For data manipulation and numerical operations.  
- `Matplotlib` and `Seaborn`: For data visualization.  
- `requests`: To fetch Bitcoin data from a public API.  
- SageMaker SDK: Provides an interface for managing SageMaker resources and kdeploying models.
