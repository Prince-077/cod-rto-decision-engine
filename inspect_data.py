import pandas as pd

df = pd.read_csv("orders_sample.csv")
#print("data:", df)

#print(df.columns)

#print(df.isnull().sum())

#print(df["final_status"].value_counts(dropna=False))

# df['final_status'] = (
#     df["final_status"].astype("string").str.strip().str.upper()
# )

#print(df["final_status"].value_counts(dropna=False))

# print(df["order_id"].duplicated().sum())
final_statusss = ["DELIVERED" , "RTO"]
df_final = df[df["final_status"].isin(final_statusss)].copy()

# print("ds",len(df)-len(df_final))

rto_count=(df_final["final_status"]=="RTO").sum()

delivered=(df_final["final_status"]=="DELIVERED").sum()

# total_final = len(df_final)
# print("final",df_final)
# print("deli",delivered)

# print("rto",rto_count)
# print("RTO Rate:", round(rto_count / total_final * 100, 2), "%")


# Step 2.2: First-time vs Repeat Customers

# Customer history ke basis par group banao
df_final["customer_type"] = df_final["customer_prior_orders"].apply(
    lambda x: "First-time" if x == 0
    else "Repeat" if pd.notna(x) and x > 0
    else "Unknown"
)

# Har customer type ka outcome analyse karo
customer_analysis = df_final.groupby("customer_type").agg(
    total_orders=("order_id", "count"),
    delivered=("final_status", lambda x: (x == "DELIVERED").sum()),
    rto=("final_status", lambda x: (x == "RTO").sum())
)

# RTO percentage calculate karo
customer_analysis["rto_rate_%"] = (
    customer_analysis["rto"] /
    (customer_analysis["delivered"] + customer_analysis["rto"]) * 100
).round(2)

print("\nFirst-time vs Repeat Customer Analysis:")
print(customer_analysis)



# Step 2.3: Previous RTO History Analysis

# Customers ko previous RTO history ke basis par group karo
df_final["prior_rto_group"] = df_final["customer_prior_rto"].apply(
    lambda x: "No previous RTO" if x == 0
    else "One previous RTO" if x == 1
    else "Multiple previous RTOs" if x > 1
    else "Unknown"
)

# Har group ka analysis
rto_history_analysis = df_final.groupby("prior_rto_group").agg(
    total_orders=("order_id", "count"),
    delivered=("final_status", lambda x: (x == "DELIVERED").sum()),
    rto=("final_status", lambda x: (x == "RTO").sum())
)

# RTO rate percentage
rto_history_analysis["rto_rate_%"] = (
    rto_history_analysis["rto"] /
    rto_history_analysis["total_orders"] * 100
).round(2)

print("\nPrevious RTO History Analysis:")
print(rto_history_analysis)


# Step 2.4: Courier-wise RTO Analysis

courier_analysis = df_final.groupby("courier").agg(
    total_orders=("order_id", "count"),
    delivered=("final_status", lambda x: (x == "DELIVERED").sum()),
    rto=("final_status", lambda x: (x == "RTO").sum())
)

courier_analysis["rto_rate_%"] = (
    courier_analysis["rto"] /
    courier_analysis["total_orders"] * 100
).round(2)

courier_analysis = courier_analysis.sort_values(
    "rto_rate_%", ascending=False
)

print("\nCourier-wise RTO Analysis:")
print(courier_analysis)


# Step 2.5: Pincode-wise RTO Analysis

# Pincode ko clean format mein convert karo
df_final["pincode_clean"] = (
    pd.to_numeric(df_final["pincode"], errors="coerce")
    .astype("Int64")
    .astype("string")
)

# Missing pincodes ko alag group mein rakho
df_final["pincode_clean"] = (
    df_final["pincode_clean"].fillna("UNKNOWN")
)

# Har pincode ka analysis
pincode_analysis = df_final.groupby("pincode_clean").agg(
    total_orders=("order_id", "count"),
    delivered=("final_status", lambda x: (x == "DELIVERED").sum()),
    rto=("final_status", lambda x: (x == "RTO").sum())
)

# RTO percentage calculate karo
pincode_analysis["rto_rate_%"] = (
    pincode_analysis["rto"] /
    pincode_analysis["total_orders"] * 100
).round(2)

# Sirf un pincodes ko dekho jahan minimum 20 orders hain
reliable_pincodes = pincode_analysis[
    pincode_analysis["total_orders"] >= 20
].sort_values("rto_rate_%", ascending=False)

print("\nTop 20 Pincodes by RTO Rate:")
print(reliable_pincodes.head(20))

print("\nTotal unique pincodes:", df_final["pincode_clean"].nunique())



# Step 2.6: Address Quality Analysis

# Missing values check
print("\nMissing values in important columns:")
print(
    df[["customer_name", "shipping_address", "pincode"]]
    .isnull()
    .sum()
)

# Empty ya whitespace-only values check
for col in ["customer_name", "shipping_address"]:
    df[col] = df[col].astype("string").str.strip()
    df[col] = df[col].replace("", pd.NA)

# Suspicious names: simple rule-based check
suspicious_names = ["asdf", "test", "unknown", "abc", "xyz"]

df["suspicious_name"] = (
    df["customer_name"]
    .str.lower()
    .isin(suspicious_names)
)

# Address missing ya bahut chhota hai?
df["address_incomplete"] = (
    df["shipping_address"].isna()
    | (df["shipping_address"].str.len() < 10)
)

# Summary
print("\nSuspicious names:", df["suspicious_name"].sum())
print("Missing/short addresses:", df["address_incomplete"].sum())

# In records ko inspect karo
print("\nSuspicious name examples:")
print(
    df.loc[df["suspicious_name"],
           ["order_id", "customer_name", "final_status"]].head(10)
)

print("\nIncomplete address examples:")
print(
    df.loc[df["address_incomplete"],
           ["order_id", "shipping_address", "final_status"]].head(10)
)


# Step 2.7: Final Data Analysis Summary

# Final outcome wale orders hi use karo
df_final = df[
    df["final_status"].isin(["DELIVERED", "RTO"])
].copy()

# Overall RTO rate
total_orders = len(df_final)
total_rto = (df_final["final_status"] == "RTO").sum()

print("\n--- DATA ANALYSIS SUMMARY ---")
print("Total final orders:", total_orders)
print("Total RTO:", total_rto)
print(
    "Overall RTO rate:",
    round(total_rto / total_orders * 100, 2), "%"
)

# Customer history
for col in ["customer_prior_orders", "customer_prior_rto"]:
    if col in df_final.columns:
        print(f"\n{col} distribution:")
        print(df_final[col].value_counts(dropna=False).head(10))

# Courier performance
if "courier" in df_final.columns:
    print("\nCourier order counts:")
    print(df_final["courier"].value_counts(dropna=False))

# Missing data in potentially useful features
features = [
    "customer_prior_orders",
    "customer_prior_rto",
    "pincode",
    "courier",
    "shipping_address",
    "customer_name"
]

available_features = [
    col for col in features if col in df_final.columns
]

print("\nMissing values in selected features:")
print(df_final[available_features].isna().sum())
