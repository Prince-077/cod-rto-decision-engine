
# backtest.py

import pandas as pd
from decision_engine import decide_order
from config import THRESHOLDS

# 1. Load and clean data
df = pd.read_csv("orders_sample.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Clean status
df["final_status"] = (
    df["final_status"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Convert order_datetime to datetime
df["order_datetime"] = pd.to_datetime(
    df["order_datetime"],
    errors="coerce"
)

# Keep only completed orders with valid dates
df = df[
    df["final_status"].isin(["DELIVERED", "RTO"])
    & df["order_datetime"].notna()
].copy()

# Clean pincode
df["pincode_clean"] = (
    df["pincode"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

# 2. Sort chronologically
df = df.sort_values("order_datetime").reset_index(drop=True)

# 3. Split: first 70% historical, remaining 30% test
split_index = int(len(df) * 0.70)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

print("Historical orders:", len(train))
print("Test orders:", len(test))
print("Test starts:", test["order_datetime"].min())

# 4. Calculate pincode RTO rates using historical data only
pincode_stats = (
    train.dropna(subset=["pincode_clean"])
    .groupby("pincode_clean")
    .agg(
        total_orders=("final_status", "size"),
        rto_orders=(
            "final_status",
            lambda s: (s == "RTO").sum()
        ),
    )
)

pincode_stats["rto_rate"] = (
    pincode_stats["rto_orders"]
    / pincode_stats["total_orders"]
)

# Ignore pincodes with insufficient historical orders
pincode_stats = pincode_stats[
    pincode_stats["total_orders"]
    >= THRESHOLDS["min_pincode_orders"]
]

rate_lookup = pincode_stats["rto_rate"].to_dict()

# 5. Apply decisions to test orders
results = []

for _, row in test.iterrows():

    rate = rate_lookup.get(row["pincode_clean"])

    result = decide_order(
        row,
        pincode_rto_rate=rate
    )

    results.append({
        "order_id": row.get("order_id"),
        "order_datetime": row["order_datetime"],
        "final_status": row["final_status"],
        "action": result["action"],
        "reason": result["reason"],
    })

# 6. Save order-level results
result_df = pd.DataFrame(results)

result_df.to_csv(
    "backtest_results.csv",
    index=False
)

# 7. Evaluate actual RTO rate for each action
summary = (
    result_df.groupby("action")
    .agg(
        orders=("order_id", "size"),
        actual_rto=(
            "final_status",
            lambda s: (s == "RTO").sum()
        ),
    )
)

summary["actual_rto_rate_%"] = (
    summary["actual_rto"]
    / summary["orders"]
    * 100
).round(2)

print("\nAction-wise test results:")
print(summary.to_string())

# 8. Overall test-period RTO rate
if len(result_df) > 0:
    overall_rto_rate = (
        (result_df["final_status"] == "RTO").mean() * 100
    )

    print(
        f"\nTest-period overall RTO rate: "
        f"{overall_rto_rate:.2f}%"
    )
else:
    print("\nNo test orders available. Check your data and dates.")

print("\nSaved: backtest_results.csv")
