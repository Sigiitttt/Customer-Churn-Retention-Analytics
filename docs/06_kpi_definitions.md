# 06 — KPI Definitions

All metrics are customer-level unless otherwise stated. Calculate them after validating that one record corresponds to one unique customer.

| KPI | Definition | Interpretation note |
|---|---|---|
| Total customers | Count of distinct valid `customerID` | Use the cleaned analysis population |
| Churned customers | Count where `Churn = 'Yes'` | Outcome label as provided |
| Retained customers | Count where `Churn = 'No'` | Do not assume lifetime retention |
| Observed churn rate | Churned customers / total valid customers × 100% | Snapshot proportion, not a future churn forecast |
| Observed non-churn rate | Retained customers / total valid customers × 100% | Snapshot complement of churn rate |
| Average tenure — churned | Mean `tenure` among `Churn = 'Yes'` | Descriptive association |
| Average tenure — retained | Mean `tenure` among `Churn = 'No'` | Descriptive association |
| Monthly charges of churned customers | Sum of `MonthlyCharges` among `Churn = 'Yes'` | Descriptive monthly-charge total, not saved revenue forecast |
| Segment churn rate | Churned customers in a segment / all valid customers in the segment × 100% | Always show segment size alongside rate |
| Churned customer share by segment | Segment's churned count / all churned customers × 100% | Helps locate where churn volume is concentrated |

## Denominator rules

- For overall churn, denominator = all records in the validated customer-level analysis population with valid churn labels.
- For segment churn, denominator = all valid customers in that segment, not all churned customers.
- Avoid averaging segment percentages to derive an overall churn rate; recompute from counts.
- If a chart has multiple filters, make the denominator clear in the title or tooltip.

## Optional KPI — average monthly charge

Report average `MonthlyCharges` separately by churn label. Do not label this as customer lifetime value or lost profit; costs, margins, contract status, and future behavior are not included.
