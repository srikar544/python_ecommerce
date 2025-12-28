from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

def seed_users():
    app = create_app()
    with app.app_context():
        users = [
            {"firstname": "Alice", "email": "alice@example.com", "password": "pass123"},
            {"firstname": "Bob", "email": "bob@example.com", "password": "pass123"},
            {"firstname": "Charlie", "email": "charlie@example.com", "password": "pass123"},
            {"firstname": "David", "email": "david@example.com", "password": "pass123"},
            {"firstname": "Eve", "email": "eve@example.com", "password": "pass123"},
            {"firstname": "Frank", "email": "frank@example.com", "password": "pass123"},
            {"firstname": "Grace", "email": "grace@example.com", "password": "pass123"},
            {"firstname": "Heidi", "email": "heidi@example.com", "password": "pass123"},
        ]
        for u in users:
            user = User(first_name=u["firstname"], email=u["email"],
                        password=generate_password_hash(u["password"], method="pbkdf2:sha256"))
            db.session.add(user)
        db.session.commit()
        print("Users seeded successfully!")
