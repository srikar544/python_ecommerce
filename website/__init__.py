from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from urllib.parse import quote_plus

# ✅ db must be created at module level
db = SQLAlchemy()


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )

    password = quote_plus("FirstApp@123")

    app.config["SECRET_KEY"] = "secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{password}@localhost/ecommerce"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ initialize db
    db.init_app(app)

    # ✅ import models AFTER db init
    from . import models

    # ✅ register blueprints
    from .views import views
    from .auth import auth
    from .cart import cart_bp

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(cart_bp)

    # ✅ login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ create tables
    with app.app_context():
        db.create_all()

    # ✅ context processor for cart count
    @app.context_processor
    def inject_cart_count():
        from .models import Cart  # import here to avoid circular import
        if current_user.is_authenticated:
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            return {"cart_count": cart.total_items() if cart else 0}
        return {"cart_count": 0}

    return app
