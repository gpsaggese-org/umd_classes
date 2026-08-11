### **Dolibarr**

**Title**: Real-Time Bitcoin Analysis with Dolibarr  
**Difficulty**: 2 (Medium)

**Description**  
Dolibarr is an open-source ERP and CRM software that integrates seamlessly with various data sources and can be customized to fit a range of business needs. It is well known for its modular design, allowing users to add specific functionalities required for their operations. Though typically used for business management, Dolibarr can be adapted for big data applications, including ingesting and processing real-time data streams, such as Bitcoin price data. For this project, students will explore Dolibarr's capabilities by implementing a system that captures, processes, and analyzes real-time Bitcoin prices.

**Describe technology**

- **Core Features**: Dolibarr offers a user-friendly interface for managing business operations, with modules available for accounting, sales, CRM, inventory, and more.  
- **Modular Design**: The platform is built to be highly modular, allowing users to add only the functionalities they need. Modules can be easily developed or customized to extend the system's capabilities, making it versatile for tasks beyond traditional ERP functionalities.  
- **Customization**: Dolibarr can be extended with custom modules to process and analyze financial data, which makes it an intriguing choice for time series analysis projects.  
- **Real-time Data Handling**: Though not originally designed for big data handling, Dolibarr can be integrated with external scripts and APIs to accommodate real-time data processing.

**Describe the project**

- **Objective**: Develop a module within Dolibarr to handle the ingestion and processing of Bitcoin price data in real-time. Extend its CRM module features to store Bitcoin transaction data.  
- **Data Source**: Utilize a public API, such as CoinGecko, to fetch real-time Bitcoin data.  
- **Data Storage**: Use Dolibarr’s extensible database structure to store Bitcoin prices, handling updates or additions for each price change.  
- **Time Series Analysis**: Implement time series analysis features within Dolibarr by creating a new module or integrating external Python scripts. Analyze trends, compute moving averages, and visualize price changes over time.  
- **User Interface**: Create a dashboard within Dolibarr to display real-time data and analysis results, making use of the platform's existing UI capabilities.

**Useful resources**

- [Dolibarr Official Website](https://www.dolibarr.org/)  
- [Dolibarr GitHub Repository](https://github.com/Dolibarr/dolibarr)  
- [Dolibarr Module Development Documentation](https://wiki.dolibarr.org/index.php/Module_development)

**Is it free?**  
Yes, Dolibarr is open-source and free to use. It is distributed under the GNU General Public License (GPL), which allows for free use, modification, and distribution of the software.

**Python libraries / bindings**

- **Requests**: To handle API calls for real-time Bitcoin price data.  
- **Pandas**: Useful for handling data analysis and manipulation tasks.  
- **Matplotlib/Plotly**: For visualization of time series data within Dolibarr’s dashboard.  
- **SQLite3/MySQL Connector**: Depending on the database setup, these libraries can be used to directly interact with Dolibarr’s database for storing and retrieving Bitcoin data.
