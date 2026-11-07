# 08 — SQL Workflow (optional, not used)

The project now runs entirely in Python from CSV files (no database). All KPIs, cleaning and segmentation are in `notebooks/01_data_audit_and_eda.ipynb`.

The PostgreSQL starter scripts in `sql/` are kept only as an optional reference for readers who want a SQL version. They were **never executed** here, so they are not evidence and no result in this project relies on them. If you run them, reconcile their totals against `outputs/kpi_summary.csv` (customer counts must match exactly).

Python-side integrity checks that replace the SQL reconciliation are in notebook section 4b: row count equals raw count, `customer_id` is unique, and the churn flag sum equals the count of `Churn = Yes`.
