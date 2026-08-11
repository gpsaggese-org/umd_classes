### **Argo Workflows**

Title: Real-Time Bitcoin Data Processing with Argo Workflows

**Difficulty**: 2 (medium)

**Description**

Argo Workflows is an open-source container-native workflow engine for orchestrating jobs on Kubernetes. It manages the execution of complex workflows, particularly in scenarios involving big data processing and machine learning pipelines. In this project, students will leverage Argo Workflows to handle real-time bitcoin price data. The focus will be on utilizing the workflow engine to automate data ingestion and processing tasks, while basic Python packages will support data manipulation and analysis, specifically targeting time series analysis.

**Describe technology**

- **Argo Workflows**:  
  - Designed for Kubernetes, Argo Workflows allows users to define, execute, and monitor multi-step workflows using Kubernetes Custom Resource Definitions (CRDs).  
  - Supports directed acyclic graphs (DAGs) of tasks, which can be executed in parallel or sequentially.  
  - Highly scalable and suitable for automating complex data processing tasks without needing an external scheduler.  
  - Integrates well with other Kubernetes tools and services, capitalizing on Kubernetes’ scalability and reliability.

**Describe the project**

- **Objective**: Implement a real-time data processing pipeline using Argo Workflows to ingest and process bitcoin prices from a live feed.  
    
- **Project Steps**:  
    
  1. **Setup Environment**: Configure a Kubernetes cluster where Argo Workflows will be installed and operated.  
  2. **Define Workflows**:  
     - Create a workflow to continuously ingest bitcoin prices from an API like Coinbase or CoinGecko.  
     - Configure parallel tasks in the workflow: one for ingesting new data and another for cleaning and preparing it for analysis.  
  3. **Processing and Storing Data**:  
     - Use Python scripts to process and transform the price data into a structured format.  
     - Analyze the data to infer trends and patterns over time, focusing on metrics like volatility and moving averages.  
     - Store processed data in a database or file system for further analysis or machine learning models.  
  4. **Real-Time Analysis**:  
     - Implement simple Python functions for time series analysis focusing on trend detection and forecasting.


- **Outcome**: Gain practical experience in orchestrating workflows on Kubernetes while handling real-time market data, which provides valuable insights into building scalable data processing pipelines.

**Useful resources**

- [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)  
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)  
- [Coinbase API Documentation](https://developers.coinbase.com/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api_documentation)

**Is it free?**

- Argo Workflows itself is open-source and free to use. However, running Kubernetes clusters may incur costs depending on the platform (such as using AWS EKS, GKE, etc.). Many platforms offer free tiers for small-scale, experimental clusters.

**Python libraries / bindings**

- **Requests**: For making HTTP requests to fetch bitcoin data from APIs.  
- **Pandas**: Essential for organizing and analyzing time series data.  
- **NumPy**: Useful for numerical computing needed in data calculations.  
- **Matplotlib/Seaborn**: For plotting and visualizing processed time series data.  
- **Kubernetes Python Client**: For interactions with the Kubernetes cluster, if needed.
