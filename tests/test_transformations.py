import pytest
import pandas as pd
import numpy as np
from src.transform.clean_customers import transform_customers
from src.transform.clean_products import transform_products
from src.transform.clean_orders import transform_orders
from src.transform.clean_sellers import transform_sellers

# ──────────────────────────────────────────────
# dim_customers tests
# ──────────────────────────────────────────────

def test_transform_customers_cleans_messy_input():
    """Validates that transform_customers deduplicates on customer_id."""
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

def test_transform_customers_no_duplicate_primary_keys():
    """Critical: dim_customers must have zero duplicate primary keys after transform."""
    mock_raw_data = pd.DataFrame({
        "customer_id": ["c1", "c1", "c2"],
        "customer_unique_id": ["u1", "u1", "u2"],
        "customer_zip_code_prefix": [1001, 1001, 1002],
        "customer_city": ["city a", "city a", "city b"],
        "customer_state": ["SP", "SP", "RJ"]
    })
    df_cleaned = transform_customers(mock_raw_data)
    assert df_cleaned["customer_id"].duplicated().sum() == 0, \
        "dim_customers has duplicate customer_id values — primary key violation!"

# ──────────────────────────────────────────────
# dim_products tests
# ──────────────────────────────────────────────

def test_transform_products_fills_missing_metrics():
    """Validates that transform_products fills null physical metrics with 0."""
    mock_raw_products = pd.DataFrame({
        "product_id": ["p1", "p2"],
        "product_category_name": ["perfumaria", "informatica_acessorios"],
        "product_name_lenght": [45.0, np.nan],
        "product_description_lenght": [200.0, np.nan],
        "product_photos_qty": [2.0, np.nan],
        "product_weight_g": [500.0, np.nan],
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
    assert df_cleaned["product_weight_g"].isnull().sum() == 0

def test_transform_products_unknown_category_fallback():
    """Products with no translation mapping should receive 'unknown', not NaN."""
    mock_raw_products = pd.DataFrame({
        "product_id": ["p1"],
        "product_category_name": ["categoria_inexistente"],
        "product_name_lenght": [10.0],
        "product_description_lenght": [100.0],
        "product_photos_qty": [1.0],
        "product_weight_g": [200.0],
        "product_length_cm": [10.0],
        "product_height_cm": [5.0],
        "product_width_cm": [10.0]
    })
    mock_translation = pd.DataFrame({
        "product_category_name": ["perfumaria"],
        "product_category_name_english": ["perfumery"]
    })
    df_cleaned = transform_products(mock_raw_products, mock_translation)
    assert df_cleaned["product_category"].iloc[0] == "unknown", \
        "Untranslated categories must fall back to 'unknown', not NaN"

# ──────────────────────────────────────────────
# fact_orders (clean_orders) tests
# ──────────────────────────────────────────────

def test_transform_orders_computes_delivery_days_correctly():
    """delivery_days must equal the integer difference between delivery and purchase dates."""
    df_orders = pd.DataFrame({
        "order_id": ["o1", "o2"],
        "customer_id": ["c1", "c2"],
        "order_status": ["delivered", "delivered"],
        "order_purchase_timestamp": ["2018-01-01", "2018-06-15"],
        "order_approved_at": ["2018-01-02", "2018-06-16"],
        "order_delivered_carrier_date": ["2018-01-05", "2018-06-20"],
        "order_delivered_customer_date": ["2018-01-11", "2018-06-25"],  # 10 days and 10 days
        "order_estimated_delivery_date": ["2018-01-20", "2018-07-01"]
    })
    df_items = pd.DataFrame({
        "order_id": ["o1", "o2"],
        "order_item_id": [1, 1],
        "product_id": ["p1", "p2"],
        "seller_id": ["s1", "s2"],
        "shipping_limit_date": ["2018-01-05", "2018-06-20"],
        "price": [100.0, 200.0],
        "freight_value": [10.0, 20.0]
    })
    df_payments = pd.DataFrame({
        "order_id": ["o1", "o2"],
        "payment_sequential": [1, 1],
        "payment_type": ["credit_card", "boleto"],
        "payment_installments": [1, 1],
        "payment_value": [110.0, 220.0]
    })
    df_reviews = pd.DataFrame({
        "review_id": ["r1", "r2"],
        "order_id": ["o1", "o2"],
        "review_score": [5, 4]
    })
    result = transform_orders(df_orders, df_items, df_payments, df_reviews)
    # o1: Jan 11 - Jan 1 = 10 days; o2: Jun 25 - Jun 15 = 10 days
    assert result["delivery_days"].tolist() == [10, 10], \
        f"Expected [10, 10] but got {result['delivery_days'].tolist()}"

def test_transform_orders_handles_missing_delivery_date():
    """Orders with no delivery date should get delivery_days=0, not NaN."""
    df_orders = pd.DataFrame({
        "order_id": ["o1"],
        "customer_id": ["c1"],
        "order_status": ["shipped"],
        "order_purchase_timestamp": ["2018-03-01"],
        "order_approved_at": ["2018-03-02"],
        "order_delivered_carrier_date": [None],
        "order_delivered_customer_date": [None],  # Not yet delivered
        "order_estimated_delivery_date": ["2018-03-20"]
    })
    df_items = pd.DataFrame({
        "order_id": ["o1"],
        "order_item_id": [1],
        "product_id": ["p1"],
        "seller_id": ["s1"],
        "shipping_limit_date": ["2018-03-05"],
        "price": [50.0],
        "freight_value": [5.0]
    })
    df_payments = pd.DataFrame({
        "order_id": ["o1"],
        "payment_sequential": [1],
        "payment_type": ["credit_card"],
        "payment_installments": [1],
        "payment_value": [55.0]
    })
    df_reviews = pd.DataFrame({"review_id": [], "order_id": [], "review_score": []})
    result = transform_orders(df_orders, df_items, df_payments, df_reviews)
    assert result["delivery_days"].isnull().sum() == 0, "delivery_days must never be null"
    assert result["delivery_days"].iloc[0] == 0, "Missing delivery date must yield 0"

# ──────────────────────────────────────────────
# dim_sellers tests
# ──────────────────────────────────────────────

def test_transform_sellers_deduplicates_and_standardizes():
    """dim_sellers must have unique seller_ids and standardized city/state casing."""
    mock_sellers = pd.DataFrame({
        "seller_id": ["s1", "s1", "s2"],
        "seller_zip_code_prefix": [10001, 10001, 20002],
        "seller_city": ["sao paulo", "sao paulo", "curitiba"],
        "seller_state": ["sp", "sp", "pr"]
    })
    df_cleaned = transform_sellers(mock_sellers)
    assert df_cleaned["seller_id"].duplicated().sum() == 0
    assert df_cleaned["seller_state"].iloc[0] == "SP"
    assert df_cleaned["seller_city"].iloc[0] == "Sao Paulo"