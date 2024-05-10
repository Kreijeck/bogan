from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main',__name__, template_folder='templates')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/profile')
def profile():
    return "Hallo neues Profil"