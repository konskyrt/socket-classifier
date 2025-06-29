# Power Outlet Classification App

A smart application that uses AI to classify power outlet images and shows similar product recommendations.

## Features

- **AI-Powered Classification**: Upload outlet images and get accurate AI classification results
- **Product Discovery**: View natural installations and product images of similar outlets
- **Detailed Specifications**: Get technical details about identified outlets
- **Modern Web Interface**: Responsive React frontend with Material-UI

## Quick Start

### Backend Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start server: `cd backend && python app.py`
3. Server runs on http://localhost:5000

### Frontend Setup
1. Install dependencies: `cd frontend && npm install`
2. Start development server: `npm start`
3. App runs on http://localhost:3000

## Usage

1. **Upload**: Drag and drop a power outlet image
2. **Classify**: AI identifies the outlet type with confidence score
3. **Discover**: View natural installations and similar product images
4. **Learn**: Get detailed specifications and product information

## Supported Outlet Types

- NEMA 5-15R (US Standard)
- BS 1363 (UK)
- CEE 7/4 (European Schuko)
- USB-A outlets

## Technology Stack

- **Backend**: Python Flask, TensorFlow, OpenCV, SQLite
- **Frontend**: React, Material-UI, Axios
- **Image Processing**: Advanced computer vision for accurate classification

## Project Structure

```
├── backend/           # Flask API server
├── frontend/          # React application
├── requirements.txt   # Python dependencies
└── README.md
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Database**
   ```bash
   cd backend
   python app.py
   ```
   The database will be automatically created with sample data.

3. **Start the Backend Server**
   ```bash
   python app.py
   ```
   The API server will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the Development Server**
   ```bash
   npm start
   ```
   The React app will run on `http://localhost:3000`

## Usage Guide

### Step 1: Upload Image
- Drag and drop or click to select a power outlet image
- Supported formats: PNG, JPG, JPEG, GIF, BMP (max 16MB)
- For best results, use clear, well-lit images taken straight-on

### Step 2: Classification
- The AI model analyzes your image
- View classification results with confidence score
- See detailed product information and specifications

### Step 3: Customization
- **Choose Color**: Select from available color options
- **Select Arrangement**: Single, double, triple, or quad outlet
- **Adjust Specifications**: Set wall thickness (1-5mm) and depth (10-50mm)
- **Add Notes**: Include any special requirements

### Step 4: Generate and Download
- Generate your custom 3D model
- Download the STL file for 3D printing
- Follow included printing tips for best results

## API Endpoints

### Classification
```http
POST /api/classify
Content-Type: multipart/form-data

# Upload image file for classification
```

### 3D Generation
```http
POST /api/generate-3d
Content-Type: application/json

{
  "outlet_type": "NEMA_5-15R",
  "color": "white",
  "arrangement": "single",
  "custom_options": {
    "wall_thickness": 2.0,
    "depth": 20
  }
}
```

### File Download
```http
GET /api/download/{session_id}

# Download generated STL file
```

## 3D Printing Guidelines

### Recommended Settings
- **Filament**: PLA or ABS
- **Layer Height**: 0.2mm
- **Infill**: 20%
- **Print Speed**: 50mm/s
- **Supports**: Use if needed for overhangs

### Post-Processing
- Light sanding for smooth finish
- Check fit before final installation
- Test electrical connections safely

## Development

### Adding New Outlet Types
1. Add outlet specifications to `database.py`
2. Update classification model in `classifier.py`
3. Implement geometry generation in `stl_generator.py`

### Customizing UI
- Modify React components in `frontend/src/components/`
- Update styles in `App.css`
- Add new Material-UI themes as needed

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

## Acknowledgments

- TensorFlow team for the machine learning framework
- Material-UI team for the component library
- OpenCV community for image processing tools
- 3D printing community for STL format standards 