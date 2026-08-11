### **SendGrid**

**Title**: Real-Time Bitcoin Data Analysis with SendGrid

**Difficulty**: Medium (2)

**Description**  
This project focuses on utilizing SendGrid, a cloud-based email service provider, to send alerts based on real-time Bitcoin data ingested via public APIs. Students will learn how to integrate SendGrid with Python to automate the process of sending notifications when certain conditions are met within the Bitcoin time series data. This project helps students grasp real-time data ingestion, processing, and email-based notification systems.

**Describe technology**

- **SendGrid**: A popular cloud-based email service that provides reliable transaction and marketing email delivery. It offers API endpoints for sending emails programmatically and allows you to manage contacts, track email delivery, and view analytics. It's highly scalable and used by businesses for email marketing campaigns, transactional emails, and alerts.

**Describe the project**

- Goal: Develop a system using SendGrid to send email alerts whenever the real-time Bitcoin price crosses a predefined threshold.  
- Steps:  
  - Use Python to ingest Bitcoin price data in real-time from a public API (e.g., CoinGecko or CryptoCompare).  
  - Process the data to analyze Bitcoin price trends and identify significant price movements or thresholds.  
  - Implement a decision-making function to trigger SendGrid's email API when Bitcoin prices exceed certain limits.  
  - Configure SendGrid's API to send customized email alerts to specified recipients, including recent Bitcoin price data and analysis results.  
  - Ensure the system can dynamically check for these conditions at regular intervals, demonstrating principles of time-series analysis and asynchronous processing.  
- This project provides a practical approach to understanding real-time data handling and automated alert systems through workflows integrating email notifications.

**Useful resources**

- [SendGrid Official Documentation](https://sendgrid.com/docs/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Twilio SendGrid API Libraries for Python](https://github.com/sendgrid/sendgrid-python)

**Is it free?**

- SendGrid offers a free tier with a limited number of emails per day. CoinGecko’s API is free for basic usage but has usage limits.

**Python libraries / bindings**

- **sendgrid**: A Python client library for SendGrid, enabling easy interaction with SendGrid's email API. Install it using `pip install sendgrid`.  
- **requests**: A Python library for making HTTP requests to APIs. Useful for interfacing with both the Bitcoin price API and the SendGrid API. Install it using `pip install requests`.  
- **schedule**: A Python library for job scheduling, allowing the automation of periodic data fetching and alert checks. Install it using `pip install schedule`.
