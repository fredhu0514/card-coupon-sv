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
