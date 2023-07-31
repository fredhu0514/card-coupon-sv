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
