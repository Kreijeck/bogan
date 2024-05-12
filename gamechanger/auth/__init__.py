from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from gamechanger.db.models import User
from .. import db

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if the user exist and check the password
    if not user or not check_password_hash(user.password, password):
        # TODO Remove print
        print("User existiert nicht oder Passwort ist falsch")
        return redirect(url_for("auth.login"))
    
    # Wenn dieser Check erfolgt ist, wurden die korrekten Credentials verwendet
    login_user(user, remember=remember)

    return redirect(url_for("main.index"))