SELECT 
    d.year,
    d.month,
    ROUND(SUM(f.payment_value)::numeric, 2) as monthly_revenue,
    COUNT(DISTINCT f.order_id) as total_orders
FROM fact_orders f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year ASC, d.month ASC;