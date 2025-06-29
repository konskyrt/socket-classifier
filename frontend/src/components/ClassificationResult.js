import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Chip,
  Grid,
  Divider
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import BuildIcon from '@mui/icons-material/Build';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

const ClassificationResult = ({ data, onViewProducts, onStartOver }) => {
  if (!data) return null;

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <CheckCircleIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Classification Complete!
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              We've identified your power outlet
            </Typography>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card variant="outlined" className="classification-card">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Outlet Type
                  </Typography>
                  <Typography variant="h4" color="primary" gutterBottom>
                    {data.classification?.outlet_type || data.outlet_type}
                  </Typography>
                  
                  <Box sx={{ mt: 2, mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Confidence Level
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={(data.classification?.confidence || data.confidence || 0.75) * 100}
                        color={getConfidenceColor(data.classification?.confidence || data.confidence || 0.75)}
                        sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                      />
                      <Typography variant="body2" sx={{ minWidth: 35 }}>
                        {Math.round((data.classification?.confidence || data.confidence || 0.75) * 100)}%
                      </Typography>
                    </Box>
                    <Chip 
                      label={getConfidenceText(data.classification?.confidence || data.confidence || 0.75)}
                      color={getConfidenceColor(data.classification?.confidence || data.confidence || 0.75)}
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card variant="outlined" className="classification-card">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Product Information
                  </Typography>
                  
                  <Typography variant="subtitle1" gutterBottom>
                    {data.product.name}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {data.product.description}
                  </Typography>

                  <Divider sx={{ my: 2 }} />
                  
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    <Chip label={`${data.product.voltage}`} variant="outlined" size="small" />
                    <Chip label={`${data.product.current_rating}`} variant="outlined" size="small" />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              What's Next?
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              View similar outlet products including natural installations and product options
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', mt: 4 }}>
            <Button 
              variant="outlined" 
              onClick={onStartOver}
              startIcon={<RestartAltIcon />}
            >
              Start Over
            </Button>
            <Button 
              variant="contained" 
              onClick={onViewProducts}
              startIcon={<BuildIcon />}
              size="large"
            >
              View Similar Products
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ClassificationResult; 