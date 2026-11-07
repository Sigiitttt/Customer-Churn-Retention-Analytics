-- Execute after telco_customer_churn_clean exists and the audit is complete.

-- 1. Overall KPI snapshot
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')) AS valid_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 'Yes')
        / NULLIF(COUNT(*) FILTER (WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')), 0),
        2
    ) AS observed_churn_rate_pct,
    ROUND(AVG(tenure_months) FILTER (WHERE churn = 'Yes'), 2) AS avg_tenure_churned_months,
    ROUND(AVG(tenure_months) FILTER (WHERE churn = 'No'), 2) AS avg_tenure_retained_months,
    ROUND(SUM(monthly_charges) FILTER (WHERE churn = 'Yes'), 2) AS monthly_charges_churn_group,
    ROUND(AVG(monthly_charges) FILTER (WHERE churn = 'Yes'), 2) AS avg_monthly_charges_churned,
    ROUND(AVG(monthly_charges) FILTER (WHERE churn = 'No'), 2) AS avg_monthly_charges_retained
FROM telco_customer_churn_clean
WHERE customer_id IS NOT NULL
  AND churn IN ('Yes', 'No');

-- 2. Overall churn counts / rate by contract
SELECT
    contract,
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM telco_customer_churn_clean
WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')
GROUP BY contract
ORDER BY churn_rate_pct DESC NULLS LAST;
