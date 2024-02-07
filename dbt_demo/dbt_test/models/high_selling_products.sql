-- models/high_selling_products.sql

{{ config(materialized='view') }}

SELECT
    product_id,
    total_sales
FROM {{ ref('product_sales') }}
WHERE total_sales > 300
