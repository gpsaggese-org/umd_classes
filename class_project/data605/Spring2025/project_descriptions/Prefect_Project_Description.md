### **Prefect**

**Title**: Real-Time Bitcoin Price Analysis using Prefect

**Difficulty**: 3 (difficult)

**Description**  
This project involves using Prefect, a modern workflow orchestration tool, to ingest, process, and analyze real-time Bitcoin price data. Prefect’s core features revolve around the design, monitoring, and scheduling of data workflow tasks. In this project, students will learn how to harness Prefect to implement a dynamic ETL (Extract, Transform, Load) pipeline for Bitcoin data and perform time series analysis. The project simulates a real-world scenario where continuous data ingestion, data quality checks, and advanced data processing are integral for generating actionable insights from financial data.

**Describe technology**

- **Prefect**: Prefect is a workflow management system that allows developers to build and deploy data pipelines with ease and flexibility. It is designed to improve data reliability by providing visibility over data workflows and allowing for complex dependency management. Prefect includes features like dynamic scheduling, ad-hoc parameterized runs, error notifications, and flow visualization.  
- **Core Concepts**:  
  - **Flow**: The top-level object representing your entire Prefect process, which consists of tasks.  
  - **Task**: The building block of a workflow that performs a single unit of work.  
  - **Executor**: Executes tasks within a flow, allowing for parallel and distributed execution.  
- **Example Use Cases**:  
  - Defining and scheduling tasks for executing Python functions.  
  - Triggering conditional workflows based on task outputs.  
  - Handling retries and rollbacks for failed tasks.

**Describe the project**

1. **Ingest Real-Time Bitcoin Data**:  
   - Utilize a Bitcoin API (e.g., CoinGecko) to fetch live Bitcoin price data.  
   - Set up a Prefect flow to poll this API every few minutes.  
2. **Data Collection**:  
   - Use Prefect tasks to systematically extract, transform, and load Bitcoin data into a database (e.g., PostgreSQL).  
   - Implement data validation checks within Prefect to ensure data quality.  
3. **Data Processing and Analysis**:  
   - Transform the raw data into a format suitable for analysis using basic Python packages such as pandas.  
   - Implement Prefect tasks for time series analysis, such as calculating moving averages or volatility.  
4. **Monitoring and Alerts**:  
   - Create Prefect sensors to monitor significant price movements and notify stakeholders via email or Slack.  
5. **Visualization**:  
   - Integrate with visualization tools (e.g., Matplotlib or Plotly) to graph Bitcoin price trends and analysis results.  
6. **Testing and Debugging**:  
   - Utilize Prefect's debugging features to test and troubleshoot the workflows.

**Useful resources**

- [Prefect Documentation](https://docs.prefect.io/)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [Plotly Documentation](https://plotly.com/python/)

**Is it free?**

- Prefect Core is open-source and free to use. Prefect Cloud, which provides additional capabilities (e.g., a hosted dashboard), may incur costs.

**Python libraries / bindings**

- **Prefect**: `pip install prefect` \- For designing and executing workflows.  
- **Requests**: `pip install requests` \- For making requests to the Bitcoin API.  
- **Pandas**: `pip install pandas` \- For data manipulation and time series analysis.  
- **SQLAlchemy**: `pip install sqlalchemy` \- For interfacing with databases.  
- **Matplotlib/Plotly**: `pip install matplotlib plotly` \- For data visualization.
