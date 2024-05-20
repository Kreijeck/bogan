from flask import Blueprint

from .vote import vote as vote_bp
tools = Blueprint('tools',__name__, url_prefix="/tools")

# Register all child blueprints
tools.register_blueprint(vote_bp)

