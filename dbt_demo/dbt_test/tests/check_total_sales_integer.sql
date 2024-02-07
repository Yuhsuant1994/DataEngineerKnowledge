-- tests/check_total_sales_integer.sql

SELECT
    product_id,
    total_sales
FROM {{ ref('high_selling_products') }}
WHERE total_sales <> CAST(total_sales AS INTEGER)
