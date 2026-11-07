# 02 — Business Context

## Scenario

A fictional telecommunications provider wants to understand customer churn and use existing customer attributes to prioritize further investigation by its retention team.

## Stakeholders and decisions

| Stakeholder | Decision supported |
|---|---|
| Retention / Customer Success | Which segments should be investigated first? |
| Marketing | Which customer groups may require clearer offers or onboarding? |
| Product / Service Operations | Are churn patterns different across service combinations? |
| Finance | What monthly charges are associated with customers who churned? |
| Management | Where should the next retention experiment be designed? |

## Decision principle

A high churn rate alone is not enough to set priority. Use at least:

- **Rate:** what proportion of a segment churned?
- **Volume:** how many customers are in that segment?
- **Business context:** does the pattern have a plausible operational explanation that can be tested?
- **Uncertainty:** is the result supported by enough customers, and could the pattern be explained by other differences?

## Important interpretation limits

This dataset is a sample snapshot. It supports comparisons of observed churn across attributes, but does not establish that an attribute caused churn. A business recommendation should be framed as a proposed investigation or test, not a proven fix.
