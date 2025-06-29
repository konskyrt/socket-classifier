#!/usr/bin/env python3
"""
Startup script for the Power Outlet Classification Backend
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import tensorflow
        import cv2
        import numpy
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_server():
    """Start the Flask backend server"""
    print("Starting Power Outlet Classification Backend...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Start the Flask app
    os.system('python app.py')

if __name__ == "__main__":
    print("Power Outlet Classification and 3D Generation App")
    print("Backend Server Startup")
    print("=" * 50)
    
    if check_requirements():
        start_server()
    else:
        sys.exit(1) 