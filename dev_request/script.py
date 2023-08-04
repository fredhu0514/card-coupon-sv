import os
import requests

# Replace this with the URL of your Flask server
BASE_URL = 'http://127.0.0.1:5000'

def add_card(card_name, bank_name, image_name):
    headers = {
        'User-Agent': 'My Python Script',
    }
    # Send a POST request to the API to add the credit card
    url = f"{BASE_URL}/api/credit_card/create_credit_card"
    files = {'image': open(f"./images/{image_name}.png", 'rb')}
    data = {
        'card_name': card_name, 
        'bank_name': bank_name
    }
    response = requests.post(url, files=files, data=data, headers=headers)

    try:
        response.raise_for_status()  # Check if the request was successful (status code 200-299)
        print(f"Credit {card_name} card added successfully!")
        # print(response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(response.text)  # Print the raw response content
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return response.json()["addCreditCardResponse"]["id"]

def add_card_input():
    card_name = input("Input card:\n")
    bank_name = input("Input bank:\n")
    image_path = input("Input image name:\n")
    add_card(card_name, bank_name, image_path)

if __name__ == '__main__':
    add_card_input()
