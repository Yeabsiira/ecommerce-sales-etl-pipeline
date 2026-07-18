import os
import pandas as pd
from pathlib import Path

# Define base directory relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# List of Olist datasets we expect to find in data/raw/
DATASETS = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

def extract_raw_data():
    """Reads raw CSV files from data/raw and validates their extraction."""
    extracted_dfs = {}
    
    print("🚀 Starting Data Extraction Phase...")
    
    for key, file_name in DATASETS.items():
        file_path = RAW_DATA_DIR / file_name
        
        # Check if the file actually exists
        if not file_path.exists():
            print(file_path)
            raise FileNotFoundError(f"❌ Critical Error: Missing expected raw data file: {file_name} at {file_path}")
        
        print(f"📥 Extracting {file_name}...")
        
        # Load the CSV data into a Pandas DataFrame
        try:
            df = pd.read_csv(file_path)
            extracted_dfs[key] = df
            print(f"✅ Successfully loaded {key}. Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to read {file_name}: {str(e)}")
            
    print("\n🎉 Extraction Phase Completed Successfully!")
    return extracted_dfs

if __name__ == "__main__":
    # Test execution when run directly
    try:
        data = extract_raw_data()
    except Exception as e:
        print(f"\n💥 Extraction Failed: {e}")
