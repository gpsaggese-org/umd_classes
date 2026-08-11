### **PyCryptodome**

**Title**: Real-Time Bitcoin Data Analysis Using PyCryptodome

**Difficulty**: 1 (Easy)

**Description**

PyCryptodome is a self-contained Python package of low-level cryptographic primitives, designed for implementing cryptographic operations in Python. Its easy-to-use interface allows students to perform cryptographic tasks such as encryption, decryption, hashing, and authentication without delving into complex cryptographic algorithms. This makes it an excellent choice for projects requiring basic security implementations.

This project involves using PyCryptodome to securely ingest real-time Bitcoin price data from an API, showcasing its cryptographic functionalities. The project will focus on securely handling time-series Bitcoin data, ensuring data integrity through hashing, and enhancing privacy through encryption before storage.

**Describe technology**

* PyCryptodome is a library focused on cryptographic algorithms and primitives.  
* It provides functionalities for encryption/decryption, cryptographic hashes, digital signatures, and random number generation.  
* PyCryptodome is a drop-in replacement for the PyCrypto library and uses a simple API for cryptographic operations.

**Describe the project**

* Retrieve real-time Bitcoin price data from a public API like CoinGecko.  
* Use PyCryptodome to hash the incoming data to ensure integrity and detect any data tampering.  
* Encrypt the data using symmetric encryption techniques before storing it.  
* Implement a simple script to decrypt and display Bitcoin prices securely.  
* Analyze the securely stored Bitcoin data to identify trends and patterns using basic Python libraries such as Pandas for time series analysis.  
* This project not only helps students understand time series data handling but also gives them hands-on experience with basic cryptographic concepts using PyCryptodome.

**Useful resources**

* [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/en/latest/)  
* [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
* [Pandas Documentation](https://pandas.pydata.org/docs/)

**Is it free?**

Yes, PyCryptodome is an open-source library and can be used freely. You only need access to a Python environment to run the code.

**Python libraries / bindings**

* PyCryptodome: For cryptographic functions like hashing and encryption. Install via pip:  pip install pycryptodome.  
* Requests: To fetch real-time Bitcoin data from APIs. Install via pip:  pip install requests.  
* Pandas: For data analysis and manipulation of time series data. Install via pip:  pip install pandas.
