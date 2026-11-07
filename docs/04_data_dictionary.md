# 04 — Data Dictionary

Field names below refer to the standard 21-column Kaggle CSV. Confirm actual headers in the downloaded version.

| Column | Expected type | Meaning / notes |
|---|---|---|
| `customerID` | String | Customer identifier; should be unique |
| `gender` | Category | Male / Female in the common sample |
| `SeniorCitizen` | Integer/category | 1 / 0 flag |
| `Partner` | Category | Yes / No |
| `Dependents` | Category | Yes / No |
| `tenure` | Integer | Number of months with the company |
| `PhoneService` | Category | Phone service status |
| `MultipleLines` | Category | Multiple line status; may include `No phone service` |
| `InternetService` | Category | DSL / Fiber optic / No in the common sample |
| `OnlineSecurity` | Category | Security add-on; may include `No internet service` |
| `OnlineBackup` | Category | Backup add-on; may include `No internet service` |
| `DeviceProtection` | Category | Protection add-on; may include `No internet service` |
| `TechSupport` | Category | Tech support add-on; may include `No internet service` |
| `StreamingTV` | Category | Streaming TV add-on; may include `No internet service` |
| `StreamingMovies` | Category | Streaming movies add-on; may include `No internet service` |
| `Contract` | Category | Month-to-month / One year / Two year in the common sample |
| `PaperlessBilling` | Category | Yes / No |
| `PaymentMethod` | Category | Payment method label |
| `MonthlyCharges` | Decimal | Observed monthly charge amount |
| `TotalCharges` | Decimal after cleaning | Observed accumulated charges; raw CSV may store this as text |
| `Churn` | Category | Yes / No; outcome label in the snapshot |

## Derived fields used in this project

| Derived field | Definition |
|---|---|
| `tenure_band` | 0–6, 7–12, 13–24, 25–48, 49–72 months; final bins documented in SQL/Python |
| `churn_flag` | 1 if `Churn = 'Yes'`, otherwise 0; only after validating category values |
| `monthly_charge_of_churned_customers` | Sum of `MonthlyCharges` for records labeled Churn = Yes; descriptive proxy, not recoverable future revenue |

`No internet service` and `No phone service` are valid service-state categories and must not be treated as missing data by default.
