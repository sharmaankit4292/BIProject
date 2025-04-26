#!/usr/bin/env python
# coding: utf-8

# updated_pipeline.py

# --- Import Libraries ---
import pandas as pd
import numpy as np
import sqlite3

def main():
    # --- Load Datasets ---
    manufacturers = pd.read_csv("./data/manufacturers.csv", sep=';')
    product_descriptions = pd.read_csv("./data/product_descriptions.csv", sep=';')
    product_properties = pd.read_csv("./data/product_properties.csv", sep=';')

    # --- Normalize Column Names ---
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

    # --- Define and Clean Bad Values ---
    bad_values = ['N/A', 'n/a', 'None', 'none', '', ' ', '-', 'nan', 'NaN', 'null', 'NULL', "'"]

    def clean_dataframe(df):
        df.replace(bad_values, np.nan, inplace=True)
        for col in df.select_dtypes(include='object'):
            df[col] = df[col].str.strip()
        return df

    manufacturers = clean_dataframe(manufacturers)
    product_descriptions = clean_dataframe(product_descriptions)
    product_properties = clean_dataframe(product_properties)

    # --- Drop Rows with Nulls in Required Join Columns ---
    product_descriptions.dropna(subset=['Article Number'], inplace=True)
    product_properties.dropna(subset=['Manufacturer number', 'Article Number'], inplace=True)
    manufacturers.dropna(subset=['Manufacturer number'], inplace=True)

    # --- Merge All Data ---
    merged_df = (
        product_properties
        .merge(product_descriptions, on='Article Number', how='inner')
        .merge(manufacturers, on='Manufacturer number', how='inner')
    )

    # --- Calculate Completeness ---
    def calculate_completeness(row):
        total_fields = merged_df.columns.tolist()
        missing_count = sum(1 for field in total_fields if pd.isna(row[field]))
        return pd.Series([missing_count == 0, missing_count], index=['Is Complete', 'Missing Fields Count'])

    completeness_df = merged_df.apply(calculate_completeness, axis=1)
    merged_df = pd.concat([merged_df, completeness_df], axis=1)

    # --- Assess Description Quality ---
    def assess_description_quality(row):
        has_description = pd.notna(row.get('Short description')) or pd.notna(row.get('Short description 2')) or pd.notna(row.get('Long description'))
        has_ean = pd.notna(row.get('EAN'))
        has_picture = pd.notna(row.get('Picture normal reduced'))
        has_technical = pd.notna(row.get('Technical details'))
        
        return 'good' if all([has_description, has_ean, has_picture, has_technical]) else 'bad'

    merged_df['Description Quality'] = merged_df.apply(assess_description_quality, axis=1)

    # --- Filter by Description Quality ---
    good_quality_df = merged_df[merged_df['Description Quality'] == 'good']
    bad_quality_df = merged_df[merged_df['Description Quality'] == 'bad']

    # --- Print Summary ---
    print(f"Total Records: {len(merged_df)}")
    print(f"Complete Records (all fields populated): {merged_df['Is Complete'].sum()}")
    print(f"Records with Missing Fields: {len(merged_df) - merged_df['Is Complete'].sum()}")

    print("\nMissing Fields Distribution:")
    print(merged_df['Missing Fields Count'].value_counts().sort_index())

    print(f"\nGood Quality Records: {len(good_quality_df)}")
    print(f"Bad Quality Records: {len(bad_quality_df)}")

    # --- Export Cleaned and Analyzed Data ---
    merged_df.to_csv("./data/merged_data_with_completeness_final.csv", index=False)
    good_quality_df.to_csv("./data/good_quality_data_final.csv", index=False)
    bad_quality_df.to_csv("./data/bad_quality_data_final.csv", index=False)

    # --- Load into SQLite In-Memory ---
    conn = sqlite3.connect(':memory:')
    merged_df.to_sql('product_data', conn, index=False, if_exists='replace')
    print("\nData loaded to SQLite with completeness metrics.")

    # --- SQL Analysis Functions ---
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

    def get_quality_insights():
        ean_corr = pd.read_sql("""
        SELECT 
            CASE WHEN [EAN] IS NULL THEN 'Missing EAN' ELSE 'Has EAN' END AS ean_status,
            ROUND(SUM(CASE WHEN [Description Quality] = 'bad' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bad_description_percentage
        FROM product_data
        GROUP BY ean_status
        """, conn)
        
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
        
        return {'ean_correlation': ean_corr, 'missing_field_combinations': missing_fields}

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
        return pd.read_sql(query, conn)

    # --- Execute and Print SQL Queries ---
    manufacturer_stats = get_manufacturer_quality_stats()
    field_completion = get_field_completion_rates()
    insights = get_quality_insights()
    most_improved = get_most_improved_manufacturer()

    print("\n=== Manufacturer Quality Stats ===")
    print(manufacturer_stats)

    print("\n=== Field Completion Rates ===")
    print(field_completion)

    print("\n=== EAN vs Description Quality Correlation ===")
    print(insights['ean_correlation'])

    print("\n=== Missing Field Combinations ===")
    print(insights['missing_field_combinations'])

    print("\n=== Most Improved Manufacturer (Best Data Quality) ===")
    print(most_improved)

    # --- Export All Results to CSV ---
    manufacturer_stats.to_csv("./data/sqlquerry1.2_Manufacturer_quality.csv", index=False)
    field_completion.to_csv("./data/sqlquerry2_field_completion_rates.csv", index=False)
    insights['ean_correlation'].to_csv("./data/Sqlquery3.1_Eanvsquality.csv", index=False)
    insights['missing_field_combinations'].to_csv("./data/Sqlquery3.2_missing_combinations.csv", index=False)
    most_improved.to_csv("./data/sqlquerry1_mostimproved.csv", index=False)

    print("\nAll CSV files saved successfully.")

# --- Run Everything ---
if __name__ == "__main__":
    main()




