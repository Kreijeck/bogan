from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from bogan.db.models import db, User
import bogan.config as cfg
from bogan.utils import load_yaml, make_dir


def create_app():
    app = Flask(__name__, static_folder="static")

    make_dir(app.instance_path)
    print(app.instance_path)

    # add migrate
    migrate = Migrate(app, db, directory=cfg.DB_MIGRATE_DIR)

    app.config["SECRET_KEY"] = cfg.FLASK_SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.DB2USE
    app.config["DEBUG"] = cfg.FLASK_DEBUG
    app.config["VERSION"] = cfg.BOGAN_VERSION

    # init Database
    db.init_app(app)

    # Add Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Load User wird benötigt um ...
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is primary key, use it in the query
        return User.query.get(int(user_id))
    
    # global verfügbare Parameter
    @app.context_processor
    def inject_nav_parameter():
        events = load_yaml(cfg.EVENT_YAML)
        # Erstelle konsistente Event-Struktur für Navigation
        events_list = []
        for event_name, event_info in events.items():
            events_list.append({
                'name': event_name,
                'location': event_info.get('location', ''),
            })
        # Sortiere alphabetisch für konsistente Darstellung
        events_list.sort(key=lambda x: x['name'])
        return dict(events=events_list)

    # add all blueprints
    # Alle /templates Ordner aus Blueprints sind verfügbar. Bei gleichem Namen, wird der erste Import genommen
    from .main import main as main_bp

    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp

    app.register_blueprint(auth_bp)

    from .tools import tools as tools_bp

    app.register_blueprint(tools_bp)

    # with app.app_context():
        # # Delete Database
        # db.drop_all()
        # # Create Database
        # db.create_all()

    return app
