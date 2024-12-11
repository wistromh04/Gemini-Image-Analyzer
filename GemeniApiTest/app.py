import os 
from flask import Flask, render_template, jsonify, request
import google.generativeai as genai
import json
import PIL.Image
import tkinter as tk
from tkinter import filedialog
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Fetch the API key from config.json
api_key = config.get("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in config.json.")

# Passes the API key to the genai library enabling authenticated access to Gemeni services.
genai.configure(api_key=api_key)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == "":
        return jsonify({'error:' 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        image = PIL.Image.open(filepath)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(["Tell me about this image", image])

        return jsonify({'response': response.text})

    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
