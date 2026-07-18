DROP TABLE IF EXISTS fact_orders CASCADE;

CREATE TABLE fact_orders (
    order_id VARCHAR(50),
    customer_id VARCHAR(50) REFERENCES dim_customers(customer_id),
    product_id VARCHAR(50) REFERENCES dim_products(product_id),
    seller_id VARCHAR(50) REFERENCES dim_sellers(seller_id),
    date_id INT REFERENCES dim_date(date_id),
    price FLOAT,
    freight_value FLOAT,
    payment_value FLOAT,
    delivery_days INT,
    review_score FLOAT
);