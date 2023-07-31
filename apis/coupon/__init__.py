from flask import Blueprint

# Create a Blueprint for the coupon routes
coupon_bp = Blueprint('coupon', __name__)

# Import the coupon routes to register the blueprint
from . import routes
