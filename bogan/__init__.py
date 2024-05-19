from flask import Flask

from flask_login import LoginManager
from bogan.db.models import db, User
from bogan.utils import env
from dotenv import load_dotenv


# init dotenv
load_dotenv(override=True)

def create_app():
    app = Flask(__name__, static_folder="static")

    app.config["SECRET_KEY"] = env("FLASK_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{env('DB_USER')}:{env('DB_PW')}@{env('DB_URL')}:{env('DB_PORT')}/{env('DB_NAME')}"
    )
    app.config["VERSION"] = env("BOGAN_VERSION")

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

    with app.app_context():
        ## Delete Database
        # db.drop_all()
        ## Create Database
        db.create_all()

    return app
