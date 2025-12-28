# Flask utilities for routing, templates, redirects, and flash messages
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Password hashing & verification (never store plain passwords!)
from werkzeug.security import generate_password_hash, check_password_hash

# Flask-Login helpers for session-based authentication
from flask_login import login_user, logout_user, login_required

# User model and database instance
from .models import User
from . import db


# ----------------------------------------------------
# AUTH BLUEPRINT
# ----------------------------------------------------
# A Blueprint helps organize authentication routes
# All auth-related URLs will be grouped under this blueprint
auth = Blueprint("auth", __name__)


# ----------------------------------------------------
# LOGIN ROUTE
# ----------------------------------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    # If user submits the login form
    if request.method == "POST":

        # Read form values from login.html
        email = request.form.get("email")
        password = request.form.get("password")

        # Look up the user in the database by email
        user = User.query.filter_by(email=email).first()

        # 1. Check if user exists
        # 2. Verify the entered password against the hashed password
        if user and check_password_hash(user.password, password):

            # login_user():
            # - Stores user ID in Flask session
            # - Marks the user as authenticated
            # - Makes `current_user` available in all requests
            login_user(user)

            # Redirect to home page after successful login
            return redirect(url_for("views.home"))

        # If login fails, show an error message
        flash("Invalid credentials", "error")

    # Render login page for GET request
    return render_template("login.html")


# ----------------------------------------------------
# SIGN-UP (REGISTRATION) ROUTE
# ----------------------------------------------------
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":

        # SQLAlchemy provides a default constructor,
        # so we can directly pass column values as arguments
        user = User(
            email=request.form.get("email"),
            first_name=request.form.get("firstname"),

            # Password is hashed before storing in DB
            password=generate_password_hash(request.form.get("password"))
        )

        # Add the new user to the database session
        db.session.add(user)

        # Commit the transaction (saves user permanently)
        db.session.commit()

        # Automatically log the user in after signup
        # This writes the user ID into Flask's session
        login_user(user)

        # Redirect to home page
        return redirect(url_for("views.home"))

    # Render signup page for GET request
    return render_template("signup.html")


# ----------------------------------------------------
# LOGOUT ROUTE
# ----------------------------------------------------
@auth.route("/logout")
@login_required  # Ensures only logged-in users can access this route
def logout():

    # logout_user():
    # - Clears user ID from session
    # - current_user becomes AnonymousUser
    logout_user()

    # Redirect back to login page
    return redirect(url_for("auth.login"))
