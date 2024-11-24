import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton
} from '@mui/material';
import { Delete, Add } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { createGroupChat } from '../store/groupChatSlice';

interface GroupChatConfigProps {
  onConfigComplete: (chatId: number) => void;
}

export const GroupChatConfig: React.FC<GroupChatConfigProps> = ({ onConfigComplete }) => {
  const [name, setName] = useState('');
  const [selectedAgents, setSelectedAgents] = useState<number[]>([]);
  const [maxIterations, setMaxIterations] = useState(10);
  const [initialPrompt, setInitialPrompt] = useState('');
  
  const dispatch = useDispatch();
  const { agents } = useSelector((state: any) => state.agents);
  
  const handleAddAgent = (agentId: number) => {
    if (!selectedAgents.includes(agentId)) {
      setSelectedAgents([...selectedAgents, agentId]);
    }
  };
  
  const handleRemoveAgent = (agentId: number) => {
    setSelectedAgents(selectedAgents.filter(id => id !== agentId));
  };
  
  const handleSubmit = async () => {
    if (!name || selectedAgents.length === 0) return;
    
    const config = {
      name,
      agent_ids: selectedAgents,
      config: {
        max_iterations: maxIterations,
        initial_prompt: initialPrompt
      }
    };
    
    const result = await dispatch(createGroupChat(config));
    if (result.meta.requestStatus === 'fulfilled') {
      onConfigComplete(result.payload.id);
    }
  };
  
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Configure Group Chat
      </Typography>
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          label="Chat Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          fullWidth
        />
        
        <FormControl fullWidth>
          <InputLabel>Add Agent</InputLabel>
          <Select
            value=""
            onChange={(e) => handleAddAgent(e.target.value as number)}
            label="Add Agent"
          >
            {agents
              .filter((agent: any) => !selectedAgents.includes(agent.id))
              .map((agent: any) => (
                <MenuItem key={agent.id} value={agent.id}>
                  {agent.name} ({agent.role})
                </MenuItem>
              ))}
          </Select>
        </FormControl>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {selectedAgents.map(agentId => {
            const agent = agents.find((a: any) => a.id === agentId);
            return (
              <Chip
                key={agentId}
                label={`${agent.name} (${agent.role})`}
                onDelete={() => handleRemoveAgent(agentId)}
              />
            );
          })}
        </Box>
        
        <TextField
          label="Max Iterations"
          type="number"
          value={maxIterations}
          onChange={(e) => setMaxIterations(parseInt(e.target.value))}
          fullWidth
        />
        
        <TextField
          label="Initial Prompt"
          value={initialPrompt}
          onChange={(e) => setInitialPrompt(e.target.value)}
          fullWidth
          multiline
          rows={4}
        />
        
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={!name || selectedAgents.length === 0}
        >
          Create Group Chat
        </Button>
      </Box>
    </Paper>
  );
}; 