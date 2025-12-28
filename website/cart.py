# Flask utilities
from sqlalchemy.orm import joinedload
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .models import Cart, CartItem, OrderItem, Product
from . import db

cart_bp = Blueprint("cart", __name__)


# ==================================================
# VIEW CART
# ==================================================
@cart_bp.route("/cart")
@login_required
def view_cart():
    items = (
        CartItem.query
        .options(joinedload(CartItem.product))
        .join(Cart)
        .filter(Cart.user_id == current_user.id)
        .all()
    )

    if not items:
        flash("Your cart is empty", "info")
        return render_template("cart.html", items=[], total=0)

    total = sum(item.product.price * item.quantity for item in items)

    return render_template("cart.html", items=items, total=total)


# ==================================================
# ADD PRODUCT TO CART
# ==================================================
@cart_bp.route("/add-to-cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    """Add a product to cart."""

    product = Product.query.get_or_404(product_id)

    # Stock validation
    if product.stock < 1:
        flash("Product is out of stock", "error")
        return redirect(url_for("views.home"))

    # Ensure user has a cart
    cart = current_user.cart
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.flush()  # get cart.id

    # Check if product already exists
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id, product_id=product.id
    ).first()

    if cart_item:
        if cart_item.quantity >= product.stock:
            flash("No more stock available", "warning")
        else:
            cart_item.quantity += 1
            flash(f"{product.name} quantity updated in cart", "success")
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)
        flash(f"{product.name} added to cart", "success")

    db.session.commit()
    return redirect(url_for("cart.view_cart"))  # redirect clears flash properly


# ==================================================
# REMOVE ITEM FROM CART
# ==================================================
@cart_bp.route("/remove-from-cart/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    cart_item = (
        CartItem.query
        .options(joinedload(CartItem.product))
        .get_or_404(item_id)
    )

    if cart_item.cart.user_id != current_user.id:
        flash("Unauthorized action", "error")
        return redirect(url_for("cart.view_cart"))

    product_name = cart_item.product.name  # SAFE now

    db.session.delete(cart_item)
    db.session.commit()

    flash(f"{product_name} removed from cart", "info")
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart/increase/<int:item_id>", methods=["POST"])
@login_required
def increase_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.quantity < item.product.stock:
        item.quantity += 1
        db.session.commit()
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart/decrease/<int:item_id>", methods=["POST"])
@login_required
def decrease_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash("Your cart is empty", "info")
        return redirect(url_for("views.home"))

    if request.method == "POST":
        # Calculate total
        total = sum(item.quantity * item.product.price for item in cart.items)

        # Create new order
        order = Order(user_id=current_user.id, total_amount=total)
        db.session.add(order)
        db.session.flush()  # Get order.id

        # Move cart items to order items
        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            db.session.delete(item)  # Remove from cart

        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for("views.home"))

    # GET request: show cart summary
    return render_template("checkout.html", items=cart.items)
  
    from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Order

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders")
@login_required
def order_history():
    # Fetch all orders for current user, newest first
    orders = Order.query.filter_by(user_id=current_user.id)\
                        .order_by(Order.created_at.desc()).all()
    return render_template("orders.html", orders=orders)



