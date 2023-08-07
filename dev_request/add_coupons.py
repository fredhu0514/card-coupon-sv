import json
import requests
from datetime import datetime

# Replace this with the URL of your Flask server
BASE_URL = 'http://127.0.0.1:5000'

def add_coupon(coupon):
    headers = {
        'User-Agent': 'My Python Script',
    }

    # Send a POST request to the API to add the coupon
    url = f"{BASE_URL}/api/coupon/add_coupon"
    data = {
        'rate': coupon['rate'],
        'lower_limit': coupon['lower_limit'],
        'upper_limit': coupon['upper_limit'],
        'start_datetime': coupon['start_datetime'],
        'end_datetime': coupon['end_datetime'],
        'card_id': coupon['card_id'],
        'category': coupon['category'],
        'payment': coupon['payment'],
        'merchant': coupon['merchant'],
    }
    response = requests.post(url, data=data, headers=headers)

    try:
        response.raise_for_status()  # Check if the request was successful (status code 200-299)
        print(f"Coupon added successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(response.text)  # Print the raw response content
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

def parse_date_string(date_str):
    try:
        return datetime.fromisoformat(date_str[:-1])
    except ValueError:
        return date_str
    
def add_testing_coupons():
    coupon_json_file_name = input("JSON file name ?.json\n\t")
    with open(f"./data/{coupon_json_file_name}.json", "r") as f:
        coupon_list = json.load(f, parse_float=lambda val: float('inf') if val == "Infinity" else val)
            
        for coupon in coupon_list:
            coupon["start_datetime"] = parse_date_string(coupon["start_datetime"])
            coupon["end_datetime"] = parse_date_string(coupon["end_datetime"])
            add_coupon(coupon)

if __name__ == '__main__':
    add_testing_coupons()
