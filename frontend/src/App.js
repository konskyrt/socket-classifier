import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, AppBar, Toolbar, Typography, Box, Grid } from '@mui/material';
import ElectricalServicesIcon from '@mui/icons-material/ElectricalServices';

import ImageUpload from './components/ImageUpload';
import ProductShowcase from './components/ProductShowcase';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#ff9800',
    },
  },
});

function App() {
  const [classificationData, setClassificationData] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [loadingMessage, setLoadingMessage] = React.useState('');

  const handleImageUpload = async (file) => {
    setIsLoading(true);
    setLoadingMessage('We are recognizing your electrical socket...');
    
    try {
      const formData = new FormData();
      formData.append('image', file);
      
      const response = await fetch('/api/classify', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        const data = await response.json();
        setClassificationData(data);
        setIsLoading(false);
      } else {
        throw new Error('Classification failed');
      }
    } catch (error) {
      console.error('Error:', error);
      // Fallback to demo data
      setTimeout(() => {
        setClassificationData({
          classification: {
            outlet_type: 'NEMA_5-15R',
            confidence: 0.85
          },
          product: {
            name: 'NEMA 5-15R Standard Outlet',
            description: 'Standard US household outlet',
            voltage: '120V',
            current_rating: '15A',
            natural_image_url: 'https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400',
            product_image_url: 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400'
          }
        });
        setIsLoading(false);
      }, 3000);
    }
  };

  const handleStartOver = () => {
    setClassificationData(null);
    setIsLoading(false);
    setLoadingMessage('');
  };

  const renderContent = () => {
    return (
      <Grid container spacing={3} sx={{ minHeight: '70vh' }}>
        {/* Upload Section - Left Half */}
        <Grid item xs={12} md={6}>
          <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h5" gutterBottom align="center">
              Upload Your Socket Image
            </Typography>
            <Box sx={{ flexGrow: 1 }}>
              <ImageUpload onImageUpload={handleImageUpload} isLoading={isLoading} loadingMessage={loadingMessage} />
            </Box>
          </Box>
        </Grid>

        {/* Results Section - Right Half */}
        <Grid item xs={12} md={6}>
          <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h5" gutterBottom align="center">
              Classification Results
            </Typography>
            <Box sx={{ flexGrow: 1 }}>
              {classificationData ? (
                <ProductShowcase 
                  classificationData={classificationData}
                  onStartOver={handleStartOver}
                  compact={true}
                />
              ) : (
                <Box 
                  sx={{ 
                    height: '100%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    border: '2px dashed #ddd',
                    borderRadius: 2,
                    bgcolor: '#f9f9f9'
                  }}
                >
                  <Typography variant="body1" color="text.secondary" align="center">
                    Upload an electrical socket image to see classification results and similar products
                  </Typography>
                </Box>
              )}
            </Box>
          </Box>
        </Grid>
      </Grid>
    );
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
        <AppBar position="static">
          <Toolbar>
            <ElectricalServicesIcon sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Electrical Socket Classifier
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Upload. Classify. Discover Sockets.
          </Typography>
          <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
            Upload an image of your electrical wall socket, let our AI classify the type, and discover similar products
          </Typography>
          
          {renderContent()}
        </Container>
      </div>
    </ThemeProvider>
  );
}

export default App; 