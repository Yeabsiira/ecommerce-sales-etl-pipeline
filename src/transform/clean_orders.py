import pandas as pd

def transform_orders(df_orders, df_items, df_payments, df_reviews):
    """Cleans orders, integrates payments/reviews, and builds the core facts dataset."""
    print("🧹 Transforming Orders and Items...")
    
    # 1. Convert text timestamp columns to true Python/Pandas Datetime objects
    datetime_cols = [
        "order_purchase_timestamp", 
        "order_approved_at", 
        "order_delivered_carrier_date", 
        "order_delivered_customer_date", 
        "order_estimated_delivery_date"
    ]
    for col in datetime_cols:
        df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')
        
    # 2. Engineer Features: Calculate actual vs estimated delivery performance
    # If delivery date is missing, we fill the performance metric with 0
    df_orders["delivery_days"] = (df_orders["order_delivered_customer_date"] - df_orders["order_purchase_timestamp"]).dt.days
    df_orders["delivery_days"] = df_orders["delivery_days"].fillna(0).astype(int)
    
    # 3. Aggregate Payments (An order can have multiple payment methods/installments)
    print("💳 Aggregating Order Payments...")
    df_pay_agg = df_payments.groupby("order_id")["payment_value"].sum().reset_index()
    
    # 4. Aggregate Reviews (Take the average review score if an order has multiple reviews)
    print("⭐ Aggregating Order Reviews...")
    df_rev_agg = df_reviews.groupby("order_id")["review_score"].mean().reset_index()
    
    # 5. Merge items with order details, payments, and reviews to form the base fact rows
    df_fact_base = pd.merge(df_items, df_orders, on="order_id", how="inner")
    df_fact_base = pd.merge(df_fact_base, df_pay_agg, on="order_id", how="left")
    df_fact_base = pd.merge(df_fact_base, df_rev_agg, on="order_id", how="left")
    
    # Fill missing values for aggregates
    df_fact_base["payment_value"] = df_fact_base["payment_value"].fillna(0)
    df_fact_base["review_score"] = df_fact_base["review_score"].fillna(5.0) # Assume 5 if unreviewed
    
    print(f"✅ Order Fact Base Ready: {df_fact_base.shape[0]} transaction items mapped.")
    return df_fact_base