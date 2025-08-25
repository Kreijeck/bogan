from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy.orm import Session
from bogan.db.models import User, Player, Game, Boardgame, Location
from bogan.utils import Logger, load_yaml, save_yaml, get_db_engine
import bogan.config as cfg
from datetime import datetime

# Add Logging
logger = Logger().setup_logger(__file__)

admin = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates")

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

@admin.route("/")
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

@admin.route("/events")
@login_required
@admin_required
def manage_events():
    """Event-Verwaltung"""
    events = load_yaml(cfg.EVENT_YAML) or {}
    
    # Lade verfügbare Locations aus der Datenbank
    with Session(get_db_engine()) as session:
        locations = session.query(Location).order_by(Location.name).all()
    
    return render_template("admin_events.html", events=events, locations=locations)

@admin.route("/events/add", methods=["POST"])
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
            return redirect(url_for("admin.manage_events"))
        
        # Events laden
        events = load_yaml(cfg.EVENT_YAML) or {}
        
        # Prüfen ob Event bereits existiert
        if name in events:
            flash("Ein Event mit diesem Namen existiert bereits.", "error")
            return redirect(url_for("admin.manage_events"))
        
        # Datum formatieren (von YYYY-MM-DD zu DD.MM.YYYY)
        start_formatted = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        end_formatted = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        
        # Event hinzufügen
        events[name] = {
            "location": location,
            "datum_start": start_formatted,
            "datum_ende": end_formatted,
            "ignored_player": None
        }
        
        # Speichern
        save_yaml(cfg.EVENT_YAML, events)
        
        flash(f"Event '{name}' wurde erfolgreich hinzugefügt.", "success")
        logger.info(f"Event '{name}' hinzugefügt von {current_user.name}")
        
    except Exception as e:
        flash(f"Fehler beim Hinzufügen des Events: {str(e)}", "error")
        logger.error(f"Fehler beim Hinzufügen des Events: {str(e)}")
    
    return redirect(url_for("admin.manage_events"))

@admin.route("/events/edit/<path:event_name>", methods=["POST"])
@login_required
@admin_required
def edit_event(event_name):
    """Event bearbeiten"""
    try:
        location = request.form.get("location")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        
        if not all([location, start_date, end_date]):
            flash("Alle Felder sind erforderlich.", "error")
            return redirect(url_for("admin.manage_events"))
        
        # Events laden
        events = load_yaml(cfg.EVENT_YAML) or {}
        
        if event_name not in events:
            flash("Event nicht gefunden.", "error")
            return redirect(url_for("admin.manage_events"))
        
        # Datum formatieren
        start_formatted = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        end_formatted = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        
        # Event aktualisieren
        events[event_name].update({
            "location": location,
            "datum_start": start_formatted,
            "datum_ende": end_formatted
        })
        
        # Speichern
        save_yaml(cfg.EVENT_YAML, events)
        
        flash(f"Event '{event_name}' wurde erfolgreich aktualisiert.", "success")
        logger.info(f"Event '{event_name}' bearbeitet von {current_user.name}")
        
    except Exception as e:
        flash(f"Fehler beim Bearbeiten des Events: {str(e)}", "error")
        logger.error(f"Fehler beim Bearbeiten des Events: {str(e)}")
    
    return redirect(url_for("admin.manage_events"))

@admin.route("/events/delete/<path:event_name>", methods=["POST"])
@login_required
@admin_required
def delete_event(event_name):
    """Event löschen"""
    try:
        events = load_yaml(cfg.EVENT_YAML) or {}
        
        if event_name in events:
            del events[event_name]
            save_yaml(cfg.EVENT_YAML, events)
            flash(f"Event '{event_name}' wurde gelöscht.", "success")
            logger.info(f"Event '{event_name}' gelöscht von {current_user.name}")
        else:
            flash("Event nicht gefunden.", "error")
            
    except Exception as e:
        flash(f"Fehler beim Löschen des Events: {str(e)}", "error")
        logger.error(f"Fehler beim Löschen des Events: {str(e)}")
    
    return redirect(url_for("admin.manage_events"))

@admin.route("/database")
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

@admin.route("/users")
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

@admin.route("/users/role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def change_user_role(user_id):
    """Benutzerrolle ändern"""
    try:
        new_role = request.form.get("role")
        
        if new_role not in ["user", "admin"]:
            flash("Ungültige Rolle.", "error")
            return redirect(url_for("admin.manage_users"))
        
        with Session(get_db_engine()) as session:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                flash("Benutzer nicht gefunden.", "error")
                return redirect(url_for("admin.manage_users"))
            
            old_role = user.role
            user.role = new_role
            session.commit()
            
            flash(f"Rolle von '{user.name}' von '{old_role}' zu '{new_role}' geändert.", "success")
            logger.info(f"Benutzerrolle geändert: {user.name} ({old_role} -> {new_role}) von {current_user.name}")
            
    except Exception as e:
        flash(f"Fehler beim Ändern der Benutzerrolle: {str(e)}", "error")
        logger.error(f"Fehler beim Ändern der Benutzerrolle: {str(e)}")
    
    return redirect(url_for("admin.manage_users"))

@admin.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    """Benutzer löschen"""
    try:
        with Session(get_db_engine()) as session:
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                flash("Benutzer nicht gefunden.", "error")
                return redirect(url_for("admin.manage_users"))
            
            # Verhindere, dass sich der Admin selbst löscht
            if user.id == current_user.id:
                flash("Sie können sich nicht selbst löschen.", "error")
                return redirect(url_for("admin.manage_users"))
            
            # Verhindere das Löschen des letzten Admin-Benutzers
            admin_count = session.query(User).filter(User.role == 'admin').count()
            if user.role == 'admin' and admin_count <= 1:
                flash("Der letzte Admin-Benutzer kann nicht gelöscht werden.", "error")
                return redirect(url_for("admin.manage_users"))
            
            username = user.name
            user_role = user.role
            session.delete(user)
            session.commit()
            
            flash(f"Benutzer '{username}' wurde erfolgreich gelöscht.", "success")
            logger.info(f"Benutzer gelöscht: {username} ({user_role}) von {current_user.name}")
            
    except Exception as e:
        flash(f"Fehler beim Löschen des Benutzers: {str(e)}", "error")
        logger.error(f"Fehler beim Löschen des Benutzers: {str(e)}")
    
    return redirect(url_for("admin.manage_users"))
