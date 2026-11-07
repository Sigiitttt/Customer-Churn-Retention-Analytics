-- Build a clean, one-row-per-customer table after reviewing the audit.
-- This script converts blank TotalCharges to NULL; it does not impute them.
-- If numeric format checks found invalid non-blank strings, fix/review those first.

DROP TABLE IF EXISTS telco_customer_churn_clean;
CREATE TABLE telco_customer_churn_clean AS
WITH parsed AS (
    SELECT
        NULLIF(BTRIM(customer_id), '') AS customer_id,
        NULLIF(BTRIM(gender), '') AS gender,
        CASE
            WHEN BTRIM(senior_citizen) IN ('0', '1') THEN BTRIM(senior_citizen)::INTEGER
            ELSE NULL
        END AS senior_citizen,
        NULLIF(BTRIM(partner), '') AS partner,
        NULLIF(BTRIM(dependents), '') AS dependents,
        CASE WHEN BTRIM(tenure) ~ '^[0-9]+$' THEN BTRIM(tenure)::INTEGER ELSE NULL END AS tenure_months,
        NULLIF(BTRIM(phone_service), '') AS phone_service,
        NULLIF(BTRIM(multiple_lines), '') AS multiple_lines,
        NULLIF(BTRIM(internet_service), '') AS internet_service,
        NULLIF(BTRIM(online_security), '') AS online_security,
        NULLIF(BTRIM(online_backup), '') AS online_backup,
        NULLIF(BTRIM(device_protection), '') AS device_protection,
        NULLIF(BTRIM(tech_support), '') AS tech_support,
        NULLIF(BTRIM(streaming_tv), '') AS streaming_tv,
        NULLIF(BTRIM(streaming_movies), '') AS streaming_movies,
        NULLIF(BTRIM(contract), '') AS contract,
        NULLIF(BTRIM(paperless_billing), '') AS paperless_billing,
        NULLIF(BTRIM(payment_method), '') AS payment_method,
        CASE
            WHEN BTRIM(monthly_charges) ~ '^[0-9]+(\.[0-9]+)?$'
            THEN BTRIM(monthly_charges)::NUMERIC(12,2)
            ELSE NULL
        END AS monthly_charges,
        CASE
            WHEN NULLIF(BTRIM(total_charges), '') ~ '^[0-9]+(\.[0-9]+)?$'
            THEN BTRIM(total_charges)::NUMERIC(12,2)
            ELSE NULL
        END AS total_charges,
        NULLIF(BTRIM(churn), '') AS churn
    FROM telco_customer_churn_raw
), validated AS (
    SELECT *,
        CASE WHEN churn = 'Yes' THEN 1 WHEN churn = 'No' THEN 0 ELSE NULL END AS churn_flag,
        CASE
            WHEN tenure_months BETWEEN 0 AND 6 THEN '00-06 months'
            WHEN tenure_months BETWEEN 7 AND 12 THEN '07-12 months'
            WHEN tenure_months BETWEEN 13 AND 24 THEN '13-24 months'
            WHEN tenure_months BETWEEN 25 AND 48 THEN '25-48 months'
            WHEN tenure_months BETWEEN 49 AND 72 THEN '49-72 months'
            WHEN tenure_months IS NULL THEN 'Unknown'
            ELSE 'Outside expected range'
        END AS tenure_band
    FROM parsed
)
SELECT * FROM validated;

-- Validation queries: should be reviewed before analysis.
SELECT COUNT(*) AS clean_rows FROM telco_customer_churn_clean;
SELECT COUNT(DISTINCT customer_id) AS distinct_customer_ids FROM telco_customer_churn_clean;
SELECT COUNT(*) AS duplicate_customer_id_groups
FROM (
    SELECT customer_id
    FROM telco_customer_churn_clean
    GROUP BY customer_id
    HAVING COUNT(*) > 1
) d;
SELECT churn, COUNT(*) AS customers
FROM telco_customer_churn_clean
GROUP BY churn
ORDER BY customers DESC;
