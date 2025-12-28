from website import create_app, db
from seeds.seed_users import seed_users
from seeds.seed_products import seed_products
from seeds.seed_categories import seed_categories
from website.models import Cart, CartItem, Category, Product, User  # optional if you have it

app = create_app()

#  Use application context
with app.app_context():
    # Clear previous data
    db.session.query(CartItem).delete()
    db.session.query(Cart).delete()
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Seed data
    seed_users()
    seed_categories()
    seed_products()
    # seed_carts()  # optional
