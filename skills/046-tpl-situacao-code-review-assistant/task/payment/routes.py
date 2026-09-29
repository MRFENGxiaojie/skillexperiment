"""Payment API routes."""
from flask import Blueprint, jsonify, request

from .refunds import refund

payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/api/payments/<int:payment_id>", methods=["DELETE"])
def cancel_payment(payment_id):
    """Cancel an unpaid payment.

    Intended for the operations dashboard. The caller provides the refund
    amount in the request body and the payment is refunded unconditionally.
    """
    body = request.get_json(silent=True) or {}
    order = refund(payment_id, body.get("amount", 0))
    return jsonify({"ok": True, "order_id": order.id}), 200
