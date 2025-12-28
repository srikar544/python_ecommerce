"""
MODELS.PY
=========
This file defines all database models (tables) used in the application.

Design goals:
- Prevent duplicate carts
- One active cart per user
- Easy checkout (Cart → Order later)
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
# Represents a registered user of the application
# SQLAlchemy automatically provides a constructor:
# User(email=..., password=...)
class User(db.Model, UserMixin):

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User email (must be unique)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Hashed password (never store plain text passwords)
    password = db.Column(db.String(255), nullable=False)

    # Optional first name
    first_name = db.Column(db.String(150))

    # Timestamp when user was created
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    # One-to-One relationship with Cart
    # uselist=False → ensures ONLY ONE active cart per user
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
# Represents product categories (Electronics, Books, etc.)
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Category name must be unique
    name = db.Column(db.String(100), unique=True, nullable=False)

    # One category can have many products
    products = db.relationship(
        "Product",
        backref="category"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# --------------------------------------------------
# PRODUCT MODEL
# --------------------------------------------------
# Represents a product that can be purchased
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Product name
    name = db.Column(db.String(200), nullable=False)

    # Product price
    price = db.Column(db.Float, nullable=False)

    # Stock count (used later for validation)
    stock = db.Column(db.Integer, nullable=False)

    # Optional description
    description = db.Column(db.Text)

    # Foreign key → Category table
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id")
    )

    # Creation timestamp
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    def __repr__(self):
        return f"<Product {self.name}>"


# --------------------------------------------------
# CART MODEL
# --------------------------------------------------
# Represents ONE active shopping cart for a user
class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Foreign key → User table
    # One cart belongs to one user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    # Cart creation time
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    # One cart can have MANY cart items
    # cascade ensures:
    # - deleting cart deletes all cart items
    items = db.relationship(
        "CartItem",
        backref="cart",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cart {self.id} for User {self.user_id}>"


# --------------------------------------------------
# CART ITEM MODEL
# --------------------------------------------------
# Represents a single product inside a cart
class CartItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Foreign key → Cart
    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("cart.id"),
        nullable=False
    )

    # Foreign key → Product
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    # Quantity of product in cart
    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    # Relationship to access product details
    product = db.relationship("Product")

    def __repr__(self):
        return (
            f"<CartItem {self.id} | "
            f"Product {self.product_id} x {self.quantity}>"
        )
