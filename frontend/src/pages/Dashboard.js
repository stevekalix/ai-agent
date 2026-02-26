import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import '../pages/Dashboard.css';

function Dashboard({ apiUrl }) {
  const [health, setHealth] = useState(null);
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    try {
      // Get health status
      const healthResponse = await axios.get(`${apiUrl}/health`);
      setHealth(healthResponse.data);

      // Get tools
      const toolsResponse = await axios.get(`${apiUrl}/agent/tools`);
      setTools(toolsResponse.data.tools);
      setError(null);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to fetch dashboard data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  if (loading) {
    return (
      <div className="main-content">
        <div className="container">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <h1 className="page-title">Dashboard</h1>

        {error && (
          <div className="message error">{error}</div>
        )}

        {health && (
          <div className="card">
            <h3>System Status</h3>
            <p><strong>Status:</strong> <span className="status-badge success">{health.status}</span></p>
            <p><strong>Version:</strong> {health.version}</p>
            <p><strong>Last Updated:</strong> {new Date(health.timestamp).toLocaleString()}</p>
          </div>
        )}

        <div className="card">
          <h3>Available Tools ({tools.length})</h3>
          <div className="tools-grid">
            {tools.map((tool, index) => (
              <div key={index} className="tool-card">
                <h4>{tool.name}</h4>
                <p>{tool.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3>Quick Info</h3>
          <ul>
            <li>📚 Access the <strong>Chat</strong> page to interact with the AI Agent</li>
            <li>🔧 Check the <strong>Tools</strong> page to see all available tools</li>
            <li>💬 Create conversations and send messages to the agent</li>
            <li>📊 View conversation history and statistics</li>
          </ul>
        </div>

        <button className="button" onClick={fetchDashboardData}>
          Refresh
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
