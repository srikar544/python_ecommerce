"""
MODELS.PY
=========
This file defines all database models (tables) used in the application.

Design goals:
- Prevent duplicate carts
- One active cart per user
- One product per cart (quantity-based)
- Clean cascading deletes
- Scalable (Amazon / Flipkart style)

Technology:
- Flask-SQLAlchemy ORM
- MySQL backend
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# --------------------------------------------------
# USER MODEL
# --------------------------------------------------
# Represents a registered user
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    # One account per email
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Hashed password
    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(150))

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    # One-to-One → User ↔ Cart
    cart = db.relationship(
        "Cart",
        uselist=False,
        backref="user"
    )

    def __repr__(self):
        return f"<User {self.email}>"


# --------------------------------------------------
# CATEGORY MODEL
# --------------------------------------------------
# Product categories (Electronics, Books, etc.)
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # No duplicate category names
    name = db.Column(db.String(100), unique=True, nullable=False)

    # One category → many products
    products = db.relationship(
        "Product",
        backref="category"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# --------------------------------------------------
# PRODUCT MODEL
# --------------------------------------------------
# Products available for purchase
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    price = db.Column(db.Float, nullable=False)

    stock = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    # Same product name allowed in different categories
    __table_args__ = (
        db.UniqueConstraint(
            "name",
            "category_id",
            name="uq_product_name_category"
        ),
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# --------------------------------------------------
# CART MODEL
# --------------------------------------------------
# One active cart per user
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

    # Cart → many cart items
    items = db.relationship(
        "CartItem",
        backref="cart",
        cascade="all, delete-orphan"
    )

    def total_items(self):
        return sum(item.quantity for item in self.items)

    def __repr__(self):
        return f"<Cart {self.id} for User {self.user_id}>"


# --------------------------------------------------
# CART ITEM MODEL
# --------------------------------------------------
# One product per cart (quantity-based)
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

    # Access product details directly
    product = db.relationship("Product")

    # Prevent duplicate products in same cart
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
