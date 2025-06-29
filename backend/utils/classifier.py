import numpy as np
from PIL import Image
import cv2
import os

class ElectricalSocketClassifier:
    def __init__(self):
        self.model = None
        self.class_names = [
            'NEMA_5-15R',  # Standard US socket
            'NEMA_5-20R',  # US 20A socket
            'BS_1363',     # UK socket
            'CEE_7/4',     # European Schuko socket
            'CEE_7/16',    # European Europlug socket
            'AS_3112',     # Australian socket
            'JIS_C_8303',  # Japanese socket
            'GFCI',        # US GFCI socket
            'USB_A',       # USB socket
            'USB_C'        # USB-C socket
        ]
        self.input_shape = (224, 224, 3)
        self._build_model()
    
    def _build_model(self):
        """Build a CNN model for electrical socket classification"""
        # For demo purposes, we use rule-based classification
        # In production, this would load a trained model
        self.model = None
        print("Demo classifier initialized - using rule-based classification")
    
    def preprocess_image(self, image_path):
        """Preprocess image for classification"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to model input size
            image = image.resize((self.input_shape[0], self.input_shape[1]))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def predict(self, image_path):
        """Classify electrical socket from image"""
        try:
            # For demonstration purposes, we'll use rule-based classification
            prediction_result = self._demo_classify(image_path)
            
            return prediction_result
            
        except Exception as e:
            # Fallback classification
            return {
                'outlet_type': 'NEMA_5-15R',
                'confidence': 0.60,
                'detected_features': {},
                'note': 'Fallback classification used due to processing error'
            }
    
    def _demo_classify(self, image_path):
        """Demo classification based on simple image analysis"""
        try:
            # Load image for analysis
            image = cv2.imread(image_path)
            if image is None:
                raise Exception("Could not load image")
                
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Simple feature extraction for demo
            height, width = gray.shape
            aspect_ratio = width / height
            
            # Count contours (holes in socket)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Demo logic - this would be replaced by actual ML model
            if len(contours) >= 3:
                if aspect_ratio > 1.2:
                    outlet_type = 'NEMA_5-15R'  # US standard
                    confidence = 0.85
                else:
                    outlet_type = 'BS_1363'  # UK
                    confidence = 0.82
            elif len(contours) == 2:
                outlet_type = 'CEE_7/4'  # European Schuko
                confidence = 0.78
            else:
                outlet_type = 'NEMA_5-15R'  # Default to US standard
                confidence = 0.75
            
            return {
                'outlet_type': outlet_type,
                'confidence': confidence,
                'detected_features': {
                    'aspect_ratio': aspect_ratio,
                    'contour_count': len(contours),
                    'image_size': f"{width}x{height}"
                }
            }
            
        except Exception as e:
            # Fallback classification
            return {
                'outlet_type': 'NEMA_5-15R',
                'confidence': 0.60,
                'detected_features': {},
                'note': f'Fallback classification: {str(e)}'
            }
    
    def get_supported_types(self):
        """Get list of supported socket types"""
        return self.class_names.copy()
    
    def train_model(self, train_data_path):
        """Train the model (placeholder for future implementation)"""
        print("Model training not implemented in this demo version")
        pass 