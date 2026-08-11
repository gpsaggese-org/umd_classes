### **DoWhy**

**Title**: Real-Time Bitcoin Causal Analysis with DoWhy  
**Difficulty**: 2 (medium)

**Description**:

- Build a Python-based big data system that continuously ingests real-time Bitcoin price data and applies causal inference techniques using DoWhy.  
- The project aims to evaluate the impact of market events on Bitcoin prices by defining causal relationships and testing their robustness.  
- Designed to be completed in around 10 days, it challenges students to integrate streaming data ingestion, time series processing, and causal inference.

**Describe technology**:

- **DoWhy Library**:  
  - A Python package for causal inference that combines graphical models with the potential outcomes framework to estimate treatment effects.  
  - Allows users to define causal models using directed acyclic graphs (DAGs) and perform counterfactual analysis.**DoWhy**  
  -   
  - Supports various refutation tests to assess the reliability of causal conclusions.  
- **Example Usage**:  
  - Use DoWhy to model the effect of a regulatory announcement or major market event on Bitcoin prices, comparing pre-event and post-event periods while controlling for confounding variables.

**Describe the project**:

- **Data Ingestion**:  
  - Create a Python module to fetch real-time Bitcoin price data from a public API (e.g., CoinGecko) using libraries like `requests` or `websockets`.  
- **Data Processing**:  
  - Utilize pandas to clean and format the streaming data into a structured time series format suitable for analysis.  
- **Causal Model Setup**:  
  - Define the causal model by identifying the treatment (e.g., a market event), the outcome (Bitcoin price changes), and potential confounders (such as trading volume or market sentiment).  
- **Application of DoWhy**:  
  - Estimate the causal effect of the identified event on Bitcoin prices using DoWhy’s causal inference methods.  
  - Run refutation tests to validate the causal assumptions and robustness of the estimated effects.  
- **Visualization and Reporting**:  
  - Generate visualizations of the time series data and the inferred causal relationships using matplotlib or seaborn.  
  - Compile a report summarizing the causal analysis, including the defined causal graph, treatment effect estimates, and validation results.

**Useful resources**:

- [DoWhy Documentation](https://github.com/py-why/dowhy)  
- [pandas Documentation](https://pandas.pydata.org/docs/)  
- [matplotlib Documentation](https://matplotlib.org/stable/contents.html)  
- [CoinGecko API Documentation](https://www.coingecko.com/en/api)

**Is it free?**:

- Yes, the project uses open-source Python libraries and free-access APIs. DoWhy is available under an open-source license.

**Python libraries / bindings**:

- **DoWhy**: For causal inference and modeling.  
- **pandas**: For data ingestion, cleaning, and time series processing.  
- **matplotlib / seaborn**: For data visualization.  
- **requests**: For fetching real-time Bitcoin data.  
- **websockets** (optional): For handling streaming data if needed.
