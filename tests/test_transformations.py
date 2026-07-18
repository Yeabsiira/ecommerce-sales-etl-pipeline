import pytest
import pandas as pd
import numpy as np
from src.transform.clean_customers import transform_customers
from src.transform.clean_products import transform_products

def test_transform_customers_cleans_messy_input():
    """Validates that transform_customers handles inputs and extracts unique records."""
    mock_raw_data = pd.DataFrame({
        "customer_id": ["c1", "c1", "c2", "c3"],
        "customer_unique_id": ["u1", "u1", "u2", "u3"],
        "customer_zip_code_prefix": [1001, 1001, 1002, 1003],
        "customer_city": ["sao paulo", "sao paulo", "rio", "belo"],
        "customer_state": ["SP", "SP", None, "MG"]
    })
    
    df_cleaned = transform_customers(mock_raw_data)
    
    assert isinstance(df_cleaned, pd.DataFrame)
    assert df_cleaned.shape[0] == 3
    assert "customer_state" in df_cleaned.columns

def test_transform_products_fills_missing_metrics():
    """Validates that transform_products functions correctly when given translation data."""
    mock_raw_products = pd.DataFrame({
        "product_id": ["p1", "p2"],
        "product_category_name": ["perfumaria", "informatica_acessorios"],
        "product_name_lenght": [45.0, np.nan],
        "product_description_lenght": [200.0, np.nan],
        "product_photos_qty": [2.0, np.nan],
        "product_weight_g": [500.0, np.nan],  # Add a null value here to test your fillna logic
        "product_length_cm": [20.0, 30.0],
        "product_height_cm": [15.0, 10.0],
        "product_width_cm": [20.0, 25.0]
    })
    
    mock_translation = pd.DataFrame({
        "product_category_name": ["perfumaria", "informatica_acessorios"],
        "product_category_name_english": ["perfumery", "computers_accessories"]
    })
    
    df_cleaned = transform_products(mock_raw_products, mock_translation)
    
    assert isinstance(df_cleaned, pd.DataFrame)
    assert df_cleaned.shape[0] == 2
    assert "product_category" in df_cleaned.columns
    # Assert against a kept column that had missing data to confirm missing values are handled
    assert df_cleaned["product_weight_g"].isnull().sum() == 0