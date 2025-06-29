import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Box, 
  Typography, 
  Button, 
  Alert,
  Card,
  CardContent
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ImageIcon from '@mui/icons-material/Image';

const ImageUpload = ({ onImageUpload, isLoading, loadingMessage }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState('');

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError('');
    
    if (rejectedFiles.length > 0) {
      setError('Please upload a valid image file (PNG, JPG, JPEG, GIF, BMP)');
      return;
    }

    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    },
    maxFiles: 1,
    maxSize: 16 * 1024 * 1024 // 16MB
  });

  const handleUpload = () => {
    if (selectedFile && onImageUpload) {
      onImageUpload(selectedFile);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
    setError('');
  };

  if (isLoading) {
    return (
      <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div className="loading-spinner"></div>
        <Typography variant="h6" sx={{ mt: 2 }}>
          {loadingMessage}
        </Typography>
        {preview && (
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <img 
              src={preview} 
              alt="Processing" 
              style={{ 
                maxWidth: '200px', 
                maxHeight: '150px',
                borderRadius: '8px',
                opacity: 0.7
              }} 
            />
          </Box>
        )}
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100%' }}>
      <Card elevation={2} sx={{ height: '100%' }}>
        <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box
            {...getRootProps()}
            className={`upload-area ${isDragActive ? 'dragover' : ''}`}
            sx={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              mb: 2,
              minHeight: 300
            }}
          >
            <input {...getInputProps()} />
            
            {preview ? (
              <Box sx={{ textAlign: 'center' }}>
                <img 
                  src={preview} 
                  alt="Preview" 
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '250px',
                    borderRadius: '8px'
                  }} 
                />
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {selectedFile?.name}
                </Typography>
              </Box>
            ) : (
              <Box sx={{ textAlign: 'center' }}>
                <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  {isDragActive ? 'Drop the socket image here' : 'Drag & drop a socket image here'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  or click to select a file
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Supports PNG, JPG, JPEG, GIF, BMP (max 16MB)
                </Typography>
              </Box>
            )}
          </Box>

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', mb: 2 }}>
            {selectedFile && (
              <>
                <Button 
                  variant="outlined" 
                  onClick={handleClear}
                >
                  Clear
                </Button>
                <Button 
                  variant="contained" 
                  onClick={handleUpload}
                  startIcon={<ImageIcon />}
                >
                  Classify Socket
                </Button>
              </>
            )}
          </Box>

          <Typography variant="body2" color="text.secondary" align="center">
            💡 <strong>Tip:</strong> Use clear, well-lit images of wall sockets taken straight-on
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ImageUpload; 