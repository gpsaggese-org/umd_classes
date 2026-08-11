### **Cloudflare Workers AI**

**Title**: Real-time Bitcoin Data Analysis Using Cloudflare Workers AI

**Difficulty**: Medium (2)

**Description** Cloudflare Workers AI is a cutting-edge platform for deploying serverless functions utilizing AI-powered capabilities at the edge of the network. It allows for real-time data processing and analysis with minimal latency. The main components include Workers for running code, and various SDKs and APIs for integrating AI functionalities and handling data processing tasks.

**Describe technology**

- **Cloudflare Workers**: Lightweight and fast, this service allows users to run JavaScript or WebAssembly code on Cloudflare's edge servers, reducing latency by processing requests closer to end-users.  
- **AI Integration**: Workers AI provides built-in support for handling AI tasks such as machine learning inference, natural language processing, and image recognition.  
- **Edge Computing**: By leveraging the edge network, Cloudflare Workers AI can handle data processing tasks, ensuring real-time and efficient management of applications like live data analysis.

**Describe the project** The project focuses on implementing a real-time system using Cloudflare Workers AI to ingest and process live Bitcoin price data:

- **Data Ingestion**: Use Cloudflare Workers to fetch live Bitcoin price data from a public API such as CoinGecko. The data will be handled at the edge to minimize latency.  
- **Data Storage and Transformation**: Write a Cloudflare Worker function to preprocess and organize incoming data. Apply AI techniques for basic time series analysis, such as predicting short-term trends and calculating moving averages.  
- **Real-time Analysis**: Utilize Workers AI capabilities to run machine learning models on the processed data to identify potential market opportunities.  
- **Visualization**: Develop a simple client-side application to query processed data from Workers and visualize potential trends or alerts in real time.

**Useful resources**

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)  
- [Cloudflare AI Platform Overview](https://www.cloudflare.com/products/workers-ai/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api/documentation)  
- [Python for Time Series Data Analysis](https://www.analyticsvidhya.com/blog/2020/07/a-quick-guide-to-time-series-forecasting-python/)

**Is it free?** Cloudflare Workers offers a free tier with limitations on compute and requests. Additional resources and features require a paid plan.

**Python libraries / bindings**

- **Cloudflare Python API**: While the main Workers tasks will be in JavaScript or WebAssembly, you can use the Cloudflare Python SDK for setting up Cloudflare accounts and managing workers programmatically.  
- **Requests**: Useful for testing API interactions to fetch Bitcoin data before implementing the edge functions.

This project helps students learn the fundamentals of edge computing and how to implement real-time data processing with AI capabilities, combining both serverless technology and Python data analysis.
