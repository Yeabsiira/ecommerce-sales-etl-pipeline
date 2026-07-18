import pandas as pd

def transform_sellers(df_sellers):
    """Cleans the sellers dataset and builds the dim_sellers dimension table."""
    print("🧹 Transforming Sellers...")

    # 1. Drop duplicates on natural primary key
    df_clean = df_sellers.drop_duplicates(subset=["seller_id"]).copy()

    # 2. Select and retain relevant columns
    df_clean = df_clean[[
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state"
    ]]

    # 3. Standardize text casing
    df_clean["seller_city"] = df_clean["seller_city"].str.title()
    df_clean["seller_state"] = df_clean["seller_state"].str.upper()

    # 4. Fill any missing city/state values
    df_clean["seller_city"] = df_clean["seller_city"].fillna("Unknown")
    df_clean["seller_state"] = df_clean["seller_state"].fillna("Unknown")

    print(f"✅ Seller Dimension Ready: {df_clean.shape[0]} unique sellers.")
    return df_clean
