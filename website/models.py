#Prevents duplicate carts
#Easy checkout → convert cart → order
#Easy stock validation
#Clean cascading deletes
#Used by Amazon / Flipkart-style systems

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    #uselist=False ensures one active cart per user.
    cart= db.relationship("Cart",uselist=False, backref="user")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship("Product", backref="category")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"<Product {self.name}>"

class Cart(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      #one cart belongs to one user
      user_id    = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
      created_at = db.Column(db.DateTime(timezone=True),default=func.now())

      #one cart many cart items
      items=db.relationship(
           "CartItem",
           backref="cart",
           cascade="all, delete-orphan"
      )

      def __repr__(self):
        return f"<Cart {self.id}> for User {self.user_id}"

      #---------
      # CartItem
      #---------
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship("Product")

    def __repr__(self):
     return f"<CartItem {self.id} | Product {self.product_id} * {self.quantity}>"        