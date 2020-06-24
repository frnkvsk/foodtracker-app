import requests
import json

# API_KEY is the public key provided by the API source
API_KEY = "DEMO_KEY"
BASE_URL = "https://api.nal.usda.gov/fdc/v1/"

def get_data_api(product):
    
    api_url = f"{BASE_URL}foods/search?api_key={API_KEY}"
    response = requests.get(api_url, {               
                "query": product,
                "dataType": ["Foundation"],
                "pageSize": 100
            })
    
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
