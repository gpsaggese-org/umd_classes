### **Bokeh**

**Title**: Visualizing Real-Time Bitcoin Prices Using Bokeh

**Difficulty**: 1 (Easy)

**Description**

Bokeh is an interactive visualization library for Python that enables you to create elegant and informative graphics for both the web and output files. It is designed to provide high-performance visual presentation of large datasets in a concise format.

In this project, students will use Bokeh to visualize real-time Bitcoin price data. The goal is to create an interactive dashboard that displays live Bitcoin prices using time series plotting. Students will gain experience in using Bokeh for data visualization and learn the basics of ingesting and processing real-time data from a public API.

**Describe technology**

- Bokeh allows you to build interactive plots, dashboards, and data applications.  
- It supports a variety of charts, including scatter, line, bar, and area plots, with interactive widgets.  
- Bokeh can integrate with other Python libraries such as Pandas for data manipulation, allowing seamless operations on dataframes.  
- It provides real-time streaming capabilities via its server, ideal for live data visualization tasks.  
- Output options include static HTML files or integration with Flask/Django for web applications.

**Describe the project**

1. **Data Ingestion**: Use Python to connect to a public API such as CoinDesk's Bitcoin Price Index API to fetch real-time Bitcoin prices.  
     
2. **Data Processing**: Process the incoming JSON data using basic Python libraries to convert it into a Pandas DataFrame for easier manipulation and analysis.  
     
3. **Visualization Using Bokeh**:  
     
   - Setup a Bokeh server application to handle the live data stream.  
   - Create a simple time series line plot of Bitcoin prices that updates in real-time.  
   - Add interactive features such as date range filtering, hover tooltips to display exact price points, and zoom/pan capabilities.  
   - Customize the plot with themes, labels, and legends to enhance readability and aesthetics.

   

4. **Deployment**: Deploy the Bokeh server locally or, optionally, integrate it into a web application using Flask for a more complete dashboard experience.

**Useful resources**

- [Bokeh Official Documentation](https://docs.bokeh.org/en/latest/)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [CoinDesk API Documentation](https://www.coindesk.com/coindesk-api)

**Is it free?**

Yes, Bokeh is an open-source library and is free to use. Accessing public APIs like CoinDesk may also be free, but be sure to check any usage limitations or subscription models.

**Python libraries / bindings**

- `bokeh`: For creating the visualization and setting up the server for real-time updates.  
- `pandas`: For data manipulation and preparation.  
- `requests`: For making HTTP requests to retrieve data from the Bitcoin API.

Installation can be done using `pip install bokeh pandas requests`.
