-- models/product_sales.sql

{{ config(materialized='table') }}

SELECT
    product_id,
    SUM(sales_amount) as total_sales
FROM {{ source('dbt_demo_set', 'sales') }}
GROUP BY product_id
