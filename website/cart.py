# ==================================================
# IMPORTS
# ==================================================

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from website.services.payment_service import PaymentService
from .models import Cart, CartItem, Order, OrderItem, Product
from . import db
from website.services.order_service import OrderService

# ==================================================
# BLUEPRINTS
# ==================================================
cart_bp = Blueprint("cart", __name__)
orders_bp = Blueprint("orders", __name__)

# ==================================================
# HELPER FUNCTIONS
# ==================================================
def get_user_cart():
    """Fetch or create a cart for the current user."""
    cart = current_user.cart
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.flush()
    return cart

def get_cart_items(cart: Cart):
    """Return cart items with product details."""
    return (
        CartItem.query
        .options(joinedload(CartItem.product))
        .filter_by(cart_id=cart.id)
        .all()
    )

# ==================================================
# VIEW CART
# ==================================================
@cart_bp.route("/cart")
@login_required
def view_cart():
    cart = get_user_cart()
    items = get_cart_items(cart)

    if not items:
        flash("Your cart is empty", "info")
        return render_template("cart.html", items=[], total=0)

    total = OrderService.calculate_cart_total(cart)
    return render_template("cart.html", items=items, total=total)

# ==================================================
# ADD PRODUCT TO CART
# ==================================================
@cart_bp.route("/add-to-cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id: int):
    product = Product.query.get_or_404(product_id)

    if product.stock < 1:
        flash("Product is out of stock", "error")
        return redirect(url_for("views.home"))

    cart = get_user_cart()

    # Check if product already exists in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
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
    return redirect(url_for("cart.view_cart"))

# ==================================================
# REMOVE PRODUCT FROM CART
# ==================================================
@cart_bp.route("/remove-from-cart/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id: int):
    cart_item = CartItem.query.options(joinedload(CartItem.product)).get_or_404(item_id)

    if cart_item.cart.user_id != current_user.id:
        flash("Unauthorized action", "error")
        return redirect(url_for("cart.view_cart"))

    product_name = cart_item.product.name
    db.session.delete(cart_item)
    db.session.commit()

    flash(f"{product_name} removed from cart", "info")
    return redirect(url_for("cart.view_cart"))

# ==================================================
# CHANGE CART ITEM QUANTITY
# ==================================================
def update_cart_item_quantity(item_id: int, increment: bool = True):
    """Increase or decrease quantity of a cart item."""
    item = CartItem.query.get_or_404(item_id)
    if increment:
        if item.quantity < item.product.stock:
            item.quantity += 1
    else:
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for("cart.view_cart"))

    db.session.commit()
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart/increase/<int:item_id>", methods=["POST"])
@login_required
def increase_quantity(item_id: int):
    return update_cart_item_quantity(item_id, increment=True)

@cart_bp.route("/cart/decrease/<int:item_id>", methods=["POST"])
@login_required
def decrease_quantity(item_id: int):
    return update_cart_item_quantity(item_id, increment=False)

# ==================================================
# CHECKOUT
# ==================================================
@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """
    Handles checkout process:
    - Displays cart items and grand total (GET)
    - Converts cart items into an order and simulates payment (POST)
    """

    # Load the current user's cart and its items with product details
    cart = Cart.query.options(
        joinedload(Cart.items).joinedload(CartItem.product)
    ).filter_by(user_id=current_user.id).first()

    # If cart is empty, redirect to home
    if not cart or not cart.items:
        flash("Your cart is empty", "info")
        return redirect(url_for("views.home"))

    # Calculate grand total
    grand_total = sum(item.quantity * item.product.price for item in cart.items)

    if request.method == "POST":
        # 1️⃣ Create the order
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.flush()  # assign order.id

        # 2️⃣ Move cart items to order items
        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price  # snapshot
            )
            db.session.add(order_item)

            # Reduce product stock
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
            else:
                flash(f"Insufficient stock for {item.product.name}", "error")
                return redirect(url_for("cart.view_cart"))

            # Remove item from cart
            db.session.delete(item)

        order.total_amount = grand_total
        db.session.commit()

        # 3️⃣ Process payment using PaymentService
        payment = PaymentService.process_payment(current_user, grand_total)

        # 4️⃣ Flash success message
        flash(f"Payment of ₹{payment.amount:.2f} successful! Your order has been placed.", "success")
        return redirect(url_for("orders.order_history"))

    # GET request: show checkout page
    return render_template("checkout.html", items=cart.items, grand_total=grand_total)

# ==================================================
# VIEW ORDER HISTORY
# ==================================================
@orders_bp.route("/orders")
@login_required
def order_history():
    orders = (
        Order.query
        .filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("orders.html", orders=orders)
