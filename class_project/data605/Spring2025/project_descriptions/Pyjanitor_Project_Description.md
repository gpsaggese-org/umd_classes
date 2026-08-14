### **Pyjanitor**

**Title**: Process Bitcoin Data Using Pyjanitor  
**Difficulty**: 1 (easy)

**Description**  
Pyjanitor is a Python library designed to simplify data cleaning tasks by providing convenient and intuitive functions. It extends the functionality of Pandas DataFrames, making it easier to perform data wrangling and preprocessing activities. The library includes methods for cleaning column names, filtering data, and handling missing values, which are commonly encountered challenges in data cleaning.

**Describe technology**

- Pyjanitor provides easy-to-use methods to clean and organize raw datasets, extending Pandas capabilities.  
- It allows you to perform operations such as:  
  - Removing and filling missing data  
  - Correcting string formatting in column headers  
  - Filtering and selecting data using expressive syntax  
  - Concatenating and merging DataFrames effortlessly  
- Pyjanitor is useful for data scientists and analysts who need a straightforward approach to data preprocessing.

**Describe the project**  
This project involves ingesting real-time Bitcoin price data from a public API, such as CoinDesk or CoinGecko, and using Pyjanitor to clean and process the data. The task consists of the following steps:

1. **Data Ingestion:**  
     
   - Use Python's `requests` library to fetch Bitcoin prices from the chosen API every 30 seconds to simulate real-time updates.  
   - Store the raw data in a Pandas DataFrame.

   

2. **Data Cleaning and Processing:**  
     
   - Use Pyjanitor to clean and organize the incoming data:  
     - Clean column names to ensure a consistent and readable format.  
     - Handle any missing values or invalid data points using Pyjanitor methods.  
     - Filter the dataset to focus on specific time intervals and relevant fields (e.g., timestamps and prices).

   

3. **Time Series Analysis:**  
     
   - Perform a simple time series analysis to visualize Bitcoin price trends.  
   - Implement basic statistics such as moving averages using Python's scientific libraries like `pandas` and `matplotlib`.

   

4. **Output and Visualization:**  
     
   - Output the cleaned data and basic statistical calculations to a CSV file.  
   - Generate visualizations to display trends in Bitcoin prices over time.

**Useful resources**

- [Pyjanitor Documentation](https://pyjanitor-devs.github.io/pyjanitor/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

**Is it free?**  
Yes, Pyjanitor is an open-source library and can be freely used and modified. The CoinGecko API is also freely accessible for basic queries, although rate limits apply.

**Python libraries / bindings**

- `pyjanitor`: Install using pip with `pip install pyjanitor`  
- `pandas`: Essential for DataFrame operations, install using `pip install pandas`  
- `requests`: For making HTTP requests to fetch data, install using `pip install requests`  
- `matplotlib`: For visualization, install using `pip install matplotlib`

This project offers hands-on experience with data cleaning and analysis using Pyjanitor, providing a practical understanding of handling real-time data in an accessible way.
