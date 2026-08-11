### **Kedro**

**Title:** Real-Time Bitcoin Price Analysis with Kedro

**Difficulty:** 1=easy

**Description**

Kedro is an open-source Python framework for creating reproducible, maintainable, and modular data science code. It is particularly useful for designing data pipelines by applying software engineering best practices. Understand the core concepts of Kedro like nodes, pipelines, and data catalog, which provide a structured approach to managing data, workflow, and experiment tracking.

**Describe technology**

- **Kedro**: This framework is designed to help data scientists and engineers create robust modular pipelines by enforcing a standard way to work with data. It promotes version control, environment management, and testing.  
- **Nodes and Pipelines**: Nodes are the building blocks in Kedro and each node represents a function. Pipelines are made up of nodes and define the order in which nodes should be executed.  
- **Data Catalog**: A feature of Kedro that catalogs all the datasets used and produced by the pipeline, which helps in data tracing and management.

**Describe the project**

- **Objective**: Use Kedro to build a simple pipeline that ingests real-time Bitcoin price data and performs a basic time series analysis, like moving averages.  
- **Data Source**: Pull real-time Bitcoin price data from a public API like CoinGecko.  
- **Steps**:  
  1. Set up a Kedro project and configure the environment.  
  2. Create a data catalog for managing the Bitcoin price data.  
  3. Implement the data ingestion node to fetch and store the Bitcoin price data.  
  4. Build a pipeline that reads the data, applies a moving average calculation as a simple time series analysis, and stores the results.  
  5. Set up version control for your Kedro project and ensure code quality with unit tests.  
- **Outcome**: By the end of the project, students should have a basic understanding of how to use Kedro to design data pipelines, while getting hands-on experience with time series analysis using Python.

**Useful resources**

- [Kedro Documentation](https://kedro.readthedocs.io)  
- [Kedro GitHub Repository](https://github.com/kedro-org/kedro)  
- [Python for Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

**Is it free?**

Yes, Kedro is an open-source project and free to use.

**Python libraries / bindings**

- **Kedro**: To create and run your data pipelines. Install it via `pip install kedro`.  
- **pandas**: For data manipulation and analysis, including computing moving averages. Install with `pip install pandas`.  
- **requests**: For fetching data from external APIs. Install with `pip install requests`.  
- **Pytest**: For unit testing your code within Kedro. Install with `pip install pytest`.

By working on this project, students will gain a foundational understanding of Kedro’s capabilities and how it can be used to streamline the data science workflow for real-time data analysis projects.
