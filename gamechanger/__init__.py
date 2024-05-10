import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from .main import main_bp as main_blueprint

# init dotenv
load_dotenv(override=True)
# init SQLALchemy
db: SQLAlchemy = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", default=None)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # app.template_folder = 

    db.init_app(app)

    # blueprint for main routes
    # from .main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app