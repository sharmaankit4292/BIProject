# 📦 NexMart Data Assessment

This project analyzes and improves the quality of product data from NexMart. The goal is to clean, validate, and assess product information to ensure it's optimized for internal operations for better decision making across various stakeholders like Sales, Product etc.

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


### 🛠️ Setup Instructions
1. Install Python 3.6 or later
2. Run: `pip install -r requirements.txt`
3. Execute: `python src/updated_pipeline.py`

## 🚀 Bonus: Ideas for Production Readiness
- Add Unit Tests
- Track Data Quality History
- Use Config Files
- Design Modular ETL Pipeline
- Separate Environments (Dev/Test/Prod)
- Implement CI/CD Pipelines
- Apply Row-Level Security

## 📈 Next Steps: Power BI Dashboard
Use `merged_data_with_completeness_final.csv` to create dashboard showing:
- Manufacturer performance
- Manufacturers with missing fields
- DAX calculations for gaps (see `Dax code & Explanation.txt`)

## ✅ Summary
Improving data quality will lead to:
- Enhanced product listings
- Streamlined internal operations
- Data-driven decision-making
