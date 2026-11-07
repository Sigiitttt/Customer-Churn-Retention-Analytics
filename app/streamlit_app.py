"""Customer Churn & Retention Analytics - Streamlit dashboard (report-canvas style).

Reads the cleaned CSV produced by notebooks/01_data_audit_and_eda.ipynb
(data/processed/telco_customer_churn_clean.csv). No database is used.

Run from the project root:
    python -m streamlit run app/streamlit_app.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "telco_customer_churn_clean.csv"

TENURE_ORDER = ["00-06 months", "07-12 months", "13-24 months", "25-48 months", "49-72 months"]
LABELS = {
    "contract": "Contract", "tenure_band": "Tenure band", "payment_method": "Payment method",
    "internet_service": "Internet service", "online_security": "Online security",
    "tech_support": "Tech support", "online_backup": "Online backup",
    "device_protection": "Device protection", "streaming_tv": "Streaming TV",
    "streaming_movies": "Streaming movies", "paperless_billing": "Paperless billing",
    "senior_citizen_label": "Senior citizen", "partner": "Partner", "dependents": "Dependents",
    "multiple_lines": "Multiple lines", "phone_service": "Phone service", "gender": "Gender",
}
MIN_RELIABLE_N = 30

# Power-BI-like palette
TEAL, DARK, RED, YELLOW, GREY, SKY, ORANGE, PURPLE = (
    "#01B8AA", "#374649", "#FD625E", "#F2C80F", "#5F6B6D", "#8AD4EB", "#FE9666", "#A66999")
PALETTE = [TEAL, DARK, RED, YELLOW, SKY, ORANGE, PURPLE, GREY]

st.set_page_config(page_title="Churn Analysis", page_icon=":bar_chart:", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
html, body, [class*="css"], .stApp { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
.stApp { background: #EAEAEA; }
header[data-testid="stHeader"] { background: transparent; height: 0; }
.block-container { padding: 0 1.2rem 2rem 1.2rem; max-width: 100%; }
#MainMenu, footer { visibility: hidden; }

.topbar { background:#1b1b1b; color:#fff; margin: 0 -1.2rem 12px -1.2rem; padding: 10px 24px;
          font-size: 13px; letter-spacing: .2px; display:flex; justify-content:space-between; }
.topbar b { font-weight: 600; }
.topbar span { color:#b5b5b5; }

/* tiles */
div[data-testid="stVerticalBlockBorderWrapper"] {
  background:#fff; border:none !important; border-radius:3px;
  box-shadow: 0 1px 2px rgba(0,0,0,.12); padding: 4px 6px;
}
.tile-title { font-size: 13px; font-weight: 600; color:#333; margin: 2px 0 0 0; }
.tile-sub { font-size: 10px; letter-spacing:.4px; text-transform: uppercase; color:#8a8a8a; margin-bottom: 4px; }
.kpi { font-size: 46px; font-weight: 300; color:#444; text-align:center; line-height: 1.15; padding: 14px 0 6px 0; }
.kpi.small { font-size: 38px; }
.kpi-note { text-align:center; font-size: 11px; color:#7a7a7a; padding-bottom: 8px; min-height: 28px; }
.filter-label { font-size: 10px; letter-spacing:.4px; text-transform: uppercase; color:#8a8a8a; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; }
.stTabs [data-baseweb="tab"] { background:#fff; border-radius:3px 3px 0 0; padding: 6px 16px; font-size: 13px; }
.stTabs [aria-selected="true"] { border-bottom: 3px solid #01B8AA; }
.footnote { font-size: 11px; color:#6b6b6b; padding: 6px 4px; }
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ helpers
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["tenure_band"] = pd.Categorical(df["tenure_band"], categories=TENURE_ORDER, ordered=True)
    return df


def segment_table(data: pd.DataFrame, column: str, total_churned: int) -> pd.DataFrame:
    t = (data.groupby(column, observed=True)
         .agg(customers=("customer_id", "nunique"), churned_customers=("churn_flag", "sum"))
         .reset_index())
    t["churn_rate_pct"] = (100 * t["churned_customers"] / t["customers"]).round(2)
    t["share_of_churned_pct"] = (100 * t["churned_customers"] / total_churned).round(2) if total_churned else 0.0
    return t


def tile_head(title: str, sub: str = ""):
    st.markdown(f'<div class="tile-title">{title}</div><div class="tile-sub">{sub}</div>', unsafe_allow_html=True)


def kpi_tile(title: str, sub: str, value: str, note: str = "", small: bool = False):
    with st.container(border=True):
        tile_head(title, sub)
        st.markdown(f'<div class="kpi{" small" if small else ""}">{value}</div>'
                    f'<div class="kpi-note">{note}</div>', unsafe_allow_html=True)


def style(fig, h=300, legend=True):
    fig.update_layout(
        height=h, margin=dict(l=6, r=6, t=8, b=6), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Segoe UI, Arial", size=11, color="#555"),
        showlegend=legend, legend=dict(orientation="h", y=1.12, x=0, font_size=10, title_text=""),
        hoverlabel=dict(font_size=11),
    )
    fig.update_xaxes(showgrid=False, linecolor="#d0d0d0", zeroline=False)
    fig.update_yaxes(gridcolor="#eeeeee", zeroline=False)
    return fig


def show(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def rate_bar(table: pd.DataFrame, column: str, overall: float, h=260):
    t = table.sort_values("churn_rate_pct")
    colors = [RED if r > overall else TEAL for r in t["churn_rate_pct"]]
    fig = go.Figure(go.Bar(
        x=t["churn_rate_pct"], y=t[column].astype(str), orientation="h", marker_color=colors,
        text=[f"{r:.1f}%  n={int(n):,}" for r, n in zip(t["churn_rate_pct"], t["customers"])],
        textposition="outside", cliponaxis=False,
        customdata=t[["customers", "churned_customers"]].values,
        hovertemplate="%{y}<br>Churn rate: %{x:.2f}%<br>Customers: %{customdata[0]:,}"
                      "<br>Churned: %{customdata[1]:,}<extra></extra>"))
    fig.add_vline(x=overall, line_dash="dash", line_color=DARK, line_width=1, layer="below")
    fig.update_xaxes(range=[0, max(t["churn_rate_pct"].max() * 1.55, 5)], ticksuffix="%")
    return style(fig, h, legend=False)


# ------------------------------------------------------------------ data
if not DATA_PATH.exists():
    st.error(f"Cleaned data not found at `{DATA_PATH}`. Run `notebooks/01_data_audit_and_eda.ipynb` first.")
    st.stop()
full = load_data()

st.markdown('<div class="topbar"><b>Customer Churn &amp; Retention Analytics</b>'
            '<span>Telco sample snapshot · 7,043 customers · descriptive, not causal</span></div>',
            unsafe_allow_html=True)

# ------------------------------------------------------------------ filters (top row)
with st.container(border=True):
    fc = st.columns(4)
    def multi(col_ui, label, column, order=None):
        opts = order or sorted(full[column].dropna().unique().tolist())
        with col_ui:
            st.markdown(f'<div class="filter-label">{label}</div>', unsafe_allow_html=True)
            return st.multiselect(label, opts, default=opts, label_visibility="collapsed")
    f_contract = multi(fc[0], "Contract", "contract")
    f_internet = multi(fc[1], "Internet service", "internet_service")
    f_payment = multi(fc[2], "Payment method", "payment_method")
    f_tenure = multi(fc[3], "Tenure band", "tenure_band", TENURE_ORDER)

df = full[full["contract"].isin(f_contract) & full["internet_service"].isin(f_internet)
          & full["payment_method"].isin(f_payment) & full["tenure_band"].isin(f_tenure)]

if df.empty:
    st.warning("No customers match the current filters.")
    st.stop()

n_total = len(df)
n_churn = int(df["churn_flag"].sum())
n_ret = n_total - n_churn
rate = 100 * n_churn / n_total
full_rate = 100 * full["churn_flag"].mean()
ch, rt = df[df["churn_flag"] == 1], df[df["churn_flag"] == 0]

tab_dash, tab_explore, tab_prio, tab_method = st.tabs(
    ["Dashboard", "Segment Explorer", "Priority Segments", "Method & Limitations"])

# ================================================================== DASHBOARD
with tab_dash:
    k = st.columns(6)
    with k[0]:
        kpi_tile("Total Customers", "Valid unique records", f"{n_total:,}", f"{100*n_total/len(full):.0f}% of all customers")
    with k[1]:
        kpi_tile("Churned Customers", "Churn = Yes", f"{n_churn:,}", f"{100*n_churn/max(len(full[full.churn_flag==1]),1):.0f}% of all churned")
    with k[2]:
        kpi_tile("Observed Churn Rate", "Churned / customers", f"{rate:.1f}%", f"{rate-full_rate:+.1f} pts vs all ({full_rate:.1f}%)")
    with k[3]:
        kpi_tile("Retained Customers", "Churn = No", f"{n_ret:,}", "snapshot, not lifetime retention")
    with k[4]:
        if len(ch) and len(rt):
            kpi_tile("Avg Tenure, Churned", "Months", f"{ch.tenure.mean():.1f}", f"vs {rt.tenure.mean():.1f} retained")
        else:
            kpi_tile("Avg Tenure", "Months", f"{df.tenure.mean():.1f}", "single churn status in filter")
    with k[5]:
        kpi_tile("Monthly Charges, Churned", "Descriptive sum", f"${ch.monthly_charges.sum()/1000:,.0f}K",
                 "billed monthly; not lost revenue", small=False)

    # ---- row 2: tenure combo | bubble | donut
    r2 = st.columns([1.35, 1.35, 0.8])
    with r2[0]:
        with st.container(border=True):
            tile_head("Customers and Churn Rate", "by tenure band")
            tb = segment_table(df, "tenure_band", n_churn)
            tb["retained"] = tb["customers"] - tb["churned_customers"]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_bar(x=tb["tenure_band"].astype(str), y=tb["retained"], name="Retained", marker_color=TEAL, secondary_y=False)
            fig.add_bar(x=tb["tenure_band"].astype(str), y=tb["churned_customers"], name="Churned", marker_color=DARK, secondary_y=False)
            fig.add_scatter(x=tb["tenure_band"].astype(str), y=tb["churn_rate_pct"], name="Churn rate %", mode="lines+markers+text",
                            text=[f"{v:.0f}%" for v in tb["churn_rate_pct"]], textposition="top center",
                            line=dict(color=ORANGE, width=3), marker=dict(size=8), secondary_y=True)
            fig.update_layout(barmode="stack")
            fig.update_yaxes(title_text="Customers", secondary_y=False)
            fig.update_yaxes(title_text="Churn rate", ticksuffix="%", range=[0, 75], showgrid=False, secondary_y=True)
            show(style(fig, 300))
    with r2[1]:
        with st.container(border=True):
            tile_head("Segment Size vs. Churn Rate", "every segment · bubble = churned customers")
            rows = []
            for d in ["contract", "tenure_band", "payment_method", "internet_service", "tech_support",
                      "online_security", "paperless_billing", "senior_citizen_label", "partner", "dependents"]:
                s = segment_table(df, d, n_churn).rename(columns={d: "segment"})
                s["segment"] = s["segment"].astype(str)
                s["dimension"] = LABELS[d]
                rows.append(s)
            allseg = pd.concat(rows, ignore_index=True)
            allseg = allseg[allseg["customers"] >= MIN_RELIABLE_N]
            fig = px.scatter(allseg, x="customers", y="churn_rate_pct", size="churned_customers", color="dimension",
                             hover_name="segment", size_max=34, color_discrete_sequence=PALETTE,
                             custom_data=["dimension", "churned_customers"],
                             labels={"customers": "Segment size (customers)", "churn_rate_pct": "Churn rate (%)"})
            fig.update_traces(hovertemplate="<b>%{hovertext}</b> (%{customdata[0]})<br>n=%{x:,}"
                              "<br>Churned: %{customdata[1]:,}<br>Rate: %{y:.1f}%<extra></extra>",
                              marker=dict(opacity=.8, line=dict(width=0)))
            fig.add_hline(y=rate, line_dash="dash", line_color=DARK, line_width=1)
            fig.update_yaxes(ticksuffix="%")
            fig = style(fig, 300)
            fig.update_layout(legend=dict(orientation="v", x=1.01, y=1, font_size=10),
                              margin=dict(l=6, r=6, t=8, b=6))
            show(fig)
    with r2[2]:
        with st.container(border=True):
            tile_head("Churn Share", "churned vs retained")
            fig = go.Figure(go.Pie(labels=["Retained", "Churned"], values=[n_ret, n_churn], hole=.62,
                                   marker_colors=[TEAL, DARK], textinfo="percent", sort=False,
                                   hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>"))
            fig.add_annotation(text=f"<b>{rate:.1f}%</b><br><span style='font-size:10px'>churn</span>",
                               showarrow=False, font_size=20)
            show(style(fig, 300))

    # ---- row 3: three rate bars
    r3 = st.columns(3)
    for col_ui, (d, sub) in zip(r3, [("contract", "by contract type"), ("payment_method", "by payment method"),
                                      ("internet_service", "by internet service")]):
        with col_ui:
            with st.container(border=True):
                tile_head("Churn Rate", sub)
                show(rate_bar(segment_table(df, d, n_churn), d, rate, 250))
    st.markdown('<div class="footnote">Red bars = above the filtered overall rate (dashed line); teal = at or below. '
                'Labels show rate and segment size n.</div>', unsafe_allow_html=True)

    # ---- row 4: heatmap | add-on | monthly charges
    r4 = st.columns([1.1, 1.1, 1])
    with r4[0]:
        with st.container(border=True):
            tile_head("Churn Rate, Contract × Tenure", "% churned · small cells are unstable")
            ct = (df.groupby(["contract", "tenure_band"], observed=True)
                  .agg(customers=("customer_id", "nunique"), churned=("churn_flag", "sum")).reset_index())
            ct["rate"] = (100 * ct["churned"] / ct["customers"]).round(1)
            heat = ct.pivot(index="tenure_band", columns="contract", values="rate")
            cnt = ct.pivot(index="tenure_band", columns="contract", values="customers").reindex_like(heat)
            fig = go.Figure(go.Heatmap(
                z=heat.values, x=heat.columns, y=[str(i) for i in heat.index], colorscale=[[0, "#E6F7F5"], [1, "#5DD6CB"]],
                text=[[("" if pd.isna(v) else f"<b>{v:.0f}%</b>  (n={int(n):,})")
                       for v, n in zip(rv, rn)] for rv, rn in zip(heat.values, cnt.values)],
                texttemplate="%{text}", textfont=dict(color="#222", size=12), showscale=False,
                hovertemplate="%{x} · %{y}<br>Churn rate: %{z:.1f}%<extra></extra>"))
            fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
            show(style(fig, 280, legend=False))
    with r4[1]:
        with st.container(border=True):
            tile_head("Churn Rate, Tech Support", "within the same internet type")
            sub = df[df["internet_service"] != "No"]
            if sub.empty:
                st.info("No internet customers in the current filter.")
            else:
                x = (sub.groupby(["internet_service", "tech_support"])
                     .agg(customers=("customer_id", "nunique"), churned=("churn_flag", "sum")).reset_index())
                x["rate"] = (100 * x["churned"] / x["customers"]).round(1)
                fig = px.bar(x, x="internet_service", y="rate", color="tech_support", barmode="group", text="rate",
                             custom_data=["customers"], color_discrete_map={"Yes": TEAL, "No": DARK},
                             labels={"rate": "Churn rate (%)", "internet_service": ""})
                fig.update_traces(texttemplate="%{y:.0f}%", textposition="outside", cliponaxis=False,
                                  hovertemplate="n=%{customdata[0]:,}<br>%{y:.1f}%<extra></extra>")
                fig.update_yaxes(ticksuffix="%", range=[0, max(x["rate"].max() * 1.25, 10)])
                show(style(fig, 280))
    with r4[2]:
        with st.container(border=True):
            tile_head("Monthly Charges", "distribution by churn status")
            fig = px.histogram(df, x="monthly_charges", color="churn", barmode="overlay", nbins=36, opacity=.75,
                               color_discrete_map={"Yes": DARK, "No": TEAL}, labels={"monthly_charges": "Monthly charges ($)"})
            fig.update_layout(yaxis_title="Customers")
            show(style(fig, 280))

    # ---- row 5: priority table
    with st.container(border=True):
        tile_head("Segments to Investigate First", "rate + volume · segments ≥ 300 customers · overlapping, do not add rows")
        rows = []
        for d in LABELS:
            s = segment_table(df, d, n_churn).rename(columns={d: "segment_value"})
            s.insert(0, "dimension", LABELS[d])
            s["segment_value"] = s["segment_value"].astype(str)
            rows.append(s)
        pri = pd.concat(rows, ignore_index=True)
        pri["lift_vs_overall"] = (pri["churn_rate_pct"] / rate).round(2)
        pri = pri[pri["customers"] >= 300].sort_values(["churn_rate_pct", "customers"], ascending=[False, False]).head(8)
        st.dataframe(
            pri.rename(columns={"dimension": "Attribute", "segment_value": "Segment", "customers": "Customers",
                                "churned_customers": "Churned", "churn_rate_pct": "Churn rate %",
                                "share_of_churned_pct": "Share of churned %", "lift_vs_overall": "Lift vs overall"}),
            hide_index=True, width="stretch",
            column_config={"Churn rate %": st.column_config.ProgressColumn("Churn rate %", min_value=0, max_value=100, format="%.1f%%")})
    st.markdown('<div class="footnote">Source: Telco Customer Churn sample snapshot. Associations only; no causal claims. '
                'Monthly charges of churned customers are a descriptive total, not recoverable revenue.</div>',
                unsafe_allow_html=True)

# ================================================================== EXPLORER
with tab_explore:
    with st.container(border=True):
        dims = list(LABELS)
        dim = st.selectbox("Attribute", dims, format_func=LABELS.get, index=dims.index("payment_method"))
        t = segment_table(df, dim, n_churn)
        tile_head(f"Churn Rate by {LABELS[dim]}", "rate with segment size")
        show(rate_bar(t, dim, rate, max(260, 60 * len(t) + 90)))
        small = t[t["customers"] < MIN_RELIABLE_N]
        if not small.empty:
            st.warning(f"Segments with fewer than {MIN_RELIABLE_N} customers have unstable rates: "
                       + ", ".join(map(str, small[dim])))
        st.dataframe(t.sort_values("churn_rate_pct", ascending=False).rename(columns={dim: LABELS[dim]}),
                     hide_index=True, width="stretch")

    with st.container(border=True):
        tile_head("Add-on Services", "churn rate within the same internet type")
        sub = df[df["internet_service"] != "No"]
        if sub.empty:
            st.info("No internet customers in the current filter.")
        else:
            addon = st.selectbox("Add-on", ["tech_support", "online_security", "online_backup", "device_protection"],
                                 format_func=LABELS.get)
            x = (sub.groupby(["internet_service", addon])
                 .agg(customers=("customer_id", "nunique"), churned_customers=("churn_flag", "sum")).reset_index())
            x["churn_rate_pct"] = (100 * x["churned_customers"] / x["customers"]).round(2)
            fig = px.bar(x, x="internet_service", y="churn_rate_pct", color=addon, barmode="group", text="churn_rate_pct",
                         custom_data=["customers"], color_discrete_map={"Yes": TEAL, "No": DARK},
                         labels={"churn_rate_pct": "Churn rate (%)", "internet_service": ""})
            fig.update_traces(texttemplate="%{y:.1f}%", hovertemplate="n=%{customdata[0]:,}<br>%{y:.2f}%<extra></extra>")
            show(style(fig, 300))
            st.dataframe(x, hide_index=True, width="stretch")
            st.caption("Customers who chose an add-on may differ in other ways: association, not proof the add-on lowers churn.")

    with st.container(border=True):
        tile_head("Billing & Tenure by Churn Status", "descriptive")
        g = (df.groupby("churn").agg(customers=("customer_id", "nunique"), avg_tenure=("tenure", "mean"),
                                     median_tenure=("tenure", "median"), avg_monthly=("monthly_charges", "mean"),
                                     median_monthly=("monthly_charges", "median"), sum_monthly=("monthly_charges", "sum"))
             .round(2).reset_index())
        st.dataframe(g, hide_index=True, width="stretch")
        fig = px.histogram(df, x="tenure", color="churn", barmode="overlay", nbins=36, opacity=.75,
                           color_discrete_map={"Yes": DARK, "No": TEAL}, labels={"tenure": "Tenure (months)"})
        show(style(fig, 260))

# ================================================================== PRIORITY
with tab_prio:
    with st.container(border=True):
        tile_head("Priority Segments", "rank by observed churn rate after a minimum-size cut")
        min_size = st.slider("Minimum segment size (customers)", 50, 2000, 300, step=50)
        rows = []
        for d in LABELS:
            s = segment_table(df, d, n_churn).rename(columns={d: "segment_value"})
            s.insert(0, "dimension", LABELS[d])
            s["segment_value"] = s["segment_value"].astype(str)
            rows.append(s)
        allseg2 = pd.concat(rows, ignore_index=True)
        allseg2["lift_vs_filtered_overall"] = (allseg2["churn_rate_pct"] / rate).round(2)
        sel = allseg2[allseg2["customers"] >= min_size]
        st.dataframe(sel.sort_values(["churn_rate_pct", "customers"], ascending=[False, False]).head(15),
                     hide_index=True, width="stretch")
        fig = px.scatter(sel, x="customers", y="churn_rate_pct", size="churned_customers", color="dimension",
                         hover_name="segment_value", size_max=40, color_discrete_sequence=PALETTE,
                         labels={"customers": "Segment size (customers)", "churn_rate_pct": "Churn rate (%)"})
        fig.add_hline(y=rate, line_dash="dash", line_color=DARK, line_width=1)
        show(style(fig, 380))
        st.caption("Segments overlap: do not add shares across rows. The ranking is descriptive, not a causal risk score.")

# ================================================================== METHOD
with tab_method:
    with st.container(border=True):
        st.markdown(
            f"""
**Data.** Telco Customer Churn sample snapshot: {len(full):,} customers, one row per customer. Cleaned by
`notebooks/01_data_audit_and_eda.ipynb`; the raw CSV is never modified.

**Cleaning.** No duplicate IDs and no invalid churn labels. 11 customers have blank `TotalCharges`; all have tenure = 0
(new, not yet billed). They were kept and not imputed. `TotalCharges` is not used in any KPI.

**KPIs.** Observed churn rate = churned / customers in scope × 100. Segment rate uses the segment's own customer count.
The overall rate is recomputed from counts, never averaged from segment percentages. Monthly charges of churned
customers are descriptive only.

**Limitations.** Cross-sectional snapshot (no dates): no cohort retention, forecasting or causal claims. Contract, tenure
and price are interrelated, so single-attribute rates overlap. Fictional telecom sample. Validate any retention action
with a controlled experiment.
""")
    with st.expander("Preview cleaned data"):
        st.dataframe(full.head(50), width="stretch")
