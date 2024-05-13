import os
from flask import Flask

from flask_login import LoginManager
from gamechanger.db.models import db
from dotenv import load_dotenv


# init dotenv
load_dotenv(override=True)


def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", default=None)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("FLASK_DATABASE_URI")

    
    # init Database
    db.init_app(app)

    # add all blueprints
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    # # Create Database and delte old
    with app.app_context():
        db.drop_all()
        db.create_all()

    return app