#!/usr/bin/env python3
"""
Test script for Power Outlet Classification Application
"""

import os
import sys
import requests
import json

def test_backend_health():
    """Test if backend server is running"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✓ Backend server is running")
            return True
        else:
            print(f"✗ Backend server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend server is not running")
        print("  Please start the backend server first: python start_backend.py")
        return False
    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        return False

def test_frontend():
    """Test if frontend server is running"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✓ Frontend server is running")
            return True
        else:
            print(f"✗ Frontend server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Frontend server is not running")
        print("  Please start the frontend server: npm start (in frontend directory)")
        return False
    except Exception as e:
        print(f"✗ Error testing frontend: {e}")
        return False

def test_database():
    """Test database functionality"""
    try:
        sys.path.append('backend')
        from utils.database import Database
        
        db = Database()
        outlet_types = db.get_all_outlet_types()
        
        if outlet_types and len(outlet_types) > 0:
            print(f"✓ Database working - found {len(outlet_types)} outlet types")
            return True
        else:
            print("✗ Database has no outlet types")
            return False
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_classifier():
    """Test classifier functionality"""
    try:
        sys.path.append('backend')
        from utils.classifier import ElectricalSocketClassifier
        
        classifier = ElectricalSocketClassifier()
        supported_types = classifier.get_supported_types()
        
        if supported_types and len(supported_types) > 0:
            print(f"✓ Classifier working - supports {len(supported_types)} outlet types")
            return True
        else:
            print("✗ Classifier has no supported types")
            return False
    except Exception as e:
        print(f"✗ Classifier error: {e}")
        return False

def test_image_processing():
    """Test image processing functionality"""
    try:
        import cv2
        import numpy as np
        from PIL import Image
        
        print("✓ Image processing libraries working")
        return True
    except Exception as e:
        print(f"✗ Image processing error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Power Outlet Classification App - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend", test_frontend),
        ("Database", test_database),
        ("Classifier", test_classifier),
        ("STL Generator", test_stl_generator)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Application is ready to use.")
        print("\nNext steps:")
        print("1. Make sure both servers are running")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Upload a power outlet image to test classification")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    run_all_tests() 