### **Fernet**

**Title**: Real-Time Bitcoin Data Processing with Fernet Encryption

**Difficulty**: 1 (easy)

**Description**  
Fernet is a part of the cryptography package in Python, which provides a way to securely encrypt and decrypt data. It ensures that the message encrypted cannot be read or altered without the encryption key. In this project, we will use Fernet encryption to securely process real-time Bitcoin price data.

**Describe technology**  
Fernet is a symmetric encryption method provided by the `cryptography` package in Python. It generates a unique key for encrypting and decrypting data, using advanced encryption mechanisms, including AES (Advanced Encryption Standard). The main functionalities of Fernet include:

- **Key Generation**: Creates a secure encryption key.  
- **Encryption**: Encrypts plaintext information, ensuring data security.  
- **Decryption**: Decrypts encrypted information back to plaintext.  
- **Token Management**: Handles secure tokens to ensure data is neither reused nor tampered with.

Example Usage:

```py
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()

# Initialize Fernet with the generated key
cipher = Fernet(key)

# Encrypt some data (e.g., a string representation of Bitcoin data)
encrypted_data = cipher.encrypt(b"Bitcoin price: $50000")

# Decrypt the data
decrypted_data = cipher.decrypt(encrypted_data)

print(decrypted_data.decode())  # Output: Bitcoin price: $50000
```

**Describe the project**  
The project focuses on ingesting real-time Bitcoin price data from a public API (e.g., CoinGecko or another open API) and securely processing this data using Fernet encryption. The steps for the project are:

1. **Data Ingestion**: Fetch real-time Bitcoin price data at regular intervals using basic HTTP requests.  
2. **Data Encryption**: Use Fernet to encrypt the fetched data immediately after retrieval.  
3. **Data Storage**: Store the encrypted data locally or in a simple database.  
4. **Data Decryption and Analysis**: Decrypt the data for basic time series analysis, such as calculating moving averages over a specified period.  
5. **Output**: Display time series analysis results on a simple console dashboard or save to a CSV file.

**Useful resources**

- [cryptography documentation](https://cryptography.io/en/latest/)  
- [Cryptography \- Fernet Documentation](https://cryptography.io/en/latest/fernet/)  
- [CoinGecko API](https://www.coingecko.com/en/api)

**Is it free?**  
Yes, Fernet is part of the open-source `cryptography` package for Python.

**Python libraries / bindings**

- **cryptography**: To install, use `pip install cryptography`. It's required to use Fernet for encrypting and decrypting data.  
- **requests**: To fetch real-time Bitcoin prices via API calls. Install using `pip install requests`.

This project will provide students a practical introduction to data security in Python, emphasizing encryption's importance when handling sensitive and real-time data.
