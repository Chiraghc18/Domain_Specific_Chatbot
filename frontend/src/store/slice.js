// src/store/slice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const sendChatMessage = createAsyncThunk(
  'chat/sendMessage',
  async (message, { dispatch }) => {
    try {
      const response = await axios.post('http://localhost:8000/api/chat/', {
        message
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    loading: false,
    error: null,
    domain: 'general'
  },
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    clearMessages: (state) => {
      state.messages = [];
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push({
          text: action.payload.reply,
          sender: 'bot'
        });
        state.domain = action.payload.domain;
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export const { addMessage, clearMessages } = chatSlice.actions;
export default chatSlice.reducer;