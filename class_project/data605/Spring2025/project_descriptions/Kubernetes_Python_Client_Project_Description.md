### **Kubernetes Python Client**

**Title**: Analyzing Bitcoin Data with Kubernetes Python Client

**Difficulty**: 1 (easy)

**Description**  
In this project, you will use the Kubernetes Python Client to manage and deploy a simple application that ingests real-time Bitcoin price data. Kubernetes is an open-source container orchestration platform that automates many manual processes involved in deploying, managing, and scaling containerized applications. This project will guide you through setting up a small Kubernetes cluster using Python to deploy a simple Bitcoin price tracker that processes time-series data from a public API and outputs basic analytics.

**Describe technology**

- **Kubernetes**: A platform designed to automate deploying, scaling, and operating application containers.  
- **Kubernetes Python Client**: A Python library that interacts with Kubernetes clusters. This client allows developers to manage Kubernetes resources easily, execute commands within containers, and handle cluster-related operations programmatically.

**Describe the project**

- You'll start by setting up a local Kubernetes cluster using Minikube or a similar tool.  
- Using the Kubernetes Python Client, you'll write scripts to deploy a Flask application in Kubernetes. This application will fetch real-time Bitcoin price data from a public API like CoinGecko.  
- You will set up a Kubernetes CronJob that schedules regular data fetching and storage tasks.  
- Implement basic time-series analysis with Python to calculate statistics such as average price over time or percentage change.  
- Extend the deployment with Kubernetes resources like ConfigMaps for configuration management and Persistent Volumes for data storage.  
- Finally, visualize the processed data by deploying a simple frontend service within the Kubernetes cluster, showcasing how Bitcoin prices change over time.

**Useful resources**

- [Kubernetes Official Documentation](https://kubernetes.io/docs/home/)  
- [Kubernetes Python Client Documentation](https://github.com/kubernetes-client/python)  
- [Minikube Quickstart](https://minikube.sigs.k8s.io/docs/start/)

**Is it free?**  
Yes, this project is free, as you can run Kubernetes locally using Minikube or a similar tool without needing a cloud service.

**Python libraries / bindings**

- **Kubernetes Python Client**: Install using `pip install kubernetes`. It allows interaction with Kubernetes clusters and resources.  
- **Requests**: Install using `pip install requests`. Used for making HTTP requests to fetch Bitcoin data from APIs.  
- **Flask**: Install using `pip install flask`. A lightweight WSGI web application framework to create the application for fetching and serving data.  
- **Pandas**: Install using `pip install pandas`. Useful for time-series analysis and handling data structures.
