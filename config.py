import os

class Config:
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "card-coupon-db/static/credit_card_images"
    DATABASE_URI = "card-coupon-db/db_public.sqlite3"

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# Determine the current environment based on the 'FLASK_ENV' environment variable
if os.environ.get("FLASK_ENV") == "production":
    app_config = ProductionConfig()
elif os.environ.get("FLASK_ENV") == "testing":
    app_config = TestingConfig()
elif os.environ.get("FLASK_ENV") == "development":
    app_config = DevelopmentConfig()
