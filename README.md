# 📦 NexMart Data Assessment

This project analyzes and improves the quality of product data from NexMart. The goal is to clean, validate, and assess product information to ensure it's optimized for internal operations for better decision making across various stakeholders like Sales, Product, etc.

## 🛠 What the Code Does

### 1. Loads the Data
Reads three raw CSV files:
- `manufacturers.csv`
- `product_descriptions.csv`
- `product_properties.csv`

### 2. Cleans the Data
- Replaces common bad values (`N/A`, `null`, `'`, empty strings, etc.) with `NaN`
- Trims whitespace from string fields

### 3. Combines the Datasets
- Merges the data using:
  - `Article Number`
  - `Manufacturer number`
- Only records with valid join keys are retained

### 4. Checks Data Completeness
- Flags whether each product is **complete** (no missing fields among key ones)
- Adds a field for **Missing Fields Count**

### 5. Assesses Data Quality

A product is labeled **"good quality"** only if:
- It has a valid **description**, determined using fallback logic (see below)
- It includes a valid **EAN** (European Article Number)
- It includes a valid image in **Picture normal reduced**
- It includes **Technical detail**

If **any** of these fields are missing, the product is labeled as **"bad quality"**. This stricter logic ensures high-quality listings that are usable across internal teams.

## 🧠 Description Logic

To determine if a product has a valid description, the following fallback logic is used:
1. Use `Short description` if available
2. If not, fall back to `Short description 2`
3. If still unavailable, use `Long description`

This cascading logic ensures every product gets the best available description, even if some fields are empty or inconsistently used.

## 🔍 Why This Matters

### Internal Benefits:
- **Product Teams** can quickly identify and fix incomplete or low-quality product records
- **Marketing & E-commerce** teams get more reliable listings to work with
- **Support & Fulfillment** staff benefit from clearer product identifiers and visuals
- **Data Teams** can track trends in quality for reporting, QA, and tooling

## 🧾 Why EAN Is Important for Internal Stakeholders

The EAN (European Article Number) is a critical internal field because:
- It acts as a **unique identifier** across internal tools, warehouses, and databases
- Ensures **accurate matching** of product information in ERP and inventory systems
- Enables reliable **linking of internal records** to suppliers, retailers, and pricing tools
- Missing EANs lead to **data duplication** and operational inconsistencies
- Teams in **logistics, fulfillment, procurement**, and even **customer support** depend on it

## 🖼️ Why `Picture normal reduced` Is Important

The `Picture normal reduced` field provides optimized product images:
- Enables **quick product recognition** by internal teams
- Supports **faster manual reviews and categorization**
- Makes internal dashboards more **navigable and informative**
- Ensures consistent image availability for **training sets and demos**

## 🛠️ Importance of `Technical Details`

Technical details are essential because:
- Ensure **accuracy in operations** for procurement and logistics
- Help **product differentiation** for sales and marketing
- Enable **efficient support** with accurate technical information
- Contribute to **data consistency** across systems
- Empower **better decision-making** with reliable information

## ❌ Why ETIM Was Excluded

ETIM (European Technical Information Model) was excluded because:
- Focus is on **internal product readiness**, not external alignment
- Limited relevance for internal completeness checks
- Other fields have more direct business impact for internal users

# 📁 Output Files

## 📊 Cleaned Data Files

| File Name | Description |
|-----------|-------------|
| `merged_data_with_completeness_final.csv` | Full dataset with completeness indicators |
| `good_quality_data_final.csv` | Products with full, high-quality data |
| `bad_quality_data_final.csv` | Products missing key fields |

## 🗃️ SQL Query Output Files

| File Name | Description |
|-----------|-------------|
| `sqlquery1.1_mostimproved.csv` | Manufacturers with most improved quality |
| `sqlquery1.2_Manufacturer_quality.csv` | Detailed manufacturer quality view |
| `sqlquery2_field_completion_rates.csv` | Field-wise completion rate analysis |
| `sqlquery3.1_EANvsquality.csv` | EAN completeness vs product quality |
| `sqlquery3.2_missing_combinations.csv` | Missing key combinations across fields |

## 📄 Documentation

| File Name | Description |
|-----------|-------------|
| `sqlqueryexplanation.docx` | Explanation of all SQL queries |

## 📋 Project Dependencies (`requirements.txt`)

### Core Requirements
- `pandas`
- `numpy`
- `sqlite3`

## 🛠️ Execution 

This repository contains a data processing pipeline for analyzing product data. The main script, `Updated_NexMart_datapipelineandSql.py`, processes, merges, cleans, and analyzes product datasets to assess the completeness and quality of product descriptions.

