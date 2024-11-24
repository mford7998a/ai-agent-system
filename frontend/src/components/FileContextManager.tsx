import React, { useState, useEffect, useCallback } from 'react';
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
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import { Delete, Edit, Upload, Visibility, Download } from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { useDispatch, useSelector } from 'react-redux';
import {
  uploadFileContext,
  createFileContext,
  updateFileContext,
  deleteFileContext,
  fetchFileContexts
} from '../store/fileContextSlice';

export const FileContextManager: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [editingContext, setEditingContext] = useState<any>(null);
  const [formData, setFormData] = useState({
    name: '',
    content: '',
    metadata: '{}'
  });
  const [previewContent, setPreviewContent] = useState<string | null>(null);

  const dispatch = useDispatch();
  const { contexts, loading, error } = useSelector((state: any) => state.fileContext);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      const reader = new FileReader();
      reader.onload = async () => {
        const content = reader.result as string;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', file.name);
        formData.append('metadata', JSON.stringify({
          type: file.type,
          size: file.size,
          lastModified: file.lastModified
        }));
        
        await dispatch(uploadFileContext(formData));
      };
      reader.readAsText(file);
    }
  }, [dispatch]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true
  });

  useEffect(() => {
    dispatch(fetchFileContexts());
  }, [dispatch]);

  const handleOpenDialog = (context?: any) => {
    if (context) {
      setEditingContext(context);
      setFormData({
        name: context.name,
        content: context.content,
        metadata: JSON.stringify(context.metadata, null, 2)
      });
    } else {
      setEditingContext(null);
      setFormData({
        name: '',
        content: '',
        metadata: '{}'
      });
    }
    setOpenDialog(true);
  };

  const handlePreview = async (context: any) => {
    setPreviewContent(context.content);
  };

  const handleDownload = (context: any) => {
    const blob = new Blob([context.content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = context.name;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <Box>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          File Context Management
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box
          {...getRootProps()}
          sx={{
            p: 3,
            border: '2px dashed',
            borderColor: isDragActive ? 'primary.main' : 'grey.300',
            borderRadius: 1,
            mb: 2,
            textAlign: 'center',
            cursor: 'pointer'
          }}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <Typography>Drop files here...</Typography>
          ) : (
            <Typography>
              Drag and drop files here, or click to select files
            </Typography>
          )}
        </Box>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
            <CircularProgress />
          </Box>
        ) : (
          <List>
            {contexts.map((context: any) => (
              <ListItem key={context.id}>
                <ListItemText
                  primary={context.name}
                  secondary={
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Size: {context.metadata?.size || 'N/A'} bytes
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Type: {context.metadata?.type || 'N/A'}
                      </Typography>
                    </Box>
                  }
                />
                <ListItemSecondaryAction>
                  <IconButton onClick={() => handlePreview(context)}>
                    <Visibility />
                  </IconButton>
                  <IconButton onClick={() => handleDownload(context)}>
                    <Download />
                  </IconButton>
                  <IconButton onClick={() => handleOpenDialog(context)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => dispatch(deleteFileContext(context.id))}>
                    <Delete />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
      </Paper>

      <Dialog
        open={Boolean(previewContent)}
        onClose={() => setPreviewContent(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>File Preview</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={20}
            value={previewContent || ''}
            InputProps={{ readOnly: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewContent(null)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}; 