
// App.js
import React, { useState,useEffect } from 'react';
// import { v4 as uuidv4 } from "uuid";
import Sidebar from './components/sidebar';
import Navbar from './components/navbar';
import ChatArea from './components/chatArea';
import './styles/global.css';
import './App.css';

const App = () => {
  const [threads, setThreads] = useState([]);
  const [activeThreadId, setActiveThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // const [activeThread, setActiveThread] = useState(0);
  // const [messages, setMessages] = useState([]);
  // const [isLoading, setIsLoading] = useState(false);
  const [isChatStarted, setIsChatStarted] = useState(false);
  const API_BASE_URL = 'http://localhost:8000';

   // ✅ NEW: Load conversations when app starts
  useEffect(() => {
    const loadConversations = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/conversations/demo`);
        const data = await res.json();

        // Convert MongoDB format to your thread format
        const loadedThreads = data.map(conv => ({
          id: conv._id,
          title: conv.messages.length > 0 
            ? conv.messages[0].content.slice(0, 30) 
            : "New Chat",
          messages: conv.messages.map(msg => ({
            role: msg.role,
            content: msg.content
          }))
        }));

        setThreads(loadedThreads);
      } catch (err) {
        console.error("Error loading conversations:", err);
      }
    };

    loadConversations();
  }, []); // ✅ Run once on mount


 /* === Streamlit: reset_chat() === */
 const handleStartChat = async () => {
  try {
    setIsLoading(true);

  const res = await fetch(`${API_BASE_URL}/new-chat?user_id=demo`, {
  method: "POST",
});
    const data = await res.json();

    const newThread = {
      id: data.conversation_id,  // ✅ MongoDB ObjectId from backend
      title: "New Chat",
      messages: []
    };

    setThreads(prev => [newThread, ...prev]);
    setActiveThreadId(newThread.id);
    setIsChatStarted(true);

  } catch (err) {
    console.error("Error creating new chat:", err);
  } finally {
    setIsLoading(false);
  }
};

const handleSelectThread = (threadId) => {
  setActiveThreadId(threadId);
  setIsChatStarted(true);
};



  /* === Streamlit: send message === */
  const handleSendMessage = async (text) => {
    if (!text.trim() || !activeThreadId) return;

    // add user message
    setThreads(prev =>
      prev.map(thread =>
        thread.id === activeThreadId
          ? {
              ...thread,
              title:
                thread.messages.length === 0
                  ? text.slice(0, 30)
                  : thread.title,
              messages: [...thread.messages, { role: "user", content: text }]
            }
          : thread
      )
    );

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          thread_id: activeThreadId
        })
      });

      const data = await response.json();

      setThreads(prev =>
        prev.map(thread =>
          thread.id === activeThreadId
            ? {
                ...thread,
                messages: [
                  ...thread.messages,
                  { role: "assistant", content: data.response }
                ]
              }
            : thread
        )
      );
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const activeThread = threads.find(t => t.id === activeThreadId);

  return (
    <div className="app-container">
      <Sidebar
        threads={threads}
        activeThreadId={activeThreadId}
        onNewChat={handleStartChat}
        onSelectThread={handleSelectThread}
      />

      <div className="main-content">
        <Navbar />
        <ChatArea
          messages={activeThread?.messages || []}
          isLoading={isLoading}
          isChatStarted={isChatStarted}
          onStartChat={handleStartChat}
          onSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
};

export default App;