from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for
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

## Routes
# Route to handle POST requests for calorie data tests
@app.route('/fats', methods=['POST'])  
def test_make_API_call_to_fatsecret():
    # Parse JSON data from the request body
    data = request.get_json()
    # Validate the presence of 'labels' key in the data
    if not data or 'labels' not in data:
        # Return error response if validation fails
        return jsonify({'error': 'No labels found'}), 400

    # Fetch calorie data based on labels provided in the request
    res = fetch_calorie_data(data['labels'])
    print(res)  # Debug print the response from fetch_calorie_data
    # Return the fetched calorie data as JSON response
    return jsonify(res), 200


# Route to handle POST requests for image processing tests
@app.route('/hug', methods=['POST'])  
def test_make_API_call_to_hug():
    # Access the raw data from the request
    data = request.data
    # Check if data is present
    if not data:
        # Return error response if no data is found
        return jsonify({'error': 'No image found'}), 400
    # Process the image data to fetch labels
    res = fetch_labels(data)
    # Return the fetched labels as JSON response
    return jsonify(res), 200


# Main route to handle POST requests for combined image processing and calorie data fetching
@app.route('/infer', methods=['POST'])  
def make_combined_requests():
    print('infer called')  # Debug print to indicate the 'infer' route was called
    # Access the raw data from the request
    data = request.data
    # Check if data is present
    if not data:
        # Return error response if no data is found
        return jsonify({'error': 'No image found'}), 400
    print('fetching labels...\n')  # Debug print to indicate label fetching process
    # Fetch labels from the image data
    labelsResponse = fetch_labels(data)
    print(labelsResponse)  # Debug print the fetched labels
    labels = labelsResponse
    label_array = []
    # Extract label names from the response for calorie data fetching
    for label in labels:
        if 'label' in label:
            label_array.append(label['label'])
    print('fetching calorie data...\n')  # Debug print to indicate calorie data fetching process
    # Fetch calorie data based on the extracted labels
    res = fetch_calorie_data(label_array)
    # Update the labels with fetched calorie data
    for i in range(len(res)):
        if res[i] is not None and 'food_name' in res[i]:
            labels[i]['label'] = res[i]['food_name']
            labels[i]['calories'] = res[i]['calorie_count']
            labels[i]['portion_size'] = res[i]['portion_size']
    # Return the updated labels as JSON response
    return jsonify(labels), 200