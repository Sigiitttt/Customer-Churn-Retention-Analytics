# Dataset Recommendation

## Recommended dataset

**Telco Customer Churn** — Kaggle uploader `blastchar`.

- Dataset page: <https://www.kaggle.com/datasets/blastchar/telco-customer-churn/>
- Common CSV filename: `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- Common published shape: 7,043 customer rows × 21 columns
- Outcome field: `Churn` (`Yes` / `No`)
- Business domain: telecommunications subscription / customer retention

The IBM documentation describes the sample as a fictional telecom company dataset, with the churn field indicating whether a customer departed within the last month. See the [IBM Telco Customer Churn sample documentation](https://www.ibm.com/docs/en/cognos-analytics/12.1.x?topic=samples-telco-customer-churn).

## Why this dataset fits a Data Analyst portfolio

1. The columns support realistic segmentation by contract, tenure, payment method, and service bundle.
2. The label supports clearly defined churn KPIs.
3. The size is small enough for a Python notebook and a local web dashboard on a normal laptop.
4. The results can be translated into specific retention questions without requiring machine learning.

## Scope choices

This project will treat the data as a **cross-sectional customer snapshot**. It will prioritize descriptive/diagnostic questions:

- Which customer segments show higher observed churn?
- How do observed churn rates differ by contract, tenure, payment, and services?
- Which high-churn segments also have a meaningful count of customers?
- What additional operational data would be required to test a retention intervention?

It will not claim to estimate a future-month churn forecast, retention lift, or causal effect.

## Data caveats to document

- `TotalCharges` may be represented as text in the CSV and can contain blank strings; audit before conversion.
- Customer IDs should be checked for duplicates.
- Some service columns use values such as `No internet service` and `No phone service`. These are meaningful categories, not automatically missing values.
- Demographic or contract segment gaps do not explain *why* customers churn.
- Monthly charges for customers labeled `Churn = Yes` are a descriptive sum for that group, not revenue guaranteed to be recoverable.
- Verify the exact file, column names, license/source terms, and any changes made after downloading.

## Dataset alternatives

The Kaggle Telco sample is the recommended starting point because it is compact and easy to explain to hiring managers. If a future project needs true time-based retention/cohort analysis, use a dataset with dated customer activity or multiple periodic snapshots instead of trying to infer a time series from this snapshot.
