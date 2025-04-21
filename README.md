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
- Flags whether each product is **complete** (no missing fields).
- Adds a field for **Missing Fields Count**.

### 5. Assesses Data Quality
A product is labeled **"good quality"** if it has:
- A valid description (see [Description Logic](#description-logic))
- A valid EAN (European Article Number)
- A valid product image (`Picture normal reduced`)

### 6. Exports the Output
- Saves the full merged dataset with completeness flags.
- Separates and saves `good_quality_data.csv` and `bad_quality_data.csv`.
- Loads the full dataset into an in-memory SQLite DB for easy SQL querying.

---

## 🧠 Description Logic

To determine if a product has a valid description, the following fallback logic is used:
1. Use `Short description` if available.
2. If not, fall back to `Short description 2`.
3. If still unavailable, use `Long description`.

This approach ensures we always retrieve the best available description without relying on a single inconsistent field. It helps prevent data loss and ensures fairer, more consistent quality assessments.

This practice is critical to clean and harmonize legacy or third-party datasets, where product details might be spread across multiple description fields.

---

## 🔍 Why This Matters

### Internal Benefits:
- **Product Teams** can easily identify and fix incomplete listings.
- **Marketing & E-commerce** teams rely on accurate data to improve listings.
- **Data Teams** gain visibility into quality trends for reporting and tooling.

---

## 🧾 Why EAN Is Important

The EAN (European Article Number) is a critical field because:
- It uniquely identifies each product across systems.
- It’s required for database integrity and platform integration.
- Products without EANs may be unsearchable or duplicated.
- It supports logistics, tracking, and synchronization.

---

## 🖼️ Why `Picture normal reduced` Is Important

The `Picture normal reduced` field provides optimized, lightweight product images:
- Helps internal teams visually validate product records at scale.
- Enables consistent appearance across internal systems and dashboards.
- Supports promotional tools and richer business reporting.
- Accelerates manual QA and reduces decision-making friction.
- Missing images disrupt product reviews and hinder marketing operations.

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

