# Flask utilities for routing, flashing messages, redirects and templates
from flask import Blueprint, flash, redirect, render_template, url_for

# Flask-Login utilities
# current_user → gives the logged-in user object
# login_required → protects routes so only logged-in users can access them
from flask_login import current_user, login_required

# Import database models
from .models import Cart, CartItem, Product

# SQLAlchemy database instance
from . import db


# ==================================================
# CART BLUEPRINT
# ==================================================
# Blueprint allows cart-related routes to be grouped
# under a single module (clean architecture)
cart_bp = Blueprint("cart", __name__)


# ==================================================
# VIEW CART
# ==================================================
@cart_bp.route("/cart")
@login_required
def view_cart():
    """
    Displays the current logged-in user's cart.
    This route is protected — user must be logged in.
    """

    # current_user comes from Flask-Login
    # Access cart using relationship: User → Cart
    cart = current_user.cart

    # If the user does not have a cart yet
    if not cart:
        flash("Your cart is empty", "info")

        # Send empty list so template doesn't break
        return render_template("cart.html", items=[])

    # Pass all cart items to the template
    return render_template("cart.html", items=cart.items)


# ==================================================
# ADD PRODUCT TO CART
# ==================================================
@cart_bp.route("/add-to-cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    """
    Adds a product to the logged-in user's cart.
    - Creates a cart if it doesn't exist
    - Increases quantity if product already exists
    """

    # Fetch product by ID
    # If product doesn't exist → 404 error automatically
    product = Product.query.get_or_404(product_id)

    # Check if user already has a cart
    if not current_user.cart:
        # Create a new cart for this user
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()  # commit required to get cart.id
    else:
        cart = current_user.cart

    # Check if this product is already present in the cart
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()

    if cart_item:
        # If product already exists → increase quantity
        cart_item.quantity += 1
    else:
        # If product is new → create CartItem entry
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(cart_item)

    # Save changes to database
    db.session.commit()

    flash(f"{product.name} added to cart", "success")

    # Redirect back to home page
    return redirect(url_for("views.home"))


# ==================================================
# REMOVE ITEM FROM CART
# ==================================================
@cart_bp.route("/remove-from-cart/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    """
    Removes a specific item from the user's cart.
    """

    # Fetch cart item or return 404 if invalid ID
    cart_item = CartItem.query.get_or_404(item_id)

    # SECURITY CHECK:
    # Ensure the cart item belongs to the logged-in user
    # Prevents deleting other users' cart items
    if cart_item.cart.user_id != current_user.id:
        flash("Unauthorized action", "error")
        return redirect(url_for("cart.view_cart"))

    # Delete the cart item
    db.session.delete(cart_item)
    db.session.commit()

    flash("Item removed from cart", "info")

    # Redirect back to cart page
    return redirect(url_for("cart.view_cart"))
