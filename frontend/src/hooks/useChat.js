// src/hooks/useChat.js
import { useState, useEffect } from 'react';
import axios from 'axios';

export const useChat = () => {
  const [sessionId, setSessionId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize or retrieve session ID
  useEffect(() => {
    const storedSessionId = localStorage.getItem('chat_session_id');
    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      const newSessionId = crypto.randomUUID();
      localStorage.setItem('chat_session_id', newSessionId);
      setSessionId(newSessionId);
    }
  }, []);

  const sendMessage = async (message) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/chat/', 
        { message },
        { headers: { 'X-Session-ID': sessionId } }
      );
      return response.data;
    } catch (err) {
      setError(err.response?.data?.error || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = async () => {
    try {
      await axios.post('/api/clear-conversation/', 
        {},
        { headers: { 'X-Session-ID': sessionId } }
      );
      // Optionally create a new session
      const newSessionId = crypto.randomUUID();
      localStorage.setItem('chat_session_id', newSessionId);
      setSessionId(newSessionId);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
      throw err;
    }
  };

  return { sendMessage, clearHistory, sessionId, isLoading, error };
};