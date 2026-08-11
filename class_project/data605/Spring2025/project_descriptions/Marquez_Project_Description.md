### **Marquez**

**Title:** Tracking and Visualizing Bitcoin Transaction Lineage with Marquez​

**Difficulty:** 2 (Medium)

**Description:** 

In this project, students will leverage Marquez, an open-source metadata management service, to track and visualize the lineage of Bitcoin transaction data. The project involves ingesting Bitcoin transaction data from a public API, processing and storing this data, and utilizing Marquez to monitor data flow and transformations. This hands-on experience will introduce students to data lineage concepts, metadata management, and the importance of data governance in the context of cryptocurrency transactions.

**Describe Technology:** 

Marquez is an open-source metadata service designed for the collection, aggregation, and visualization of a data ecosystem's metadata. It maintains the provenance of how datasets are consumed and produced, provides global visibility into job runtime and dataset access frequency, and centralizes dataset lifecycle management.Marquez enables highly flexible data lineage queries across all datasets, efficiently associating dependencies between jobs and the datasets they produce and consume. 

**Describe the Project:**

**Objective:** To monitor, process, and visualize the lineage of Bitcoin transaction data using Marquez.​

**Steps:**

1. **Data Ingestion:** Utilize a public Bitcoin API (such as CoinGecko) to fetch real-time transaction data in JSON format.​  
2. **Data Processing:** Parse the JSON response to extract relevant transaction details, including transaction IDs, timestamps, input and output addresses, and amounts.​  
3. **Data Storage:** Store the processed transaction data in a database (e.g., PostgreSQL) for further analysis and lineage tracking.​  
4. **Marquez Integration:**  
   * **Metadata Collection:** Implement Marquez's metadata API to collect metadata about the data sources, transformations, and outputs related to the Bitcoin transaction data.  
   * **Lineage Tracking:** Use Marquez to track the lineage of the transaction data as it flows through various processing stages, ensuring transparency and traceability.​  
5. **Data Visualization:** Utilize Marquez's web user interface to visualize the data lineage, showing the interdependencies between datasets and the transformations applied to the Bitcoin transaction data.​  
6. **Automation:** Develop a Python script to automate the data ingestion, processing, and metadata collection processes, ensuring continuous tracking and updating of data lineage.​

**Useful Resources:**

* [Marquez Documentation](https://marquezproject.ai/)  
* [CoinGecko API Documentation](https://docs.coingecko.com/v3.0.1/reference/introduction)  
* [Marquez GitHub Repository](https://github.com/MarquezProject/marquez)

**Is it Free?** 

Marquez is an open-source project released under the Apache 2.0 license, making it free to use and modify.CoinGecko also offers a free tier for their API, which should be sufficient for educational and small-scale projects.​

**Python Libraries / Bindings:**

* **Requests:** To make HTTP requests for fetching Bitcoin transaction data from the API.​  
* **psycopg2:** To interact with the PostgreSQL database for storing transaction data.​  
* **Marquez Python Client:** For interacting with the Marquez API to collect and manage metadata.​  
* **Schedule:** To assist with running the script at regular intervals for continuous data ingestion and processing.

This project offers students practical experience in data governance and lineage tracking within the cryptocurrency domain, highlighting the significance of metadata management in ensuring data quality and transparency.​
