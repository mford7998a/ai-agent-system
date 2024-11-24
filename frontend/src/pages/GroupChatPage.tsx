import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Grid,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress
} from '@mui/material';
import {
  Add,
  PlayArrow,
  Stop,
  Delete,
  Edit,
  Save
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { 
  createGroupChat,
  updateGroupChat,
  deleteGroupChat,
  startGroupChat,
  stopGroupChat
} from '../store/groupChatSlice';

export const GroupChatPage: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedChat, setSelectedChat] = useState<any>(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    system_prompt: '',
    max_iterations: 10,
    agents: []
  });
  
  const dispatch = useDispatch();
  const { 
    groupChats,
    availableAgents,
    loading,
    activeChats
  } = useSelector((state: any) => state.groupChat);
  
  useEffect(() => {
    // Fetch initial data
    dispatch(fetchGroupChats());
    dispatch(fetchAvailableAgents());
  }, [dispatch]);
  
  const handleCreateChat = () => {
    setSelectedChat(null);
    setFormData({
      name: '',
      description: '',
      system_prompt: '',
      max_iterations: 10,
      agents: []
    });
    setOpenDialog(true);
  };
  
  const handleSubmit = async () => {
    if (selectedChat) {
      await dispatch(updateGroupChat({ id: selectedChat.id, ...formData }));
    } else {
      await dispatch(createGroupChat(formData));
    }
    setOpenDialog(false);
  };
  
  const handleStartChat = async (chatId: number) => {
    await dispatch(startGroupChat(chatId));
  };
  
  const handleStopChat = async (chatId: number) => {
    await dispatch(stopGroupChat(chatId));
  };
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" gutterBottom>
          Group Chats
        </Typography>
        
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleCreateChat}
          sx={{ mb: 3 }}
        >
          Create Group Chat
        </Button>
        
        <Grid container spacing={3}>
          {groupChats.map((chat: any) => (
            <Grid item xs={12} key={chat.id}>
              <Paper sx={{ p: 2 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="h6">{chat.name}</Typography>
                  <Box>
                    {activeChats[chat.id] ? (
                      <IconButton
                        color="secondary"
                        onClick={() => handleStopChat(chat.id)}
                      >
                        <Stop />
                      </IconButton>
                    ) : (
                      <IconButton
                        color="primary"
                        onClick={() => handleStartChat(chat.id)}
                      >
                        <PlayArrow />
                      </IconButton>
                    )}
                    <IconButton onClick={() => handleEditChat(chat)}>
                      <Edit />
                    </IconButton>
                    <IconButton onClick={() => handleDeleteChat(chat.id)}>
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>
                
                <Typography color="textSecondary" gutterBottom>
                  {chat.description}
                </Typography>
                
                <Box sx={{ mt: 1 }}>
                  {chat.agents.map((agent: any) => (
                    <Chip
                      key={agent.id}
                      label={agent.name}
                      sx={{ mr: 1, mb: 1 }}
                    />
                  ))}
                </Box>
                
                {activeChats[chat.id] && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Recent Messages
                    </Typography>
                    <List>
                      {chat.messages.slice(-5).map((message: any) => (
                        <ListItem key={message.id}>
                          <ListItemText
                            primary={message.content}
                            secondary={`${message.role}${message.agent_name ? ` - ${message.agent_name}` : ''}`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>
      
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedChat ? 'Edit Group Chat' : 'Create Group Chat'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              multiline
              rows={4}
              label="System Prompt"
              value={formData.system_prompt}
              onChange={(e) => setFormData({ ...formData, system_prompt: e.target.value })}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              type="number"
              label="Max Iterations"
              value={formData.max_iterations}
              onChange={(e) => setFormData({ ...formData, max_iterations: parseInt(e.target.value) })}
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth>
              <InputLabel>Agents</InputLabel>
              <Select
                multiple
                value={formData.agents}
                onChange={(e) => setFormData({ ...formData, agents: e.target.value })}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value: any) => (
                      <Chip key={value} label={availableAgents.find((a: any) => a.id === value)?.name} />
                    ))}
                  </Box>
                )}
              >
                {availableAgents.map((agent: any) => (
                  <MenuItem key={agent.id} value={agent.id}>
                    {agent.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {selectedChat ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}; 