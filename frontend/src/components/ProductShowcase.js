import React from 'react';
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Grid,
  Chip,
  Divider
} from '@mui/material';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import InfoIcon from '@mui/icons-material/Info';

const ProductShowcase = ({ classificationData, onStartOver, compact = false }) => {
  if (!classificationData) return null;

  const product = classificationData.product;
  const classification = classificationData.classification;

  const confidence = classification?.confidence || 0.75;

  return (
    <Box sx={{ height: '100%' }}>
      <Card elevation={2} sx={{ height: '100%' }}>
        <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column', p: 2 }}>
          {/* Classification Info */}
          <Box sx={{ mb: 2, p: 2, bgcolor: 'primary.light', color: 'white', borderRadius: 1 }}>
            <Typography variant="h6">
              {product?.name || 'Electrical Socket'}
            </Typography>
            <Typography variant="body2">
              Confidence: {Math.round(confidence * 100)}%
            </Typography>
          </Box>
          
          <Grid container spacing={2} sx={{ flex: 1, mb: 2 }}>
            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom align="center">
                Similar Products
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Card variant="outlined" sx={{ height: '100%' }}>
                <CardMedia
                  component="img"
                  height="140"
                  image={product?.natural_image_url || 'https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400'}
                  alt="Natural installation"
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ p: 1 }}>
                  <Typography variant="subtitle2">Natural Installation</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Real-world example
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Card variant="outlined" sx={{ height: '100%' }}>
                <CardMedia
                  component="img"
                  height="140"
                  image={product?.product_image_url || 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400'}
                  alt="Product image"
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ p: 1 }}>
                  <Typography variant="subtitle2">Available Product</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {product?.name || 'Professional outlet'}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Product Details */}
          <Box sx={{ mb: 2, p: 2, bgcolor: '#f9f9f9', borderRadius: 1 }}>
            <Typography variant="subtitle2" gutterBottom>Specifications</Typography>
            <Grid container spacing={1}>
              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Voltage</Typography>
                <Typography variant="body2">{product?.voltage || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Current</Typography>
                <Typography variant="body2">{product?.current_rating || 'N/A'}</Typography>
              </Grid>
            </Grid>
          </Box>

          <Box sx={{ textAlign: 'center' }}>
            <Button 
              variant="outlined" 
              onClick={onStartOver}
              startIcon={<RestartAltIcon />}
              size="small"
              sx={{ mr: 1 }}
            >
              Try Another
            </Button>
            <Button 
              variant="contained" 
              startIcon={<ShoppingCartIcon />}
              size="small"
            >
              Find Products
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ProductShowcase; 