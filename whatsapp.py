
# whatsapp_mock.py

def generate_whatsapp_message(order, action):
    name = str(order.get("customer_name", "Customer")).strip()
    order_id = order.get("order_id", "N/A")
    amount = order.get("order_value", "N/A")

    if not name or name.lower() in {"nan", "none", "unknown"}:
        name = "Customer"

    if action == "WHATSAPP_CONFIRMATION":
        message = (
            f"Hi {name}, your order #{order_id} "
            f"worth Rs. {amount} is ready for processing. "
            "Please confirm your delivery address and that "
            "you will be available to receive the order. "
            "Reply YES to confirm or HELP if you need assistance."
        )

    elif action == "PREPAID_NUDGE":
        message = (
            f"Hi {name}, your order #{order_id} "
            f"worth Rs. {amount} is currently Cash on Delivery. "
            "If you prefer, you can choose prepaid payment "
            "through our official checkout. "
            "Your order remains subject to the normal order policy."
        )

    elif action == "HOLD_MANUAL_REVIEW":
        message = (
            f"Hi {name}, we need to verify a few details "
            f"for order #{order_id} before processing it. "
            "Our support team will assist you shortly."
        )

    else:
        message = (
            f"Hi {name}, your order #{order_id} "
            "is being processed. Thank you for shopping with us!"
        )

    return message


# Test the mock
if __name__ == "__main__":
    sample_order = {
        "customer_name": "Rahul",
        "order_id": "ORD101",
        "order_value": 1499,
    }

    for action in [
        "WHATSAPP_CONFIRMATION",
        "PREPAID_NUDGE",
        "HOLD_MANUAL_REVIEW",
        "SHIP_AS_IS",
    ]:
        print(f"\nAction: {action}")
        print(generate_whatsapp_message(sample_order, action))
