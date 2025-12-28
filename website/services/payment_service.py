class PaymentService:
    """Handles payment processing."""

    @staticmethod
    def process_payment(user, amount, payment_method="dummy"):
        """
        Dummy payment processor.
        In a real app, integrate with Stripe, Razorpay, PayPal, etc.
        """
        print(f"Processing {payment_method} payment for {user.email}: ${amount}")
        return True  # Simulate success
