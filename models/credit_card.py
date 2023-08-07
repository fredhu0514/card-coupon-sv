from peewee import CharField, UUIDField, AutoField
import uuid

# Get the shared database connection from the BaseModel
from .interfaces.base_model import BaseModel

class CreditCard(BaseModel):
    """
    CreditCard model represents a credit card entity.

    Attributes:
        id (AutoField): The primary key for the credit card.
        uuid (UUIDField): The unique identifier (UUID) for the credit card (for secondary display only).
        name (CharField): The name of the credit card.
        issuer (CharField): The name of the bank associated with the credit card.
        system (CharField): The payment system the card belongs to (e.g., Visa, Mastercard).
        cobranded (CharField): The other companies that co-branded this card with the issuer.
        image_url (CharField): The URL storing the image of the credit card.
    """

    id = AutoField(primary_key=True)
    uuid = UUIDField(default=uuid.uuid4, unique=True)
    name = CharField(max_length=64)
    issuer = CharField(max_length=64)
    system = CharField(max_length=64)
    cobranded = CharField(max_length=64)
    image_url = CharField(max_length=256)
    
    class Meta:
        table_name = "credit_cards"
