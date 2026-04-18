import React, { useState, useEffect } from 'react';
import Sidebar from './components/sidebar';
import ChatArea from './components/chatArea';
import './styles/global.css';
import './App.css';

const App = () => {
  const [threads, setThreads] = useState([]);
  const [activeThreadId, setActiveThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isChatStarted, setIsChatStarted] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const API_BASE_URL = 'http://localhost:8000';

  // receive user from parent
  useEffect(() => {
    const handleAuth = (event) => {
      if (event.data.type === "AUTH_USER") {
        setCurrentUser(event.data.user);
      }
    };
    window.addEventListener("message", handleAuth);
    return () => window.removeEventListener("message", handleAuth);
  }, []);

  // load conversations when user is known
  useEffect(() => {
    if (!currentUser) return;
    const loadConversations = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/conversations/${currentUser.id}`);
        const data = await res.json();
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
  }, [currentUser]);

  const handleStartChat = async () => {
    if (!currentUser) return;
    try {
      setIsLoading(true);
      const res = await fetch(`${API_BASE_URL}/new-chat?user_id=${currentUser.id}`, {
        method: "POST"
      });
      const data = await res.json();
      const newThread = {
        id: data.conversation_id,
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

  const handleSendMessage = async (text) => {
    if (!text.trim() || !activeThreadId) return;

    setThreads(prev =>
      prev.map(thread =>
        thread.id === activeThreadId
          ? {
              ...thread,
              title: thread.messages.length === 0 ? text.slice(0, 30) : thread.title,
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
        body: JSON.stringify({ message: text, thread_id: activeThreadId })
      });

      const data = await response.json();

      const assistantContent = data.lawyer_data
        ? JSON.stringify(data.lawyer_data)
        : data.response;

      setThreads(prev =>
        prev.map(thread =>
          thread.id === activeThreadId
            ? {
                ...thread,
                messages: [...thread.messages, { role: "assistant", content: assistantContent }]
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

  if (!currentUser) {
    return (
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        backgroundColor: "#1a1a1a",
        color: "white"
      }}>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Sidebar
        threads={threads}
        activeThreadId={activeThreadId}
        onNewChat={handleStartChat}
        onSelectThread={handleSelectThread}
      />
      <div className="main-content">
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