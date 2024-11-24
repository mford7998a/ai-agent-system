import React from 'react';
import { Card, CardContent, CardActions, Typography, Button, Chip } from '@mui/material';
import { Agent } from '../types/agent';

interface AgentCardProps {
  agent: Agent;
  onActivate: (id: number) => void;
  onProcess: (id: number) => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onActivate, onProcess }) => {
  return (
    <Card sx={{ minWidth: 275, m: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {agent.name}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {agent.role}
        </Typography>
        <Typography variant="body2">
          {agent.description}
        </Typography>
        <Chip 
          label={agent.status} 
          color={agent.status === 'active' ? 'success' : 'default'}
          sx={{ mt: 1 }}
        />
      </CardContent>
      <CardActions>
        <Button 
          size="small" 
          onClick={() => onActivate(agent.id)}
          disabled={agent.status === 'active'}
        >
          Activate
        </Button>
        <Button 
          size="small" 
          onClick={() => onProcess(agent.id)}
          disabled={agent.status !== 'active'}
        >
          Process
        </Button>
      </CardActions>
    </Card>
  );
}; 