# 07 — Analysis Plan

## Analysis sequence

### A. Data audit

Check schema, customer uniqueness, missing/blank values, type conversions, valid categories, and numeric ranges. Save the audit results before cleaning.

### B. Overall churn profile

Calculate total customers, churned customers, retained customers, observed churn rate, tenure averages, and monthly charge summaries.

### C. Segment analysis

Compare churn rate and segment size by:

- Contract type
- Tenure band
- Payment method
- Internet service
- Tech support and online security
- Paperless billing
- Senior-citizen flag, partner, and dependents (only where useful and handled respectfully)

### D. Prioritization

Rank segments using **observed churn rate plus segment volume**. Consider a minimum segment-size threshold (document the threshold and test whether the ranking changes). Do not interpret the ranking as causal risk without additional evidence.

### E. Translate results into business questions

Examples, only if supported after running the analysis:

- Should onboarding for a short-tenure segment be investigated?
- Should the business review value proposition or service experience in a high-churn contract segment?
- Would service-support usage or availability be worth investigating?
- Which segment would be suitable for a controlled retention experiment?

### F. Validate and communicate

Reconcile notebook and dashboard KPI totals; document filters; export summary tables; build the Streamlit dashboard; write an evidence-based final report.

## Deliverables

- Data-quality audit table
- KPI summary table
- Churn rate by key segments
- Tenure-band analysis
- Two or three focused charts with meaningful denominators
- Streamlit dashboard
- Final report with limitations and actionable next steps
