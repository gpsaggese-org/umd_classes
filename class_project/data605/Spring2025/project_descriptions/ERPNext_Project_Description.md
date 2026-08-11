### **ERPNext**

**Title**: Sales Trend Analysis and Reporting with ERPNext and Python  
**Difficulty**: 1 (Easy)

**Description**  
This project involves extracting sales data from ERPNext, analyzing trends using Python, and generating visual reports. Students will learn to interact with ERPNext's database/API and apply basic data analysis techniques.

**Describe Technology**

- **ERPNext**: Open-source ERP platform for managing business operations (sales, inventory, accounting).  
  1. Built on **Frappe Framework** (Python \+ MariaDB).  
  2. Use cases: Sales order tracking, inventory management, financial reporting.  
  3. Relevance: ERP systems are foundational for business data engineering.  
     

**Describe the Project**

1. **Set Up ERPNext (Local/Cloud)**:  
   - Install ERPNext locally or use a free cloud trial.  
   - Populate dummy sales data (e.g., 100+ sales orders with dates, items, prices).  
2. **Extract Data**:  
   - Option 1: Use ERPNext’s REST API (`requests` library) to fetch sales orders.  
   - Option 2: Directly query the MariaDB database with `pymysql` to extract sales data.  
3. **Analyze Sales Trends**:  
   - Clean data with `pandas` (e.g., handle missing values, format dates).  
   - Calculate metrics:  
     - Monthly revenue trends.  
     - Top-selling items.  
     - Customer purchase frequency.  
4. **Visualization**:  
   - Create bar charts (top-selling items) and line graphs (revenue trends) with `matplotlib`.  
   - Export results to a PDF report using `reportlab` or a Jupyter Notebook.

**Useful Resources**

- [ERPNext Documentation](https://docs.erpnext.com/)  
- [ERPNext REST API Guide](https://frappeframework.com/docs/user/en/api/rest)  
- [PyMySQL Tutorial](https://pynative.com/python-mysql-database-connection/)

**Is it free?**  
ERPNext is open-source (free for local use). Cloud trials are free for 14 days.

**Python Libraries / Bindings**

- `pandas` (data manipulation), `matplotlib` (visualization).  
- `requests` (API calls), `pymysql` (database connection).  
- `jupyter` (optional for interactive analysis).

-
