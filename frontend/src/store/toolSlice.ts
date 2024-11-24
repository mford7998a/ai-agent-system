import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface ToolState {
  tools: any[];
  loading: boolean;
  error: string | null;
}

const initialState: ToolState = {
  tools: [],
  loading: false,
  error: null
};

export const fetchTools = createAsyncThunk(
  'tools/fetchTools',
  async () => {
    const response = await fetch('/api/v1/tools');
    return response.json();
  }
);

export const createTool = createAsyncThunk(
  'tools/createTool',
  async (toolData: any) => {
    const response = await fetch('/api/v1/tools', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(toolData)
    });
    return response.json();
  }
);

export const updateTool = createAsyncThunk(
  'tools/updateTool',
  async ({ id, ...toolData }: any) => {
    const response = await fetch(`/api/v1/tools/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(toolData)
    });
    return response.json();
  }
);

export const deleteTool = createAsyncThunk(
  'tools/deleteTool',
  async (id: number) => {
    await fetch(`/api/v1/tools/${id}`, {
      method: 'DELETE'
    });
    return id;
  }
);

const toolSlice = createSlice({
  name: 'tools',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTools.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchTools.fulfilled, (state, action) => {
        state.loading = false;
        state.tools = action.payload;
      })
      .addCase(fetchTools.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch tools';
      })
      .addCase(createTool.fulfilled, (state, action) => {
        state.tools.push(action.payload);
      })
      .addCase(updateTool.fulfilled, (state, action) => {
        const index = state.tools.findIndex(tool => tool.id === action.payload.id);
        if (index !== -1) {
          state.tools[index] = action.payload;
        }
      })
      .addCase(deleteTool.fulfilled, (state, action) => {
        state.tools = state.tools.filter(tool => tool.id !== action.payload);
      });
  }
});

export default toolSlice.reducer; 