from flask import Flask
from config import app_config
from models.interfaces.base_model import initialize_database

def create_app():
    # Create and configure the Flask app instance
    app = Flask(__name__)
    app.config.from_object(app_config)

    # Register the blueprints for different resources
    from apis.coupon import coupon_bp
    from apis.credit_card import credit_card_bp

    app.register_blueprint(coupon_bp, url_prefix='/api/coupon')
    app.register_blueprint(credit_card_bp, url_prefix='/api/credit_card')

    # Call the function to initialize the database
    with app.app_context():
        initialize_database(app)

    return app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=5000)
