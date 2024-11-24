import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Alert,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip
} from '@mui/material';
import { Add, Edit, Delete, Check, Close } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchModelProviders,
  createModelProvider,
  updateModelProvider,
  deleteModelProvider
} from '../store/modelProviderSlice';

export const SettingsPage: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<any>(null);
  const [formData, setFormData] = useState({
    name: '',
    base_url: '',
    api_key: '',
    config: '{}'
  });
  const [predefinedProviders, setPredefinedProviders] = useState<any>({});
  
  const dispatch = useDispatch();
  const { providers, loading, error } = useSelector((state: any) => state.modelProviders);
  
  useEffect(() => {
    dispatch(fetchModelProviders());
    fetchPredefinedProviders();
  }, [dispatch]);
  
  const fetchPredefinedProviders = async () => {
    const response = await fetch('/api/v1/model-providers/predefined');
    const data = await response.json();
    setPredefinedProviders(data);
  };
  
  const handleAddProvider = () => {
    setSelectedProvider(null);
    setFormData({
      name: '',
      base_url: '',
      api_key: '',
      config: '{}'
    });
    setOpenDialog(true);
  };
  
  const handleEditProvider = (provider: any) => {
    setSelectedProvider(provider);
    setFormData({
      name: provider.name,
      base_url: provider.base_url || '',
      api_key: provider.api_key,
      config: JSON.stringify(provider.config, null, 2)
    });
    setOpenDialog(true);
  };
  
  const handleSubmit = async () => {
    try {
      if (selectedProvider) {
        await dispatch(updateModelProvider({
          id: selectedProvider.id,
          ...formData,
          config: JSON.parse(formData.config)
        }));
      } else {
        await dispatch(createModelProvider({
          ...formData,
          config: JSON.parse(formData.config)
        }));
      }
      setOpenDialog(false);
    } catch (error) {
      console.error('Failed to save provider:', error);
    }
  };
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" gutterBottom>
          Settings
        </Typography>
        
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">AI Model Providers</Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={handleAddProvider}
            >
              Add Provider
            </Button>
          </Box>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          
          <List>
            {providers.map((provider: any) => (
              <ListItem key={provider.id}>
                <ListItemText
                  primary={provider.name}
                  secondary={`Models: ${provider.models?.length || 0}`}
                />
                <Chip
                  label={provider.is_active ? 'Active' : 'Inactive'}
                  color={provider.is_active ? 'success' : 'default'}
                  size="small"
                  sx={{ mr: 1 }}
                />
                <ListItemSecondaryAction>
                  <IconButton onClick={() => handleEditProvider(provider)}>
                    <Edit />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
      
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedProvider ? 'Edit Provider' : 'Add Provider'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            {!selectedProvider && (
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Predefined Provider</InputLabel>
                <Select
                  value=""
                  onChange={(e) => {
                    const provider = predefinedProviders[e.target.value];
                    if (provider) {
                      setFormData({
                        name: provider.name,
                        base_url: provider.base_url,
                        api_key: '',
                        config: '{}'
                      });
                    }
                  }}
                >
                  {Object.entries(predefinedProviders).map(([key, provider]: [string, any]) => (
                    <MenuItem key={key} value={key}>
                      {provider.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
            
            <TextField
              fullWidth
              label="Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Base URL"
              value={formData.base_url}
              onChange={(e) => setFormData({ ...formData, base_url: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={formData.api_key}
              onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Additional Configuration (JSON)"
              multiline
              rows={4}
              value={formData.config}
              onChange={(e) => setFormData({ ...formData, config: e.target.value })}
              error={!isValidJson(formData.config)}
              helperText={!isValidJson(formData.config) ? 'Invalid JSON' : ''}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={!isValidJson(formData.config)}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

const isValidJson = (str: string) => {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}; 