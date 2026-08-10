### **mock**

**Title:** Unit Testing Cryptocurrency Applications with Python's `unittest.mock`​

**Difficulty:** 2 (Medium)​

**Description:** This project introduces students to Python's `unittest.mock` library, a powerful tool for creating mock objects and conducting unit tests. Participants will develop a cryptocurrency price alert application and utilize `unittest.mock` to simulate external API responses, ensuring the application's reliability without relying on real-time data.​

**Describe technology:** `unittest.mock` is a library for testing in Python. It allows developers to replace parts of their system under test with mock objects and make assertions about how they have been used. This is particularly useful for isolating the code under test and controlling its environment during testing.

**Describe the project:**

* **Objective:** To develop a cryptocurrency price alert application and implement unit tests using `unittest.mock` to simulate API responses.  
* **Steps:**  
  1. **Application Development:**  
     * Create a Python application that fetches cryptocurrency prices from a public API (e.g., CoinGecko) and sends alerts when prices cross certain thresholds.  
  2. **Mocking External APIs:**  
     * Use `unittest.mock` to simulate responses from the cryptocurrency API, allowing testing of various price scenarios without making actual API calls.  
  3. **Writing Unit Tests:**  
     * Develop unit tests to verify that the application correctly processes API data and triggers alerts as expected.  
  4. **Assertion Checks:**  
     * Implement assertions to ensure that the application behaves correctly under different simulated conditions, such as price increases, decreases, or API errors.

**Useful resources:**

* [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)​  
* [Real Python: Understanding the Python Mock Object Library](https://realpython.com/python-mock-library/)​  
* [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?** Yes, `unittest.mock` is part of Python's standard library and is free to use. CoinGecko provides free access to its API with certain rate limits, suitable for educational purposes.​

**Python libraries / bindings:**

* `unittest.mock`: For creating mock objects and patching dependencies during testing.  
* `requests`: To make HTTP requests for fetching data from APIs.​  
* `pandas`: For data manipulation and analysis.​

This project offers students practical experience in developing applications that interact with external APIs and implementing unit tests using mock objects to ensure code reliability without depending on live data.​
