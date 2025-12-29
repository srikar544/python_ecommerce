# ==================================================
# IMPORTS
# ==================================================

# Blueprint → helps organize routes into modules
# render_template → renders HTML pages
# request → reads query parameters from URL (?category=1&page=2 etc.)
from flask import Blueprint, render_template, request

# Database models
from .models import Product, Category


# ==================================================
# VIEWS BLUEPRINT
# ==================================================
# This blueprint handles public-facing pages (home, product listing)
views = Blueprint("views", __name__)


# ==================================================
# HOME PAGE / PRODUCT LISTING
# ==================================================
@views.route("/")
def home():
    """
    Home page that displays products with:
    - Category filtering
    - Sorting
    - Pagination
    """

    # ----------------------------------------------
    # READ QUERY PARAMETERS FROM URL
    # ----------------------------------------------
    # Example URL:
    # /?category=2&sort=price_desc&page=3

    # Selected category ID (None if not provided)
    category_id = request.args.get("category", type=int)

    # Sorting option (default: name_asc)
    sort = request.args.get("sort", default="name_asc")

    # Current page number (default: page 1)
    page = request.args.get("page", default=1, type=int)

    # Number of products per page
    per_page = 6


    # ----------------------------------------------
    # BASE PRODUCT QUERY
    # ----------------------------------------------
    # Start with all products
    query = Product.query


    # ----------------------------------------------
    # FILTER BY CATEGORY (if selected)
    # ----------------------------------------------
    if category_id:
        query = query.filter_by(category_id=category_id)


    # ----------------------------------------------
    # SORTING LOGIC
    # ----------------------------------------------
    # User-selected sorting option
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())

    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())

    elif sort == "name_desc":
        query = query.order_by(Product.name.desc())

    else:
        # Default sorting: name ascending
        query = query.order_by(Product.name.asc())


    # ----------------------------------------------
    # PAGINATION
    # ----------------------------------------------
    # paginate() automatically limits results and calculates pages
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Total number of pages (safe fallback for empty results)
    total_pages = pagination.pages if pagination.total > 0 else 0


    # ----------------------------------------------
    # FETCH ALL CATEGORIES (for sidebar / filter menu)
    # ----------------------------------------------
    categories = Category.query.order_by(Category.name.asc()).all()


    # ----------------------------------------------
    # RENDER TEMPLATE
    # ----------------------------------------------
    return render_template(
        "home.html",

        # Products for current page
        products=pagination.items,

        # All categories (for filter UI)
        categories=categories,

        # Pagination object (has next, prev, pages, total)
        pagination=pagination,

        # Keep selected values for UI state
        selected_category=category_id,
        selected_sort=sort,
        page=page,
        total_pages=total_pages
    )
