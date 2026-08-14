### **EconML**

**Title**: Bitcoin Time Series Analysis with EconML

**Difficulty**: 2 (medium difficulty)

**Description**  
In this project, students will explore the application of EconML, a Python library developed by Microsoft Research, for understanding and analyzing causal inference in economics. EconML is designed to interpret machine learning models to estimate causal effects in observational data. Students will leverage this library to perform a time series analysis on real-time Bitcoin price data. By the end of this project, students will gain hands-on experience with causal inference techniques, time series data manipulation, and the analysis of economic phenomena using Python.

**Describe technology**

- EconML: An open-source library for estimating heterogeneous treatment effects in Python based on methods from the field of causal inference.  
- Key Components:  
  - DML (Double Machine Learning) and DR (Doubly Robust) methods for causal effect estimation.  
  - Support for integrating with common machine learning tools such as scikit-learn.  
  - Ability to estimate and interpret causal effects in a variety of setups, particularly instrumental variable and panel data settings.

**Describe the project**

- **Objective**: Analyze real-time Bitcoin price data to identify causal relationships using EconML. The focus will be on understanding how various factors, potentially including market indicators or external economic data, impact Bitcoin prices.  
    
- **Steps**:  
    
  1. **Ingest Bitcoin Data**: Use a Python package like `requests` to fetch real-time Bitcoin price data from a public API (e.g., CoinGecko).  
  2. **Pre-process and Explore Data**: Utilize Pandas to clean and prepare the data, check time stamps, and remove any outliers or missing values.  
  3. **Apply EconML Models**: Implement EconML’s DML or DR learners to estimate the causal impact of one or more independent variables on Bitcoin prices over time.  
  4. **Time Series Analysis**: Leverage time-based features and analyze how causal effects vary over time. This may involve separating data into training and testing sets based on time, for example, pre- and post-event analysis.  
  5. **Results Interpretation**: Interpret the output of the model, examining causal effects and discussing potential real-world economic implications.

**Useful resources**

- EconML Documentation:   
- [https://econml.azurewebsites.net/](https://econml.azurewebsites.net/)  
- Tutorials and Examples: [https://github.com/py-why/EconML](https://github.com/py-why/EconML)  
- CoinGecko API Documentation: [https://www.coingecko.com/en/api](https://www.coingecko.com/en/api)

**Is it free?**  
Yes, EconML is an open-source package and freely available to use. However, any API queries may be subject to terms set by the data providers.

**Python libraries / bindings**

- `econml`: Install via pip (`pip install econml`) to access the library functionalities.  
- `pandas`: For data manipulation and preprocessing, install via pip (`pip install pandas`).  
- `requests`: To interact and fetch data from Bitcoin APIs.  
- `scikit-learn`: For integrating machine learning models with EconML. Install via pip (`pip install scikit-learn`).
