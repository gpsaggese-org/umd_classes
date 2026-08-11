### **Mailgun**

**Title**: Real-Time Bitcoin Data Processing with Mailgun  
**Difficulty**: 1 (easy)

**Description:**  
In this project, students will use Mailgun, a popular email automation service, to set up notifications based on real-time Bitcoin price changes. The project will involve ingesting Bitcoin data using a public API and processing this data to send automated alerts when specific price thresholds are crossed. This project provides a great introduction to using APIs, handling real-time data, and integrating automated notification systems using Python.

**Describe technology:**  
Mailgun is an API-driven email service designed for sending, receiving, and tracking emails. It offers features like email validation, detailed analytics, and email infrastructure optimization. In this project, we will use Mailgun's API to send automated email notifications based on Bitcoin price data.

**Describe the project:**

- **Objective**: To monitor Bitcoin prices in real-time and send email alerts when specific thresholds are crossed.  
- **Steps:**  
  1. **Data Ingestion**: Use a public Bitcoin API (like CoinGecko) to fetch real-time price data in JSON format.  
  2. **Data Processing**: Parse the JSON response to extract the current Bitcoin price.  
  3. **Conditional Logic**: Implement logic to evaluate if the price crosses predetermined thresholds (e.g., a 5% drop from the previous hour).  
  4. **Email Alerts**: Utilize the Mailgun API to send email notifications to the user when the set conditions are met.  
  5. **Automation**: Set up a Python script to automatically execute these steps at regular intervals (e.g., every 10 minutes).

**Useful resources:**

- [Mailgun Documentation](https://documentation.mailgun.com/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Mailgun offers a free tier, but it has limitations on the number of emails sent per month. For small projects and testing, the free tier is usually sufficient.

**Python libraries / bindings:**

- **Requests**: To make HTTP requests for fetching Bitcoin price data from the API (`pip install requests`).  
- **Mailgun Python SDK**: For easily interacting with the Mailgun API (`pip install mailgun2`).  
- **Schedule**: To assist with running the script at regular intervals (`pip install schedule`).