## Prerequisites

To run this project, ensure that you have the following installed on your system:

- Python 3.x
- pip (Python package installer)
- [Visual Studio Code](https://code.visualstudio.com/) (VS Code)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sharmaankit4292/NexMart.git
    cd NexMart
    ```

2. Install the required Python libraries:

    It is recommended to use a virtual environment for managing dependencies. You can create and activate a virtual environment using the following commands:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

    Then install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    **Note**: If `requirements.txt` is not present in the repo, you can manually install the dependencies with:

    ```bash
    pip install pandas numpy sqlite3
    ```

## Setting Up in Visual Studio Code

1. **Open the Project in VS Code**:  
   After cloning the repository, you can open the project in Visual Studio Code by running:

    ```bash
    code .
    ```

   This will open the project in VS Code.

2. **Python Extension**:  
   Make sure to install the [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python) if you haven't already. This extension provides features like IntelliSense, code linting, debugging, and more.

3. **Configure the Python Environment**:  
   In VS Code, select the virtual environment as the Python interpreter for the project:

   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
   - Type `Python: Select Interpreter` and select the virtual environment you created earlier (e.g., `./venv`).

4. **Run the Script in VS Code**:  
   You can run the `Updated_NexMart_datapipelineandSql.py` script directly from VS Code:

   - Open the `Updated_NexMart_datapipelineandSql.py` file.
   - Click the **Run** button at the top-right of the editor or use the shortcut `F5` to run the script.

## File Structure

- `data/`: Directory containing raw CSV files such as `manufacturers.csv`, `product_descriptions.csv`, and `product_properties.csv`.
- `updated_pipeline.py`: The main script for processing and analyzing the product data.

## How to Execute

- Ensure that the required data files (`manufacturers.csv`, `product_descriptions.csv`, and `product_properties.csv`) are placed in the `data/` directory.

- Run the pipeline:

    ```bash
    python Updated_NexMart_datapipelineandSql.py
    ```

 - The script will:
    - Load the datasets
    - Clean and preprocess the data
    - Merge the datasets based on common fields
    - Analyze the data for completeness and description quality
    - Export the results to CSV files in the `data/` directory

### Output Files:
- `merged_data_with_completeness_final.csv`: Contains the merged data with completeness metrics.
- `good_quality_data_final.csv`: Contains products with "good" description quality.
- `bad_quality_data_final.csv`: Contains products with "bad" description quality.
- Additional CSV files from SQL queries, such as `Manufacturer_quality.csv`, `field_completion_rates.csv`, and others.

### 🛠️ Setup Instructions
1. Install Python 3.6 or later
2. Run: `pip install -r requirements.txt`
3. Execute: `python src/Updated_NexMart_datapipelineandSql.py`

## 🛠️ Improvements Made During Additional Time

To enhance the workflow, I created a dedicated branch named **`dev`** using Visual Studio Code.  
In this branch, I improved the **print statement formatting** for better readability across outputs.  
After committing the changes, I pushed the branch to the repository and created a **Pull Request**.  
This ensures a clean and traceable development history for better collaboration and tracking.  
🔗 [View Pull Request #1 – NexMart Repository](https://github.com/sharmaankit4292/NexMart/pull/1)


## 🚀 Bonus: Ideas for Production Readiness

- **Add Unit Tests**: Ensure critical parts of the pipeline are tested automatically, improving reliability and reducing bugs.
- **Track Data Quality History**: Implement versioning for data quality metrics over time to track improvements or regressions.
- **Use Config Files**: Parameterize the pipeline using configuration files for better flexibility and easier environment changes.
- **Design Modular ETL Pipeline**: Break down the pipeline into smaller, reusable modules for better maintainability and scalability.
- **Separate Environments (Dev/Test/Prod)**: Set up separate environments for development, testing, and production to ensure stable deployments.
- **Implement CI/CD Pipelines**: 
  - Set up **Continuous Integration/Continuous Deployment (CI/CD)** pipelines to automate testing and deployment. 
  - Use services like GitHub Actions, GitLab CI, or Jenkins to trigger tests and deployments on code changes.
- **Apply Row-Level Security**: Protect sensitive data by applying security rules at the row level within the data warehouse or database, ensuring only authorized users can view certain rows of data.

## 📈 Next Steps: Power BI Dashboard
Use `merged_data_with_completeness_final.csv` to create dashboard showing:
- Manufacturer performance
- Manufacturers with missing fields
- DAX calculations for gaps (see `Dax code & Explanation.txt`)

## ✅ Summary
Improving data quality will lead to:
- Enhanced product listings which directly affects the sales
- Streamlined internal operations
- Data-driven decision-making
