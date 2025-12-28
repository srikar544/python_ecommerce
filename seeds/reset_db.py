from website import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Disable FK checks
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

    # Truncate tables (order matters)
    db.session.execute(text("TRUNCATE TABLE cart_item;"))
    db.session.execute(text("TRUNCATE TABLE cart;"))
    db.session.execute(text("TRUNCATE TABLE product;"))
    db.session.execute(text("TRUNCATE TABLE category;"))
    db.session.execute(text("TRUNCATE TABLE user;"))

    # Enable FK checks
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    db.session.commit()

print(" Database reset complete (IDs restart from 1)")
