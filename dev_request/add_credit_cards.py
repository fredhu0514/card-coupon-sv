import json
import requests

# Replace this with the URL of your Flask server
BASE_URL = 'http://127.0.0.1:5000'

def add_card(card):
    headers = {
        'User-Agent': 'My Python Script',
    }
    # Send a POST request to the API to add the credit card
    url = f"{BASE_URL}/api/credit_card/create_credit_card"
    files = {'image': open(f"./images/{card['image_path']}.png", 'rb')}
    data = {
        'name': card['name'], 
        'issuer': card['issuer'],
        'system': card['system'],
        'cobranded': card['cobranded']
    }
    response = requests.post(url, files=files, data=data, headers=headers)

    try:
        response.raise_for_status()  # Check if the request was successful (status code 200-299)
        print(f"Credit {card['name']} card added successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(response.text)  # Print the raw response content
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return response.json()["addCreditCardResponse"]["id"]

def add_card_input():
    card_json_file_name = input("JSON file name ?.json\n\t")
    with open(f"./data/{card_json_file_name}.json", "r") as f:
        card_list = json.load(f)
        for card in card_list:
            add_card(card)

if __name__ == '__main__':
    add_card_input()
