import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface GroupChatState {
  groupChats: any[];
  availableAgents: any[];
  loading: boolean;
  error: string | null;
  activeChats: Record<number, boolean>;
}

const initialState: GroupChatState = {
  groupChats: [],
  availableAgents: [],
  loading: false,
  error: null,
  activeChats: {}
};

export const fetchGroupChats = createAsyncThunk(
  'groupChat/fetchAll',
  async () => {
    const response = await fetch('/api/v1/group-chats');
    return response.json();
  }
);

export const createGroupChat = createAsyncThunk(
  'groupChat/create',
  async (chatData: any) => {
    const response = await fetch('/api/v1/group-chats', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(chatData)
    });
    return response.json();
  }
);

export const startGroupChat = createAsyncThunk(
  'groupChat/start',
  async (chatId: number) => {
    const response = await fetch(`/api/v1/group-chats/${chatId}/start`, {
      method: 'POST'
    });
    return response.json();
  }
);

export const stopGroupChat = createAsyncThunk(
  'groupChat/stop',
  async (chatId: number) => {
    const response = await fetch(`/api/v1/group-chats/${chatId}/stop`, {
      method: 'POST'
    });
    return response.json();
  }
);

const groupChatSlice = createSlice({
  name: 'groupChat',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchGroupChats.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchGroupChats.fulfilled, (state, action) => {
        state.loading = false;
        state.groupChats = action.payload;
      })
      .addCase(fetchGroupChats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch group chats';
      })
      .addCase(createGroupChat.fulfilled, (state, action) => {
        state.groupChats.push(action.payload);
      })
      .addCase(startGroupChat.fulfilled, (state, action) => {
        state.activeChats[action.payload.id] = true;
      })
      .addCase(stopGroupChat.fulfilled, (state, action) => {
        state.activeChats[action.payload.id] = false;
      });
  }
});

export default groupChatSlice.reducer; 