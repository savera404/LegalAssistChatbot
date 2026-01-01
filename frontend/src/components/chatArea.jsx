import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import '../styles/chat.css';

const ChatArea = ({ messages, isLoading, isChatStarted, onStartChat, onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-area">
      {!isChatStarted ? (
        /* Welcome Screen */
        <div className="welcome-screen">
          <h1 className="welcome-text">
            Welcome! I am <span className="welcome-highlight">Adil AI</span>. How may I help you?
          </h1>
          <button onClick={onStartChat} className="start-chat-button">
            Start Chat
          </button>
        </div>
      ) : (
        <>
          {/* Messages Area */}
          <div className="messages-container">
            <div className="messages-list">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-wrapper ${
                    message.role === 'user' ? 'message-user' : 'message-assistant'
                  }`}
                >
                  <div className={`message-bubble ${message.role}`}>
                    <p className="message-content">{message.content}</p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message-wrapper message-assistant">
                  <div className="message-bubble assistant">
                    <p className="message-content">Thinking...</p>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input Area */}
          <div className="input-area">
            <div className="input-container">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Chat"
                className="chat-input"
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={isLoading || !inputValue.trim()}
                className="send-button"
              >
                <Send className="send-icon" />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatArea;