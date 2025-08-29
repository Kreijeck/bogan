from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy.orm import Session
from bogan.db.models import db, User, Player, Game, Boardgame, Location
from bogan.utils import Logger, load_yaml, save_yaml, get_db_engine
import bogan.config as cfg
from datetime import datetime

# Add Logging
logger = Logger().setup_logger(__file__)


auth = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

def admin_required(f):
    """Decorator für Admin-Zugriff"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Sie müssen angemeldet sein, um auf diesen Bereich zuzugreifen.", "error")
            return redirect(url_for("auth.login"))
        
        if current_user.role != "admin":
            flash("Sie haben keine Berechtigung für diesen Bereich.", "error")
            return redirect(url_for("main.index"))
        
        return f(*args, **kwargs)
    return decorated_function


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


# ===== ADMIN FUNCTIONALITY =====

@auth.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    """Admin Dashboard - Übersicht"""
    # Statistiken sammeln
    with Session(get_db_engine()) as session:
        user_count = session.query(User).count()
        player_count = session.query(Player).count()
        game_count = session.query(Game).count()
        boardgame_count = session.query(Boardgame).count()
        location_count = session.query(Location).count()
    
    # Events aus YAML laden
    events = load_yaml(cfg.EVENT_YAML)
    event_count = len(events) if events else 0
    
    stats = {
        'users': user_count,
        'players': player_count,
        'games': game_count,
        'boardgames': boardgame_count,
        'locations': location_count,
        'events': event_count
    }
    
    logger.info(f"Admin Dashboard aufgerufen von {current_user.name}")
    return render_template("admin_dashboard.html", stats=stats)


@auth.route("/admin/events")
@login_required
@admin_required
def manage_events():
    """Event-Verwaltung"""
    events = load_yaml(cfg.EVENT_YAML) or {}
    
    # Lade verfügbare Locations aus der Datenbank
    with Session(get_db_engine()) as session:
        locations = session.query(Location).order_by(Location.name).all()
    
    return render_template("admin_events.html", events=events, locations=locations)


@auth.route("/admin/events/add", methods=["POST"])
@login_required
@admin_required
def add_event():
    """Neues Event hinzufügen"""
    try:
        name = request.form.get("name")
        location = request.form.get("location")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        
        if not all([name, location, start_date, end_date]):
            flash("Alle Felder sind erforderlich.", "error")
            return redirect(url_for("auth.manage_events"))
        
        # Events laden
        events = load_yaml(cfg.EVENT_YAML) or {}
        
        # Prüfen ob Event bereits existiert
        if name in events:
            flash("Ein Event mit diesem Namen existiert bereits.", "error")
            return redirect(url_for("auth.manage_events"))
        
        # Datum formatieren (von YYYY-MM-DD zu DD.MM.YYYY)
        start_formatted = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        end_formatted = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        
        # Event hinzufügen
        events[name] = {
            'location': location,
            'datum_start': start_formatted,
            'datum_ende': end_formatted
        }
        
        # Speichern
        save_yaml(cfg.EVENT_YAML, events)
        flash(f"Event '{name}' wurde erfolgreich erstellt.", "success")
        
    except Exception as e:
        logger.error(f"Fehler beim Erstellen des Events: {e}")
        flash("Fehler beim Erstellen des Events.", "error")
    
    return redirect(url_for("auth.manage_events"))


@auth.route("/admin/users")
@login_required
@admin_required
def manage_users():
    """Benutzer-Verwaltung"""
    from sqlalchemy.orm import joinedload
    
    with Session(get_db_engine()) as session:
        # Users mit eager loading der player Beziehung
        users = session.query(User).options(joinedload(User.player)).all()
        
        # Session expunge all objects to detach them from session
        for user in users:
            session.expunge(user)
    
    return render_template("admin_users.html", users=users)


@auth.route("/admin/database")
@login_required
@admin_required
def manage_database():
    """Datenbank-Verwaltung"""
    from sqlalchemy.orm import joinedload
    
    tables = {}
    
    with Session(get_db_engine()) as session:
        # Users mit Player info - eager loading
        tables['users'] = session.query(User).options(joinedload(User.player)).all()
        
        # Players mit User info - eager loading
        tables['players'] = session.query(Player).options(joinedload(Player.user)).all()
        
        # Games mit allen Beziehungen - eager loading
        tables['games'] = session.query(Game).options(
            joinedload(Game.boardgame),
            joinedload(Game.location),
            joinedload(Game.player_pos)
        ).order_by(Game.datum.desc()).limit(100).all()
        
        # Boardgames
        tables['boardgames'] = session.query(Boardgame).order_by(Boardgame.name_primary).all()
        
        # Locations - speziell behandeln
        locations_query = session.query(Location).options(joinedload(Location.games)).all()
        tables['locations'] = []
        for location in locations_query:
            # Games count innerhalb der Session berechnen
            games_count = len(location.games)
            # Location Objekt mit games_count erweitern
            location.games_count = games_count
            tables['locations'].append(location)
    
    return render_template("admin_database.html", tables=tables)


@auth.route("/admin/users/role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def change_user_role(user_id):
    """Benutzerrolle ändern"""
    try:
        new_role = request.form.get("role")
        
        if new_role not in ["user", "admin"]:
            flash("Ungültige Rolle.", "error")
            return redirect(url_for("auth.manage_users"))
        
        with Session(get_db_engine()) as session:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                flash("Benutzer nicht gefunden.", "error")
                return redirect(url_for("auth.manage_users"))
            
            old_role = user.role
            user.role = new_role
            session.commit()
            
            flash(f"Rolle von '{user.name}' von '{old_role}' zu '{new_role}' geändert.", "success")
            logger.info(f"Benutzerrolle geändert: {user.name} ({old_role} -> {new_role}) von {current_user.name}")
            
    except Exception as e:
        flash(f"Fehler beim Ändern der Benutzerrolle: {str(e)}", "error")
        logger.error(f"Fehler beim Ändern der Benutzerrolle: {str(e)}")
    
    return redirect(url_for("auth.manage_users"))
