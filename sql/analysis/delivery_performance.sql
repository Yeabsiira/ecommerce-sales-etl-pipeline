SELECT 
    p.product_category,
    ROUND(AVG(f.delivery_days)::numeric, 1) as avg_delivery_days,
    ROUND(AVG(f.review_score)::numeric, 2) as avg_review_score,
    COUNT(f.order_id) as total_items_sold
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_category
HAVING COUNT(f.order_id) > 100
ORDER BY avg_review_score ASC;