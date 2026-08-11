### **Tableau**

**Title**: Analyze Bitcoin Trends Using Tableau

**Difficulty**: 1 (easy)

**Description**  
Tableau is a powerful data visualization tool used to simplify raw data into easy-to-understand, interactive visual forms. It's popular for helping users see and understand data through natural language queries, trend lines, and other visual reporting functionalities. This project introduces students to the basics of working with Tableau to perform time series analysis on real-time Bitcoin price data.

**Describe technology**

- Tableau enables users to quickly visualize data in an intuitive manner.  
- Key features include interactive dashboards, dynamic sorting, trends and predictive analysis, and varied graph types.  
- Drag-and-drop capability makes developing complex visualizations simple without extensive programming knowledge.  
- It connects to various data sources such as spreadsheets, relational databases, and cloud platforms, allowing flexible data integration.

**Describe the project**  
This easy one-week project involves using Tableau to visualize and analyze the historical price trends of Bitcoin. Students will fetch Bitcoin price data from a public API like CoinGecko using Python, creating a CSV file for later use in Tableau. The tasks include the following steps:

1. Use Python to regularly gather price data from a public Bitcoin API. Parse and store this data in CSV format.  
2. Import the CSV data into Tableau and clean it if necessary (e.g., handle missing values or outliers).  
3. Develop a series of time series visualizations using Tableau:  
   - Create basic line charts demonstrating Bitcoin’s price changes over time.  
   - Use Tableau’s built-in functionalities to calculate moving averages and add trend lines.  
   - Make dashboards to display different visualizations and facilitate easy trend analysis.  
4. Analyze data features such as price dips, peaks, and any noticeable seasonal or periodic patterns.

**Useful resources**

- [Tableau Official Website](https://www.tableau.com/)  
- [Tableau Public](https://public.tableau.com/s/) \- A free platform to visualize data and share insights online.  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Tableau Public can be utilized to perform all required tasks in this project for free, although it has limitations compared to the paid versions like Tableau Desktop.

**Python libraries / bindings**

- `requests`: This library will be used to fetch data from the Bitcoin API. Install it via `pip install requests`.  
- `pandas`: Useful for managing data within Python and converting it into CSV format. Install using `pip install pandas`.

This project serves as a practical introduction to using Tableau for data visualization with real-world cryptocurrency data, incorporating essential concepts in data ingestion, cleansing, and time series analysis.
