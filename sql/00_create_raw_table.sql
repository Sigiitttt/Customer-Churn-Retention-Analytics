-- Staging table for the standard Kaggle CSV.
-- Columns are TEXT to preserve raw values for audit (including blank TotalCharges).
-- IMPORTANT: Confirm CSV header/order before using psql \copy without a column list.

DROP TABLE IF EXISTS telco_customer_churn_raw;
CREATE TABLE telco_customer_churn_raw (
    customer_id TEXT,
    gender TEXT,
    senior_citizen TEXT,
    partner TEXT,
    dependents TEXT,
    tenure TEXT,
    phone_service TEXT,
    multiple_lines TEXT,
    internet_service TEXT,
    online_security TEXT,
    online_backup TEXT,
    device_protection TEXT,
    tech_support TEXT,
    streaming_tv TEXT,
    streaming_movies TEXT,
    contract TEXT,
    paperless_billing TEXT,
    payment_method TEXT,
    monthly_charges TEXT,
    total_charges TEXT,
    churn TEXT
);
