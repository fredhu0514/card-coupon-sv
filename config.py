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
