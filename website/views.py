from flask import Blueprint, render_template
from .models import Product, Category

views = Blueprint("views", __name__)


@views.route("/")
def home():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template(
        "home.html",
        products=products,
        categories=categories
    )
