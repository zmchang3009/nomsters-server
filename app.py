from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for
import requests
from werkzeug.utils import secure_filename
from FatSecretAPI import fetch_calorie_data
from HuggingFaceAPI import fetch_labels


## Create flask app
app = Flask(__name__) 

## App configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


## Helper functions
## Checks filename and type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def make_API_call_to_huggingface(image):
    return

def make_API_call_to_fatsecret(labels):
    return fetch_calorie_data(labels)
     

## Handles photo upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = app.config['UPLOAD_FOLDER'] + '/' + filename
        file.save(file_path)
        # return jsonify({'message': 'File successfully uploaded', 'output': output}), 200
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return jsonify({'error': 'File type not allowed'}), 400
    
@app.route('/fats', methods=['POST'])  # Ensure the method is set to accept POST requests
def test_make_API_call_to_fatsecret():
    data = request.get_json()  # Parse JSON data from the request body
    if not data or 'labels' not in data:  # Check if data is parsed and 'labels' key exists
        return jsonify({'error': 'No labels found'}), 400

    res =  fetch_calorie_data(data['labels'])
    print(res)
    return jsonify(res), 200

@app.route('/hug', methods=['POST'])  # Ensure the method is set to accept POST requests
def test_make_API_call_to_hug():
    data = request.data
    if not data: 
        return jsonify({'error': 'No image found'}), 400
    res = fetch_labels(data)
    return jsonify(res), 200

@app.route('/infer', methods=['POST'])  # Ensure the method is set to accept POST requests
def make_combined_requests():
    print('infer called')
    data = request.data
    if not data: 
        return jsonify({'error': 'No image found'}), 400
    print('fetching labels...\n')
    labelsResponse = fetch_labels(data)
    print(labelsResponse)
    labels = labelsResponse
    label_array = []
    for label in labels:
        if 'label' in label:
            label_array.append(label['label'])
    print('fetching calorie data...\n')
    res = fetch_calorie_data(label_array)
    for i in range(len(res)):
        if res[i] is not None and 'food_name' in res[i]:
            labels[i]['label'] = res[i]['food_name']
            labels[i]['calories'] = res[i]['calorie_count']
            labels[i]['portion_size'] = res[i]['portion_size']
    return jsonify(labels), 200