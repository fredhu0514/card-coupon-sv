import json
import requests
from datetime import datetime

# Replace this with the URL of your Flask server
BASE_URL = 'http://127.0.0.1:5000'

def get_coupons():
    headers = {
        'User-Agent': 'My Python Script',
    }

    # Send a POST request to the API to add the coupon
    url = f"{BASE_URL}/api/coupon/get_available_coupons_with_constraints"
    data = {
            "card_id": 1,
            "datetime": datetime.now(), # TODO: make a persistent date
            "category": 1,
            "payment": 0,
            "merchant": 0,
        }
    response = requests.get(url, data=data, headers=headers)

    try:
        response.raise_for_status()  # Check if the request was successful (status code 200-299)
        print(f"{response.json()['getAvailableCouponsWithConstraintsResponse']}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(response.text)  # Print the raw response content
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

if __name__ == '__main__':
    get_coupons()
