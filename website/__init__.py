from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote_plus
from .cart import cart_bp

db = SQLAlchemy()

password = quote_plus("FirstApp@123")

DB_NAME  = 'ecommerce'

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://root:{password}@localhost/{DB_NAME}?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .views import views
    from .auth  import auth

    app.register_blueprint(views)
    app.register_blueprint(auth,url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix="/cart")

    login_manager= LoginManager() 
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
         db.create_all()

    return app     

