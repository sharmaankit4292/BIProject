#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import sqlite3 as sqldf

# --- Load datasets ---
manufacturers = pd.read_csv("C:/Users/Ankit/NexMart/manufacturers.csv", sep=';')
product_descriptions = pd.read_csv("C:/Users/Ankit/NexMart/product_descriptions.csv", sep=';')
product_properties = pd.read_csv("C:/Users/Ankit/NexMart/product_properties.csv", sep=';')

# --- Normalize column names ---
manufacturers.rename(columns={
    'Manufacturernumber': 'Manufacturer number',
    'Manufacturername': 'Manufacturer name'
}, inplace=True)

product_descriptions.rename(columns={
    'Articlenumber': 'Article Number'
}, inplace=True)

product_properties.rename(columns={
    'Manufacturernumber': 'Manufacturer number',
    'Articlenumber': 'Article Number'
}, inplace=True)

# --- Define bad values to normalize to NULL ---
bad_values = ['N/A', 'n/a', 'None', 'none', '', ' ', '-', 'nan', 'NaN', 'null', 'NULL', "'"]

def clean_dataframe(df):
    df.replace(bad_values, np.nan, inplace=True)
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip()
    return df

# --- Clean data ---
manufacturers = clean_dataframe(manufacturers)
product_descriptions = clean_dataframe(product_descriptions)
product_properties = clean_dataframe(product_properties)

# --- Drop rows with nulls in required join columns ---
product_descriptions.dropna(subset=['Article Number'], inplace=True)
product_properties.dropna(subset=['Manufacturer number', 'Article Number'], inplace=True)
manufacturers.dropna(subset=['Manufacturer number'], inplace=True)

# --- INNER JOINs ---
merged_df = (
    product_properties
    .merge(product_descriptions, on='Article Number', how='inner')
    .merge(manufacturers, on='Manufacturer number', how='inner')
)

# --- Calculate completeness metrics ---
def calculate_completeness(row):
    all_fields = merged_df.columns.tolist()
    missing_count = sum(1 for field in all_fields if pd.isna(row[field]))
    is_complete = missing_count == 0
    return pd.Series([is_complete, missing_count], index=['Is Complete', 'Missing Fields Count'])

# Apply completeness calculation
completeness_df = merged_df.apply(calculate_completeness, axis=1)
merged_df = pd.concat([merged_df, completeness_df], axis=1)

# --- Assess description quality (ETIM excluded) ---
def assess_description_quality(row):
    has_description = (
        pd.notna(row.get('Short description')) or
        pd.notna(row.get('Short description 2')) or
        pd.notna(row.get('Long description'))
    )
    has_ean = pd.notna(row.get('EAN'))
    has_picture = pd.notna(row.get('Picture normal reduced'))
    has_technical = pd.notna(row.get('Technical details'))

    if has_description and has_ean and has_picture and has_technical:
        return 'good'
    else:
        return 'bad'

merged_df['Description Quality'] = merged_df.apply(assess_description_quality, axis=1)

# --- Filter for good and bad quality ---
good_quality_df = merged_df[merged_df['Description Quality'] == 'good']
bad_quality_df = merged_df[merged_df['Description Quality'] == 'bad']

# --- Output summary ---
print(f"Total Records: {len(merged_df)}")
print(f"Complete Records (all fields populated): {merged_df['Is Complete'].sum()}")
print(f"Records with missing fields: {len(merged_df) - merged_df['Is Complete'].sum()}")

print("\nMissing Fields Distribution:")
print(merged_df['Missing Fields Count'].value_counts().sort_index())

print(f"\nGood Quality Records (valid description + EAN + Picture + Technical details): {len(good_quality_df)}")
print(f"Bad Quality Records (missing any required fields): {len(bad_quality_df)}")

# --- Export data ---
merged_df.to_csv("C:/Users/Ankit/NexMart/merged_data_with_completeness_withoutETIM.csv", index=False)
good_quality_df.to_csv("C:/Users/Ankit/NexMart/good_quality_data_withoutETIM.csv", index=False)
bad_quality_df.to_csv("C:/Users/Ankit/NexMart/bad_quality_data_withoutETIM.csv", index=False)

