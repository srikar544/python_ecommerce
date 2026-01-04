# Import core Flask class to create the web application
from flask import Flask

# SQLAlchemy is the ORM used to interact with the database
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

# Flask-Login handles user authentication (login, logout, sessions)
from flask_login import LoginManager, current_user

# Used to safely encode special characters in the database password
from urllib.parse import quote_plus

from .config import config_map
from .logger import setup_logger
from .cache import cache
import os
 


# --------------------------------------------------
# Create the database object at MODULE LEVEL
# This allows models to import and use `db`
# --------------------------------------------------
db = SQLAlchemy()
cache = Cache()


def create_app():
    """
    Application factory function.
    This function creates and configures the Flask app instance.
    """

    # Create Flask app instance
    app = Flask(
        __name__,
        static_folder="static",     # Folder for CSS, JS, images
        template_folder="templates"  # Folder for HTML templates
    )

    # --------------------------------------------------
    # Load environment-based configuration
    # ---

    env= os.getenv("FLASK_ENV","development")
    app.config.from_object(config_map[env])
   

    # --------------------------------------------------
    # Application configuration
    # --------------------------------------------------

    # Secret key is used for sessions, cookies, CSRF protection
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret-key")
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    db_user = os.getenv("DB_USER", "root")
    db_password = quote_plus(os.getenv("DB_PASSWORD", ""))
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "ecommerce")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    cache.init_app(app)
    

    #----
    # Setup Logging
    #----

    setup_logger(app)

    # --------------------------------------------------
    # Import models AFTER initializing db
    # This avoids circular import problems
    # --------------------------------------------------
    from . import models


    # --------------------------------------------------
    # Register Blueprints (modular route groups)
    # --------------------------------------------------
    from .views import views     # main website routes
    from .auth import auth       # authentication routes
    from .cart import cart_bp,orders_bp    # shopping cart routes
     

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp, url_prefix="/orders")


    # --------------------------------------------------
    # Setup Flask-Login
    # --------------------------------------------------
    login_manager = LoginManager()
    # If a user tries to access a protected page,
    # they will be redirected to this login route
    login_manager.login_view = "auth.login"
    # Attach login manager to the app
    login_manager.init_app(app)

    # Import User model for login handling
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        This function tells Flask-Login how to get a user
        from the database using the user ID stored in session.
        """
        return User.query.get(int(user_id))

    # --------------------------------------------------
    # Create database tables (only if they don't exist)
    # --------------------------------------------------
    with app.app_context():
        db.create_all()

    # --------------------------------------------------
    # Context processor (runs before every template render)
    # Used to make cart_count available in ALL templates
    # --------------------------------------------------
    @app.context_processor
    def inject_cart_count():
        # Import here to avoid circular import issues
        #Run this function before rendering any template, and add whatever it returns to the template context.”
        from .models import Cart

        if not current_user.is_authenticated:
             return {"cart_count":0}
        
        cache_key= f"cart_count_{current_user.id}"
        count = cache.get(cache_key)

        # Only check cart if user is logged in
        if count is None:
            cart  = Cart.query.filter_by(user_id=current_user.id).first()
            count = cart.total_items() if cart else 0
            cache.set(cache_key,count,timeout=30)
            return {"cart_count": count}

        # For guest users
        return {"cart_count": 0}


    # Return the fully configured app
    return app
