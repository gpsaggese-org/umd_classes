# Haiku Project Blueprints

## Description  

Haiku is a powerful tool designed for creating and managing machine learning workflows with a focus on simplicity and collaboration. It allows users to build, train, and deploy models efficiently while providing a clear structure for versioning and experimentation. Key features include:  

- **Workflow Management**: Streamlines the process of creating and managing ML pipelines.  
- **Version Control**: Keeps track of datasets, model versions, and experiment results.  
- **Collaboration**: Facilitates teamwork through shared projects and reproducible experiments.  
- **Integration**: Connects seamlessly with popular data libraries and frameworks.  

---

## Project 1: Forecasting UK House Prices (Difficulty: 1)  

**Project Objective**  
The goal is to predict house sale prices in the UK based on features such as location, time period, and property type. Students will optimize their models to minimize Root Mean Squared Error (RMSE).  

**Dataset Suggestions**  
- **Dataset**: *“UK House Prices: 1995–2022”* (Kaggle)  
- **Link**: [UK House Prices Dataset](https://www.kaggle.com/datasets/khushikhushikhushi/uk-house-prices-1995-to-2022)  

**Tasks**  
- **Data Ingestion**: Load the dataset into Haiku’s workflow pipeline for reproducibility.  
- **Preprocessing**: Handle missing values, encode categorical variables (property type, region), and normalize numerical features.  
- **Feature Engineering**: Create time-based features (e.g., moving averages, year-over-year price changes).  
- **Model Training**: Compare Linear Regression, Random Forest, and Gradient Boosting models while tracking results in Haiku.  
- **Model Evaluation**: Use RMSE and R² to evaluate models, logging metrics with Haiku’s version control.  
- **Deployment**: Package and deploy the final model within Haiku for batch predictions.  

**Bonus Ideas**  
- Incorporate macroeconomic indicators (inflation, interest rates) for improved performance.  
- Perform rolling-window forecasting to simulate real-world prediction.  

---

## Project 2: Customer Segmentation Using Clustering (Difficulty: 2)  

**Project Objective**  
The goal is to segment customers into meaningful groups based on purchasing behavior. Students will optimize clustering algorithms for better marketing insights and customer targeting.  

**Dataset Suggestions**  
- **Dataset**: *“Online Retail Dataset”* (UCI ML Repository)  
- **Link**: [UCI Online Retail](https://archive.ics.uci.edu/ml/datasets/Online+Retail)  

**Tasks**  
- **Data Preparation**: Load and clean the dataset, filtering canceled or invalid transactions.  
- **Feature Engineering**: Derive customer-level features (e.g., Recency, Frequency, Monetary — RFM scores).  
- **Clustering Models**: Apply K-Means and DBSCAN, tracking experiment results in Haiku.  
- **Evaluation**: Assess clusters using silhouette score and Davies-Bouldin index, logging metrics with Haiku.  
- **Visualization**: Use PCA/t-SNE to visualize segments and generate customer profiles.  
- **Insights**: Translate segments into actionable business strategies.  

**Bonus Ideas**  
- Add time-series features (monthly purchase trends) for dynamic segmentation.  
- Compare clustering stability across different random seeds tracked in Haiku.  

---

## Project 3: Sentiment Analysis on Amazon Product Reviews (Difficulty: 3)  

**Project Objective**  
The goal is to classify product reviews into positive, neutral, or negative sentiment. Students will optimize their models for accuracy and F1-score while managing large-scale text workflows.  

**Dataset Suggestions**  
- **Dataset**: *“Amazon Fine Food Reviews”* (Kaggle)  
- **Link**: [Amazon Reviews Dataset](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)  

**Tasks**  
- **Data Preprocessing**: Clean and tokenize reviews, removing stopwords and handling imbalanced classes.  
- **Vectorization**: Experiment with TF-IDF, Word2Vec embeddings, and pretrained BERT embeddings.  
- **Model Training**: Train Logistic Regression, Random Forest, and a fine-tuned BERT model, logging runs in Haiku.  
- **Evaluation**: Compare performance across models using accuracy, precision, recall, and F1-score.  
- **Error Analysis**: Investigate common misclassifications to refine preprocessing steps.  
- **Deployment**: Deploy the chosen model using Haiku for real-time inference on new reviews.  

**Bonus Ideas**  
- Build a sentiment dashboard to visualize trends over time.  
- Compare performance between traditional ML models and transformer-based approaches tracked within Haiku.  
