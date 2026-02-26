import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import './Chat.css';

function Chat({ apiUrl }) {
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [userId] = useState('user_' + Date.now());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const fetchConversations = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/agent/conversations/${userId}`);
      setConversations(response.data.conversations);
    } catch (err) {
      console.error('Error fetching conversations:', err);
    }
  }, [apiUrl, userId]);

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const createConversation = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${apiUrl}/agent/conversation`, {
        user_id: userId,
        title: `Chat ${new Date().toLocaleTimeString()}`
      });
      const newConversation = response.data;
      setCurrentConversation(newConversation);
      setMessages([]);
      setConversations([newConversation, ...conversations]);
      setError(null);
    } catch (err) {
      setError('Failed to create conversation');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadConversation = async (conversation) => {
    try {
      setCurrentConversation(conversation);
      const response = await axios.get(
        `${apiUrl}/agent/conversation/${conversation.id}/history`
      );
      setMessages(response.data.messages);
      setError(null);
    } catch (err) {
      setError('Failed to load conversation');
      console.error('Error:', err);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !currentConversation) return;

    const userMessage = input;
    setInput('');
    setLoading(true);

    try {
      // Add user message optimistically
      setMessages([...messages, {
        role: 'user',
        content: userMessage,
        created_at: new Date().toISOString()
      }]);

      // Send to API
      const response = await axios.post(`${apiUrl}/agent/message`, {
        conversation_id: currentConversation.id,
        content: userMessage,
        user_id: userId
      });

      // Add agent response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response,
        tool_used: response.data.tool_used,
        created_at: new Date().toISOString()
      }]);

      setError(null);
    } catch (err) {
      setError('Failed to send message');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-sidebar">
        <button className="button" onClick={createConversation} disabled={loading}>
          + New Chat
        </button>
        <div className="conversations-list">
          {conversations.map(conv => (
            <div
              key={conv.id}
              className={`conversation-item ${currentConversation?.id === conv.id ? 'active' : ''}`}
              onClick={() => loadConversation(conv)}
            >
              <p className="conv-title">{conv.title}</p>
              <p className="conv-date">
                {new Date(conv.updated_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="chat-main">
        {!currentConversation ? (
          <div className="chat-empty">
            <h2>Welcome to AI Agent Chat</h2>
            <p>Create a new conversation or select one from the sidebar to get started</p>
            <button className="button" onClick={createConversation}>
              Start New Conversation
            </button>
          </div>
        ) : (
          <>
            <div className="chat-header">
              <h2>{currentConversation.title}</h2>
              <p className="conv-id">ID: {currentConversation.id.slice(0, 8)}...</p>
            </div>

            {error && (
              <div className="message error">{error}</div>
            )}

            <div className="messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message-bubble ${msg.role}`}>
                  <div className="message-content">
                    <p>{msg.content}</p>
                    {msg.tool_used && (
                      <p className="tool-info">🔧 Tool used: {msg.tool_used}</p>
                    )}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <form onSubmit={sendMessage} className="message-input-form">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message here..."
                disabled={loading}
              />
              <button type="submit" disabled={loading || !input.trim()} className="button">
                {loading ? 'Sending...' : 'Send'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

export default Chat;

