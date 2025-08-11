from flask import Blueprint, render_template, redirect, url_for, request, flash
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
    logger.info("Login wird aufgerufen")
    name = request.form.get("name")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    
    # Validiere Eingaben
    if not name or not password:
        flash("Name und Passwort sind erforderlich.", "error")
        return redirect(url_for("auth.login"))
    
    user = User.query.filter_by(name=name).first()

    # check if the user exist and check the password
    if not user or not check_password_hash(user.password, password):
        logger.info("User existiert nicht oder Passwort ist falsch")
        flash("Ungültiger Name oder Passwort.", "error")
        return redirect(url_for("auth.login"))

    # Wenn dieser Check erfolgt ist, wurden die korrekten Credentials verwendet
    login_user(user, remember=remember)
    flash(f"Willkommen zurück, {name}!", "success")

    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")  # Email ist jetzt optional
    name = request.form.get("name")
    password = request.form.get("password")
    signup_secret = request.form.get("signup_secret")

    # Validiere Eingaben
    if not name or not password:
        flash("Name und Passwort sind erforderlich.", "error")
        return redirect(url_for("auth.signup"))

    # Import hier um zirkuläre Imports zu vermeiden
    import bogan.config as cfg

    # Überprüfe Sign-up Secret
    if signup_secret != cfg.SIGNUP_SECRET:
        logger.warning(f"Ungültiges Sign-up Secret für Nutzer {name}")
        flash("Ungültiger Sign-Up Code. Bitte wende dich an den Administrator.", "error")
        return redirect(url_for("auth.signup"))

    # Überprüft ob Name bereits vergeben ist (Name ist jetzt der eindeutige Identifier)
    user = User.query.filter_by(name=name).first()

    # Wenn Name schon vorhanden, reset to basic
    if user:
        logger.info(f"Name {name} already exists!")
        flash(f"Der Name '{name}' ist bereits vergeben. Bitte wähle einen anderen Namen.", "error")
        return redirect(url_for("auth.signup"))

    try:
        # Erstelle neuen Benutzer (Email kann None/leer sein)
        new_user = User(
            email=email if email else None, 
            name=name, 
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"Neuer Nutzer erstellt: {name}")
        flash(f"Account für '{name}' wurde erfolgreich erstellt! Du kannst dich jetzt anmelden.", "success")
        return redirect(url_for("auth.login"))
    
    except Exception as e:
        logger.error(f"Fehler beim Erstellen des Nutzers {name}: {str(e)}")
        db.session.rollback()
        flash("Ein Fehler ist aufgetreten. Bitte versuche es erneut.", "error")
        return redirect(url_for("auth.signup"))


@auth.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for("main.index"))
