import React, { useState, useEffect, useRef } from 'react';
import { 
  Paper, 
  Box, 
  TextField, 
  Button, 
  List, 
  ListItem, 
  Typography,
  CircularProgress
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { sendMessage, fetchMessages } from '../store/chatSlice';

interface ChatWindowProps {
  sessionId: number;
  agentId: number;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ sessionId, agentId }) => {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const dispatch = useDispatch();
  const { messages, loading } = useSelector((state: any) => state.chat);

  useEffect(() => {
    dispatch(fetchMessages(sessionId));
    const interval = setInterval(() => {
      dispatch(fetchMessages(sessionId));
    }, 3000);
    return () => clearInterval(interval);
  }, [sessionId, dispatch]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!message.trim()) return;
    
    await dispatch(sendMessage({
      sessionId,
      agentId,
      content: message,
      messageType: 'user'
    }));
    setMessage('');
  };

  return (
    <Paper sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
        <List>
          {messages.map((msg: any) => (
            <ListItem
              key={msg.id}
              sx={{
                justifyContent: msg.messageType === 'user' ? 'flex-end' : 'flex-start',
                mb: 1
              }}
            >
              <Paper
                sx={{
                  p: 2,
                  backgroundColor: msg.messageType === 'user' ? '#e3f2fd' : '#f5f5f5',
                  maxWidth: '70%'
                }}
              >
                <Typography variant="body1">{msg.content}</Typography>
                <Typography variant="caption" color="text.secondary">
                  {msg.messageType === 'user' ? 'You' : msg.agentName}
                </Typography>
              </Paper>
            </ListItem>
          ))}
        </List>
        <div ref={messagesEndRef} />
      </Box>
      
      <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={loading}
          multiline
          maxRows={4}
        />
        <Box sx={{ mt: 1, display: 'flex', justifyContent: 'flex-end' }}>
          {loading && <CircularProgress size={24} sx={{ mr: 1 }} />}
          <Button
            variant="contained"
            onClick={handleSend}
            disabled={loading || !message.trim()}
          >
            Send
          </Button>
        </Box>
      </Box>
    </Paper>
  );
}; 