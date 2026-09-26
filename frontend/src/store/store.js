// src/store/store.js
import { configureStore } from '@reduxjs/toolkit';
import chatReducer from './slice';

export default configureStore({
  reducer: {
    chat: chatReducer
  }
});