import React, { useState } from 'react';
import {
  Button,
  TextField,
  Checkbox,
  FormControlLabel,
  Alert,
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  Grid,
  IconButton,
  Chip
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SendIcon from '@mui/icons-material/Send';

const UserForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    agree: false
  });
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [tags, setTags] = useState(['user', 'new']);

  const handleChange = (event) => {
    const { name, value, checked } = event.target;
    setFormData({
      ...formData,
      [name]: name === 'agree' ? checked : value
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    
    // Simple validation
    const newErrors = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.agree) newErrors.agree = 'You must agree to terms';
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      setSubmitted(true);
      console.log('Form submitted:', formData);
    }
  };

  const handleDeleteTag = (tagToDelete) => {
    setTags(tags.filter(tag => tag !== tagToDelete));
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom>
            User Registration Form
          </Typography>
          
          {submitted && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Registration successful!
            </Alert>
          )}
          
          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  error={!!errors.name}
                  helperText={errors.name}
                  required
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  error={!!errors.email}
                  helperText={errors.email}
                  required
                />
              </Grid>
              
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                  {tags.map((tag) => (
                    <Chip
                      key={tag}
                      label={tag}
                      onDelete={() => handleDeleteTag(tag)}
                      color="primary"
                      size="small"
                    />
                  ))}
                  <IconButton size="small" color="primary">
                    <AddIcon />
                  </IconButton>
                </Box>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={formData.agree}
                      onChange={handleChange}
                      name="agree"
                      color="primary"
                    />
                  }
                  label="I agree to the terms and conditions"
                />
                {errors.agree && (
                  <Typography variant="caption" color="error">
                    {errors.agree}
                  </Typography>
                )}
              </Grid>
            </Grid>
          </form>
        </CardContent>
        
        <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
          <Button
            variant="text"
            color="secondary"
            startIcon={<DeleteIcon />}
            onClick={() => setFormData({ name: '', email: '', agree: false })}
          >
            Clear
          </Button>
          <Button
            variant="contained"
            color="primary"
            endIcon={<SendIcon />}
            onClick={handleSubmit}
            disabled={!formData.agree}
          >
            Submit
          </Button>
        </CardActions>
      </Card>
    </Box>
  );
};

export default UserForm;
