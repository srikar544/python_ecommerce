from typing import List, Optional
from website.models import Product
from website import db


class ProductService:
    """Handles all product-related business logic."""

    @staticmethod
    def get_all_products() -> List[Product]:
        """Return all products from the database."""
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """
        Return a single product by its ID.

        Args:
            product_id (int): Product ID

        Returns:
            Product | None
        """
        return Product.query.get(product_id)

    @staticmethod
    def create_product(
        name: str,
        price: float,
        stock: int,
        category_id: int,
        description: Optional[str] = None
    ) -> Product:
        """
        Create and save a new product.

        Args:
            name (str): Product name
            price (float): Product price
            stock (int): Available stock
            category_id (int): ID of the category
            description (str, optional): Product description

        Returns:
            Product: The newly created product
        """
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
    def get_products_by_category(category_id: int) -> List[Product]:
        """
        Return all products under a specific category.

        Args:
            category_id (int): Category ID

        Returns:
            List[Product]: Products in the category
        """
        return Product.query.filter_by(category_id=category_id).all()
