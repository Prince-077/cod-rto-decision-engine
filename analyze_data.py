
# analyze_data.py

import pandas as pd

# 1. Load dataset
df = pd.read_csv("orders_sample.csv")

# 2. Clean status
df["final_status"] = (
    df["final_status"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# 3. Keep only completed orders
df = df[df["final_status"].isin(["DELIVERED", "RTO"])].copy()

# 4. Clean pincode without converting it to a number
df["pincode_clean"] = (
    df["pincode"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

# 5. Calculate pincode-wise historical outcome summary
pincode_stats = (
    df.dropna(subset=["pincode_clean"])
    .groupby("pincode_clean")
    .agg(
        total_orders=("final_status", "size"),
        rto_orders=("final_status", lambda s: (s == "RTO").sum()),
    )
    .reset_index()
)

pincode_stats["rto_rate"] = (
    pincode_stats["rto_orders"] / pincode_stats["total_orders"]
)

# 6. Small samples ko reliable risk signal mat samjho
pincode_stats["risk_level"] = "INSUFFICIENT_DATA"

pincode_stats.loc[
    (pincode_stats["total_orders"] >= 20)
    & (pincode_stats["rto_rate"] < 0.25),
    "risk_level",
] = "LOW"

pincode_stats.loc[
    (pincode_stats["total_orders"] >= 20)
    & (pincode_stats["rto_rate"] >= 0.25)
    & (pincode_stats["rto_rate"] < 0.40),
    "risk_level",
] = "MEDIUM"

pincode_stats.loc[
    (pincode_stats["total_orders"] >= 20)
    & (pincode_stats["rto_rate"] >= 0.40),
    "risk_level",
] = "HIGH"

# 7. Show highest RTO-rate pincodes with sufficient data
report = pincode_stats[
    pincode_stats["total_orders"] >= 20
].sort_values("rto_rate", ascending=False)

print("\nTop 10 pincode risk signals:")
print(
    report.head(10).to_string(
        index=False,
        formatters={"rto_rate": "{:.1%}".format},
    )
)

# 8. Save the report
pincode_stats.to_csv("pincode_risk_report.csv", index=False)

print("\nSaved: pincode_risk_report.csv")
