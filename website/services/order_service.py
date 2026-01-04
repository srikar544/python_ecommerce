from website.models import Cart, CartItem, Order, OrderItem, Product, User
from website import db
from typing import Optional


class OrderService:
    """Handles all order-related operations: calculating totals, checkout, and order creation."""

    @staticmethod
    def calculate_cart_total(cart: Cart) -> float:
        """
        Calculate the total price for a cart.
        
        Args:
            cart (Cart): The user's cart
        
        Returns:
            float: Total amount
        """
        return sum(item.product.price * item.quantity for item in cart.items)

    @staticmethod
    def validate_cart_stock(cart: Cart) -> bool:
        """
        Ensure all items in the cart have enough stock.
        
        Args:
            cart (Cart)
        
        Returns:
            bool: True if stock is sufficient, False otherwise
        
        Raises:
            Exception if any item has insufficient stock
        """
        for item in cart.items:
            if item.product.stock < item.quantity:
                raise Exception(f"Insufficient stock for {item.product.name}")
        return True

    @staticmethod
    def clear_cart(cart: Cart) -> None:
        """
        Delete all items from the cart.
        
        Args:
            cart (Cart)
        """
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

    @staticmethod
    def reduce_stock(cart: Cart) -> None:
        """
        Reduce stock of all products in the cart.
        
        Args:
            cart (Cart)
        """
        for item in cart.items:
            item.product.stock -= item.quantity
        db.session.commit()

    @staticmethod
    def create_order_from_cart(cart: Cart) -> Optional[Order]:
        """
        Create an Order and associated OrderItems from a cart.
        
        Args:
            cart (Cart)
        
        Returns:
            Order: The created order
        """
        if not cart.items:
            return None

        order = Order(user_id=cart.user_id, total_amount=OrderService.calculate_cart_total(cart))
        db.session.add(order)
        db.session.flush()  # assign order.id before creating items

        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)

        db.session.commit()
        return order

    @staticmethod
    def checkout_cart(cart: Cart) -> Order:
        """
        Complete checkout process:
        1. Validate stock
        2. Reduce stock
        3. Create Order + OrderItems
        4. Clear cart
        
        Args:
            cart (Cart)
        
        Returns:
            Order: The completed order
        """
        if not cart or not cart.items:
            raise Exception("Cart is empty")

        # Step 1: Validate stock
        OrderService.validate_cart_stock(cart)

        # Step 2: Reduce stock
        OrderService.reduce_stock(cart)

        # Step 3: Create order and items
        order = OrderService.create_order_from_cart(cart)

        # Step 4: Clear cart
        OrderService.clear_cart(cart)

        return order
