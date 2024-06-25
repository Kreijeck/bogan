from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from bogan.db.models import db, User
import bogan.config as cfg


def create_app():
    app = Flask(__name__, static_folder="static")

    # add migrate
    migrate = Migrate(app, db, directory=cfg.DB_MIGRATE_DIR)

    app.config["SECRET_KEY"] = cfg.FLASK_SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.DB_SERVER
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

    # add all blueprints
    # Alle /templates Ordner aus Blueprints sind verfügbar. Bei gleichem Namen, wird der erste Import genommen
    from .main import main as main_bp

    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp

    app.register_blueprint(auth_bp)

    from .tools import tools as tools_bp

    app.register_blueprint(tools_bp)

    # with app.app_context():
        ## Delete Database
        # db.drop_all()
        ## Create Database
        # db.create_all()

    return app
