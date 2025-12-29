# ----------------------------------------------------
# Flask helpers
# ----------------------------------------------------
# Blueprint      → Used to split routes into modules (auth, cart, views, etc.)
# render_template→ Renders HTML files
# request        → Reads data sent by the browser (form data)
# redirect       → Sends user to another URL
# url_for        → Generates URLs using route names (safe & flexible)
# flash          → Temporarily shows messages to the user (errors, success)
from flask import Blueprint, render_template, request, redirect, url_for, flash


# ----------------------------------------------------
# Password utilities
# ----------------------------------------------------
# generate_password_hash → Converts plain password into a secure hash
# check_password_hash   → Compares plain password with stored hash
# NEVER store plain passwords in the database!
from werkzeug.security import generate_password_hash, check_password_hash


# ----------------------------------------------------
# Flask-Login utilities
# ----------------------------------------------------
# login_user    → Logs a user in (stores user_id in session)
# logout_user   → Logs the user out (clears session)
# login_required→ Restricts routes to logged-in users only
from flask_login import login_user, logout_user, login_required


# ----------------------------------------------------
# Import database and User model
# ----------------------------------------------------
# User → SQLAlchemy model representing users table
# db   → SQLAlchemy database instance
from .models import User
from . import db


# ====================================================
# AUTH BLUEPRINT
# ====================================================
# A Blueprint groups all authentication-related routes
# Example URLs:
#   /login
#   /sign-up
#   /logout
auth = Blueprint("auth", __name__)


# ====================================================
# LOGIN ROUTE
# ====================================================
@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    - GET  → Show login page
    - POST → Validate user credentials and log in
    """

    # If user submits the login form
    if request.method == "POST":

        # Read form values sent from login.html
        # name="email" and name="password" in HTML form
        email = request.form.get("email")
        password = request.form.get("password")

        # Search for a user with this email in the database
        user = User.query.filter_by(email=email).first()

        # Check:
        # 1. User exists
        # 2. Entered password matches the hashed password in DB
        if user and check_password_hash(user.password, password):

            # login_user():
            # - Saves user ID in Flask session
            # - Marks user as authenticated
            # - Enables `current_user` everywhere
            login_user(user)

            # After successful login, go to home page
            return redirect(url_for("views.home"))

        # If email or password is incorrect
        flash("Invalid credentials. Please sign up first!", "error")

        # Redirect user to signup page
        return redirect(url_for("auth.sign_up"))

    # If request is GET → just show the login page
    return render_template("login.html")


# ====================================================
# SIGN-UP (REGISTRATION) ROUTE
# ====================================================
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """
    Handles new user registration.
    - GET  → Show signup page
    - POST → Create a new user account
    """

    if request.method == "POST":

        # Create a new User object
        # SQLAlchemy automatically maps this to the users table
        user = User(
            email=request.form.get("email"),
            first_name=request.form.get("firstname"),

            # Password is HASHED before storing
            # This protects users even if DB is compromised
            password=generate_password_hash(
                request.form.get("password")
            )
        )

        # Add user to database session (temporary state)
        db.session.add(user)

        # Commit → permanently saves user in database
        db.session.commit()

        # Automatically log in the new user
        # No need to login again after signup
        login_user(user)

        # Redirect to home page
        return redirect(url_for("views.home"))

    # If request is GET → show signup page
    return render_template("signup.html")


# ====================================================
# LOGOUT ROUTE
# ====================================================
@auth.route("/logout")
@login_required
def logout():
    """
    Logs the user out.
    Only accessible if user is logged in.
    """

    # logout_user():
    # - Removes user ID from session
    # - current_user becomes AnonymousUser
    logout_user()

    # Redirect user back to login page
    return redirect(url_for("auth.login"))
