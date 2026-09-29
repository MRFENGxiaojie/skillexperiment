"""Order model with payment status state machine."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ORDER_STATES = ("created", "pending", "paid", "refunded", "cancelled")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    total_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(16), nullable=False, default="created")
    refund_amount = db.Column(db.Integer, nullable=False, default=0)
    paid_at = db.Column(db.DateTime)

    def mark_paid(self):
        """Transition created/pending -> paid."""
        if self.status in ("paid", "refunded"):
            raise ValueError(f"cannot mark {self.status} order as paid")
        self.status = "paid"
        self.paid_at = db.func.now()

    def mark_refunded(self):
        """Transition any state -> refunded (no guard)."""
        self.status = "refunded"
