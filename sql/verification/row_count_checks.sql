SELECT 'dim_customers' as table_name, COUNT(*) as row_count FROM dim_customers
UNION ALL
SELECT 'dim_products', COUNT(*) FROM dim_products
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'fact_orders', COUNT(*) FROM fact_orders;