import os
from flask import Flask

from flask_login import LoginManager
from gamechanger.db.models import db, User
from dotenv import load_dotenv


# init dotenv
load_dotenv(override=True)


def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", default=None)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("FLASK_DATABASE_URI")

    
    # init Database
    db.init_app(app)

    # Add Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
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