from peewee import Model, SqliteDatabase

# Define the database variable
database = SqliteDatabase(None)

class BaseModel(Model):
    """
    Base model class for all models in the application.

    Attributes:
        database (SqliteDatabase): The shared database connection for all models.
    """
    class Meta:
        database = database

def initialize_database(app):
    # Import the models here to avoid circular import
    from models.credit_card import CreditCard
    from models.coupon import Coupon

    # Connect to the database
    database.init(app.config['DATABASE_URI'])
    database.connect()

    # Create the tables if they don't exist
    database.create_tables([CreditCard, Coupon])
