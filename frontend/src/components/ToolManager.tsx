import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import { Edit, Delete, Add } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchTools, 
  createTool, 
  updateTool, 
  deleteTool 
} from '../store/toolSlice';

interface Tool {
  id: number;
  name: string;
  description: string;
  tool_type: string;
  config: Record<string, any>;
}

export const ToolManager: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [editingTool, setEditingTool] = useState<Tool | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    tool_type: '',
    config: '{}'
  });

  const dispatch = useDispatch();
  const { tools, loading } = useSelector((state: any) => state.tools);

  useEffect(() => {
    dispatch(fetchTools());
  }, [dispatch]);

  const handleOpen = (tool?: Tool) => {
    if (tool) {
      setEditingTool(tool);
      setFormData({
        name: tool.name,
        description: tool.description,
        tool_type: tool.tool_type,
        config: JSON.stringify(tool.config, null, 2)
      });
    } else {
      setEditingTool(null);
      setFormData({
        name: '',
        description: '',
        tool_type: '',
        config: '{}'
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingTool(null);
  };

  const handleSubmit = async () => {
    try {
      const toolData = {
        ...formData,
        config: JSON.parse(formData.config)
      };

      if (editingTool) {
        await dispatch(updateTool({ id: editingTool.id, ...toolData }));
      } else {
        await dispatch(createTool(toolData));
      }
      handleClose();
    } catch (error) {
      console.error('Error saving tool:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this tool?')) {
      await dispatch(deleteTool(id));
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">Tool Management</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Tool
        </Button>
      </Box>

      <Paper>
        <List>
          {tools.map((tool: Tool) => (
            <ListItem key={tool.id}>
              <ListItemText
                primary={tool.name}
                secondary={tool.description}
              />
              <ListItemSecondaryAction>
                <IconButton onClick={() => handleOpen(tool)}>
                  <Edit />
                </IconButton>
                <IconButton onClick={() => handleDelete(tool.id)}>
                  <Delete />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </Paper>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingTool ? 'Edit Tool' : 'Add Tool'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
            />
            <TextField
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              fullWidth
              multiline
              rows={2}
            />
            <FormControl fullWidth>
              <InputLabel>Tool Type</InputLabel>
              <Select
                value={formData.tool_type}
                onChange={(e) => setFormData({ ...formData, tool_type: e.target.value })}
                label="Tool Type"
              >
                <MenuItem value="filesystem">File System</MenuItem>
                <MenuItem value="code_execution">Code Execution</MenuItem>
                <MenuItem value="visual_validation">Visual Validation</MenuItem>
                <MenuItem value="api_interaction">API Interaction</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Configuration (JSON)"
              value={formData.config}
              onChange={(e) => setFormData({ ...formData, config: e.target.value })}
              fullWidth
              multiline
              rows={4}
              error={!isValidJson(formData.config)}
              helperText={!isValidJson(formData.config) ? 'Invalid JSON' : ''}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button 
            onClick={handleSubmit}
            disabled={!isValidJson(formData.config)}
            variant="contained"
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

const isValidJson = (str: string): boolean => {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}; 