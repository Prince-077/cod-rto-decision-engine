
# main.py

import pandas as pd
from decision_engine import decide_order
from whatsapp import generate_whatsapp_message

df = pd.read_csv("orders_sample.csv")
df.columns = df.columns.str.strip()

df["final_status"] = (
    df["final_status"].astype("string").str.strip().str.upper()
)

df["pincode_clean"] = (
    df["pincode"].astype("string").str.strip().replace("", pd.NA)
)

# Use the pincode report created earlier
pincode_stats = pd.read_csv("pincode_risk_report.csv")
pincode_stats["pincode_clean"] = (
    pincode_stats["pincode_clean"]
    .astype("string")
    .str.strip()
)

rate_lookup = (
    pincode_stats.set_index("pincode_clean")["rto_rate"].to_dict()
)

results = []

for _, row in df.iterrows():
    rate = rate_lookup.get(row["pincode_clean"])

    if pd.isna(rate):
        rate = None

    result = decide_order(row, pincode_rto_rate=rate)

    message = generate_whatsapp_message(row, result["action"])

    results.append({
        "order_id": row.get("order_id"),
        "action": result["action"],
        "reason": result["reason"],
        "whatsapp_message": message,
    })

output = pd.DataFrame(results)
output.to_csv("order_decisions_with_messages.csv", index=False)

print(output.head(10).to_string(index=False))
print("\nSaved: order_decisions_with_messages.csv")
