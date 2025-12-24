from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("views.home"))

        flash("Invalid credentials", "error")

    return render_template("login.html")


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user = User(
            email=request.form.get("email"),
            first_name=request.form.get("firstname"),
            password=generate_password_hash(request.form.get("password"))
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("views.home"))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
