### **pytracking**

**Title:** Real-Time Bitcoin Price Alert System with PyTracking​

**Difficulty:** 2 (Medium)​

**Description:** In this project, students will develop a real-time Bitcoin price alert system using PyTracking, a Python library designed for tracking and analyzing data. The system will monitor Bitcoin prices and send notifications when specific thresholds are crossed. This project introduces students to data ingestion from APIs, data processing, and implementing alert mechanisms using Python.​

**Describe Technology:** PyTracking is a Python library primarily used for tracking and analyzing data. It provides functionalities to process and monitor data, making it suitable for applications that require real-time tracking and alerts. In this project, PyTracking will be utilized to monitor Bitcoin price movements and trigger alerts based on predefined conditions.​

**Describe the Project:**

**Objective:** To monitor real-time Bitcoin prices and send alerts when specific price thresholds are reached.​

**Steps:**

1. **Data Ingestion:** Utilize a public Bitcoin API (such as CoinGecko) to fetch real-time price data in JSON format.​  
2. **Data Processing:** Parse the JSON response to extract the current Bitcoin price.​  
3. **Conditional Logic:** Implement logic to evaluate if the price crosses predetermined thresholds (e.g., a 5% increase or decrease from the previous hour).​  
4. **Alerts:** Use PyTracking to monitor the price data and trigger alerts when the set conditions are met.​  
5. **Automation:** Set up a Python script to automatically execute these steps at regular intervals (e.g., every 10 minutes).​

**Useful Resources:**

* [PyTracking Documentation](https://pypi.org/project/pytracking/)​  
* [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?** Yes, PyTracking is an open-source library and free to use. CoinGecko also offers free access to their API for fetching cryptocurrency data.​

**Python Libraries / Bindings:**

* **Requests:** To make HTTP requests for fetching Bitcoin price data from the API (`pip install requests`).​  
* **PyTracking:** For monitoring and analyzing data (`pip install pytracking`).​  
* **Schedule:** To assist with running the script at regular intervals (`pip install schedule`).​

By completing this project, students will gain experience in working with APIs, processing real-time data, and implementing alert systems using Python.​
