from datetime import datetime
from typing import Optional
from website.models import Payment, User
from website import db

class PaymentService:
    """Simulates payment processing for testing without Razorpay."""

    @staticmethod
    def process_payment(user: User, amount: float) -> Payment:
        """
        Simulate a payment for a user.
        Creates a Payment record in the database.

        Args:
            user (User): The user making the payment
            amount (float): Amount to "charge"

        Returns:
            Payment: The created payment record
        """
        # Create a payment record
        payment = Payment(
            user_id=user.id,
            amount=amount,
            status="SUCCESS",  # Always succeed for testing
            created_at=datetime.utcnow()
        )
        db.session.add(payment)
        db.session.commit()

        print(f"[PaymentService] Payment of ₹{amount:.2f} recorded for {user.email}")
        return payment

    @staticmethod
    def create_order(amount: float, currency: str = "INR", receipt: Optional[str] = None) -> dict:
        """
        Simulate creating a Razorpay-style order (dummy for testing).
        Returns a dictionary with order info.
        """
        order = {
            "id": receipt or f"receipt_{datetime.utcnow().timestamp()}",
            "amount": amount,
            "currency": currency,
            "status": "created"
        }
        print(f"[PaymentService] Created test order: {order}")
        return order

    @staticmethod
    def verify_payment(payment_id: str, order_id: str, signature: str) -> bool:
        """
        Simulate payment verification (always True for testing).
        """
        print(f"[PaymentService] Verified payment {payment_id} for order {order_id}")
        return True
