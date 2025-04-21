#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
    # This query finds which manufacturers have the most products with bad descriptions
    # It counts bad descriptions for each manufacturer and calculates the percentage
    # Useful to identify which manufacturers need the most help improving their product info
    
    return pd.read_sql(query, conn)

# 2. Field completion rates by manufacturer
def get_field_completion_rates():
    fields = ['Short description', 'Short description 2', 'Long description', 'EAN', 'Picture normal reduced']
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
        # This query checks how complete each data field is for each manufacturer
        # It calculates what percentage of products have each field filled out
        # Useful to see which information is most often missing for each brand
        
        results.append(pd.read_sql(query, conn))
    
    return pd.concat(results).sort_values(['Manufacturer name', 'completion_rate'], ascending=[True, False])

# 3. Interesting insights
def get_quality_insights():
    # Insight 1: EAN vs description quality correlation
    ean_corr = pd.read_sql("""
    SELECT 
        CASE WHEN [EAN] IS NULL THEN 'Missing EAN' ELSE 'Has EAN' END AS ean_status,
        ROUND(SUM(CASE WHEN [Description Quality] = 'bad' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bad_description_percentage
    FROM product_data
    GROUP BY ean_status
    """, conn)
    # This query checks if products with missing EAN codes tend to have worse descriptions
    # Useful to see if missing one piece of info relates to other missing info
    
    # Insight 2: Missing field combinations
    missing_fields = pd.read_sql("""
    SELECT 
        SUM(CASE WHEN [Short description] IS NULL THEN 1 ELSE 0 END) AS missing_short_desc,
        SUM(CASE WHEN [Short description 2] IS NULL THEN 1 ELSE 0 END) AS missing_short_desc2,
        SUM(CASE WHEN [Long description] IS NULL THEN 1 ELSE 0 END) AS missing_long_desc,
        SUM(CASE WHEN [EAN] IS NULL THEN 1 ELSE 0 END) AS missing_ean,
        COUNT(*) AS total_records
    FROM product_data
    """, conn)
    # This query counts how many products are missing each type of information
    # Useful to understand which fields are most commonly empty across all products
    
    return {
        'ean_correlation': ean_corr,
        'missing_field_combinations': missing_fields
    }

def get_most_improved_manufacturer():
    query = """
    SELECT 
        [Manufacturer name],
        COUNT(*) AS total_products,
        SUM(CASE WHEN [Description Quality] = 'good' THEN 1 ELSE 0 END) AS good_quality_count,
        ROUND(SUM(CASE WHEN [Description Quality] = 'good' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS good_quality_percentage
    FROM product_data
    GROUP BY [Manufacturer name]
    ORDER BY good_quality_percentage DESC, good_quality_count DESC
    LIMIT 1
    """
    # This query finds which manufacturer has the highest percentage of good descriptions
    # Useful to identify which brands are doing the best job with their product information
    
    return pd.read_sql(query, conn)

# --- Get and display results ---

manufacturer_stats = get_manufacturer_quality_stats()
field_completion = get_field_completion_rates()
insights = get_quality_insights()
best_manufacturer = get_most_improved_manufacturer()

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

print("\n=== Best Performing Manufacturer ===")
print(best_manufacturer)


# In[ ]:


def get_most_improved_manufacturer():
    query = """
    SELECT 
        [Manufacturer name],
        COUNT(*) AS total_products,
        SUM(CASE WHEN [Description Quality] = 'good' THEN 1 ELSE 0 END) AS good_quality_count,
        ROUND(SUM(CASE WHEN [Description Quality] = 'good' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS good_quality_percentage
    FROM product_data
    GROUP BY [Manufacturer name]
    ORDER BY good_quality_percentage DESC, good_quality_count DESC
    LIMIT 1
    """
    return pd.read_sql(query, conn) # this query gives you most improved manufacturer pertaining to data quality.

