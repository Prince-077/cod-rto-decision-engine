
# config.py

THRESHOLDS = {
    "high_rto_rate": 0.40,       # 40% ya usse zyada
    "medium_rto_rate": 0.25,     # 25% ya usse zyada
    "min_pincode_orders": 20,
    "min_prior_rto_for_hold": 2,
}

# Business assumptions — baad mein actual data se calibrate karna
BUSINESS = {
    "whatsapp_confirmation_cost": 2,
    "prepaid_nudge_cost": 1,
    "rto_handling_cost": 80,
}
