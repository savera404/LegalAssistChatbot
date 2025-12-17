// import "../styles/sidebar.css";
// import logo from "../assets/logo.png";

// function Sidebar(props) {
//   const {
//     threads,
//     activeThread,
//     onSelectThread,
//     onNewChat
//   } = props;

//   return (
//     <div className="sidebar">
//       <div className="logo">
//         <img src={logo} alt="LegalAssist Logo" />
//         <span>LegalAssist</span>
//       </div>

//       <button className="chat-btn" onClick={onNewChat}>
//         Chat with Adil AI
//       </button>

//       <p className="section-title">Your chats</p>

//       <ul className="chat-list">
//         {threads.map((thread) => (
//           <li
//             key={thread.id}
//             className={thread.id === activeThread ? "active" : ""}
//             onClick={() => onSelectThread(thread.id)}
//           >
//             {thread.title}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default Sidebar;

// components/Sidebar.js
// import React from 'react';
// import { MessageSquare, Plus, Bot } from 'lucide-react';
// import '../styles/sidebar.css';

// const Sidebar = ({ threads, currentThreadId, onNewChat, onLoadConversation }) => {
//   return (
//     <div className="sidebar">
//       {/* Logo */}
//       <div className="sidebar-header">
//         <div className="logo-container">
//           <MessageSquare className="logo-icon" />
//           <span className="logo-text">LegalAssist</span>
//         </div>
//       </div>

//       {/* Chat with Adil AI */}
//       <div className="sidebar-title">
//         <div className="chat-ai-container">
//           <Bot className="bot-icon" />
//           <span className="chat-ai-text">Chat with Adil AI</span>
//         </div>
//       </div>

//       {/* New Chat Button */}
//       <div className="new-chat-section">
//         <button onClick={onNewChat} className="new-chat-button">
//           <Plus className="plus-icon" />
//           Start New Chat
//         </button>
//       </div>

//       {/* Your chats */}
//       <div className="chats-list">
//         <div className="chats-container">
//           <h3 className="chats-heading">Your chats</h3>
//           <div className="chats-items">
//             {threads.length === 0 ? (
//               <p className="no-chats">No chats yet</p>
//             ) : (
//               threads.map((threadId, index) => (
//                 <button
//                   key={threadId}
//                   onClick={() => onLoadConversation(threadId)}
//                   className={`chat-item ${
//                     currentThreadId === threadId ? 'chat-item-active' : ''
//                   }`}
//                 >
//                   Chat {threads.length - index}
//                 </button>
//               ))
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Sidebar;

// components/Sidebar.js
// components/Sidebar.jsx
import React from 'react';
import { MessageSquare, Search } from 'lucide-react';
import '../styles/sidebar.css';

// const Sidebar = ({ threads, activeThread, onSelectThread }) => {
//   return (
//     <div className="sidebar">
//       {/* Logo */}
//       <div className="sidebar-header">
//         <div className="logo-container">
//           <MessageSquare className="logo-icon" />
//           <span className="logo-text">LegalAssist</span>
//         </div>
//       </div>

//       {/* Chat with Adil AI */}
//       <div className="sidebar-title">
//         <div className="chat-ai-container">
//           <MessageSquare className="chat-icon" />
//           <span className="chat-ai-text">Chat with Adil AI</span>
//         </div>
//       </div>

//       {/* Chats List */}
//       <div className="chats-list">
//         <div className="chats-container">
//           <h3 className="chats-heading">Your chats</h3>
//           <div className="chats-items">
//             {threads.length === 0 ? (
//               <p className="no-chats">No chats yet</p>
//             ) : (
//               threads.map((thread, index) => (
//                 <button
//                   key={index}
//                   onClick={() => onSelectThread(index)}
//                   className={`chat-item ${
//                     activeThread === index ? 'chat-item-active' : ''
//                   }`}
//                 >
//                   {thread}
//                 </button>
//               ))
//             )}
//           </div>
//         </div>
//       </div>

//       {/* Search Icon at Bottom */}
//       <div className="sidebar-footer">
//         <button className="search-button">
//           <Search className="search-icon" />
//         </button>
//       </div>
//     </div>
//   );
// };

// export default Sidebar;

const Sidebar = ({ threads, activeThreadId, onSelectThread, onNewChat }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>LegalAssist</h2>
      </div>

      <button className="new-chat-btn" onClick={onNewChat}>
        + Start New Chat
      </button>

      <h4 className="chats-heading">Your chats</h4>

      {threads.length === 0 && (
        <p className="no-chats">No chats yet</p>
      )}

      {threads.map(thread => (
        <button
          key={thread.id}
          onClick={() => onSelectThread(thread.id)}
          className={`chat-item ${
            thread.id === activeThreadId ? "active" : ""
          }`}
        >
          {thread.title}
        </button>
      ))}
    </div>
  );
};

export default Sidebar;
