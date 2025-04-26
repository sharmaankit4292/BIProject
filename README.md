# 📦 NexMart Data Assessment

This project analyzes and improves the quality of product data from NexMart. The goal is to clean, validate, and assess product information to ensure it’s optimized for internal operations. Hence for better decision making accross various stakeholders like Sales, Product etc.

---

## 🛠 What the Code Does

### 1. Loads the Data
Reads three raw CSV files:
- `manufacturers.csv`
- `product_descriptions.csv`
- `product_properties.csv`

### 2. Cleans the Data
- Replaces common bad values (`N/A`, `null`, `'`, empty strings, etc.) with `NaN`.
- Trims whitespace from string fields.

### 3. Combines the Datasets
- Merges the data using:
  - `Article Number`
  - `Manufacturer number`
- Only records with valid join keys are retained.

### 4. Checks Data Completeness
- Flags whether each product is **complete** (no missing fields among key ones).
- Adds a field for **Missing Fields Count**.

### 5. Assesses Data Quality

A product is labeled **"good quality"** only if:
- It has a valid **description**, determined using fallback logic (see below).
- It includes a **valid EAN** (European Article Number).
- It includes a valid image in **Picture normal reduced**.
- It includes a **Technical detail**.

If **any** of these fields are missing, the product is labeled as **"bad quality"**. This stricter logic ensures high-quality listings that are usable across internal teams.

---

## 🧠 Description Logic

To determine if a product has a valid description, the following fallback logic is used:
1. Use `Short description` if available.
2. If not, fall back to `Short description 2`.
3. If still unavailable, use `Long description`.

This cascading logic ensures every product gets the best available description, even if some fields are empty or inconsistently used. It reduces noise in quality scoring and helps the business work with the most informative version of each product description.

This approach is critical to maintaining consistent quality metrics, especially when aggregating or displaying products internally.

---

## 🔍 Why This Matters

### Internal Benefits:
- **Product Teams** can quickly identify and fix incomplete or low-quality product records.
- **Marketing & E-commerce** teams get more reliable listings to work with.
- **Support & Fulfillment** staff benefit from clearer product identifiers and visuals.
- **Data Teams** can track trends in quality for reporting, QA, and tooling.

---

## 🧾 Why EAN Is Important for Internal Stakeholders

The EAN (European Article Number) is a critical internal field because:
- It acts as a **unique identifier** across internal tools, warehouses, and databases.
- Ensures **accurate matching** of product information in ERP and inventory systems.
- Enables reliable **linking of internal records** to suppliers, retailers, and pricing tools.
- Missing EANs lead to **data duplication** and operational inconsistencies.
- Teams in **logistics, fulfillment, procurement**, and even **customer support** depend on it for validation and referencing.

---

## 🖼️ Why `Picture normal reduced` Is Important for Internal Stakeholders

The `Picture normal reduced` field provides optimized product images, tailored for internal usability:
- Enables **quick product recognition** by internal teams like QA, product management, and support.
- Supports **faster manual reviews and categorization** by giving a visual cue.
- Makes internal dashboards and listings more **navigable and informative**.
- Ensures consistent image availability for **training sets, internal demos, or tooling**.
- Its absence leads to **slower validation processes** and poor stakeholder experience during review or audit.
  

### 🛠️ Importance of `Technical Details` for Internal Stakeholders

Technical details play a crucial role in maintaining data integrity and supporting business operations. Here's why they're essential for internal teams:

- **Accuracy in Operations**: They ensure product listings, procurement, and logistics are based on precise specifications.
- **Product Differentiation**: Sales and marketing teams use them to highlight unique features and compare products effectively.
- **Efficient Support**: Customer service relies on them for accurate, fast responses to technical questions and issue resolution.
- **Data Consistency**: They contribute to better data validation and consistency across platforms and systems.
- **Better Decision-Making**: Well-documented technical data empowers teams with reliable information for planning and execution.



---

## ❌ Why ETIM Was Excluded

ETIM (European Technical Information Model) is valuable for **external** product classification but was **not used** in this internal-focused analysis.

- Our focus: **internal product readiness**, not external alignment.
- ETIM relevance is limited for internal completeness and display validation.
- Descriptions, EANs, and images have direct business impact for internal users.

---



# 📁 Output Files

The **data** folder contains cleaned datasets along with results from various SQL queries run during the data quality assessment process.

---

## 📊 Cleaned Data Files

