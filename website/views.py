"""
VIEWS.PY
========
This file contains routes related to displaying pages
that do NOT require authentication.

Responsibilities:
- Load products from database
- Load categories
- Send data to templates (HTML)
"""

from flask import Blueprint, render_template
from .models import Product, Category


# --------------------------------------------------
# Blueprint for main site pages
# --------------------------------------------------
# Blueprint name = "views"
# __name__ helps Flask locate templates & static files
views = Blueprint("views", __name__)


# --------------------------------------------------
# HOME PAGE ROUTE
# --------------------------------------------------
@views.route("/")
def home():
    """
    Home page of the application.

    Flow:
    1. Fetch all products from database
    2. Fetch all categories from database
    3. Pass both to the HTML template
    4. Jinja renders the data dynamically
    """

    # Query all products from Product table
    # Equivalent SQL: SELECT * FROM product;
    products = Product.query.all()

    # Query all categories from Category table
    # Equivalent SQL: SELECT * FROM category;
    categories = Category.query.all()

    # Render home.html and pass data to it
    # products → accessible in template
    # categories → accessible in template
    return render_template(
        "home.html",
        products=products,
        categories=categories
    )
