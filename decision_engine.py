
# decision_engine.py

from config import THRESHOLDS


def decide_order(row, pincode_rto_rate=None):
    prior_rto = row.get("customer_prior_rto", 0)
    address = str(row.get("shipping_address", "")).strip()
    name = str(row.get("customer_name", "")).strip()

    # Missing historical data ko automatically safe mat samjho
    try:
        prior_rto = int(prior_rto) if prior_rto is not None else 0
    except (ValueError, TypeError):
        prior_rto = 0

    # 1. Address ya name mein issue ho toh confirmation
    suspicious_names = {"", "nan", "unknown", "test", "asdf", "abc", "xyz"}

    if (
        len(address) < 10
        or name.lower() in suspicious_names
    ):
        return {
            "action": "WHATSAPP_CONFIRMATION",
            "reason": "Address/name needs verification"
        }

    # 2. High historical customer risk + high pincode risk
    if (
        prior_rto >= THRESHOLDS["min_prior_rto_for_hold"]
        and pincode_rto_rate is not None
        and pincode_rto_rate >= THRESHOLDS["high_rto_rate"]
    ):
        return {
            "action": "HOLD_MANUAL_REVIEW",
            "reason": "Repeated previous RTO and high-risk pincode"
        }

    # 3. High-risk pincode
    if (
        pincode_rto_rate is not None
        and pincode_rto_rate >= THRESHOLDS["high_rto_rate"]
    ):
        return {
            "action": "WHATSAPP_CONFIRMATION",
            "reason": "High historical pincode RTO rate"
        }

    # 4. Previous RTO history
    if prior_rto >= 1:
        return {
            "action": "PREPAID_NUDGE",
            "reason": "Customer has previous RTO history"
        }

    # 5. Default decision
    return {
        "action": "SHIP_AS_IS",
        "reason": "No strong risk signal found"
    }
