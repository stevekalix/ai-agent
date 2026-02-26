import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          🤖 AI Agent
        </Link>
        <ul className="navbar-menu">
          <li>
            <Link to="/" className="navbar-link">Dashboard</Link>
          </li>
          <li>
            <Link to="/chat" className="navbar-link">Chat</Link>
          </li>
          <li>
            <Link to="/tools" className="navbar-link">Tools</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;

