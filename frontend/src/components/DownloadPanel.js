import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Divider,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import PrintIcon from '@mui/icons-material/Print';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import InfoIcon from '@mui/icons-material/Info';
import { saveAs } from 'file-saver';

const DownloadPanel = ({ downloadData, customizationData, onStartOver }) => {
  const handleDownload = () => {
    // Create a simple STL file content for demo
    const demoSTLContent = `solid outlet
facet normal 0.0 0.0 1.0
  outer loop
    vertex 0.0 0.0 0.0
    vertex 1.0 0.0 0.0
    vertex 1.0 1.0 0.0
  endloop
endfacet
endsolid outlet`;

    const blob = new Blob([demoSTLContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = downloadData.filename || 'outlet_model.stl';
    a.click();
    URL.revokeObjectURL(url);
  };

  const formatFileSize = (filename) => {
    // Mock file size calculation
    return "245 KB";
  };

  const printingTips = [
    "Use PLA or ABS filament for best results",
    "Print at 0.2mm layer height for good detail",
    "Use 20% infill for strength and material efficiency",
    "Print with supports if needed for overhangs",
    "Sand lightly after printing for smooth finish"
  ];

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <CheckCircleOutlineIcon sx={{ fontSize: 64, color: 'success.main', mb: 2 }} />
            <Typography variant="h4" gutterBottom color="success.main">
              3D Model Ready!
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Your custom power outlet model has been generated successfully
            </Typography>
          </Box>

          <Alert severity="success" sx={{ mb: 3 }}>
            <strong>Generation Complete!</strong> Your STL file is ready for download and 3D printing.
          </Alert>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    File Information
                  </Typography>
                  <Typography variant="body2">
                    <strong>Filename:</strong> {downloadData.filename}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Format:</strong> STL (Stereolithography)
                  </Typography>
                  <Typography variant="body2">
                    <strong>Generated:</strong> {new Date().toLocaleString()}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Your Customization
                  </Typography>
                  <Typography variant="body2">
                    <strong>Color:</strong> {customizationData?.color || 'White'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Arrangement:</strong> {customizationData?.arrangement || 'Single'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Specifications:</strong> {customizationData?.custom_options?.wall_thickness || 2.0}mm wall, {customizationData?.custom_options?.depth || 20}mm depth
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* 3D Printing Tips */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              <PrintIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              3D Printing Tips
            </Typography>
            
            <Grid container spacing={2}>
              {printingTips.map((tip, index) => (
                <Grid item xs={12} sm={6} key={index}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
                    <Typography variant="body2" color="primary" sx={{ mr: 1, fontWeight: 'bold' }}>
                      {index + 1}.
                    </Typography>
                    <Typography variant="body2">
                      {tip}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Box>

          <Divider sx={{ my: 3 }} />

          {/* Action Buttons */}
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button 
              variant="contained" 
              onClick={handleDownload}
              startIcon={<DownloadIcon />}
              size="large"
              color="success"
            >
              Download STL File
            </Button>
            <Button 
              variant="outlined" 
              onClick={onStartOver}
              startIcon={<RestartAltIcon />}
            >
              Create Another Model
            </Button>
          </Box>

          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Need help with 3D printing? Check our{' '}
              <Button variant="text" size="small">
                printing guide
              </Button>{' '}
              or{' '}
              <Button variant="text" size="small">
                contact support
              </Button>
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DownloadPanel; 