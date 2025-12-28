from app.models import Product, Category
from app import db

class ProductService:
    """Handles all product-related business logic."""

    @staticmethod
    def get_all_products():
        """Return all products from the database."""
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        """Return a single product by its ID."""
        return Product.query.get(product_id)

    @staticmethod
    def create_product(name, price, stock, category_id, description=None):
        """Create and save a new product."""
        product = Product(
            name=name,
            price=price,
            stock=stock,
            category_id=category_id,
            description=description
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_products_by_category(category_id):
        """Return all products under a specific category."""
        return Product.query.filter_by(category_id=category_id).all()
