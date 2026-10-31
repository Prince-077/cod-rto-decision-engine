
from decision_engine import decide_order

order = {
    "customer_name": "Rahul Kumar",
    "shipping_address": "House 12, Main Road, Patna",
    "customer_prior_rto": 0,
}

result = decide_order(order, pincode_rto_rate=0.10)

print("Action:", result["action"])
print("Reason:", result["reason"])
    