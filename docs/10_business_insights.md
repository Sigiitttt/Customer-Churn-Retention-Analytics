# 10 — Business Insights

> **Status: Populated from executed analysis.** Every number below comes from `notebooks/01_data_audit_and_eda.ipynb` run on `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` (see [11 — Final Report](11_final_report.md) for the data source note). Source tables are in `outputs/`. All statements are **associations in a snapshot**, not causes.

## 1. Overall churn

- Total validated customers: **7,043** (no rows excluded)
- Churned customers: **1,869**
- Retained customers: **5,174**
- Observed churn rate: **26.54%** (1,869 / 7,043)
- Interpretation: roughly 1 in 4 customers in this sample is labeled as having left within the last month. The denominator is all valid customers in the snapshot.

## 2. Highest-priority segments (rate + volume)

Ranked by observed churn rate among segments with at least 300 customers (`outputs/segment_priority.csv`). The top 5 are identical for minimum sizes of 100, 300, 500 and 1,000 (`outputs/segment_priority_sensitivity.csv`), so the ranking does not depend on the threshold.

| Segment | Customers | Churned | Churn rate | Share of all churned | Lift vs overall |
|---|---:|---:|---:|---:|---:|
| Tenure 0–6 months | 1,481 | 784 | 52.94% | 41.95% | 1.99x |
| Payment: Electronic check | 2,365 | 1,071 | 45.29% | 57.30% | 1.71x |
| Contract: Month-to-month | 3,875 | 1,655 | 42.71% | 88.55% | 1.61x |
| Internet: Fiber optic | 3,096 | 1,297 | 41.89% | 69.40% | 1.58x |
| Online security: No | 3,498 | 1,461 | 41.77% | 78.17% | 1.57x |

Segments overlap, so the "share of all churned" column must not be summed.

## 3. Tenure patterns

- Churn falls steadily with tenure: 52.94% (0–6 months, n=1,481) → 35.89% (7–12, n=705) → 28.71% (13–24, n=1,024) → 20.39% (25–48, n=1,594) → 9.51% (49–72, n=2,239).
- Churned customers have a median tenure of **10 months** vs **38 months** for retained customers (means 17.98 vs 37.57).
- 784 of the 1,869 churned customers (41.95%) were in their first six months.
- Business question: what happens to customers in the first six months (onboarding, first bill, installation, early service problems), and how do early leavers differ from those who stay?

## 4. Contract, payment, and service patterns

- **Contract:** Month-to-month 42.71% (n=3,875) vs One year 11.27% (n=1,473) vs Two year 2.83% (n=1,695). Month-to-month customers are 55% of the sample but 88.55% of churned customers.
- **Contract and tenure overlap:** within Month-to-month, churn still falls with tenure (55.20% at 0–6 months, n=1,413 → 26.02% at 49–72 months, n=342). So the tenure pattern is not just an artifact of contract mix. One-year and two-year contracts have very few customers in the first year (e.g. two-year 0–6 months n=29, 0 churned), so their short-tenure rates are not reliable.
- **Payment method:** Electronic check 45.29% vs 15–19% for mailed check (19.11%), bank transfer (16.71%) and credit card (15.24%), the last two being automatic payment. The overlap of electronic check with contract type and tenure was **not** tested here.
- **Internet service:** Fiber optic 41.89% vs DSL 18.96% vs no internet 7.40%. Fiber customers are 44% of the sample and 69.40% of churned customers. Price, service quality, competition and customer mix are all untested explanations.
- **Support add-ons:** Customers without tech support churn at 41.64% (n=3,473) vs 15.17% with it (n=2,044). The gap holds within the same internet type: DSL 27.76% vs 9.68%; Fiber 49.37% vs 22.63% (`outputs/churn_by_internet_x_techsupport.csv`). Online security shows a similar gap (41.77% vs 14.61%). Customers who choose add-ons may differ in other ways, so this is not evidence the add-on reduces churn.
- **Paperless billing:** Yes 33.57% (n=4,171) vs No 16.33% (n=2,872).
- **Customer profile:** Senior citizens 41.68% (n=1,142) vs 23.61% for others; no partner 32.96% vs 19.66%; no dependents 31.28% vs 15.45%. Gender shows almost no difference (Female 26.92%, Male 26.16%). Treat profile attributes with care and only as descriptive context, not as targeting criteria.
- **Billing:** Churned customers pay more per month on average ($74.44 vs $61.27; medians $79.65 vs $64.43). The monthly charges of the churn-labeled group sum to **$139,130.85**. This is a descriptive total, not lost or recoverable revenue.

## 5. Business recommendations (hypotheses to investigate, not proven fixes)

| # | Evidence | Target segment | Proposed next action | Metric to monitor | How to test |
|---|---|---|---|---|---|
| 1 | 0–6 month tenure churns at 52.94%, 41.95% of all churn | New customers, first 6 months (n=1,481 in sample) | Review the onboarding and first-bills experience; interview early leavers | Churn within first 6 months | Randomized onboarding-contact pilot vs. control |
| 2 | Month-to-month: 42.71% churn, 88.55% of churn volume | Month-to-month customers (n=3,875) | Examine whether a contract-upgrade offer is viable and profitable | Month-to-month → annual conversion; churn after offer | A/B offer test with margin tracking |
| 3 | Electronic check 45.29% vs 15–19% elsewhere | Electronic check payers (n=2,365) | Check for billing/payment friction; first untangle overlap with contract and tenure | Churn by payment method, adjusted for contract and tenure | Pilot of payment-method nudges after the overlap analysis |
| 4 | Fiber optic 41.89% vs DSL 18.96% | Fiber customers (n=3,096) | Investigate service quality, pricing and competitor offers for fiber | Churn and support-ticket rate in fiber | Needs operational data first |
| 5 | No tech support: 41.64% vs 15.17% (gap persists within DSL and Fiber) | Internet customers without tech support (n=3,473) | Test whether offering a trial of tech support or support outreach changes churn | Churn of offered vs. not offered | Randomized trial; observational gap alone cannot justify it |

No recommendation promises a specific churn reduction, revenue recovery or campaign uplift.

## 6. Further data needed

Dated monthly customer snapshots (for cohorts and survival), cancellation dates and reasons, support tickets, outage and service-quality events, offer and campaign exposure, contract renewal events, competitor pricing, contribution margin by plan, and acquisition channel. A multivariate or modeling phase (e.g. logistic regression to separate overlapping effects) is a possible future step and was deliberately left out of this project's scope.
