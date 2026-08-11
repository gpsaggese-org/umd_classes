### **Postmark**

**Title**: Ingest Bitcoin Prices Using Postmark

**Difficulty**: 1 (easy)

**Description**:  
Postmark is primarily known for its email delivery services, but for this project, we'll delve into its less-discussed functionality of real-time data processing. Although not typically used for data ingestion, students will learn how Postmark's webhook support can be adapted to ingest real-time Bitcoin price data into a Python-based system.

The project involves setting up a simple webhook server using Python that interacts with the Postmark API. By leveraging Postmark's capability to push real-time updates, students will integrate it with a public Bitcoin price API, such as CoinGecko, to acquire and process current price data.

**Describe technology**:

- **Postmark**: Primarily an email delivery service, it provides webhook features that can be repurposed for real-time data ingestion.  
- **Webhooks**: Postmark's webhooks send HTTP requests to a user-defined URL endpoint, which in this project will read and process Bitcoin price data.  
- **Python**: Basic Python packages will be used to handle HTTP requests and data manipulation.

**Describe the project**:

- **Phase 1**: Familiarize with Postmark's webhook setup. Register an account and read the documentation on creating webhooks.  
- **Phase 2**: Create a basic Python server to handle incoming HTTP POST requests from a public Bitcoin price API.  
- **Phase 3**: Configure Postmark to send notifications via a webhook upon significant changes in Bitcoin prices.  
- **Phase 4**: Implement time series analysis on the ingested data. Use Python's basic data processing libraries like Pandas and Matplotlib to visualize trends and perform elementary analysis such as moving averages.  
- **Phase 5**: Configure Postmark to send notifications via a webhook upon analyzed data.

**Useful resources**:

- [Postmark Documentation](https://postmarkapp.com/developer)  
- [Python Requests Library](https://docs.python-requests.org/en/master/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)  
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

**Is it free?**  
Postmark offers a free trial with limited usage for exploring its features, including webhooks. Additional requests may incur fees.

**Python libraries / bindings**:

- `requests`: To handle HTTP requests and ingest data from APIs. Installable via `pip install requests`.  
- `Flask` or `Django`: To create a simple server to receive webhook data. Installable via `pip install Flask` or `pip install Django`.  
- `Pandas`: For processing and analyzing time series data. Installable via `pip install pandas`.  
- `Matplotlib`: For visualizing the price trends and analysis results. Installable via `pip install matplotlib`.

This project provides a practical introduction to using Postmark's webhook capability and simple Python libraries to create a system for ingesting and analyzing real-time data.
