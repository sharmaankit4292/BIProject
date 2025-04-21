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
  

### 🛠️ Importance of Technical Details for Internal Stakeholders

Technical details play a crucial role in maintaining data integrity and supporting business operations. Here's why they're essential for internal teams:

1. **Accuracy in Operations**: They ensure product listings, procurement, and logistics are based on precise specifications.
2. **Product Differentiation**: Sales and marketing teams use them to highlight unique features and compare products effectively.
3. **Efficient Support**: Customer service relies on them for accurate, fast responses to technical questions and issue resolution.
4. **Data Consistency**: They contribute to better data validation and consistency across platforms and systems.
5. **Better Decision-Making**: Well-documented technical data empowers teams with reliable information for planning and execution.



---

## ❌ Why ETIM Was Excluded

ETIM (European Technical Information Model) is valuable for **external** product classification but was **not used** in this internal-focused analysis.

- Our focus: **internal product readiness**, not external alignment.
- ETIM relevance is limited for internal completeness and display validation.
- Descriptions, EANs, and images have direct business impact for internal users.

---

## 📂 Output Files

| File Name                                   | Description                                  |
|--------------------------------------------|----------------------------------------------|
| `merged_data_with_completeness_cleaned_final.csv`        | Full dataset with completeness indicators    |
| `good_quality_data_cleaned_final.csv`                    | Products with full, high-quality data        |
| `bad_quality_data_cleaned_final.csv`                     | Products missing key fields                  |

---

## ▶️ How to Run

1. Clone the repo and place the data files inside the `/data` folder.
2. Adjust the file paths in the script if necessary.
3. Run the Python script in your local environment.
4. Check the printed console output and exported files.

---

## 🧪Use SQL for Analysis

The cleaned dataset is loaded into an in-memory SQLite DB:
- You can query it using the notebook itself with Sqlite library.
- Useful for additional insights (e.g., most improved manufacturers, field-level gaps).
- The explanation and output is attached in the folder. 

---

##  Bonus: Ideas for Production Readiness

To elevate this project into a production-ready pipeline, consider the following best practices:

-  **Add Unit Tests**: Test each data cleaning, merging, and validation step to ensure robustness and prevent regressions.
-  **Track Data Quality History**: Implement versioning and audit logging to monitor data quality trends over time and support rollback if needed.
-  **Parameterize via Config Files**: Manage file paths, validation thresholds, and column mappings using config files or environment variables for flexibility and scalability.
-  **Build a Modular ETL Pipeline**: Break the logic into clear, reusable steps using an Extract-Transform-Load framework to support batch or streaming data.
-  **Environment Separation (Dev, Test, Prod)**: Establish different environments to support experimentation, testing, and deployment without data contamination. This helps enforce data governance and approval flows.
-  **Implement CI/CD Pipelines**: Use DevOps practices like GitHub Actions, Jenkins, or Azure Pipelines to automate testing, linting, deployment, and report generation. This improves delivery speed and reduces manual errors.
- **Implement Row level security**: managing access level for different departments, stakeholders & externals.
   
These practices ensure scalability, reliability, and maintainability—making the solution enterprise-ready and aligned with NexMart’s data strategy goals.


---

## 📊 Next Steps: Power BI Dashboard

- The exported `merged_data_with_completeness_cleaned_final.csv` can be used in Power BI.
- Create a one-page dashboard with:
  - Manufacturer performance
  - Manfactures with bad fields
  - Dax for Product Name and bad fields. This helps us finds gaps in products/main_product, manufactures, manufacturer numbers etc.
  - The Code and Explanation for the Dax code is the Dax code & Explanation.txt file

---

## ✅ Summary

Improving data quality drives better product listings, internal efficiency, and decision-making. This project provides a framework to identify gaps, prioritize fixes, and improve the data landscape at NexMart.