| File Name                                         | Description                                      |
|--------------------------------------------------|--------------------------------------------------|
| `merged_data_with_completeness_final.csv` | Full dataset with completeness indicators        |
| `good_quality_data_final.csv`             | Products with full, high-quality data            |
| `bad_quality_data_final.csv`              | Products missing key fields                      |

---
## 🗃️ SQL Query Output Files

| File Name                             | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| `sqlquery1.1_mostimproved.csv`       | Manufacturers with the most improved quality (Query 1.1)                    |
| `sqlquery1.2_Manufacturer_quality.csv` | Detailed manufacturer quality view (Subquery 1.2)                         |
| `sqlquery2_field_completion_rates.csv` | Field-wise completion rate analysis (Query 2)                             |
| `sqlquery3.1_EANvsquality.csv`       | Relationship between EAN completeness and product quality (Query 3.1)      |
| `sqlquery3.2_missing_combinations.csv` | Missing key combinations across fields (Query 3.2)                        |

           

---

## 📄 Documentation

| File Name              | Description                                    |
|------------------------|------------------------------------------------|
| `sqlqueryexplanation.docx` | Explanation of all SQL queries and logic used |

---

## 📋 Project Dependencies (`requirements.txt`)

### Purpose
The `requirements.txt` file ensures consistent Python package versions across all environments running this data pipeline.

---

### 🧰 Required Packages
| Package | Minimum Version | Purpose |
|---------|----------------|---------|
| `pandas` | 1.3.0 | Data manipulation (CSV processing, merging datasets) |
| `numpy` | 1.21.0 | Handling missing data (`NaN` values) |

📜 File Contents
plaintext
Copy
Edit
# Core Data Processing
pandas>=1.3.0
numpy>=1.21.0
🛠️ Setup Instructions
Prerequisites
Python 3.6 or later

pip package manager (included with Python)

Installation
bash
Copy
Edit
pip install -r requirements.txt
Verification
bash
Copy
Edit
python src/updated_pipeline.py
💻 Technical Notes
Version syntax (>=) allows newer compatible versions.

sqlite3 is included in Python's standard library.

No additional packages are needed for basic execution.

🔧 Recommended for Development
Add these to your requirements.txt for development:

plaintext
Copy
Edit
# Development Tools
jupyter>=1.0.0      # Interactive notebooks
flake8>=3.9.0       # Code quality checks
📂 Project Structure
plaintext
Copy
Edit
NewMart_DataPipeline/
├── requirements.txt           # Dependency file
├── src/                       # Python scripts
│   └── updated_pipeline.py
└── data/                      # All data files
    ├── manufacturers.csv
    ├── product_descriptions.csv
    └── product_properties.csv
▶️ How to Run
Place input files inside the /data folder.

Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Execute the pipeline:

bash
Copy
Edit
python src/updated_pipeline.py
🧪 Use SQL for Analysis
The cleaned dataset is loaded into an in-memory SQLite database.

You can query it using the provided notebook and the built-in sqlite3 library.

Useful for insights like most improved manufacturers, and detecting field-level gaps.

SQL query explanations are provided in sqlqueryexplanation.docx.

SQL outputs are available in the data/ folder.

🚀 Bonus: Ideas for Production Readiness
To take this project to production level:

Add Unit Tests: Ensure all steps like data cleaning, merging, and validation are tested.

Track Data Quality History: Implement versioning, audit logs, and rollback mechanisms.

Use Config Files: Parameterize paths, thresholds, and mappings for flexibility.

Design a Modular ETL Pipeline: Extract, transform, and load steps should be separate and reusable.

Separate Environments: Set up Dev, Test, and Production environments.

Implement CI/CD Pipelines: Automate tests, code linting, and deployments using GitHub Actions, Jenkins, or Azure Pipelines.

Apply Row-Level Security: Manage data access for different departments and external stakeholders.

📈 Next Steps: Power BI Dashboard
Exported file: merged_data_with_completeness_cleaned_final.csv is available for Power BI.

Create a one-page dashboard: NexMart.pbix showcasing:

Manufacturer performance

Manufacturers with missing fields

DAX calculations for gaps in product fields

The DAX code and explanations are available in Dax code & Explanation.txt.

✅ Summary
Improving data quality will lead to:

Enhanced product listings

Streamlined internal operations

Data-driven decision-making

This project builds a foundation to identify data gaps, prioritize corrections, and improve the overall data ecosystem at NexMart..

