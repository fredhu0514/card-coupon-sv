from flask import jsonify, request
from models.coupon import Coupon
from models.credit_card import CreditCard
from datetime import datetime
from . import coupon_bp  # Import the existing 'coupon_bp' Blueprint


# Route for adding a coupon
@coupon_bp.route('/add_coupon', methods=['POST'])
def add_coupon():
    """
    Add a new coupon to the system.

    This function processes a POST request with coupon data and creates a new coupon instance
    in the database. The data is expected to be sent in form format.

    URL: /add_coupon

    Method: POST

    Parameters (via request.form):
        rate (float): The rate (percentage) of the coupon.
        lower_limit (float): The lower limit value for the coupon.
        upper_limit (float): The upper limit value for the coupon.
        start_datetime (str): The start date and time for the coupon validity in ISO 8601 format.
        end_datetime (str): The end date and time for the coupon validity in ISO 8601 format.
        card_id (int): The ID of the credit card associated with the coupon.
        category (int): The category ID associated with the coupon.
        payment (int): The payment method ID associated with the coupon.
        merchant (int): The merchant ID associated with the coupon.

    Returns:
        Response: A JSON response containing the ID of the newly created coupon.

    Response (JSON):
        {
            "addCouponResponse": {
                "id": "<coupon_id>"
            }
        }

    Example Usage:
        POST /add_coupon
        Form Data:
        {
            "rate": 0.05,
            "lower_limit": 0,
            "upper_limit": 1500,
            "start_datetime": "2023-08-15T12:00:00.000Z",
            "end_datetime": "2023-08-31T23:59:59.000Z",
            "card_id": 1,  # ID of the associated credit card
            "category": 1,
            "payment": 1,
            "merchant": 1
        }

    Notes:
        - The function assumes that the CreditCard and Coupon models are defined
          with a proper database connection and foreign key relationship.
        - Proper error handling for invalid data and non-existent credit card ID is implemented.
          If any error occurs during processing, an appropriate error response will be sent to the client.
    """
    data = request.form
    
    try:
        # Extract coupon data from the JSON payload
        rate = data['rate']
        lower_limit = data['lower_limit']
        upper_limit = data['upper_limit']
        start_datetime = data['start_datetime']
        end_datetime = data['end_datetime']
        card_id = data['card_id']
        category = data['category']
        payment = data['payment']
        merchant = data['merchant']

        # Get the credit card first
        credit_card = CreditCard.get_by_id(card_id)

        # Create a new coupon instance and save it to the database
        coupon = Coupon.create(
            rate=rate,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            card=credit_card,
            category=category,
            payment=payment,
            merchant=merchant
        )

        return jsonify({"addCouponResponse": {"id": str(coupon.id)}}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
