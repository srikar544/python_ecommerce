from flask import Blueprint, render_template, request
from .models import Product, Category

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # Query parameters
    category_id = request.args.get("category", type=int)
    sort = request.args.get("sort", default="name_asc")
    page = request.args.get("page", default=1, type=int)
    per_page = 6

    # Base query
    query = Product.query

    # Filter by category
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Sorting
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "name_desc":
        query = query.order_by(Product.name.desc())
    else:
        query = query.order_by(Product.name.asc())

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    
    total_pages = pagination.pages if pagination.total > 0 else 0

    # Categories
    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template(
        "home.html",
        products=pagination.items,
        categories=categories,
        pagination=pagination,
        selected_category=category_id,
        selected_sort=sort,
        page=page,
        total_pages=total_pages
    )
