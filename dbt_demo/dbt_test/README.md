# DBT Demo Project

## Overview

This project demonstrates the advantages of using dbt for data transformation, including version control, modularity, testing, documentation, and performance optimization.

## Setup Instructions

1. **Install DBT**
   - Run `pip install dbt` `pip install dbt-postgres` to install dbt.

2. **Configure Database Connection**
   - Check `~/.dbt/profiles.yml` with your PostgreSQL connection details. 

3. **Load Sample Data**
   - Load the provided CSV files into your PostgreSQL database.

4. **Running Your DBT Project**
   - Navigate to the project directory and run `dbt run` to execute your models. 
    ```
    {{ config(materialized='view') }} -> create a view or table
    ```    
   - Run `dbt test` to execute tests. Self define column test need to use `macros`
   - Generate documentation with `dbt docs generate` and view it by running `dbt docs serve`.

## Advantages of DBT

- **Version Control and Collaboration:** Utilize **Git** for collaborative development and version history.
- **Modularity and Reusability:** Define transformations in modular SQL files for easy management.
- **Testing and Data Quality:** Implement data tests to ensure quality.
- **Documentation:** Automatically generate and maintain project documentation.
- **Performance Optimization:** Leverage database features for efficient data transformation.
- **Scheduling and Orchestration:** easily work with **airflow**

## other 
- Run `dbt debug`: This command helps identify connection issues or configuration problems. 
- dbt run use case: creating view / tables, Incremental Updates (incremental materialization), Triggers and Updates
- `macros` test: {% macro test_email_validation(model, column_name) %}, it auto detect the name after test_
- if test failed, we need action to roll back or fix the issue, not include in dbt services 