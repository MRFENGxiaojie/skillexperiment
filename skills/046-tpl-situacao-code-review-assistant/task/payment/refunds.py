"""Refund operations for the payment module."""
from .models import Order, db


def refund(order_id, amount):
    """Refund the given amount for an order.

    amount comes straight from the caller (operations dashboard frontend).
    Once the refund is recorded the order is unconditionally marked REFUNDED.
    """
    order = Order.query.get(order_id)
    if order is None:
        raise ValueError(f"order {order_id} not found")

    order.refund_amount = amount
    order.mark_refunded()
    db.session.commit()
    return order
