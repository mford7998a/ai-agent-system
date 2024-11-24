import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { Agent } from '../types/agent';

interface AgentState {
  agents: Agent[];
  loading: boolean;
  error: string | null;
}

const initialState: AgentState = {
  agents: [],
  loading: false,
  error: null,
};

export const fetchAgents = createAsyncThunk(
  'agents/fetchAgents',
  async () => {
    const response = await fetch('/api/v1/agents');
    return response.json();
  }
);

export const activateAgent = createAsyncThunk(
  'agents/activateAgent',
  async (agentId: number) => {
    const response = await fetch(`/api/v1/agents/${agentId}/activate`, {
      method: 'POST',
    });
    return response.json();
  }
);

const agentSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAgents.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchAgents.fulfilled, (state, action) => {
        state.loading = false;
        state.agents = action.payload;
      })
      .addCase(fetchAgents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch agents';
      })
      .addCase(activateAgent.fulfilled, (state, action) => {
        const agent = state.agents.find(a => a.id === action.meta.arg);
        if (agent) {
          agent.status = 'active';
        }
      });
  },
});

export default agentSlice.reducer; 