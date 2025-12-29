"""
MODELS.PY
=========
This file defines all database models (tables) used in the application.

DESIGN GOALS
------------
- One active cart per user
- Prevent duplicate carts
- One product per cart (quantity-based)
- Clean cascading deletes
- Scalable e-commerce design (Amazon / Flipkart style)

TECHNOLOGY
----------
- Flask-SQLAlchemy ORM
- MySQL backend
"""

from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# ==================================================
# USER MODEL
# ==================================================
# Represents a registered user of the application
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    # Each user must have a unique email
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Password is stored as a HASH, never plain text
    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(150))

    # Automatically stores account creation time
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    # One-to-One relationship
    # One user → one active cart
    cart = db.relationship(
        "Cart",
        uselist=False,
        backref="user"
    )

    def __repr__(self):
        return f"<User {self.email}>"


# ==================================================
# CATEGORY MODEL
# ==================================================
# Used to group products (Electronics, Books, Fashion, etc.)
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Category names must be unique
    name = db.Column(db.String(100), unique=True, nullable=False)

    # One category → many products
    products = db.relationship(
        "Product",
        backref="category"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# ==================================================
# PRODUCT MODEL
# ==================================================
# Represents a product that can be purchased
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    price = db.Column(db.Float, nullable=False)

    # Available stock quantity
    stock = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text)

    # Each product must belong to a category
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    # Prevent duplicate product names within the same category
    # Example:
    # "iPhone" allowed in Electronics
    # "iPhone" NOT allowed twice in Electronics
    __table_args__ = (
        db.UniqueConstraint(
            "name",
            "category_id",
            name="uq_product_name_category"
        ),
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# ==================================================
# CART MODEL
# ==================================================
# Represents the user's active shopping cart
class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Enforces ONE cart per user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    # One cart → many cart items
    # cascade ensures cart items are deleted if cart is deleted
    items = db.relationship(
        "CartItem",
        backref="cart",
        cascade="all, delete-orphan"
    )

    def total_items(self):
        """
        Returns total quantity of all items in cart.
        Used for cart badge (🛒 count).
        """
        return sum(item.quantity for item in self.items)

    def __repr__(self):
        return f"<Cart {self.id} for User {self.user_id}>"


# ==================================================
# CART ITEM MODEL
# ==================================================
# Represents a product inside a cart
# Quantity-based (no duplicate products per cart)
class CartItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("cart.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    # Relationship to access product details
    product = db.relationship("Product")

    # Prevent duplicate products in the same cart
    # Same product can appear only once per cart
    __table_args__ = (
        db.UniqueConstraint(
            "cart_id",
            "product_id",
            name="uq_cart_product"
        ),
    )

    def __repr__(self):
        return (
            f"<CartItem {self.id} | "
            f"Product {self.product_id} x {self.quantity}>"
        )


# ==================================================
# ORDER MODEL
# ==================================================
# Represents a completed purchase (checkout result)
class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Order belongs to a user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Total price of the order
    total_amount = db.Column(db.Float)

    # One order → many order items
    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True
    )

    def __repr__(self):
        return f"<Order {self.id} User {self.user_id}>"


# ==================================================
# ORDER ITEM MODEL
# ==================================================
# Represents a product inside an order
# Stores snapshot of price at purchase time
class OrderItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id")
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id")
    )

    quantity = db.Column(db.Integer)

    # Price is stored separately to preserve history
    # Even if product price changes later
    price = db.Column(db.Float)

    # Relationship to product for display
    product = db.relationship("Product")

    def __repr__(self):
        return (
            f"<OrderItem {self.id} | "
            f"Product {self.product_id} x {self.quantity}>"
        )
