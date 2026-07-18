import pandas as pd

def transform_customers(df_customers):
    """Cleans the customers dataset for the Star Schema."""
    print("🧹 Transforming Customers...")
    
    # 1. Drop duplicates if any exist on the natural primary key
    df_clean = df_customers.drop_duplicates(subset=["customer_id"]).copy()
    
    # 2. Select and rename columns cleanly for the database
    # In Olist, customer_unique_id tracks the physical person, customer_id tracks the specific order session.
    df_clean = df_clean[[
        "customer_id", 
        "customer_unique_id", 
        "customer_zip_code_prefix", 
        "customer_city", 
        "customer_state"
    ]]
    
    # 3. Standardize text strings to title case or uppercase for clean reporting
    df_clean["customer_city"] = df_clean["customer_city"].str.title()
    df_clean["customer_state"] = df_clean["customer_state"].str.upper()
    
    print(f"✅ Customer Dimension Ready: {df_clean.shape[0]} unique rows.")
    return df_clean