# 01 — Project Objective

## Project title

**Customer Churn & Retention Analytics**

## Objective

Analyze a telecommunications customer snapshot to understand the distribution of observed churn, identify customer segments associated with higher churn, and prepare evidence-based questions for the retention team.

## Business problem

Customer churn can reduce recurring revenue and increase pressure on acquisition teams. The business needs a clear view of where churn is concentrated before deciding where to investigate retention opportunities.

## Objectives

1. Calculate the overall customer count, churned customer count, and observed churn rate.
2. Compare churn rates across contract types, tenure bands, payment methods, and service attributes.
3. Combine churn rate with segment volume so the business does not prioritize a tiny segment solely because its rate is high.
4. Describe the monthly charges associated with customers labeled as churned, with appropriate caveats.
5. Turn findings into practical, testable next steps and identify data needed to validate interventions.

## Out of scope

- Production-grade machine learning or automated customer scoring.
- Causal claims such as “month-to-month contracts cause churn.”
- Cohort retention, survival analysis, or future-month forecast claims without dated longitudinal data.
- Calculating customer lifetime value unless a valid definition and the necessary data are introduced.
- Claiming that a retention campaign will achieve a specific uplift without an experiment.

## Success criteria

- Every KPI has a written definition and can be reproduced from the notebook.
- Data-quality decisions are documented.
- Notebook totals and dashboard totals reconcile exactly (customer counts) and within rounding (rates).
- The Streamlit dashboard has clear filters, a useful summary page, and segment-level context.
- Recommendations distinguish observed evidence from hypotheses.
