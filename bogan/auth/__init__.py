from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from bogan.db.models import db, User
from bogan.utils import Logger

# Add Logging
logger = Logger().setup_logger(__file__)


auth = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")


@auth.route("/login")
def login():
    logger.info("LOGIN wird aufgerufen")
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    logger.info("Wird aufgerufen")
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(email=email).first()

    # check if the user exist and check the password
    if not user or not check_password_hash(user.password, password):
        logger.info("User existiert nicht oder Passwort ist falsch")
        return redirect(url_for("auth.login"))

    # Wenn dieser Check erfolgt ist, wurden die korrekten Credentials verwendet
    login_user(user, remember=remember)

    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    # Überprüft ob email bereits vergeben ist
    user = User.query.filter_by(email=email).first()

    # Wenn email schon vorhanden, reset to basic
    if user:
        logger.info("Email address already exist!")
        return redirect(url_for("auth.signup"))

    # Erstelle neuen Benutzer
    new_user = User(email=email, name=name, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for("main.index"))
