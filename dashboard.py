
# dashboard.py

import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="COD RTO Decision Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 COD RTO Decision Dashboard")
st.caption("Founder View | Historical Backtest & Illustrative Impact")

file_path = Path("backtest_results.csv")

if not file_path.exists():
    st.error("backtest_results.csv nahi mili. Pehle python backtest.py run karo.")
    st.stop()

df = pd.read_csv(file_path)

required_columns = {
    "order_id", "order_datetime", "final_status", "action"
}

if not required_columns.issubset(df.columns):
    st.error("Backtest CSV mein required columns missing hain.")
    st.stop()

df["order_datetime"] = pd.to_datetime(
    df["order_datetime"], errors="coerce"
)
df["final_status"] = (
    df["final_status"].astype("string").str.strip().str.upper()
)

df = df[
    df["order_datetime"].notna()
    & df["final_status"].isin(["DELIVERED", "RTO"])
].copy()

if df.empty:
    st.warning("Valid completed test orders nahi mile.")
    st.stop()

# Sidebar: transparent business assumptions
st.sidebar.header("Business Assumptions")

rto_cost = st.sidebar.number_input(
    "Cost per RTO (₹)",
    min_value=0,
    value=80,
    step=10
)

message_cost = st.sidebar.number_input(
    "Cost per intervention (₹)",
    min_value=0,
    value=2,
    step=1
)

effectiveness = st.sidebar.slider(
    "Assumed RTO reduction for targeted orders (%)",
    min_value=0,
    max_value=100,
    value=20
) / 100

# Date-wise reporting
df["report_date"] = df["order_datetime"].dt.date
available_dates = sorted(df["report_date"].unique())

yesterday = pd.Timestamp.now().date() - pd.Timedelta(days=1)

if yesterday in available_dates:
    selected_date = yesterday
else:
    selected_date = available_dates[-1]
    st.info(
        f"Dataset mein yesterday ({yesterday}) ke orders nahi mile. "
        f"Latest available date {selected_date} dikhayi ja rahi hai."
    )

daily = df[df["report_date"] == selected_date]
total_orders = len(daily)
total_rto = (daily["final_status"] == "RTO").sum()
rto_rate = total_rto / total_orders * 100 if total_orders else 0

st.subheader(f"Daily Snapshot — {selected_date}")

col1, col2, col3 = st.columns(3)

col1.metric("Orders", total_orders)
col2.metric("RTO Orders", int(total_rto))
col3.metric("Actual RTO Rate", f"{rto_rate:.1f}%")

st.subheader("Decision Buckets")

bucket_counts = (
    daily["action"]
    .value_counts()
    .rename_axis("Action")
    .reset_index(name="Orders")
)

st.bar_chart(bucket_counts.set_index("Action"))

st.dataframe(bucket_counts, use_container_width=True, hide_index=True)

# Illustrative financial scenario on the full held-out test set
st.subheader("Illustrative Financial Impact — Test Period")

target_actions = [
    "WHATSAPP_CONFIRMATION",
    "PREPAID_NUDGE",
    "HOLD_MANUAL_REVIEW",
]

targeted = df[df["action"].isin(target_actions)]
targeted_rto = (targeted["final_status"] == "RTO").sum()

# Scenario assumption: intervention prevents a fraction of observed RTOs
estimated_avoided_rto = targeted_rto * effectiveness
gross_savings = estimated_avoided_rto * rto_cost
intervention_cost = len(targeted) * message_cost
net_impact = gross_savings - intervention_cost

col1, col2, col3, col4 = st.columns(4)

col1.metric("Estimated RTOs Avoided", f"{estimated_avoided_rto:.1f}")
col2.metric("Potential Savings", f"₹{gross_savings:,.0f}")
col3.metric("Intervention Cost", f"₹{intervention_cost:,.0f}")
col4.metric("Estimated Net Impact", f"₹{net_impact:,.0f}")

st.caption(
    "Scenario only, not measured savings. Assumes the selected reduction "
    "percentage applies to observed RTOs in targeted action buckets. "
    "Actual intervention effectiveness has not been established."
)

st.subheader("Test-Period Outcome by Action")

summary = (
    df.groupby("action")
    .agg(
        orders=("order_id", "size"),
        rto_orders=(
            "final_status",
            lambda s: (s == "RTO").sum()
        ),
    )
    .reset_index()
)

summary["rto_rate_%"] = (
    summary["rto_orders"] / summary["orders"] * 100
).round(2)

st.dataframe(summary, use_container_width=True, hide_index=True)

st.download_button(
    "Download Test Results CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="dashboard_test_results.csv",
    mime="text/csv"
)
