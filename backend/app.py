from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sqlite3
import io
import json
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import tensorflow as tf
from utils.classifier import ElectricalSocketClassifier
from utils.database import Database
from utils.stl_generator import STLGenerator
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
stl_generator = STLGenerator()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/api/generate-3d', methods=['POST'])
def generate_3d_model():
    try:
        data = request.get_json()
        
        outlet_type = data.get('outlet_type')
        color = data.get('color', 'white')
        arrangement = data.get('arrangement', 'single')
        custom_options = data.get('custom_options', {})
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Generate STL file
        stl_filename = f"{session_id}_{outlet_type}_{arrangement}_{color}.stl"
        stl_path = os.path.join(app.config['GENERATED_FOLDER'], stl_filename)
        
        # Get product specifications
        product_specs = database.get_product_specs(outlet_type)
        
        # Generate 3D model
        stl_generator.generate_outlet_stl(
            product_specs, 
            arrangement, 
            custom_options, 
            stl_path
        )
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': stl_filename,
            'download_url': f'/api/download/{session_id}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<session_id>', methods=['GET'])
def download_file(session_id):
    try:
        # Find file with session_id
        for filename in os.listdir(app.config['GENERATED_FOLDER']):
            if filename.startswith(session_id):
                filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
                return send_file(filepath, as_attachment=True, download_name=filename)
        
        return jsonify({'error': 'File not found'}), 404
        
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