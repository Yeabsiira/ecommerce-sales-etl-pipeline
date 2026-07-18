import pandas as pd

def transform_products(df_products, df_translation):
    """Cleans and translates the products dataset."""
    print("🧹 Transforming Products...")
    
    # 1. Map Portuguese category names to English using the translation file
    # We do a left join to bring in the English column
    df_merged = pd.merge(
        df_products, 
        df_translation, 
        on="product_category_name", 
        how="left"
    )
    
    # 2. Handle missing categories or missing translations
    # If it's missing, label it as 'unknown' rather than leaving it Null
    df_merged["product_category_name_english"] = df_merged["product_category_name_english"].fillna("unknown")
    
    # 3. Handle structural missing metrics (weights/dimensions) by filling with 0 or a median
    metric_cols = ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
    for col in metric_cols:
        df_merged[col] = df_merged[col].fillna(0)
        
    # 4. Clean up columns and rename to fit database conventions
    df_merged = df_merged.rename(columns={"product_category_name_english": "product_category"})
    
    df_clean = df_merged[[
        "product_id",
        "product_category",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]].drop_duplicates(subset=["product_id"])
    
    print(f"✅ Product Dimension Ready: {df_clean.shape[0]} rows.")
    return df_clean