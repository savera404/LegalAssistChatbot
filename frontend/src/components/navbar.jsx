// import "../styles/navbar.css";
// import { FaBell, FaSearch, FaUser } from "react-icons/fa";

// export default function Navbar() {
//   return (
//     <div className="navbar">
//       <div className="nav-links">
//         <span>Home</span>
//         <span>Laws</span>
//         <span>Cases</span>
//         <span>Community Forum</span>
//       </div>

//       <div className="nav-icons">
//         <FaSearch />
//         <FaBell />
//         <FaUser />
//       </div>
//     </div>
//   );
// }

// components/Navbar.jsx
import React from 'react';
import { Search, Bell, User } from 'lucide-react';
import '../styles/navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-links">
        <span>Home</span>
        <span>Laws</span>
        <span>Cases</span>
        <span>Community Forum</span>
      </div>
      <div className="nav-icons">
        <Search className="nav-icon" />
        <Bell className="nav-icon" />
        <User className="nav-icon" />
      </div>
    </nav>
  );
};

export default Navbar;