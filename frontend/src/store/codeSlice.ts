import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface CodeState {
  executionResult: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: CodeState = {
  executionResult: null,
  loading: false,
  error: null
};

export const executeCode = createAsyncThunk(
  'code/execute',
  async ({ content, language }: { content: string; language: string }) => {
    const response = await fetch('/api/v1/code/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, language })
    });
    return response.json();
  }
);

export const saveCode = createAsyncThunk(
  'code/save',
  async ({ fileId, content }: { fileId: string; content: string }) => {
    const response = await fetch(`/api/v1/code/files/${fileId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    return response.json();
  }
);

const codeSlice = createSlice({
  name: 'code',
  initialState,
  reducers: {
    clearExecutionResult: (state) => {
      state.executionResult = null;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(executeCode.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(executeCode.fulfilled, (state, action) => {
        state.loading = false;
        state.executionResult = action.payload.result;
      })
      .addCase(executeCode.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Execution failed';
      })
      .addCase(saveCode.rejected, (state, action) => {
        state.error = action.error.message || 'Save failed';
      });
  }
});

export const { clearExecutionResult } = codeSlice.actions;
export default codeSlice.reducer; 