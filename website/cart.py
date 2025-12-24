from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from website.models import Cart, CartItem, Product
from . import db


cart_bp=Blueprint("cart",__name__)

#Route to view current user's cart
@cart_bp.route("/cart")
@login_required()
def view_cart():
    cart=current_user.cart
    if not cart:
        flash("Your Cart is Empty","info")
        return render_template("cart.html",items[])
    
    return render_template("cart.html",items=cart.items)


#Route to add product to cart
@cart_bp.route("/add-to-cart/<int:product_id>",methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    #Create Cart if not exists
    if not current_user.cart:
        cart=Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    else:
        cart=current_user.cart

    # check if product already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id,product_id=product.id).first()
    if cart_item:
        cart_item.quantity+=1
    else:
        cart_item = CartItem(cart_id=cart.id,product_id=product.id,quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash(f"{product.name} added to cart.","success") 
    return redirect(url_for("views.home")) 

@cart_bp.route("/remove-from-cart/<int:item_id>",methods=["POST"])   
@login_required
def remove_from_cart(item_id):
      cart_item = CartItem.query.get_or_404(item_id)
      db.session.delete(cart_item)
      db.session.commit()
      flash("Item removed from cart.","info")
      return redirect(url_for("cart.view_cart"))     


    
