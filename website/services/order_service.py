from app.models import Cart, CartItem, User, Product
from app import db

class OrderService:
    """Handles all order-related logic (checkout, totals, etc.)."""

    @staticmethod
    def calculate_cart_total(cart: Cart):
        """Calculate total price for a cart."""
        total = sum(item.product.price * item.quantity for item in cart.items)
        return total

    @staticmethod
    def checkout_cart(cart: Cart):
        """
        Convert cart items to an order (to be implemented).
        For now, this just clears the cart and reduces stock.
        """
        for item in cart.items:
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
            else:
                raise Exception(f"Insufficient stock for {product.name}")

        # Clear cart
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
