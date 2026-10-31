
import pandas as pd
from decision_engine import decide_order

df = pd.read_csv("orders_sample.csv")
pincode_stats = pd.read_csv("pincode_risk_report.csv")

df["final_status"] = (
    df["final_status"].astype("string").str.strip().str.upper()
)

df["pincode_clean"] = (
    df["pincode"].astype("string").str.strip().replace("", pd.NA)
)

# Report se pincode -> RTO rate lookup
rate_lookup = pincode_stats.set_index("pincode_clean")["rto_rate"].to_dict()

# Sirf demonstration ke liye:
# Full-dataset rates use karna valid backtest nahi hai.
decisions = []

for _, row in df.iterrows():
    rate = rate_lookup.get(row["pincode_clean"])

    if pd.isna(rate):
        rate = None

    result = decide_order(row, pincode_rto_rate=rate)

    decisions.append({
        "order_id": row.get("order_id"),
        "action": result["action"],
        "reason": result["reason"],
    })

decision_df = pd.DataFrame(decisions)
decision_df.to_csv("order_decisions_demo.csv", index=False)

print("\nDecision counts:")
print(decision_df["action"].value_counts())

print("\nSaved: order_decisions_demo.csv")
