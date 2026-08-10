### **Watchtower**

**Title:** Implementing Cloud-Based Logging for a Cryptocurrency Price Tracker Using Watchtower​

**Difficulty:** 1 (Easy)​

**Description:** This project guides students through the development of a cryptocurrency price tracker application with integrated cloud-based logging using the Watchtower library. Participants will build a Python application that fetches real-time cryptocurrency prices and logs relevant information to AWS CloudWatch Logs, facilitating centralized monitoring and analysis.​

**Describe technology:** Watchtower is a lightweight adapter between the Python logging system and AWS CloudWatch Logs. It allows applications to send log messages directly to CloudWatch without the need for additional system-wide log collectors, enabling centralized log management and analysis.​

**Describe the project:**

* **Objective:** To develop a Python application that tracks cryptocurrency prices and utilizes Watchtower to log data to AWS CloudWatch Logs for centralized monitoring.​  
* **Steps:**  
  1. **Set Up AWS Environment:**  
     * Create an AWS account if you don't have one.  
     * Configure AWS credentials using the AWS CLI (`aws configure`).  
  2. **Install Required Libraries:**  
- Install Watchtower and Boto3 using pip:  
  `pip install watchtower boto3`  
  *   
  3. **Develop the Cryptocurrency Price Tracker:**  
     * Use a public API (e.g., CoinGecko) to fetch real-time cryptocurrency prices.  
     * Implement functionality to retrieve and display current prices for selected cryptocurrencies.  
  4. **Integrate Watchtower for Logging:**  
     * Set up Python's logging module to use Watchtower's `CloudWatchLogHandler`.  
     * Configure the logger to send log messages to a specified CloudWatch log group.  
     * Log relevant information, such as fetched prices and any errors encountered during API requests.  
  5. **Run and Monitor the Application:**  
     * Execute the application to ensure it fetches prices and logs data correctly.  
     * Verify that log messages appear in the AWS CloudWatch console under the designated log group.

**Useful resources:**

* [Watchtower Documentation](https://kislyuk.github.io/watchtower/)​  
* [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)​  
* [CoinGecko API Documentation](https://www.coingecko.com/en/api)​

**Is it free?** Watchtower and Boto3 are open-source and free to use. AWS CloudWatch offers a free tier with limited usage; exceeding the free tier may incur costs.​

**Python libraries / bindings:**

* `watchtower`: For sending log messages to AWS CloudWatch Logs.​  
* `boto3`: AWS SDK for Python, used by Watchtower for AWS interactions.​  
* `requests`: For making HTTP requests to the cryptocurrency API.​

This project provides students with practical experience in integrating cloud-based logging into a Python application, enhancing skills in application monitoring and cloud services.​
