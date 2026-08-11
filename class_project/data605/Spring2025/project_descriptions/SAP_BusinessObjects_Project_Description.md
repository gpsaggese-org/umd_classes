### **SAP BusinessObjects**

**Title**: Real-time Bitcoin Data Analysis using SAP BusinessObjects

**Difficulty**: 1 (easy)

**Description**

This project will introduce students to SAP BusinessObjects, a suite of front-end applications that allow business users to view, sort, and analyze business intelligence data. In this project, students will focus on using SAP BusinessObjects alongside basic Python packages to implement a real-time data ingestion system for Bitcoin price analysis. The goal is to showcase the capabilities of SAP BusinessObjects in integrating and visualizing Bitcoin time-series data, providing students with an understanding of its basic functionalities without overwhelming them with complex setups.

**Describe Technology**

- *SAP BusinessObjects*: A comprehensive business intelligence suite that offers tools for reporting, data visualization, and analytics. It is designed to take data from various sources and present it in a user-friendly graph, chart, or report format.  
- Core functionalities include:  
  - **Reporting**: Create pixel-perfect, rich reports that cater to diverse business needs.  
  - **Dashboards**: Build interactive dashboards for a real-time view of business performance.  
  - **Data Visualization**: Utilize intuitive visualizations to discover insights and make informed decisions.  
  - **Ad-hoc Queries**: Generate insights on demand with self-service querying tools.

**Describe the Project**

- **Objective**: Use SAP BusinessObjects to visualize real-time Bitcoin prices and conduct a basic time-series analysis.  
- **Steps Involved**:  
  1. **Data Ingestion with Python**: Utilize Python to fetch real-time Bitcoin data from a public API such as CoinGecko.  
  2. **Data Storage**: Store the fetched data in a simple CSV format which SAP BusinessObjects can access.  
  3. **Connect SAP BusinessObjects**: Import the stored Bitcoin data into SAP BusinessObjects for reporting and visualization.  
  4. **Create Reports and Dashboards**: Use the reporting and dashboard features of SAP BusinessObjects to visualize Bitcoin price trends.  
  5. **Basic Time-Series Analysis**: Implement a simple time-series analysis to identify and visualize patterns in the Bitcoin data over time, such as moving averages.  
- **Outcome**: Understand how SAP BusinessObjects can be leveraged for real-time data integration and visualization, providing insights into Bitcoin price movements efficiently.

**Useful Resources**

- [SAP BusinessObjects Overview](https://www.sap.com/products/technology-platform/bi-platform.html)  
- [Getting Started with SAP BusinessObjects](https://help.sap.com/doc/85513bb7cec348c8ad353cab52e87822/4.3.2/en-US/webi43sp2_getting_started_en.pdf)  
- [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)

**Is it Free?**

SAP BusinessObjects is a commercial product and requires a valid license for use. However, students may use a trial version or access the software through institutional licensing provided by their college or university.

**Python Libraries / Bindings**

- *requests*: For making HTTP requests to fetch real-time Bitcoin data.  
- *pandas*: For manipulating and storing data in a CSV format suitable for SAP BusinessObjects.  
- *matplotlib/plotly*: For preliminary data visualization (if needed) before importing to SAP BusinessObjects.
