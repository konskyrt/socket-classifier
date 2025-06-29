from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sqlite3
import io
import json
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from utils.classifier import ElectricalSocketClassifier
from utils.database import Database
import uuid
import time

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Initialize components
classifier = ElectricalSocketClassifier()
database = Database()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return '''
    <html>
    <head>
        <title>Electrical Socket Classifier API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { color: #007bff; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🔌 Electrical Socket Classifier API</h1>
        <p>AI-powered socket type classification and product information system.</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/health</code><br>
            <small>Check API health status</small>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/api/outlet-types</code><br>
            <small>List all supported socket types</small>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/classify</code><br>
            <small>Upload socket image for AI classification (multipart/form-data with 'image' field)</small>
        </div>
        
        <h2>Supported Socket Types:</h2>
        <ul>
            <li>NEMA 5-15R (US Standard)</li>
            <li>BS 1363 (UK)</li>
            <li>CEE 7/4 (European Schuko)</li>
            <li>AS 3112 (Australian)</li>
            <li>JIS C 8303 (Japanese)</li>
            <li>GFCI (US Safety)</li>
            <li>USB-A & USB-C</li>
        </ul>
        
        <p><strong>Ready to classify electrical socket images!</strong></p>
    </body>
    </html>
    '''

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/classify', methods=['POST'])
def classify_outlet():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Simulate processing time for "We are recognizing your power outlet" message
        time.sleep(2)
        
        # Classify the image
        classification_result = classifier.predict(filepath)
        
        # Get product information from database
        product_info = database.get_product_by_type(classification_result['outlet_type'])
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'classification': classification_result,
            'product': product_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/outlet-types', methods=['GET'])
def get_outlet_types():
    try:
        outlet_types = database.get_all_outlet_types()
        return jsonify({'outlet_types': outlet_types})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database
    database.initialize()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 