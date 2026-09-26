import { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addMessage, sendChatMessage } from '../store/slice';
import Message from './message';

const Chat = () => {
  const [input, setInput] = useState('');
  const [inputHistory, setInputHistory] = useState([]);
  const messageRefs = useRef({});
  const dispatch = useDispatch();
  const { messages, loading, domain } = useSelector((state) => state.chat);

  const handleSend = async () => {
    if (!input.trim()) return;

    setInputHistory((prev) => [...prev, input]);
    dispatch(addMessage({ text: input, sender: 'user' }));
    dispatch(sendChatMessage(input));
    setInput('');
  };

  const handleHistoryClick = (questionText) => {
    const targetIndex = messages.findIndex(
      (msg) => msg.text === questionText && msg.sender === 'user'
    );
    if (targetIndex !== -1 && messageRefs.current[targetIndex]) {
      messageRefs.current[targetIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <div className="chat-page">
  <header className="chat-header">
  <h1>AI Chatbot</h1>

  </header>

  <div className="chat-layout">
    <div className="sidebar">
      <h3>History</h3>
      <ul>
        {inputHistory.map((item, index) => (
          <li
            key={index}
            className="history-item"
            onClick={() => handleHistoryClick(item)}
            style={{ cursor: 'pointer' }}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>

    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            ref={(el) => (messageRefs.current[index] = el)}
          >
            <Message text={msg.text} sender={msg.sender} />
          </div>
        ))}
        {loading && <div className="loading">Thinking...</div>}
      </div>

      <div className="input-area">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
        <div className="domain-tag">Domain: {domain}</div>
      </div>
    </div>
  </div>
</div>

  );
};

export default Chat;
