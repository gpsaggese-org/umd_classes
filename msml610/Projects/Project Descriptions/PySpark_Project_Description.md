**Description**

In this project, students will utilize PySpark, an open-source data processing framework, to handle large-scale datasets efficiently. PySpark allows for distributed data processing and offers a rich set of APIs for machine learning, SQL, and data manipulation. Its features include:

- **Distributed Computing**: Enables the processing of large datasets across multiple nodes.
- **MLlib**: A scalable machine learning library for building and deploying machine learning models.
- **DataFrame API**: Provides high-level abstractions for data manipulation similar to Pandas.
- **Integration with Hadoop**: Seamlessly works with big data tools like Hadoop and Spark.

---

### Project 1: Movie Recommendation System (Difficulty: 1)

**Project Objective**  
Develop a movie recommendation system that predicts user preferences based on past ratings and user behavior, optimizing for personalized movie suggestions.

**Dataset Suggestions**  
- **Dataset**: MovieLens 100K Dataset  
- **Source**: [Kaggle - MovieLens 100K](https://www.kaggle.com/grouplens/movielens-100k)

**Tasks**  
- **Data Ingestion**: Load the MovieLens dataset into a PySpark DataFrame.
- **Data Cleaning**: Handle missing values and filter out irrelevant data.
- **Feature Engineering**: Create user and item features for collaborative filtering.
- **Model Training**: Implement ALS (Alternating Least Squares) for the recommendation model using MLlib.
- **Evaluation**: Use metrics like RMSE to evaluate the model's performance.
- **User Interface**: Create a simple recommendation interface for users to input their preferences.

---

### Project 2: Predicting Customer Churn (Difficulty: 2)

**Project Objective**  
Build a predictive model to identify customers at risk of churn in a telecommunications dataset, optimizing for accuracy and recall.

**Dataset Suggestions**  
- **Dataset**: Telco Customer Churn Dataset  
- **Source**: [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

**Tasks**  
- **Data Ingestion**: Import the Telco dataset into a PySpark DataFrame.
- **Data Preprocessing**: Clean the dataset by removing duplicates and encoding categorical variables.
- **Exploratory Data Analysis**: Use PySpark SQL to analyze customer behavior and identify churn patterns.
- **Feature Selection**: Select relevant features for the churn prediction model.
- **Model Training**: Implement classification algorithms (e.g., Logistic Regression, Decision Trees) using MLlib.
- **Model Evaluation**: Assess model performance using confusion matrix, precision, and recall metrics.

---

### Project 3: Anomaly Detection in Network Traffic (Difficulty: 3)

**Project Objective**  
Create an anomaly detection system to identify unusual patterns in network traffic data, optimizing for detection rate and minimizing false positives.

**Dataset Suggestions**  
- **Dataset**: UNSW-NB15 Network Traffic Dataset  
- **Source**: [UNSW-NB15 Dataset](https://www.unsw.edu.au/engineering/our-story/our-research/cybersecurity/unsw-nb15-dataset)

**Tasks**  
- **Data Ingestion**: Load the UNSW-NB15 dataset using PySpark.
- **Data Preprocessing**: Clean and normalize the dataset, handling missing values and feature scaling.
- **Exploratory Data Analysis**: Analyze traffic patterns and visualize normal vs. anomalous behavior.
- **Feature Engineering**: Create new features that may help in distinguishing normal and anomalous traffic.
- **Model Training**: Implement unsupervised learning techniques (e.g., Isolation Forest, One-Class SVM) for anomaly detection using MLlib.
- **Model Evaluation**: Use metrics like precision, recall, and F1-score to evaluate the detection performance.

**Bonus Ideas (Optional)**  
- For Project 1, integrate user feedback to improve recommendations over time.
- For Project 2, compare models against a baseline model (e.g., Random Forest) to assess improvements.
- For Project 3, implement a real-time monitoring system using Spark Streaming to detect anomalies on-the-fly.

