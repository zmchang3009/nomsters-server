import requests
import json  # Import json module for dumping dict to json string
from dishes_list import dishes


FATS_URL = 'http://127.0.0.1:5000/fats'
HUG_URL = 'http://127.0.0.1:5000/hug'
INFER_URL = 'http://127.0.0.1:5000/infer'

def fat_query():
    dishes
    data = {'labels': ['chicken rice', 'soup', 'tacos']}
    headers = {'Content-Type': 'application/json'}  # Specify content type as JSON
    response = requests.post(FATS_URL, data=json.dumps(data), headers=headers)  # Convert data to JSON string
    return response.text

def hug_query(image_data):
    headers = {'Content-Type': 'application/json'}  # Specify content type as image/jpeg
    response = requests.post(HUG_URL, data=image_data, headers=headers)  # Send image data in the request body
    return response.text

def combined_query(image_data):
    headers = {'Content-Type': 'application/json'}  # Specify content type as image/jpeg
    response = requests.post(INFER_URL, data=image_data, headers=headers)  # Send image data in the request body
    return response.text
    
data = None
with open('static/ramen.jpg', "rb") as f:
        data = f.read()
with open('uploads/formal.jpg', "rb") as f:
        data = f.read()
print(combined_query(data))
# print(fat_query())
