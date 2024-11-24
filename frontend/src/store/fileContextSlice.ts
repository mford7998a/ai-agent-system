import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface FileContextState {
  contexts: any[];
  loading: boolean;
  error: string | null;
}

const initialState: FileContextState = {
  contexts: [],
  loading: false,
  error: null
};

export const fetchFileContexts = createAsyncThunk(
  'fileContext/fetchContexts',
  async () => {
    const response = await fetch('/api/v1/file-context');
    return response.json();
  }
);

export const uploadFileContext = createAsyncThunk(
  'fileContext/upload',
  async (formData: FormData) => {
    const response = await fetch('/api/v1/file-context/upload', {
      method: 'POST',
      body: formData
    });
    return response.json();
  }
);

export const createFileContext = createAsyncThunk(
  'fileContext/create',
  async (contextData: any) => {
    const response = await fetch('/api/v1/file-context', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(contextData)
    });
    return response.json();
  }
);

export const updateFileContext = createAsyncThunk(
  'fileContext/update',
  async ({ id, ...contextData }: any) => {
    const response = await fetch(`/api/v1/file-context/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(contextData)
    });
    return response.json();
  }
);

export const deleteFileContext = createAsyncThunk(
  'fileContext/delete',
  async (id: number) => {
    await fetch(`/api/v1/file-context/${id}`, {
      method: 'DELETE'
    });
    return id;
  }
);

const fileContextSlice = createSlice({
  name: 'fileContext',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchFileContexts.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchFileContexts.fulfilled, (state, action) => {
        state.loading = false;
        state.contexts = action.payload;
      })
      .addCase(fetchFileContexts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch contexts';
      })
      .addCase(uploadFileContext.fulfilled, (state, action) => {
        state.contexts.push(action.payload);
      })
      .addCase(createFileContext.fulfilled, (state, action) => {
        state.contexts.push(action.payload);
      })
      .addCase(updateFileContext.fulfilled, (state, action) => {
        const index = state.contexts.findIndex(
          context => context.id === action.payload.id
        );
        if (index !== -1) {
          state.contexts[index] = action.payload;
        }
      })
      .addCase(deleteFileContext.fulfilled, (state, action) => {
        state.contexts = state.contexts.filter(
          context => context.id !== action.payload
        );
      });
  }
});

export default fileContextSlice.reducer; 