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
