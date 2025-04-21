# 📦 NexMart Data Quality Assessment

This project analyzes and improves the quality of product data from NexMart. The goal is to clean, validate, and assess product information to ensure it’s optimized for internal operations.

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

---

## ❌ Why ETIM Was Excluded

ETIM (European Technical Information Model) is valuable for **external** product classification but was **not used** in this internal-focused analysis.

- Our focus: **internal product readiness**, not external taxonomy alignment.
- ETIM relevance is limited for internal completeness and display validation.
- Descriptions, EANs, and images have direct business impact for internal users.

---

## 📂 Output Files

| File Name                                   | Description                                  |
|--------------------------------------------|----------------------------------------------|
| `merged_data_with_completeness.csv`        | Full dataset with completeness indicators    |
| `good_quality_data.csv`                    | Products with full, high-quality data        |
| `bad_quality_data.csv`                     | Products missing key fields                  |

---

## ▶️ How to Run

1. Clone the repo and place the data files inside the `/data` folder.
2. Adjust the file paths in the script if necessary.
3. Run the Python script in your local environment.
4. Check the printed console output and exported files.

---

## 🧪 Optional: Use SQL for Analysis

The cleaned dataset is loaded into an in-memory SQLite DB:
- You can query it using standard SQL.
- Useful for additional insights (e.g., most incomplete manufacturers, field-level gaps).

---

## 🧩 Bonus: Ideas for Production Readiness

For a full production setup:
- Add **unit tests** for each cleaning step.
- Use **logging** instead of `print()` statements.
- Track data quality history with **versioning or audit logs**.
- Parameterize file paths and thresholds via a **config file**.
- Package the logic in a **modular pipeline or ETL framework**.

---

## 📊 Next Steps: Power BI Dashboard

- The exported `merged_data_with_completeness.csv` can be used in Power BI.
- Create a one-page dashboard with:
  - Completeness trends
  - Manufacturer performance
  - Top product gaps
  - Visual filters by quality label

---

## ✅ Summary

Improving data quality drives better product listings, internal efficiency, and decision-making. This project provides a framework to identify gaps, prioritize fixes, and improve the data landscape at NexMart.

