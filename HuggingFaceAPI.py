import os
import requests
from dotenv import load_dotenv


load_dotenv()
auth_token = os.getenv('HUGGINGFACE_AUTH_TOKEN')

API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
headers = {"Authorization": "Bearer "+auth_token}

def query(image):
    response = requests.post(API_URL, headers=headers, data=image)
    return response.json()

def fetch_labels(image):
    return query(image=image)
