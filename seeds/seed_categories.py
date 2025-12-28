from website import db
from website.models import Category

def seed_categories():
    # Delete existing categories
    Category.query.delete()

    categories = [
        "Electronics",
        "Books",
        "Clothing",
        "Footwear",
        "Audio",
        "Kitchen",
        "Travel",
        "Sports",
        "Toys",
        "Accessories"
    ]

    for cat in categories:
        category = Category(name=cat)
        db.session.add(category)

    db.session.commit()
    print("Seeded categories successfully!")
