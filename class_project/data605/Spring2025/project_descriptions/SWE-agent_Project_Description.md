### **SWE-agent**

**Title:** Automated Bitcoin Price Alert System with SWE-Agent​

**Difficulty:** 2 (Medium)​

**Description:** In this project, students will utilize SWE-Agent, an AI-driven system designed to assist in software engineering tasks, to develop an automated Bitcoin price alert system. The project involves setting up SWE-Agent to monitor real-time Bitcoin prices and send notifications when specific price thresholds are reached. This provides a practical introduction to integrating AI agents with cryptocurrency data monitoring.​

**Technology Overview:**

* **SWE-Agent:**  
  * Transforms large language models (LLMs) into autonomous software engineering agents capable of interacting with codebases.​  
  * Utilizes Agent-Computer Interfaces (ACIs) to perform tasks such as browsing repositories, editing code, and executing commands.​  
  * Simplifies the automation of software tasks, making it accessible for users with basic programming knowledge.​

**Project Outline:**

1. **Setup and Configuration:**  
   * Install SWE-Agent by following the official [Getting Started Guide](https://swe-agent.com/).​  
   * Configure SWE-Agent to use a suitable LLM (e.g., GPT-4) by setting the appropriate API keys.​  
2. **Data Ingestion:**  
   * Use a public API, such as CoinGecko, to fetch real-time Bitcoin price data.​  
   * Implement a Python script that retrieves the current Bitcoin price at regular intervals.​  
3. **Price Monitoring and Alert System:**  
   * Develop a function that checks if the Bitcoin price crosses predefined thresholds (e.g., a 5% increase or decrease).​  
   * Configure SWE-Agent to send email notifications or log alerts when these thresholds are met.​  
4. **Automation:**  
   * Set up a scheduling mechanism to run the price monitoring script at regular intervals (e.g., every 10 minutes).​  
   * Ensure that SWE-Agent operates autonomously, requiring minimal manual intervention.​

**Useful Resources:**

* [SWE-Agent Documentation](https://swe-agent.com/)​  
* [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
* [Python `requests` Library Documentation](https://docs.python-requests.org/en/latest/)​

**Is it Free?**

SWE-Agent is an open-source project and free to use. Access to certain LLMs may require subscriptions or incur usage costs. The CoinGecko API provides free access to cryptocurrency data, though with rate limits.​

**Python Libraries / Dependencies:**

* `sweagent`: Core library for deploying and managing SWE-Agent.​  
* `requests`: For making HTTP requests to fetch Bitcoin price data. Install using `pip install requests`.​  
* `schedule`: To assist with running the script at regular intervals. Install using `pip install schedule`.​  
* `smtplib`: For sending email notifications (included in Python's standard library).​

This project offers a practical introduction to using AI agents for automating tasks, specifically in monitoring cryptocurrency prices and sending alerts based on real-time data.​
