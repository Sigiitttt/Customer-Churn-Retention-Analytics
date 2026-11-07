# Start Here

1. Put `WA_Fn-UseC_-Telco-Customer-Churn.csv` in `data/raw/` (Kaggle: https://www.kaggle.com/datasets/blastchar/telco-customer-churn/ ; the file currently there came from the public IBM copy, see `docs/11_final_report.md`).
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Run `notebooks/01_data_audit_and_eda.ipynb` top to bottom. It creates `data/processed/telco_customer_churn_clean.csv` and the tables/figures in `outputs/`.
4. Launch the dashboard: `python -m streamlit run app/streamlit_app.py`.
5. Read results in `docs/10_business_insights.md` and `docs/11_final_report.md`.

No database and no Power BI are needed.
