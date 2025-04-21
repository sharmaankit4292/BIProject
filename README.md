NexMart Data Quality Assessment
This project helps analyze and improve the quality of product data from NexMart. The goal is to clean up the product information, identify gaps, and make sure the data is ready for use across internal teams.

What the Code Does
Loads the data
It reads three CSV files: manufacturers.csv, product_descriptions.csv, and product_properties.csv.

Cleans up the data
It replaces common bad values like "N/A", "null", or blank fields with NaN to standardize the data.

Combines the data
It merges the three files together using common columns (like Article Number and Manufacturer number) to create one full dataset.

Checks data completeness
It checks each product to see if all the required fields (like descriptions, EAN, etc.) are filled out. It flags whether a product is "complete" or missing information.

Assesses data quality
It labels each product as either "good" or "bad" quality. A product is considered "good" if it has:

A description (logic explained below)

A valid EAN (barcode)

A product image (Picture normal reduced)

Outputs the results

It saves the cleaned data with completeness checks.

It separates products into two files: good quality and bad quality.

It also loads the data into an in-memory database (SQLite) for easy querying.

Description Field Logic
To assess if a product has a valid description, the following fallback logic is applied:
We first check Short description. If it’s missing, we check Short description 2. If that’s also missing, we look at the Long description.
This step ensures we capture any useful product detail even if it appears in an alternate field.
The logic guarantees the best available product description is used for quality checks.
It prevents otherwise usable products from being marked "bad" due to minor field inconsistencies.
This approach significantly boosts data quality metrics and ensures fairer, more accurate evaluations.

Why This Matters
For Internal Teams:
Product & Content Teams: They can focus on improving data where it’s most needed.

Marketing & E-commerce: They can see which products have complete data for better listings.

Data & Tech Teams: They can track data quality trends over time.

Why EAN Is Important
EAN (European Article Number) is essential because:

It uniquely identifies each product.

It’s required for proper syncing with other systems and platforms.

Without an EAN, products won’t appear in search results or may not be recognized properly.

Why Picture normal reduced Is Important
The Picture normal reduced field provides a lightweight, optimized image of the product.
It helps internal teams visually verify and QA products at scale.
This image improves catalog consistency across platforms and dashboards.
It enables richer promotional content and better user experience in internal tools.
Without it, internal workflows slow down and product data loses visual context.

Why ETIM Was Not Considered
ETIM (European Technical Information Model) is a standardized classification system used primarily for external systems (e.g., third-party platforms or suppliers). It’s essential for categorizing products in specific ways for external trade.

However, ETIM wasn’t considered in this analysis because:

Internal Focus: The goal was to assess and improve internal data quality, specifically product descriptions, EANs, and images, which directly affect how the products are displayed and managed in NexMart’s internal systems.

External Use: ETIM is more relevant for product classification in external marketplaces or systems, not for assessing the quality of data that is used directly within NexMart’s internal processes.

Thus, focusing on fields like description, EAN, and product image provides more immediate value for NexMart’s internal teams, and these are the primary fields impacting product visibility, completeness, and quality.

Files Generated
merged_data_with_completeness.csv: Full dataset with completeness information.

good_quality_data.csv: Products that have all the required fields (good quality).

bad_quality_data.csv: Products missing key fields (bad quality).

How to Use
Make sure the CSV file paths are correct.

Run the script in a Python environment.

Check the printed results and explore the exported CSV files or the SQLite database for more details.
