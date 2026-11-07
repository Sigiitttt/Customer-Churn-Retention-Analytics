# 11 — Final Report

## Executive summary

This project analyzes **7,043** customer records from the Telco Customer Churn sample to understand patterns associated with observed churn. The observed churn rate is **26.54%** (1,869 churned customers). The segments most worth investigating are **customers in their first six months** (1,481 customers, 52.94% churn, 41.95% of all churn) and **month-to-month contract customers** (3,875 customers, 42.71% churn, 88.55% of all churn). Electronic-check payers, fiber-optic customers, and customers without tech support or online security also show churn rates around 1.6–1.7x the overall rate. These findings are descriptive associations and do not establish causality.

## Business problem

A telecom retention team has limited capacity. Before designing retention experiments it needs to know where observed churn is concentrated, using both the **rate** and the **volume** of each segment, and what data would be needed to validate any intervention.

## Dataset and methodology

- Source: Telco Customer Churn sample (IBM sample dataset, also published on Kaggle by `blastchar`: <https://www.kaggle.com/datasets/blastchar/telco-customer-churn/>).
- **Actual file used:** downloaded on **2026-11-07** from the public IBM copy (`raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv`) and saved as `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`. The Kaggle copy could not be downloaded without an account. The header, column order, and shape match the documented Kaggle file, but the two files were not compared byte-for-byte. SHA-256 of the file used: `16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91`.
- Raw shape: 7,043 rows × 21 columns. Validated analytical population: 7,043 (no rows excluded).
- Cleaning rules (full log: `outputs/cleaning_decision_log.csv`, [05 — Data Quality Plan](05_data_quality_plan.md)): no duplicates or invalid labels found; 11 blank `TotalCharges` values (all with tenure = 0) kept and left missing, not imputed.
- Tools: Python (pandas, matplotlib, plotly), Jupyter notebook, Streamlit dashboard. No database; everything runs locally from CSV files.
- Internal reconciliation: raw rows = clean rows; churn flag sum = count of `Churn = Yes`; the dashboard reproduces the notebook totals (overall and for a Month-to-month filter).

## KPI results

| KPI | Verified result | Definition / denominator |
|---|---:|---|
| Total customers | 7,043 | Valid unique customer records |
| Churned customers | 1,869 | `Churn = Yes` |
| Observed churn rate | 26.54% | Churned / valid customers |
| Retained customers | 5,174 | `Churn = No` |
| Average tenure, churned / retained | 17.98 / 37.57 months | Mean `tenure` by label (medians 10 / 38) |
| Average monthly charge, churned / retained | $74.44 / $61.27 | Mean `MonthlyCharges` by label |
| Monthly charges associated with churned customers | $139,130.85 | Sum of monthly charges for churn-labeled customers; descriptive only |

## Key findings

### Finding 1 — Churn is concentrated in the first six months

Evidence: tenure 0–6 months, n=1,481, 784 churned, 52.94% vs 26.54% overall (`outputs/churn_by_tenure_band.csv`). Rates decline with every later band down to 9.51% at 49–72 months (n=2,239).

Interpretation: new customers are the most fragile group and hold 41.95% of all churn. The pattern persists within Month-to-month customers (55.20% at 0–6 months vs 26.02% at 49–72 months), so it is not only a contract-mix effect. The snapshot cannot say why they leave.

### Finding 2 — Month-to-month contracts hold almost all churn volume

Evidence: Month-to-month n=3,875, 1,655 churned, 42.71%; One year 11.27% (n=1,473); Two year 2.83% (n=1,695) (`outputs/churn_by_contract.csv`).

Interpretation: month-to-month customers are 55% of the sample but 88.55% of churn. Customers who choose longer contracts differ from those who do not (and are bound by the contract term), so the gap is not an estimate of what a contract change would do.

### Finding 3 — Payment method, internet type, and support add-ons mark further high-churn groups

Evidence: Electronic check 45.29% (n=2,365) vs 15.24–19.11% for other methods; Fiber optic 41.89% (n=3,096) vs DSL 18.96%; no tech support 41.64% vs 15.17% with it, and the gap holds within DSL (27.76% vs 9.68%) and Fiber (49.37% vs 22.63%) (`outputs/segments_all.csv`, `outputs/churn_by_internet_x_techsupport.csv`).

Interpretation: these groups are large enough to matter, but they overlap with each other and with contract and tenure. The overlap for electronic check was not analyzed, so no attribute here should be called an independent driver.

### Also noted

Gender shows essentially no difference (26.92% vs 26.16%). Senior citizens (41.68%, n=1,142) and customers without partner or dependents churn more, but these are descriptive profile differences and should not be used as targeting rules without legal and ethical review.

## Recommendations

See [10 — Business Insights](10_business_insights.md) section 5 for the full table (evidence, target, action, metric, test design). In short:

1. Investigate the first-six-month experience and pilot an onboarding intervention against a randomized control.
2. Evaluate a contract-upgrade offer for month-to-month customers with margin tracking.
3. Untangle the electronic-check effect from contract and tenure before acting on it.
4. Collect service-quality and support data for fiber customers.
5. Test tech-support outreach experimentally rather than assuming the observed gap is causal.

## Limitations

- The data is a snapshot, not a longitudinal history; there are no dates, so no cohort retention, forecasting, or survival analysis.
- Associations do not prove causes; segments overlap and single-attribute rates are confounded (contract, tenure, price, service type).
- Monthly charges associated with churned customers are not recoverable revenue (no margins, contract terms, or future behavior).
- The sample is from a fictional telecom provider and may not represent any real company.
- The CSV came from the IBM public copy, not the Kaggle download; byte-level equality with Kaggle was not verified.
- The minimum segment size (300) is an analyst choice; the top-5 ranking was unchanged at 100, 300, 500 and 1,000.
- No statistical tests or multivariate modeling were done (out of scope); the sample is large, but differences between small segments should be read with caution.

## Reproducibility

- Notebook: `notebooks/01_data_audit_and_eda.ipynb` (run all cells; writes `data/processed/` and `outputs/`)
- Output tables and figures: `outputs/`, `outputs/figures/`
- Cleaned data: `data/processed/telco_customer_churn_clean.csv`
- Dashboard: `python -m streamlit run app/streamlit_app.py` (see [09 — Streamlit Dashboard](09_streamlit_dashboard.md))
