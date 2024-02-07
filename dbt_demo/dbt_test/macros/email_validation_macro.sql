-- macros/email_validation_macro.sql

{% macro test_email_validation(model, column_name) %}

SELECT
    {{ column_name }}
FROM
    {{ model }}
WHERE
    {{ column_name }} IS NOT NULL
    AND {{ column_name }} !~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

{% endmacro %}
