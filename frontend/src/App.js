import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Tools from './pages/Tools';
import './App.css';

function App() {
  const apiUrl = 'http://localhost:8000/api/v1';
  const [error, setError] = useState(null);

  const checkBackendHealth = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/health`);
      console.log('✅ Backend is running:', response.data);
    } catch (err) {
      console.error('❌ Backend not available:', err.message);
      setError('Cannot connect to backend. Make sure the server is running on http://localhost:8000');
    }
  }, [apiUrl]);

  // Check if backend is available
  useEffect(() => {
    checkBackendHealth();
  }, [checkBackendHealth]);

  return (
    <Router>
      <div className="App">
        <Navbar />
        {error && (
          <div className="error-banner">
            <p>⚠️ {error}</p>
            <button onClick={checkBackendHealth}>Retry Connection</button>
          </div>
        )}
        <Routes>
          <Route path="/" element={<Dashboard apiUrl={apiUrl} />} />
          <Route path="/chat" element={<Chat apiUrl={apiUrl} />} />
          <Route path="/tools" element={<Tools apiUrl={apiUrl} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
