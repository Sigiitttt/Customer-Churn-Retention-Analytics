# 09 — Streamlit Dashboard

This dashboard replaces the originally planned Power BI report. It is a local Python web app; no database is used.

## Run it

```bash
python -m pip install -r requirements.txt
# 1) run notebooks/01_data_audit_and_eda.ipynb first (creates data/processed/telco_customer_churn_clean.csv)
python -m streamlit run app/streamlit_app.py
```

The app opens at <http://localhost:8501>.

## Purpose

Help a retention or customer-success stakeholder inspect where observed churn is concentrated and compare rates with customer counts. It guides investigation; it does not present correlations as causes.

## Pages

| Page | Content |
|---|---|
| Executive Overview | Cards (total, churned, churn rate, retained); churn by contract and by tenure band; selectable segment table with size, churned count and rate |
| Segment Explorer | Churn rate for any attribute with `n` labels; small-segment warning (< 30 customers); add-on services within the same internet type |
| Billing & Tenure | Average tenure and monthly charges by churn status; distributions; contract × tenure heatmap with the counts behind it |
| Priority Segments | Rate + volume ranking with an adjustable minimum segment size; rate-vs-volume bubble chart |
| Method & Limitations | Cleaning decisions, KPI definitions, caveats |

Sidebar filters (contract, internet service, payment method, tenure band) apply to every page, and all KPIs are recomputed from the filtered counts.

## Design principles kept from the original plan

- Counts shown alongside rates (bar labels and tooltips).
- Overall rate recomputed from counts, never averaged from segment percentages.
- Monthly charges for churned customers labeled as descriptive, never "lost revenue".
- Source/limitations note visible in the sidebar and on the Method page.
- No predictive risk scoring.

## Acceptance checks (all passed on 2026-11-07)

- All five pages render without exceptions (headless `AppTest` run).
- Unfiltered totals match the notebook: 7,043 / 1,869 / 26.54% / 5,174.
- Filter Contract = Month-to-month gives 3,875 / 1,655 / 42.71%, equal to `outputs/churn_by_contract.csv`.
- An empty filter shows a warning instead of crashing.
- The server starts and answers HTTP 200 on `/_stcore/health`.
