import requests
import tempfile
import json
import os
from dotenv import load_dotenv

load_dotenv()

tmp_dir = tempfile.gettempdir()
DATABASE_PATH = "/tmp"

def fetch_products():
    url = os.getenv('SWELL_API_URL')

    # Define your custom headers here
    headers = {
        'Authorization': os.getenv('SWELL_AUTHORIZATION_KEY'),  # If you have an API token or authentication
        'Content-Type': 'application/json',  # If needed for the request body
    }

    # Make the HTTP request with custom headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data from the response
        json_data = response.json()

        # Initialize an empty list to store extracted data for each item
        extracted_data_list = []

        # Loop through each item in the array and extract the desired information
        for item in json_data["results"]:
            extracted_data = {
                "id": item.get("id", None),
                "name": item.get("name", None),
                "description": item.get("description", None),
                "price": item.get("price", None),
                "currency": item.get("currency", None),
                "slug": item.get("slug", None),
                "image": item.get("images", [])[0].get("file", {}).get("url", None)
            }
            extracted_data_list.append(extracted_data)    
        
        # Writing the extracted data into the data.json file in DATABASE_PATH
        data_file_path = os.path.join(DATABASE_PATH, 'data.json')
        with open(data_file_path, 'w') as data_file:
            json.dump(extracted_data_list, data_file, indent=4)
       
    else:
        print(f"Request failed with status code: {response.status_code}")