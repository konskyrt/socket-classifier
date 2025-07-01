#!/bin/bash

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to frontend directory
echo "Building React application..."
cd frontend

# Clean any existing build
if [ -d "build" ]; then
    echo "Removing existing build directory..."
    rm -rf build
fi

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Build React app
echo "Building React app..."
npm run build

# Verify build was successful
if [ -d "build" ]; then
    echo "React build successful!"
    echo "Build contents:"
    ls -la build/
    if [ -d "build/static" ]; then
        echo "Static folder contents:"
        ls -la build/static/
    fi
else
    echo "ERROR: React build failed - build directory not found!"
    exit 1
fi

# Return to root directory
cd ..

echo "Build process completed successfully!" 