# 05 — Data Quality Plan

## Checks to run before analysis

1. File and schema: confirm the correct source file and expected fields.
2. Shape: record total rows and columns from the downloaded file.
3. Uniqueness: count duplicated `customerID` values.
4. Missingness: count nulls and blank strings by column.
5. Types: convert `tenure`, `MonthlyCharges`, and `TotalCharges` carefully.
6. Category validation: inspect distinct values for `Churn`, `Contract`, `PaymentMethod`, and service columns.
7. Numeric validity: inspect negative values and out-of-range tenure.
8. Logical checks: compare blank `TotalCharges` records with tenure and billing fields; do not impute without documenting the reason.
9. Reconciliation: ensure clean-table customer count equals raw count minus explicitly excluded rows.

## Expected known risk

In the commonly distributed CSV, `TotalCharges` can be stored as text and may have blank-looking values. Treat whitespace-only strings as missing before numeric conversion. Report how many are affected and decide how to handle them after inspecting related fields.

## Cleaning decision log

Executed on 2026-11-07 against `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` (7,043 rows × 21 columns). Source: `outputs/cleaning_decision_log.csv`, `outputs/data_quality_checks.csv`.

| Issue | Actual count | Decision | Rationale |
|---|---:|---|---|
| Duplicate customer IDs | 0 | No action | `customerID` is unique; no row dropped |
| Blank / null `TotalCharges` | 11 | Keep rows; leave missing, no imputation | All 11 have `tenure = 0` (new customers not yet billed) and `Churn = No`. Their churn label is valid, so they stay in churn KPIs. `TotalCharges` is not used in any KPI |
| Invalid churn categories | 0 | No action | Only `Yes` / `No` present |
| Invalid tenure / charge values | 0 | No action | `tenure` within 0–72; `MonthlyCharges` > 0 (range 18.25–118.75) |
| Rows excluded from analysis | 0 | — | Clean rows = raw rows = 7,043 |

## Rule

Do not write “data is clean” until each check has a recorded result. Results above come from the executed notebook (`notebooks/01_data_audit_and_eda.ipynb`, sections 2–4b). Because no database is used, the SQL-vs-Python reconciliation was replaced by in-notebook assertions (row count, ID uniqueness, churn flag sum).
