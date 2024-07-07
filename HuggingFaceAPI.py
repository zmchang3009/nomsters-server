import os
import requests


auth_token = 'placeholder'

API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
headers = {"Authorization": "Bearer "+auth_token}

def query(image):
    response = requests.post(API_URL, headers=headers, data=image)
    return response.json()

def fetch_labels(image):
    return query(image=image)
