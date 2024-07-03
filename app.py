import os
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for, send_from_directory
import json
from werkzeug.utils import secure_filename

## Data for flask app
with open('data.json', 'r') as file:
    data = json.load(file)


## Create flask app
app = Flask(__name__) 

## App configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


## Routes
## Returns data by default
@app.route('/', methods = ['GET']) 
def home(): 
    if request.method == 'GET': 
        return jsonify(data)

## Form
@app.route('/form') 
def form(): 
    return render_template('form.html')

## Returns relevant data according to form submission
@app.route('/submit', methods = ['GET', 'POST']) 
def submit(): 
    food_name = request.form['food_name']
    for food_obj in data:
        if food_obj['food_name'] == food_name:
            return food_obj
    return f'No result found for {food_name}!'

## Returns relevant data according to route
@app.route('/food/<food_name>', methods = ['GET']) 
def food(food_name): 
    for food_obj in data:
        if food_obj['food_name'] == food_name:
            return food_obj
    return f'No result found for {food_name}!'

## Photo upload
@app.route('/pics')
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
        # return jsonify({'message': 'File successfully uploaded', 'filename': filename}), 200
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return jsonify({'error': 'File type not allowed'}), 400
    
## Serve uploaded photo
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)