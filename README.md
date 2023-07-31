This is my tree diagram: 
card-coupon-sv
├── Dockerfile
├── apis
│   ├── __init__.py
│   ├── coupon
│   │   ├── __init__.py
│   │   └── routes.py
│   └── credit_card
│       ├── __init__.py
│       └── routes.py
├── app.py
├── card-coupon-db
│   ├── production
│   │   ├── db_public.sqlite3
│   │   └── static
│   │       └── credit_card_images
│   └── testing
│       ├── db_public.sqlite3
│       └── static
│           └── credit_card_images
├── config.py
├── docker-compose.yml
├── models
│   ├── __init__.py
│   ├── coupon.py
│   ├── credit_card.py
│   └── interfaces
│       ├── __init__.py
│       └── base_model.py
└── requirements.txt

My `Dockerfile`: 
# Use the official Python image as the base image
FROM python:3.8.13

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Set the entrypoint command to run the Flask app
CMD ["python", "app.py"]

My `docker-compose.yml`:
version: "3.9"

services:
  production:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      FLASK_ENV: production
    volumes:
      - ./card-coupon-db/production:/app/card-coupon-db
    ports:
      - "5500:5000"
  
  testing:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      FLASK_ENV: testing
    volumes:
      - ./card-coupon-db/testing:/app/card-coupon-db
    ports:
      - "5555:5000"

My `apis/__init__.py`:
# This is the initialization file for the 'apis' package.
# It is left empty since we don't have any specific initialization tasks for now.

My `apis/coupon/__init__.py`:
from flask import Blueprint

# Create a Blueprint for the coupon routes
coupon_bp = Blueprint('coupon', __name__)

# Import the coupon routes to register the blueprint
from . import routes

My `apis/coupon/routes.py`:
from flask import Blueprint, jsonify, request
from models.coupon import Coupon
from datetime import datetime
from . import coupon_bp  # Import the existing 'coupon_bp' Blueprint

# Define your API routes for coupons
@coupon_bp.route('/get_all_available_coupons', methods=['GET'])
def get_all_available_coupons():
    """
    Get all available coupons associated with the specified credit card.

    URL Parameters:
        card_id (str): The ID of the credit card to retrieve coupons for.
        datetime (str, optional): The current date and time for filtering available coupons (ISO 8601 format).

    Returns:
        Response: A JSON response containing a list of available coupons.
    """
    card_id = request.args["card_id"]
    _datetime = request.args.get('datetime', datetime.now())
    coupons = Coupon.get_all_available_coupons(
        card_id=card_id,
        _datetime=_datetime
    )
    return jsonify({"getAllAvailableCouponsResponse": coupons})

# Define your API routes for coupons
@coupon_bp.route('/get_available_coupons_with_constraints', methods=['GET'])
def get_available_coupons_with_constraints():
    """
    Get available coupons associated with the specified credit card, filtered by constraints.

    URL Parameters:
        card_id (str): The ID of the credit card to retrieve coupons for.
        datetime (str, optional): The current date and time for filtering available coupons (ISO 8601 format).
        category (int, optional): The category constraint for filtering coupons. Default is 0.
        payment (int, optional): The payment constraint for filtering coupons. Default is 0.
        merchant (int, optional): The merchant constraint for filtering coupons. Default is 0.

    Returns:
        Response: A JSON response containing a list of available coupons.
    """
    card_id = request.args["card_id"]
    _datetime = request.args.get('datetime', datetime.now())
    category = request.args.get('category', 0)
    payment = request.args.get('payment', 0)
    merchant = request.args.get('merchant', 0)
    coupons = Coupon.get_available_coupons_with_constraints(
        card_id=card_id,
        _datetime=_datetime,
        category=category, 
        payment=payment, 
        merchant=merchant
    )
    return jsonify({"getAvailableCouponsWithConstraintsResponse": coupons})

My `apis/credit_card/__init__.py`:
from flask import Blueprint

# Create a Blueprint for the credit card routes
credit_card_bp = Blueprint('credit_card', __name__)

# Import the credit_card routes to register the blueprint
from . import routes

