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

    if not data or not all(key in data for key in ["name", "issuer", "system"]) or not image_file:
        return jsonify({"error": "Invalid or missing request data"}), 400

    try:
        name = data["name"]
        issuer = data["issuer"]
        system = data["issuer"]
        cobranded = data["cobranded"]
        filename = secure_filename(f"{secrets.token_hex(16)}.png")

        # Determine the path to store the image based on the environment
        image_folder = app.app.config["UPLOAD_FOLDER"] # TODO: Need to change the UPLOAD_FOLDER in different env.
        image_path = os.path.join(image_folder, filename)

        # Save the image file to the appropriate directory
        image_file.save(image_path)

        # Create the credit card record in the database
        credit_card = CreditCard.create(
            name=name,
            issuer=issuer,
            system=system,
            cobranded=cobranded,
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
