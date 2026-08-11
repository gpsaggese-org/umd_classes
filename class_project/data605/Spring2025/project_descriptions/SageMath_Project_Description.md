### **SageMath**

**Title**: Analyzing Bitcoin Time Series with SageMath

**Difficulty**: 3 (Difficult \- it should take around 14 days to complete)

**Description**:  
SageMath is an open-source mathematics software system that integrates a wide range of mathematics-related packages and functionalities into a unified Python-based interface. It provides extensive tools for symbolic mathematics, numerical computations, data visualization, algebra, calculus, and much more. For this project, students will leverage SageMath’s capabilities to ingest, process, and analyze real-time Bitcoin price data, focusing on time series analysis.

**Describe technology**:

- **SageMath**: A powerful mathematical software built on Python, combining many existing open-source packages into a common interface. It covers many aspects of mathematics, such as algebra, calculus, and discrete mathematics.  
- **Capabilities**:  
  - Symbolic computation using SymPy, a symbolic mathematics library.  
  - Data visualization using matplotlib and other related plotting libraries.  
  - Advanced mathematical algorithms and functions accessible through an intuitive interface.  
- **Use Cases**:  
  - Complex mathematical modeling and simulations.  
  - Statistical analysis and probability calculations.  
  - Educational purposes for teaching advanced mathematics and computations.

**Describe the project**:

- **Objective**: Implement a real-time data ingestion pipeline for Bitcoin price data using SageMath, followed by an in-depth time series analysis with focus on pattern identification and prediction.  
    
- **Steps**:  
    
  1. **Data Ingestion**: Set up a Python script to fetch real-time Bitcoin price data from a public API (e.g., CoinGecko). Implement a mechanism to store the captured data in an SQLite database or a CSV file for local storage and retrieval.  
       
  2. **Preprocessing**: Utilize SageMath to clean and preprocess the ingested data, handling missing values and smoothing out noise in the series.  
       
  3. **Exploratory Data Analysis**: Use SageMath's visualization tools to plot the time series data, identifying trends, seasonality, and any anomalies present in the dataset.  
       
  4. **Time Series Modeling**: Apply advanced time series models, such as ARIMA or Exponential Smoothing, for forecasting future Bitcoin prices. Students will explore parameter tuning and model validation within SageMath, utilizing its strong support for mathematical operations and modeling.  
       
  5. **Visualization and Reporting**: Create detailed plots and reports that encompass findings from the data analysis and modeling phases. This includes predictions, model accuracy, and insights derived from the data.

**Useful resources**:

- [SageMath Documentation](https://doc.sagemath.org/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it free?**  
Yes, SageMath is open-source and free to use.

**Python libraries / bindings**:

- **SageMath**: Provides extensive functionality for mathematics; install using instructions from the [SageMath Install Guide](https://www.sagemath.org/download.html).  
- **SymPy**: For symbolic mathematics; install via `pip install sympy`.  
- **matplotlib**: For data visualization; install using `pip install matplotlib`.  
- **pandas**: To handle data structures like DataFrames; one can install it with `pip install pandas`.  
- **requests**: For HTTP requests to fetch data from APIs; can be installed via `pip install requests`.  
- **SQLite3 or csv**: For data storage, both of which are part of the Python standard library.
