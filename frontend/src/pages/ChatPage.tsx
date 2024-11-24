import React, { useState } from 'react';
import { Container, Grid, Paper, Typography, Box } from '@mui/material';
import { ChatWindow } from '../components/ChatWindow';
import { AgentCard } from '../components/AgentCard';
import { useSelector } from 'react-redux';

export const ChatPage: React.FC = () => {
  const [selectedAgent, setSelectedAgent] = useState<number | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const { agents } = useSelector((state: any) => state.agents);

  const handleAgentSelect = (agentId: number) => {
    setSelectedAgent(agentId);
    // In a real app, you'd create a new chat session here
    setSessionId(Date.now()); // Temporary solution for demo
  };

  return (
    <Container maxWidth="xl">
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Available Agents
            </Typography>
            {agents.map((agent: any) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onActivate={() => {}}
                onProcess={() => handleAgentSelect(agent.id)}
              />
            ))}
          </Paper>
        </Grid>
        <Grid item xs={12} md={8}>
          {selectedAgent && sessionId ? (
            <ChatWindow
              sessionId={sessionId}
              agentId={selectedAgent}
            />
          ) : (
            <Box
              sx={{
                height: '600px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <Typography variant="h6" color="text.secondary">
                Select an agent to start chatting
              </Typography>
            </Box>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}; 