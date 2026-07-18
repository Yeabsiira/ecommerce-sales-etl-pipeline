import pandas as pd

def generate_date_dimension(df_fact_base):
    """Dynamically generates a dim_date table based on order timestamps."""
    print("📅 Generating Date Dimension...")
    
    # Extract unique dates from the purchase timestamp
    timestamps = df_fact_base["order_purchase_timestamp"].dropna().unique()
    df_date = pd.DataFrame({"full_date": timestamps})
    
    # Create a unique ID string format (YYYYMMDD) for fast SQL indexing
    df_date["date_id"] = df_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    
    # Breakdown time parts for easy filtering in dashboards
    df_date["day"] = df_date["full_date"].dt.day
    df_date["month"] = df_date["full_date"].dt.month
    df_date["year"] = df_date["full_date"].dt.year
    df_date["day_of_week"] = df_date["full_date"].dt.day_name()
    
    # Drop duplicates to keep it as a clean dimensional lookup
    df_date = df_date.drop_duplicates(subset=["date_id"])
    return df_date

def assemble_star_schema(extracted_data, clean_cust, clean_prod, clean_ord, clean_sell):
    """Assembles all components into the final Star Schema structure."""
    
    # 1. Transform individual dimensions
    dim_customers = clean_cust(extracted_data["customers"])
    dim_products = clean_prod(extracted_data["products"], extracted_data["category_translation"])
    dim_sellers = clean_sell(extracted_data["sellers"])
    
    # 2. Transform raw transactional data into base facts
    df_fact_base = clean_ord(
        extracted_data["orders"], 
        extracted_data["order_items"], 
        extracted_data["order_payments"], 
        extracted_data["order_reviews"]
    )
    
    # 3. Generate the Date Dimension table
    dim_date = generate_date_dimension(df_fact_base)
    
    # 4. Map the fact table rows to use the date_id key instead of the full timestamp
    print("🏭 Assembling Final fact_orders Table...")
    df_fact_base["date_id"] = df_fact_base["order_purchase_timestamp"].dt.strftime("%Y%m%d").fillna(0).astype(int)
    
    fact_orders = df_fact_base[[
        "order_id",
        "customer_id",
        "product_id",
        "seller_id",
        "date_id",
        "price",
        "freight_value",
        "payment_value",
        "delivery_days",
        "review_score"
    ]].drop_duplicates()
    
    print(f"✅ Fact Table Compiled: {fact_orders.shape[0]} final rows.")
    
    return {
        "dim_customers": dim_customers,
        "dim_products": dim_products,
        "dim_sellers": dim_sellers,
        "dim_date": dim_date,
        "fact_orders": fact_orders
    }