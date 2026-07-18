WITH product_revenue AS (
    SELECT 
        c.customer_state,
        p.product_category,
        ROUND(SUM(f.price)::numeric, 2) as total_sales,
        ROW_NUMBER() OVER (PARTITION BY c.customer_state ORDER BY SUM(f.price) DESC) as rank
    FROM fact_orders f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY c.customer_state, p.product_category
)
SELECT 
    customer_state,
    product_category,
    total_sales
FROM product_revenue
WHERE rank <= 3
ORDER BY customer_state ASC, total_sales DESC;