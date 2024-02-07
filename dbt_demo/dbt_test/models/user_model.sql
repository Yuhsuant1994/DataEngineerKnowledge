SELECT *
FROM {{ source('dbt_demo_set', 'users') }}