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
    def CouponData(cls, id, rate, lower_limit, upper_limit, category, payment, merchant):
        return {
            "id": id,
            "rate": rate,
            "lower_limit": lower_limit,
            "upper_limit": upper_limit,
            "category": category,
            "payment": payment,
            "merchant": merchant
        }

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

        return [cls.CouponData(
            coupon.id,
            coupon.rate,
            coupon.lower_limit,
            coupon.upper_limit,
            coupon.category,
            coupon.payment,
            coupon.merchant
        ) for coupon in coupons_data]
    
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

        coupons_general = [cls.CouponData(
            coupon.id,
            coupon.rate,
            coupon.lower_limit,
            coupon.upper_limit,
            coupon.category,
            coupon.payment,
            coupon.merchant
        ) for coupon in general_query]

        query = cls.select().where(
            cls.start_datetime <= _datetime,
            cls.end_datetime > _datetime,
            cls.card_id == card_id,
            cls.category == category if category != 0 else True,
            cls.payment == payment if payment != 0 else True,
            cls.merchant == merchant if merchant != 0 else True,
        ).order_by(cls.category, cls.payment, cls.merchant)

        return coupons_general + [cls.CouponData(
            coupon.id,
            coupon.rate,
            coupon.lower_limit,
            coupon.upper_limit,
            coupon.category,
            coupon.payment,
            coupon.merchant
        ) for coupon in query]
