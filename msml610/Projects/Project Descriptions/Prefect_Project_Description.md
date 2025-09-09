**Description**

In this project, students will utilize Prefect, a workflow orchestration tool, to automate and manage data pipelines for various data science tasks. Prefect helps streamline data workflows, allowing for efficient scheduling, monitoring, and error handling. Its features include:

- **Dynamic Workflows**: Build workflows that can adapt based on real-time data.
- **Task Scheduling**: Schedule tasks to run at specific intervals or based on triggers.
- **Error Handling**: Implement retry logic and notifications for task failures.
- **Visualization**: Monitor workflow execution and performance through an intuitive UI.

---

### Project 1: Predicting House Prices (Difficulty: 1)

**Project Objective**: Build a data pipeline that ingests housing data, preprocesses it, and trains a machine learning model to predict house prices based on various features.

**Dataset Suggestions**:
- **Dataset**: Ames Housing Dataset (available on Kaggle)
- **Link**: [Ames Housing Dataset](https://www.kaggle.com/datasets/prestonvong/AmesHousing)

**Tasks**:
- **Set Up Prefect Environment**: Create a Prefect project and configure the necessary infrastructure.
- **Data Ingestion**: Use Prefect to automate the download of the Ames Housing dataset from Kaggle.
- **Data Preprocessing**: Implement data cleaning and preprocessing tasks (handling missing values, encoding categorical features).
- **Model Training**: Train a regression model (e.g., Linear Regression) to predict house prices.
- **Evaluation**: Evaluate model performance using metrics like RMSE and visualize results.

---

### Project 2: Real-Time Twitter Sentiment Analysis (Difficulty: 2)

**Project Objective**: Develop a data pipeline to collect tweets in real-time related to a specific topic and perform sentiment analysis to gauge public opinion.

**Dataset Suggestions**:
- **Dataset**: Twitter API for real-time data (free tier)
- **Link**: [Twitter Developer Portal](https://developer.twitter.com/en/docs/twitter-api)

**Tasks**:
- **Set Up Prefect Flow**: Create a flow to manage the data pipeline for Twitter API integration.
- **Stream Tweets**: Use Prefect to continuously fetch tweets containing specific keywords using the Twitter API.
- **Sentiment Analysis**: Integrate a pre-trained model (e.g., VADER) to analyze the sentiment of each tweet.
- **Data Storage**: Store the results in a structured format (e.g., CSV or a database) for further analysis.
- **Visualization**: Create visualizations to display sentiment trends over time.

---

### Project 3: Anomaly Detection in Network Traffic (Difficulty: 3)

**Project Objective**: Implement a complex data pipeline to analyze network traffic data and detect anomalies that could indicate security threats.

**Dataset Suggestions**:
- **Dataset**: UNSW-NB15 dataset (available on Kaggle)
- **Link**: [UNSW-NB15 Dataset](https://www.kaggle.com/datasets/mohammadami/unsw-nb15-dataset)

**Tasks**:
- **Prefect Workflow Design**: Design a Prefect workflow that orchestrates the entire data processing and analysis pipeline.
- **Data Ingestion**: Automate the loading of the UNSW-NB15 dataset from Kaggle.
- **Feature Engineering**: Extract and engineer relevant features from the raw network traffic data for better anomaly detection performance.
- **Anomaly Detection Model**: Implement a machine learning model (e.g., Isolation Forest or Autoencoder) to identify anomalous patterns in the data.
- **Monitoring and Alerts**: Set up monitoring for the workflow and create alerts for detected anomalies.

**Bonus Ideas**:
- For Project 1: Compare different regression models and analyze performance differences.
- For Project 2: Extend the pipeline to include geolocation data and analyze sentiment by region.
- For Project 3: Implement a dashboard using tools like Dash or Streamlit to visualize detected anomalies in real time.

