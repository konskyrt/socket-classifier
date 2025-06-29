#!/usr/bin/env python3
"""
Setup script for Power Outlet Classification Application
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} is not compatible")
        print("  Please install Python 3.8 or higher")
        return False

def check_node():
    """Check Node.js installation"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ Node.js {version} is installed")
            return True
        else:
            print("✗ Node.js is not installed")
            return False
    except FileNotFoundError:
        print("✗ Node.js is not installed")
        print("  Please install Node.js from https://nodejs.org/")
        return False

def setup_backend():
    """Setup backend dependencies"""
    print("\nSetting up backend...")
    
    # Install Python requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("\nSetting up frontend...")
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    if not os.path.exists(frontend_dir):
        print("✗ Frontend directory not found")
        return False
    
    os.chdir(frontend_dir)
    
    # Install npm dependencies
    if not run_command("npm install", "Installing Node.js dependencies"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = [
        'backend/uploads',
        'backend/generated',
        'backend/data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    return True

def main():
    """Main setup function"""
    print("Power Outlet Classification App - Setup")
    print("=" * 50)
    
    # Check system requirements
    print("Checking system requirements...")
    if not check_python():
        return False
    
    if not check_node():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Setup backend
    if not setup_backend():
        return False
    
    # Setup frontend
    if not setup_frontend():
        return False
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend server: python start_backend.py")
    print("2. Start the frontend server: start_frontend.bat (Windows) or npm start (in frontend/)")
    print("3. Open http://localhost:3000 in your browser")
    print("4. Test the application: python test_application.py")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        print("\n✗ Setup failed. Please check the errors above.")
        sys.exit(1) 