// import { useState } from "react";
// import "./styles/global.css";
// import Sidebar from "./components/sidebar";
// import Navbar from "./components/navbar";
// import ChatArea from "./components/chatArea";
// import { FaBell } from "react-icons/fa";


// import { v4 as uuidv4 } from "uuid";

// function App() {
//   const [messages, setMessages] = useState([]);
//   const [threads, setThreads] = useState([]);
//   const [activeThread, setActiveThread] = useState(null);
//   const [input, setInput] = useState("");

//   const startNewChat = () => {
//     const newThread = uuidv4();
//     setThreads(prev => [...prev, { id: newThread, title: "New Chat" }]);
//     setActiveThread(newThread);
//     setMessages([]);
//   };

//   const sendMessage = async () => {
//     if (!input || !activeThread) return;

//     const userMsg = { role: "user", content: input };
//     setMessages(prev => [...prev, userMsg]);
//     setInput("");

//     const res = await fetch("http://127.0.0.1:8000/chat", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         message: input,
//         thread_id: activeThread
//       })
//     });

//     const data = await res.json();

//     const aiMsg = { role: "assistant", content: data.response };
//     setMessages(prev => [...prev, aiMsg]);

//     setThreads(prev =>
//       prev.map(t =>
//         t.id === activeThread && t.title === "New Chat"
//           ? { ...t, title: input.slice(0, 30) }
//           : t
//       )
//     );
//   };

//   const loadChat = async (threadId) => {
//     setActiveThread(threadId);

//     const res = await fetch(
//       `http://127.0.0.1:8000/history/${threadId}`
//     );
//     const data = await res.json();
//     setMessages(data);
//   };

//   return (
//     <div style={{ display: "flex", height: "100vh" }}>
//       <Sidebar
//         threads={threads}
//         activeThread={activeThread}
//         onNewChat={startNewChat}
//         onSelectThread={loadChat}
//       />

//       <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
//         <Navbar />
//         <ChatArea
//           messages={messages}
//           input={input}
//           setInput={setInput}
//           onSend={sendMessage}
//         />
//       </div>
//     </div>
//   );
// }
// export default App;

// App.js
// App.js
import React, { useState } from 'react';
import { v4 as uuidv4 } from "uuid";
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

 /* === Streamlit: reset_chat() === */
  const handleStartChat = () => {
    const newThread = {
      id: uuidv4(),
      title: "New Chat",
      messages: []
    };

    setThreads(prev => [newThread, ...prev]);
    setActiveThreadId(newThread.id);
    setIsChatStarted(true);
  };

  /* === Streamlit: clicking old chat === */
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