# --- Optional: SQLite export ---
conn = sqldf.connect(":memory:")
merged_df.to_sql("product_data", conn, index=False, if_exists="replace")
print("\nData loaded to SQLite with completeness metrics")


# In[7]:


import pandas as pd
import sqlite3

# Connect to the in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Load your merged dataframe into SQLite
merged_df.to_sql('product_data', conn, index=False, if_exists='replace')

# 1. Manufacturers with biggest improvement potential
def get_manufacturer_quality_stats():
    query = """
    SELECT 
        [Manufacturer name],
        COUNT(*) AS total_products,
        SUM(CASE WHEN [Description Quality] = 'bad' THEN 1 ELSE 0 END) AS bad_quality_count,
        ROUND(SUM(CASE WHEN [Description Quality] = 'bad' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bad_quality_percentage
    FROM product_data
    GROUP BY [Manufacturer name]
    ORDER BY bad_quality_count DESC
    """
    return pd.read_sql(query, conn)

# 2. Field completion rates by manufacturer (added Technical details)
def get_field_completion_rates():
    fields = ['Short description', 'Short description 2', 'Long description', 'EAN', 'Picture normal reduced', 'Technical details']
    results = []
    
    for field in fields:
        query = f"""
        SELECT 
            [Manufacturer name],
            '{field}' AS field_name,
            ROUND(SUM(CASE WHEN [{field}] IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS completion_rate
        FROM product_data
        GROUP BY [Manufacturer name]
        """
        results.append(pd.read_sql(query, conn))
    
    return pd.concat(results).sort_values(['Manufacturer name', 'completion_rate'], ascending=[True, False])

# 3. Interesting insights (added Technical details to missing field counts)
def get_quality_insights():
    # Insight 1: EAN vs description quality correlation
    ean_corr = pd.read_sql("""
    SELECT 
        CASE WHEN [EAN] IS NULL THEN 'Missing EAN' ELSE 'Has EAN' END AS ean_status,
        ROUND(SUM(CASE WHEN [Description Quality] = 'bad' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bad_description_percentage
    FROM product_data
    GROUP BY ean_status
    """, conn)
    
    # Insight 2: Missing field combinations
    missing_fields = pd.read_sql("""
    SELECT 
        SUM(CASE WHEN [Short description] IS NULL THEN 1 ELSE 0 END) AS missing_short_desc,
        SUM(CASE WHEN [Short description 2] IS NULL THEN 1 ELSE 0 END) AS missing_short_desc2,
        SUM(CASE WHEN [Long description] IS NULL THEN 1 ELSE 0 END) AS missing_long_desc,
        SUM(CASE WHEN [EAN] IS NULL THEN 1 ELSE 0 END) AS missing_ean,
        SUM(CASE WHEN [Picture normal reduced] IS NULL THEN 1 ELSE 0 END) AS missing_picture,
        SUM(CASE WHEN [Technical details] IS NULL THEN 1 ELSE 0 END) AS missing_technical_details,
        COUNT(*) AS total_records
    FROM product_data
    """, conn)
    
    return {
        'ean_correlation': ean_corr,
        'missing_field_combinations': missing_fields
    }

# --- Get and display results ---

manufacturer_stats = get_manufacturer_quality_stats()
field_completion = get_field_completion_rates()
insights = get_quality_insights()

# Display results
print("=== Manufacturers by Improvement Potential ===")
print(manufacturer_stats)

print("\n=== Field Completion Rates by Manufacturer (Top 10 Fields Per Manufacturer) ===")
print(field_completion.groupby('Manufacturer name').head(10))

print("\n=== Key Insights ===")
print("\n1. EAN vs Description Quality Correlation:")
print(insights['ean_correlation'])

print("\n2. Missing Field Combinations:")
print(insights['missing_field_combinations'])


# In[ ]:




