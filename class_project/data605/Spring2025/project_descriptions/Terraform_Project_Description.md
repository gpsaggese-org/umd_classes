### **Terraform**

**Title:** Local Bitcoin Price Data Processing with Terraform​

**Difficulty:** 1 (Easy)

**Description:** In this project, students will utilize Terraform, an open-source infrastructure as code (IaC) tool by HashiCorp, to automate the setup of a local environment for ingesting and processing Bitcoin price data. By leveraging Terraform's capabilities, students can define and manage infrastructure components locally without the need for a cloud provider. This project offers a hands-on introduction to Terraform's functionalities in a local setting, focusing on data ingestion, processing, and storage using Python.​

**Describe Technology:**

* **Terraform:**  
  * A declarative IaC tool that allows users to define infrastructure components in configuration files using HashiCorp Configuration Language (HCL).​  
  * Supports various providers, including local resources, enabling infrastructure management without external cloud services.​  
  * Features such as execution plans and a dependency graph facilitate safe and efficient infrastructure changes.​

**Describe the Project:**

**Objective:** Use Terraform to provision a local environment for ingesting and processing Bitcoin price data using Python.​

**Steps:**

1. **Set Up Terraform:**  
   * Install Terraform on your local machine by downloading the appropriate binary and adding it to your system's PATH.​  
2. **Provision Local Resources:**  
   * Write Terraform configurations to create local resources, such as directories for data storage and local files for logging.​  
   * Utilize Terraform's `local_file` resource to manage local files.​  
3. **Ingest Bitcoin Data:**  
   * Develop a Python script that fetches real-time Bitcoin price data from a public API (e.g., CoinGecko) at regular intervals.​  
   * Store the retrieved data in the provisioned local directories.​  
4. **Process Data:**  
   * Implement basic time series analysis using Python libraries to preprocess the ingested data, such as calculating moving averages or identifying trends.​  
5. **Automate with Terraform:**  
   * Use Terraform's `null_resource` with `local-exec` provisioner to automate the execution of the Python scripts, ensuring data ingestion and processing occur at defined intervals.

**Useful Resources:**

* [Terraform Official Documentation](https://developer.hashicorp.com/terraform/docs)  
* [CoinGecko API Documentation](https://www.coingecko.com/en/api)  
* [Python `pandas` Library Documentation](https://pandas.pydata.org/docs/)

**Is it Free?**

Yes, Terraform is free and open-source. Accessing real-time data from CoinGecko's API is also free, though there may be rate limits or usage terms to consider.​

**Python Libraries / Bindings:**

* **`requests`:** For making HTTP requests to the Bitcoin pricing API (`pip install requests`).​  
* **`pandas`:** For data manipulation and time series analysis (`pip install pandas`).​  
* **`schedule`:** For scheduling the data fetching at regular intervals (`pip install schedule`).​

This project guides students through the basics of Terraform for local infrastructure management while utilizing Python for data processing, offering a practical approach to Infrastructure as Code in the context of real-time data handling.​
