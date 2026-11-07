-- Common segment comparisons. Always keep segment size beside the rate.

-- Churn by tenure band
SELECT
    tenure_band,
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM telco_customer_churn_clean
WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')
GROUP BY tenure_band
ORDER BY MIN(tenure_months) NULLS LAST;

-- Churn by payment method
SELECT
    payment_method,
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM telco_customer_churn_clean
WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')
GROUP BY payment_method
ORDER BY churn_rate_pct DESC NULLS LAST;

-- Churn by internet service
SELECT
    internet_service,
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM telco_customer_churn_clean
WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')
GROUP BY internet_service
ORDER BY churn_rate_pct DESC NULLS LAST;

-- Churn by tech support status
SELECT
    tech_support,
    COUNT(*) AS customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM telco_customer_churn_clean
WHERE customer_id IS NOT NULL AND churn IN ('Yes', 'No')
GROUP BY tech_support
ORDER BY churn_rate_pct DESC NULLS LAST;
