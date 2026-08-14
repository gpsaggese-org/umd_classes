### **Rasa**

Title: Real-time Bitcoin Price Analysis using Rasa

Difficulty: 3 (Difficult)

**Description**

- Rasa is an open-source machine learning framework for building AI assistants and chatbots. It enables developers to create conversational AI applications that can understand and process natural language input, and respond accordingly.  
- This project focuses on leveraging Rasa to ingest real-time Bitcoin price data via conversational interfaces. Participants will utilize basic Python packages for additional data processing and analysis.  
- The goal is to provide hands-on experience with Rasa and demonstrate its potential in developing applications for real-time data interaction and time series analysis.

**Describe technology**

- Rasa consists of two main components: Rasa NLU (Natural Language Understanding), which handles intent classification and entity extraction, and Rasa Core, which is responsible for dialogue management.  
- It uses machine learning models to interpret user input and make decisions about which actions to take next.  
- Rasa allows integration with various messaging platforms, APIs, and data sources to build versatile chatbots and assistants.

**Describe the project**

- Students will create a basic AI assistant using Rasa to interact with users and provide real-time updates on Bitcoin prices.  
- The assistant will use a public API, such as CoinGecko, to fetch Bitcoin prices at regular intervals.  
- Participants will implement a module in Rasa to process incoming data, analyze price trends, and provide insights by performing basic time series analysis, such as identifying price highs and lows within specified time frames.  
- The project includes setting up a simple conversation flow where users can ask about current Bitcoin prices or request historical data summaries.  
- The Rasa assistant will frame responses in natural language, allowing users to interact seamlessly and intuitively.

**Useful resources**

- Rasa documentation: [Rasa Official Documentation](https://rasa.com/docs/)  
- Rasa GitHub repository: [Rasa GitHub](https://github.com/RasaHQ/rasa)  
- CoinGecko API documentation: [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- Tutorials for integrating Rasa with external APIs: [Rasa API Integration Guide](https://rasa.com/docs/rasa/connectors/your-own-website)

**Is it free?**

- Yes, Rasa is open-source and free to use. There are no associated costs for using the Rasa framework. Public data APIs like CoinGecko also offer free access to a wide range of cryptocurrency data.

**Python libraries/bindings**

- `rasa`: The main Python package for building and running Rasa assistants. Install using `pip install rasa`.  
- `requests`: A simple Python HTTP library to fetch data from public APIs such as CoinGecko. Install using `pip install requests`.  
- `pandas`: A popular data manipulation library useful for processing and analyzing time series data. Install using `pip install pandas`.
