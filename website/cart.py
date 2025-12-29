# ==================================================
# IMPORTS
# ==================================================

# SQLAlchemy utility for eager loading related objects
# Prevents multiple database queries (performance optimization)
from sqlalchemy.orm import joinedload

# Flask utilities
from flask import Blueprint, flash, redirect, render_template, request, url_for

# Flask-Login utilities
# current_user  → currently logged-in user object
# login_required → restricts access to authenticated users only
from flask_login import current_user, login_required

# Database models
from .models import Cart, CartItem, Order, OrderItem, Product

# SQLAlchemy database instance
from . import db


# ==================================================
# CART BLUEPRINT
# ==================================================
# All cart-related routes live here
cart_bp = Blueprint("cart", __name__)


# ==================================================
# VIEW CART
# ==================================================
@cart_bp.route("/cart")
@login_required
def view_cart():
    """
    Display all items in the logged-in user's cart.
    """

    # Fetch cart items belonging to the current user
    # joinedload loads product details in the same query
    items = (
        CartItem.query
        .options(joinedload(CartItem.product))
        .join(Cart)
        .filter(Cart.user_id == current_user.id)
        .all()
    )

    # If cart is empty
    if not items:
        flash("Your cart is empty", "info")
        return render_template("cart.html", items=[], total=0)

    # Calculate total cart price
    total = sum(item.product.price * item.quantity for item in items)

    return render_template("cart.html", items=items, total=total)


# ==================================================
# ADD PRODUCT TO CART
# ==================================================
@cart_bp.route("/add-to-cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    """
    Add a product to the user's cart.
    """

    # Fetch product or return 404 if it does not exist
    product = Product.query.get_or_404(product_id)

    # Check stock availability
    if product.stock < 1:
        flash("Product is out of stock", "error")
        return redirect(url_for("views.home"))

    # Get user's cart (one cart per user)
    cart = current_user.cart

    # Create cart if it doesn't exist
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)

        # flush() assigns cart.id without committing to DB
        db.session.flush()

    # Check if product already exists in cart
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()

    if cart_item:
        # Prevent adding more items than available stock
        if cart_item.quantity >= product.stock:
            flash("No more stock available", "warning")
        else:
            cart_item.quantity += 1
            flash(f"{product.name} quantity updated in cart", "success")
    else:
        # Add new product to cart
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(cart_item)
        flash(f"{product.name} added to cart", "success")

    # Save changes
    db.session.commit()

    return redirect(url_for("cart.view_cart"))


# ==================================================
# REMOVE ITEM FROM CART
# ==================================================
@cart_bp.route("/remove-from-cart/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    """
    Remove a product from the cart.
    """

    # Fetch cart item along with its product
    cart_item = (
        CartItem.query
        .options(joinedload(CartItem.product))
        .get_or_404(item_id)
    )

    # Security check: ensure cart belongs to current user
    if cart_item.cart.user_id != current_user.id:
        flash("Unauthorized action", "error")
        return redirect(url_for("cart.view_cart"))

    product_name = cart_item.product.name

    # Delete item from cart
    db.session.delete(cart_item)
    db.session.commit()

    flash(f"{product_name} removed from cart", "info")
    return redirect(url_for("cart.view_cart"))


# ==================================================
# INCREASE CART ITEM QUANTITY
# ==================================================
@cart_bp.route("/cart/increase/<int:item_id>", methods=["POST"])
@login_required
def increase_quantity(item_id):
    """
    Increase quantity of a cart item (up to stock limit).
    """

    item = CartItem.query.get_or_404(item_id)

    if item.quantity < item.product.stock:
        item.quantity += 1
        db.session.commit()

    return redirect(url_for("cart.view_cart"))


# ==================================================
# DECREASE CART ITEM QUANTITY
# ==================================================
@cart_bp.route("/cart/decrease/<int:item_id>", methods=["POST"])
@login_required
def decrease_quantity(item_id):
    """
    Decrease quantity of a cart item.
    Removes the item if quantity becomes zero.
    """

    item = CartItem.query.get_or_404(item_id)

    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        # Remove item completely if quantity reaches 0
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for("cart.view_cart"))


# ==================================================
# CHECKOUT
# ==================================================
from sqlalchemy.orm import joinedload
from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from .models import Cart, CartItem, Order, OrderItem
from . import db
from .cart import cart_bp

@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """
    Handles checkout process:
    - Displays cart items and grand total (GET)
    - Converts cart items into an order (POST)
    """

    # Load the current user's cart and its items with product details
    cart = Cart.query.options(
        joinedload(Cart.items).joinedload(CartItem.product)
    ).filter_by(user_id=current_user.id).first()

    # If cart is empty, redirect to home
    if not cart or not cart.items:
        flash("Your cart is empty", "info")
        return redirect(url_for("views.home"))

    if request.method == "POST":
        # Create order for the user
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.flush()  # Assign order.id before adding items

        total_amount = 0  # accumulator for order total

        # Move cart items into order items
        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price  # snapshot of price at purchase
            )
            db.session.add(order_item)

            # Add to total
            total_amount += item.quantity * item.product.price

            # Remove from cart
            db.session.delete(item)

        # Assign total_amount to the order
        order.total_amount = total_amount

        # Commit all changes
        db.session.commit()

        flash("Your order has been placed successfully!", "success")
        return redirect(url_for("orders.order_history"))

    # GET request: render checkout template
    grand_total = sum(item.quantity * item.product.price for item in cart.items)
    return render_template("checkout.html", items=cart.items, grand_total=grand_total)

# ==================================================
# ORDER HISTORY BLUEPRINT
# ==================================================
# Shows previous orders placed by the user
orders_bp = Blueprint("orders", __name__)


# ==================================================
# VIEW ORDER HISTORY
# ==================================================
@orders_bp.route("/orders")
@login_required
def order_history():
    """
    Display all past orders of the logged-in user.
    """

    # Fetch user's orders, newest first
    orders = (
        Order.query
        .filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return render_template("orders.html", orders=orders)
