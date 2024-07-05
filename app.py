from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for
import requests
from werkzeug.utils import secure_filename


## Create flask app
app = Flask(__name__) 

## App configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


## Functions
## Checks filename and type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

## Run inference on HuggingFace
API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

def query(filename):
    file_path = app.config['UPLOAD_FOLDER'] + '/' + filename
    with open(file_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    ## TODO: Handle errors from HuggingFace
    return response.json() ## Reponse should be image labels and scores


## Get nutrition info from FatSecret
def query_fs(food_label):

    return

## Routes
## Photo upload
@app.route('/')
def upload():
    return render_template('upload.html')

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
    
## Serve uploaded photo
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    output = query(filename)
    ## TODO: For each label, get nutrition info
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename), \
        jsonify({'message': 'File successfully uploaded', 'output': output}), 200



if __name__ == '__main__':
    app.run(debug=True)