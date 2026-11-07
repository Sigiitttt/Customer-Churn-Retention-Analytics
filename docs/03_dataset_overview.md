# 03 — Dataset Overview

## Source

- Dataset: **Telco Customer Churn**
- Kaggle: <https://www.kaggle.com/datasets/blastchar/telco-customer-churn/>
- IBM sample documentation: <https://www.ibm.com/docs/en/cognos-analytics/12.1.x?topic=samples-telco-customer-churn>
- Common file: `WA_Fn-UseC_-Telco-Customer-Churn.csv`

The commonly distributed version contains 7,043 customer rows and 21 columns. Confirm row/column counts after downloading rather than hardcoding these values as analysis results.

## Grain

**One row is intended to represent one customer in the supplied snapshot.** Verify that `customerID` is unique before computing customer-level KPIs.

## Data groups

- Customer profile: gender, senior-citizen flag, partner, dependents.
- Tenure and service usage: tenure, phone/internet, add-on services.
- Contract and billing: contract, paperless billing, payment method, monthly charges, total charges.
- Outcome: churn label.

## File placement

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

Keep the source CSV unchanged. Store any cleaned output separately under `data/processed/` or `outputs/`.

## Snapshot limitations

The file does not provide a complete event history for each customer or repeated monthly snapshots. Avoid time-series claims, month-by-month cohort retention, causal claims, and claims that a model can forecast a particular future period.
