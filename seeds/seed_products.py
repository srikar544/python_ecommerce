from website import db
from website.models import Product

def seed_products():
    Product.query.delete()

    products = [
        {"name": "Smartphone", "price": 299.99, "stock": 10, "description": "Latest model", "category_id": 1},
        {"name": "Laptop", "price": 899.99, "stock": 5, "description": "High performance", "category_id": 1},
        {"name": "Novel Book", "price": 19.99, "stock": 20, "description": "Bestseller", "category_id": 2},
        {"name": "T-Shirt", "price": 9.99, "stock": 50, "description": "Cotton T-shirt", "category_id": 3},
        {"name": "Jeans", "price": 39.99, "stock": 25, "description": "Denim jeans", "category_id": 3},
        {"name": "Football", "price": 29.99, "stock": 15, "description": "Soccer ball", "category_id": 8},
        {"name": "Headphones", "price": 59.99, "stock": 30, "description": "Audio gear", "category_id": 5},
        {"name": "Sneakers", "price": 69.99, "stock": 20, "description": "Comfortable footwear", "category_id": 4},
        {"name": "Blender", "price": 49.99, "stock": 10, "description": "Kitchen appliance", "category_id": 6},
        {"name": "Travel Bag", "price": 79.99, "stock": 12, "description": "Durable bag", "category_id": 7},
    ]

    for p in products:
        product = Product(
            name=p["name"],
            price=p["price"],
            stock=p["stock"],
            description=p["description"],
            category_id=p["category_id"]
        )
        db.session.add(product)

    db.session.commit()
    print("Seeded products successfully!")
