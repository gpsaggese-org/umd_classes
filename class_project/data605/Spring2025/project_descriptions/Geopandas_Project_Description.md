### **Geopandas**

**Title**: Visualizing Bitcoin Price Trends Using Geopandas

**Difficulty**: 1 (easy)

**Description**  
This project involves creating a simple system for ingesting real-time Bitcoin price data and visualizing it using Geopandas, which is a Python library specifically designed for handling geospatial data. Geopandas extends the data types used by pandas to allow spatial operations on geometric types. This task will guide students through the basics of Geopandas and how it can be used to visualize data in a geographic context.

**Describe technology**

- **Geopandas** is a Python library that makes working with geospatial data in Python easier. It extends the capabilities of pandas to support spatial data operations.  
- Geopandas allows you to read common geospatial file formats including ESRI shapefile, GeoJSON, TopoJSON, and others using the `geopandas.read_file()` function.  
- Once data is imported, Geopandas provides powerful operations for data analysis such as spatial joins, geometric manipulations, and data visualization.

**Describe the project**

- **Objective**: To design a system that ingests real-time Bitcoin price data and visualizes daily trends on a map using Geopandas.  
- **Data Ingestion**  
  - Use an API like CoinGecko to fetch the real-time Bitcoin price data. You will use Python requests library to handle the API requests.  
- **Data Processing**  
  - Store the extracted data in a convenient format using pandas DataFrames.  
  - Perform simple data manipulation to format timestamps and calculate required metrics like moving averages.  
- **Data Visualization**  
  - Utilize Geopandas to plot a geographic visualization of Bitcoin price changes.  
  - For simplicity, you will visualize the data as a simple time series overlay on a geographic plot (though not typically geospatial, this is an exercise in using Geopandas and plots).  
  - Enhance the plot with matplotlib to show time series trends of Bitcoin prices over a specific period.

**Useful resources**

- [Geopandas Documentation](https://geopandas.org/)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
- [Python Requests Documentation](https://docs.python-requests.org/en/master/)  
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

**Is it free?**  
Yes, Geopandas is an open-source library. CoinGecko's API also provides a free tier suitable for educational projects.

**Python libraries / bindings**

- **Geopandas** for geospatial data manipulation and visualization. Install using `pip install geopandas`.  
- **Pandas** for general data manipulation and analysis. Install using `pip install pandas`.  
- **Matplotlib** for creating static, interactive, and animated plots. Install using `pip install matplotlib`.  
- **Requests** for making HTTP requests to call the CoinGecko API. Install using `pip install requests`.
