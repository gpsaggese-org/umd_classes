### **cryptography**

**Title**: Secure Bitcoin Price Ingestion using Cryptography

**Difficulty**: 3 (difficult)

**Description**  
Cryptography is a critical technology in securing data transmission and storage, especially in applications dealing with sensitive information like financial data. This project involves the use of cryptographic techniques to ingest and process real-time Bitcoin price data securely. Students will explore the fundamental aspects of cryptography, including encryption, decryption, and digital signatures, and learn how these can be applied in a Python-based big data system.

**Describe Technology**  
Cryptography involves techniques for secure communication in the presence of third parties. The key functionalities include:

- **Encryption and Decryption**: Transforming readable data into unreadable format (encryption) and vice versa (decryption), using keys.  
- **Digital Signatures**: Ensuring data integrity and authenticity by allowing the receiver to verify that the data was not altered.  
- **Hashing**: Converting data into a fixed-size string of characters, which acts as a "fingerprint" of the data.

Examples of cryptographic algorithms include AES for symmetric encryption, RSA for asymmetric encryption, and SHA-256 for hashing.

**Describe the Project**  
The project's objective is to design a system that securely ingests real-time Bitcoin price data from a public API (e.g., CoinGecko) while ensuring data integrity and confidentiality. The project involves the following tasks:

1. **Data Ingestion**: Set up a Python script to fetch Bitcoin price data from the API at regular intervals.  
2. **Data Encryption**: Encrypt the incoming data using a symmetric key algorithm like AES to ensure privacy during transmission.  
3. **Data Storage**: Store the encrypted data in a secure format.  
4. **Data Processing**: Decrypt the data for analysis, verifying its integrity using digital signatures or hashes.  
5. **Time Series Analysis**: Implement a basic time series analysis on the decrypted data, such as moving averages or trend analysis.  
6. **Security Reporting**: Document the cryptographic methods used and their effectiveness in securing the data pipeline.

**Useful Resources**

- "Cryptography and Network Security" by William Stallings  
- PyCryptodome Documentation ([https://pycryptodome.readthedocs.io](https://pycryptodome.readthedocs.io))  
- Python's hashlib Documentation ([https://docs.python.org/3/library/hashlib.html](https://docs.python.org/3/library/hashlib.html))

**Is it free?**  
Yes, cryptographic libraries in Python, such as PyCryptodome and hashlib, are open-source and free to use.

**Python Libraries / Bindings**

- **PyCryptodome**: A self-contained Python package of low-level cryptographic primitives. You can install it with `pip install pycryptodome`.  
- **hashlib**: A built-in Python module for various secure hash and message digest algorithms.  
- **requests**: For HTTP requests to fetch data from the Bitcoin price API (`pip install requests`).

This project will provide students with hands-on experience in cryptography, data security, and time series analysis, preparing them for real-world challenges in data science and cybersecurity.
