from flask import Blueprint

# Create a Blueprint for the credit card routes
credit_card_bp = Blueprint('credit_card', __name__)

# Import the credit_card routes to register the blueprint
from . import routes
