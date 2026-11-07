-- Run after importing the CSV into telco_customer_churn_raw.

-- 1. Raw shape
SELECT COUNT(*) AS raw_rows FROM telco_customer_churn_raw;

-- 2. Duplicate customer identifiers
SELECT customer_id, COUNT(*) AS records
FROM telco_customer_churn_raw
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY records DESC, customer_id;

-- 3. Blank/null counts per commonly problematic fields
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL OR BTRIM(customer_id) = '') AS blank_customer_id,
    COUNT(*) FILTER (WHERE churn IS NULL OR BTRIM(churn) = '') AS blank_churn,
    COUNT(*) FILTER (WHERE tenure IS NULL OR BTRIM(tenure) = '') AS blank_tenure,
    COUNT(*) FILTER (WHERE monthly_charges IS NULL OR BTRIM(monthly_charges) = '') AS blank_monthly_charges,
    COUNT(*) FILTER (WHERE total_charges IS NULL OR BTRIM(total_charges) = '') AS blank_total_charges
FROM telco_customer_churn_raw;

-- 4. Category profile: values outside expected categories should be inspected.
SELECT BTRIM(churn) AS churn_value, COUNT(*) AS customers
FROM telco_customer_churn_raw
GROUP BY BTRIM(churn)
ORDER BY customers DESC;

SELECT BTRIM(contract) AS contract_value, COUNT(*) AS customers
FROM telco_customer_churn_raw
GROUP BY BTRIM(contract)
ORDER BY customers DESC;

SELECT BTRIM(payment_method) AS payment_method, COUNT(*) AS customers
FROM telco_customer_churn_raw
GROUP BY BTRIM(payment_method)
ORDER BY customers DESC;

-- 5. Numeric conversion diagnostic. This safely excludes blank TotalCharges from the cast.
SELECT
    COUNT(*) FILTER (WHERE NULLIF(BTRIM(tenure), '') IS NULL) AS missing_tenure,
    COUNT(*) FILTER (WHERE NULLIF(BTRIM(monthly_charges), '') IS NULL) AS missing_monthly_charges,
    COUNT(*) FILTER (WHERE NULLIF(BTRIM(total_charges), '') IS NULL) AS missing_total_charges,
    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(tenure), '') IS NOT NULL
          AND BTRIM(tenure) !~ '^[0-9]+$'
    ) AS non_integer_tenure,
    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(monthly_charges), '') IS NOT NULL
          AND BTRIM(monthly_charges) !~ '^[0-9]+(\.[0-9]+)?$'
    ) AS invalid_monthly_charges_format,
    COUNT(*) FILTER (
        WHERE NULLIF(BTRIM(total_charges), '') IS NOT NULL
          AND BTRIM(total_charges) !~ '^[0-9]+(\.[0-9]+)?$'
    ) AS invalid_total_charges_format
FROM telco_customer_churn_raw;

-- 6. Tenure range diagnostic (only cast after validating integer format above).
SELECT
    MIN(NULLIF(BTRIM(tenure), '')::INTEGER) AS min_tenure_months,
    MAX(NULLIF(BTRIM(tenure), '')::INTEGER) AS max_tenure_months
FROM telco_customer_churn_raw
WHERE NULLIF(BTRIM(tenure), '') ~ '^[0-9]+$';

-- 7. Inspect blank TotalCharges records; do not impute before reviewing these rows.
SELECT customer_id, tenure, monthly_charges, total_charges, churn
FROM telco_customer_churn_raw
WHERE NULLIF(BTRIM(total_charges), '') IS NULL
ORDER BY customer_id;
