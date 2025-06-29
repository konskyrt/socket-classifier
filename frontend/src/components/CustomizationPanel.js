import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  FormControl,
  FormLabel,
  RadioGroup,
  Radio,
  FormControlLabel,
  Slider,
  TextField,
  Divider
} from '@mui/material';
import PaletteIcon from '@mui/icons-material/Palette';
import ViewModuleIcon from '@mui/icons-material/ViewModule';
import PrintIcon from '@mui/icons-material/Print';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const CustomizationPanel = ({ classificationData, onCustomize, onBack }) => {
  const [selectedColor, setSelectedColor] = useState('white');
  const [selectedArrangement, setSelectedArrangement] = useState('single');
  const [wallThickness, setWallThickness] = useState(2.0);
  const [depth, setDepth] = useState(20);
  const [customNotes, setCustomNotes] = useState('');

  const colorOptions = [
    { name: 'white', hex: '#FFFFFF', border: '#DDDDDD' },
    { name: 'black', hex: '#000000', border: '#000000' },
    { name: 'gray', hex: '#808080', border: '#808080' },
    { name: 'beige', hex: '#F5F5DC', border: '#D3D3D3' },
    { name: 'ivory', hex: '#FFFFF0', border: '#DDDDDD' }
  ];

  const arrangementOptions = [
    { 
      name: 'single', 
      label: 'Single Outlet',
      description: 'One outlet',
      icon: '⚡' 
    },
    { 
      name: 'double', 
      label: 'Double Outlet',
      description: 'Two outlets side by side',
      icon: '⚡⚡' 
    },
    { 
      name: 'triple', 
      label: 'Triple Outlet',
      description: 'Three outlets in a row',
      icon: '⚡⚡⚡' 
    },
    { 
      name: 'quad', 
      label: 'Quad Outlet',
      description: 'Four outlets in a grid',
      icon: '⚡⚡\n⚡⚡' 
    }
  ];

  const handleGenerate = () => {
    const customizationData = {
      color: selectedColor,
      arrangement: selectedArrangement,
      custom_options: {
        wall_thickness: wallThickness,
        depth: depth,
        notes: customNotes
      },
      outlet_type: classificationData.outlet_type
    };

    onCustomize(customizationData);
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', p: 2 }}>
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <PaletteIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Customize Your Power Outlet
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Choose colors, arrangements, and specifications for your 3D model
            </Typography>
          </Box>

          <Grid container spacing={4}>
            {/* Color Selection */}
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <PaletteIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Color Selection
                  </Typography>
                  
                  <Box className="color-picker" sx={{ justifyContent: 'flex-start', flexWrap: 'wrap' }}>
                    {colorOptions.map((color) => (
                      <Box
                        key={color.name}
                        className={`color-option ${selectedColor === color.name ? 'selected' : ''}`}
                        onClick={() => setSelectedColor(color.name)}
                        sx={{
                          backgroundColor: color.hex,
                          borderColor: color.border,
                          position: 'relative',
                          cursor: 'pointer'
                        }}
                        title={color.name}
                      />
                    ))}
                  </Box>
                  
                  <Typography variant="body2" sx={{ mt: 2, textAlign: 'center' }}>
                    Selected: <strong>{selectedColor}</strong>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Arrangement Selection */}
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <ViewModuleIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Outlet Arrangement
                  </Typography>
                  
                  <FormControl component="fieldset">
                    <RadioGroup
                      value={selectedArrangement}
                      onChange={(e) => setSelectedArrangement(e.target.value)}
                    >
                      {arrangementOptions.map((option) => (
                        <FormControlLabel
                          key={option.name}
                          value={option.name}
                          control={<Radio />}
                          label={
                            <Box>
                              <Typography variant="subtitle2">
                                {option.icon} {option.label}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {option.description}
                              </Typography>
                            </Box>
                          }
                        />
                      ))}
                    </RadioGroup>
                  </FormControl>
                </CardContent>
              </Card>
            </Grid>

            {/* Technical Specifications */}
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Technical Specifications
                  </Typography>
                  
                  <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                      <Typography variant="subtitle2" gutterBottom>
                        Wall Thickness (mm)
                      </Typography>
                      <Slider
                        value={wallThickness}
                        onChange={(e, newValue) => setWallThickness(newValue)}
                        min={1}
                        max={5}
                        step={0.1}
                        valueLabelDisplay="auto"
                        marks={[
                          { value: 1, label: '1mm' },
                          { value: 2, label: '2mm' },
                          { value: 3, label: '3mm' },
                          { value: 4, label: '4mm' },
                          { value: 5, label: '5mm' }
                        ]}
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <Typography variant="subtitle2" gutterBottom>
                        Depth (mm)
                      </Typography>
                      <Slider
                        value={depth}
                        onChange={(e, newValue) => setDepth(newValue)}
                        min={10}
                        max={50}
                        step={1}
                        valueLabelDisplay="auto"
                        marks={[
                          { value: 10, label: '10mm' },
                          { value: 20, label: '20mm' },
                          { value: 30, label: '30mm' },
                          { value: 40, label: '40mm' },
                          { value: 50, label: '50mm' }
                        ]}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Custom Notes */}
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Custom Notes (Optional)
                  </Typography>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    value={customNotes}
                    onChange={(e) => setCustomNotes(e.target.value)}
                    placeholder="Add any special requirements or notes for your 3D model..."
                    variant="outlined"
                  />
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* Summary */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Summary
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} sm={3}>
                <Typography variant="subtitle2">Outlet Type</Typography>
                <Typography variant="body2">{classificationData.outlet_type}</Typography>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Typography variant="subtitle2">Color</Typography>
                <Typography variant="body2">{selectedColor}</Typography>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Typography variant="subtitle2">Arrangement</Typography>
                <Typography variant="body2">{selectedArrangement}</Typography>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Typography variant="subtitle2">Specifications</Typography>
                <Typography variant="body2">{wallThickness}mm / {depth}mm</Typography>
              </Grid>
            </Grid>
          </Box>

          {/* Action Buttons */}
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button 
              variant="outlined" 
              onClick={onBack}
              startIcon={<ArrowBackIcon />}
            >
              Back to Results
            </Button>
            <Button 
              variant="contained" 
              onClick={handleGenerate}
              startIcon={<PrintIcon />}
              size="large"
            >
              Generate 3D Model
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CustomizationPanel; 