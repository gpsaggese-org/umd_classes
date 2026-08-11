### **PyDrive**

**Title**: Real-Time Bitcoin Data Ingestion with PyDrive

**Difficulty**: 1 (easy)

**Description**

This project involves implementing a simple system to ingest and process real-time Bitcoin price data using Python with a focus on utilizing PyDrive. PyDrive is a wrapper for Google Drive API that provides an interface to interact with files in Google Drive using Python. Students will explore fundamental tasks of connecting to Google Drive, uploading and downloading files, and creating folders to manage datasets.

**Describe technology**

- **PyDrive**: PyDrive is a Python library that simplifies the process of authenticating and interacting with Google Drive. It provides easy access to Google Drive with minimal setup and allows easy manipulation of files and directories in your Drive account.  
    
  * Example Basic Functionalities:  
      
    - Authenticate Google Drive account using OAuth2.  
    - List files and directories in Google Drive.  
    - Upload, download, and delete files.  
    - Create and manage folders.

    

  * Typical setup involves setting up OAuth2.0 credentials through Google Cloud Console and using them to authorize access.

**Describe the project**

- **Objective**: Students will develop a simple project to continuously fetch Bitcoin price data from a public API like CoinGecko and store it in a Google Drive folder for easy access and sharing.  
    
- **Steps Involved**:  
    
  1. Set up a Google Cloud Project and enable the Google Drive API.  
  2. Use PyDrive to authenticate and connect to Google Drive.  
  3. Create a folder in Google Drive to store the Bitcoin price data.  
  4. Write a Python script to ingest Bitcoin price data at regular intervals and save it to Google Drive as CSV files.  
  5. Use basic Python libraries like pandas for data handling and simple time-series transformations (e.g., converting timestamps, calculating price averages).


- **Outcome**: Students will gain hands-on experience in using PyDrive to manage files with Google Drive, practicing how to combine it with real-time data ingestion and basic data processing.

**Useful resources**

- [PyDrive Documentation](https://pythonhosted.org/PyDrive/)  
- [Google Cloud Console](https://console.cloud.google.com/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**

Yes, using Google Drive for basic needs with PyDrive is free, subject to Google Drive's standard storage quotas and API request limits. No cost is associated with installing and using PyDrive.

**Python libraries / bindings**

- **PyDrive**: A Python library to interact with Google Drive easily. Install using `pip install PyDrive`.  
- **pandas**: Used for data manipulation and analysis. Install using `pip install pandas`.  
- **requests**: A Python package used for making HTTP requests to fetch data from APIs. Install using `pip install requests`.

This project provides experience in handling real-time data ingestion, understanding basic time-series data manipulation, and using Google Drive for seamless data storage and access.
