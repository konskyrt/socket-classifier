from flask import Flask, request, jsonify, send_file, send_from_directory
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

# Get the directory of the current file (backend)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_root = os.path.dirname(current_dir)
# Path to the React build folder
react_build_path = os.path.join(project_root, 'frontend', 'build')

# Debug: Print paths to see what's happening
print(f"Current dir: {current_dir}")
print(f"Project root: {project_root}")
print(f"React build path: {react_build_path}")
print(f"Build path exists: {os.path.exists(react_build_path)}")
if os.path.exists(react_build_path):
    print(f"Build contents: {os.listdir(react_build_path)}")

# Create Flask app with proper static configuration
app = Flask(__name__, 
            static_folder=react_build_path,
            static_url_path='')
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

# API Routes (must come before catch-all route)
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

# Serve static files explicitly
@app.route('/static/<path:filename>')
def serve_static(filename):
    static_dir = os.path.join(react_build_path, 'static')
    if os.path.exists(static_dir):
        return send_from_directory(static_dir, filename)
    return send_from_directory(react_build_path, filename)

# Serve React App (catch-all route - must be last)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    # Handle static files (css, js, etc.)
    if path and (path.endswith('.css') or path.endswith('.js') or path.endswith('.map')):
        # Try to serve from static folder first
        static_file_path = os.path.join(react_build_path, 'static', path)
        if os.path.exists(static_file_path):
            return send_file(static_file_path)
        
        # Try to serve from build root
        build_file_path = os.path.join(react_build_path, path)
        if os.path.exists(build_file_path):
            return send_file(build_file_path)
    
    # Handle other static assets
    if path and os.path.exists(os.path.join(react_build_path, path)):
        return send_from_directory(react_build_path, path)
    
    # Default to index.html for SPA routing
    index_path = os.path.join(react_build_path, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    else:
        return jsonify({'error': 'React build not found. Please run the build process.'}), 404

if __name__ == '__main__':
    # Initialize database
    database.initialize()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 