My `apis/credit_card/routes.py`:
import os
import secrets
from flask import Blueprint, jsonify, request
from models.credit_card import CreditCard
from werkzeug.utils import secure_filename
import app
from . import credit_card_bp  # Import the existing 'credit_card_bp' Blueprint


@credit_card_bp.route('/create_credit_card', methods=['POST'])
def create_credit_card():
    """
    Create a new credit card.

    Expected JSON data in request body:
    {
        "card_name": "Card Name",
        "bank_name": "Bank Name",
        "image": <file> (multipart/form-data)
    }

    Returns:
    - 201 Created: If the credit card is successfully created.
    - 400 Bad Request: If the request data is invalid or missing.
    - 500 Internal Server Error: If there was an error while creating the credit card.
    """
    data = request.form
    image_file = request.files['image']

    if not data or not all(key in data for key in ["card_name", "bank_name"]) or not image_file:
        return jsonify({"error": "Invalid or missing request data"}), 400

    try:
        card_name = data["card_name"]
        bank_name = data["bank_name"]
        filename = secure_filename(f"{secrets.token_hex(16)}.png")

        # Determine the path to store the image based on the environment
        image_folder = app.config["UPLOAD_FOLDER"] # TODO: Need to change the UPLOAD_FOLDER in different env.
        image_path = os.path.join(image_folder, "credit_card_images", filename)

        # Save the image file to the appropriate directory
        image_file.save(image_path)

        # Create the credit card record in the database
        credit_card = CreditCard.create(
            card_name=card_name,
            bank_name=bank_name,
            image_url=filename  # Store the image URL as the file path
        )

        return jsonify({"addCreditCardResponse": {"id": str(credit_card.id)}}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@credit_card_bp.route('/get_all_credit_cards', methods=['GET'])
def get_all_credit_cards():
    """
    Get all credit cards.

    Returns:
    - 200 OK: A list of all credit cards.
    - 500 Internal Server Error: If there was an error while fetching the credit cards.
    """
    try:
        credit_cards = CreditCard.select()
        return jsonify({"getAllCreditCardsResponse": {"creditCards": credit_cards}}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

My `models/__init__.py`:
# Nothing here

My `models/coupon.py`:
from collections import namedtuple 

from peewee import *
from .interfaces.base_model import BaseModel
from .credit_card import CreditCard

# Named tuple to hold the data for each coupon
CouponData = namedtuple(
    "CouponData",
    [
        "id",
        "rate",
        "lower_limit",
        "upper_limit",
        "category",
        "payment",
        "merchant",
    ],
)

class Coupon(BaseModel):
    """
    Coupon model represents a discount coupon that can be associated with a credit card.
    """

    id = AutoField(primary_key=True)
    rate = FloatField()
    lower_limit = FloatField()
    upper_limit = FloatField()
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    card = ForeignKeyField(CreditCard, backref="coupons")
    category = IntegerField(default=0, null=True)  # Nullable field
    payment = IntegerField(default=0, null=True)  # Nullable field
    merchant = IntegerField(default=0, null=True)  # Nullable field

    class Meta:
        table_name = "coupons"  # Specify the table name (optional, default would be 'coupon')

    @classmethod
    def get_all_available_coupons(cls, card_id, _datetime):
        """
        Get all available coupons associated with the specified credit card.

        Args:
            card_id (str): The ID of the credit card to retrieve coupons for.
            _datetime (datetime.datetime): The current date and time for filtering available coupons.

        Returns:
            List[CouponData]: A list of named tuples representing available coupons.
        """
        coupons_data = cls.select(
            cls.id,
            cls.rate,
            cls.lower_limit,
            cls.upper_limit,
            cls.category,
            cls.payment,
            cls.merchant,
        ).where(
            cls.start_datetime <= _datetime,
            cls.end_datetime > _datetime,
            cls.card_id == card_id,
        )

        return [CouponData(**coupon._data) for coupon in coupons_data]
    
    @classmethod
    def get_available_coupons_with_constraints(
        cls, card_id, _datetime, category=0, payment=0, merchant=0
    ):
        """
        Get available coupons associated with the specified credit card, filtered by constraints.

        Args:
            card_id (str): The ID of the credit card to retrieve coupons for.
            _datetime (datetime.datetime): The current date and time for filtering available coupons.
            category (int, optional): The category constraint for filtering coupons. Default is 0.
            payment (int, optional): The payment constraint for filtering coupons. Default is 0.
            merchant (int, optional): The merchant constraint for filtering coupons. Default is 0.

        Returns:
            List[CouponData]: A list of named tuples representing available coupons.
        """
        if category == payment == merchant == 0:
            raise ValueError(
                "Invalid query with all empty/general category, payment, and merchant."
            )

        general_query = cls.select().where(
            cls.start_datetime <= _datetime,
            cls.end_datetime > _datetime,
            cls.card_id == card_id,
            cls.category == 0,
            cls.payment == 0,
            cls.merchant == 0,
        ).order_by(-cls.rate).limit(1)

        coupons_general = [CouponData(**coupon._data) for coupon in general_query]

        query = cls.select().where(
            cls.start_datetime <= _datetime,
            cls.end_datetime > _datetime,
            cls.card_id == card_id,
            cls.category == category if category != 0 else True,
            cls.payment == payment if payment != 0 else True,
            cls.merchant == merchant if merchant != 0 else True,
        ).order_by(cls.category, cls.payment, cls.merchant)

        return coupons_general + [CouponData(**coupon._data) for coupon in query]


My `models/credit_card.py`:
from peewee import CharField, UUIDField
import uuid

# Get the shared database connection from the BaseModel
from .interfaces.base_model import BaseModel

class CreditCard(BaseModel):
    """
    CreditCard model represents a credit card entity.

    Attributes:
        id (UUIDField): The unique identifier (UUID) for the credit card.
        card_name (CharField): The name of the credit card.
        bank_name (CharField): The name of the bank associated with the credit card.
        image_url (CharField): The URL storing the image of the credit card.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    card_name = CharField(max_length=64)
    bank_name = CharField(max_length=64)
    image_url = CharField(max_length=256)  # Storing the image URL

    class Meta:
        table_name = "credit_cards"

My `models/interfaces/__init__.py`:
# Nothing here

My `models/interfaces/base_model.py`:
from flask import current_app
from peewee import Model, SqliteDatabase

# The `database` variable will be initialized later within the application context.
database = None

class BaseModel(Model):
    """
    Base model class for all models in the application.

    Attributes:
        database (SqliteDatabase): The shared database connection for all models.
    """
    class Meta:
        database = database

# Import this after defining the BaseModel to avoid circular import
from app import app

# Initialize the database with the current app's configuration
with app.app_context():
    database = SqliteDatabase(current_app.config['DATABASE_URI'])

My `app.py`:
from flask import Flask
from config import app_config

def create_app():
    # Create and configure the Flask app instance
    app = Flask(__name__)
    app.config.from_object(app_config)

    # Register the blueprints for different resources
    from apis.coupon import coupon_bp
    from apis.credit_card import credit_card_bp

    app.register_blueprint(coupon_bp, url_prefix='/api/coupon')
    app.register_blueprint(credit_card_bp, url_prefix='/api/credit_card')

    return app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=5000)

My `config.py`:
import os

class Config:
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "card-coupon-db/production/images"
    DATABASE_URI = "card-coupon-db/production/db_public.sqlite3"

class ProductionConfig(Config):
    DATABASE_URI = "card-coupon-db/production/db_public.sqlite3"

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = "card-coupon-db/testing/images"
    DATABASE_URI = "card-coupon-db/testing/db_public.sqlite3"

# Determine the current environment based on the 'FLASK_ENV' environment variable
if os.environ.get("FLASK_ENV") == "production":
    app_config = ProductionConfig()
elif os.environ.get("FLASK_ENV") == "testing":
    app_config = TestingConfig()

My `requirements.txt`:
flask==2.0.1
peewee==3.14.4

However, how can I initialize the database by creating all the tables in the current enrionment without circular import?
