import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './Tools.css';

function Tools({ apiUrl }) {
  const [tools, setTools] = useState([]);
  const [selectedTool, setSelectedTool] = useState(null);
  const [toolInputs, setToolInputs] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTools = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/agent/tools`);
      setTools(response.data.tools);
    } catch (err) {
      setError('Failed to fetch tools');
      console.error('Error:', err);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchTools();
  }, [fetchTools]);

  const getToolInputFields = (toolName) => {
    const inputs = {
      calculator: [
        { name: 'operation', label: 'Operation', type: 'select', options: ['add', 'subtract', 'multiply', 'divide'] },
        { name: 'a', label: 'First Number', type: 'number' },
        { name: 'b', label: 'Second Number', type: 'number' }
      ],
      weather_lookup: [
        { name: 'city', label: 'City Name', type: 'text', placeholder: 'e.g., London' }
      ],
      web_search: [
        { name: 'query', label: 'Search Query', type: 'text', placeholder: 'e.g., Python programming' }
      ],
      file_list: [
        { name: 'directory', label: 'Directory Path', type: 'text', placeholder: 'e.g., .' }
      ]
    };
    return inputs[toolName] || [];
  };

  const handleInputChange = (field, value) => {
    setToolInputs({
      ...toolInputs,
      [field]: value
    });
  };

  const executeTool = async (e) => {
    e.preventDefault();
    if (!selectedTool) return;

    setLoading(true);
    try {
      const response = await axios.post(
        `${apiUrl}/agent/tools/${selectedTool}/execute`,
        toolInputs
      );
      setResult(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to execute tool');
      console.error('Error:', err);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-content">
      <div className="container">
        <h1 className="page-title">Tools</h1>

        {error && (
          <div className="message error">{error}</div>
        )}

        <div className="tools-layout">
          <div className="tools-list-panel">
            <h3>Available Tools</h3>
            <div className="tools-list">
              {tools.map((tool, index) => (
                <div
                  key={index}
                  className={`tool-list-item ${selectedTool === tool.name ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedTool(tool.name);
                    setToolInputs({});
                    setResult(null);
                  }}
                >
                  <p className="tool-name">{tool.name}</p>
                  <p className="tool-desc">{tool.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="tools-execute-panel">
            {selectedTool ? (
              <>
                <h3>Execute: {selectedTool}</h3>
                <form onSubmit={executeTool} className="tool-form">
                  {getToolInputFields(selectedTool).map((field, index) => (
                    <div key={index} className="input-group">
                      <label>{field.label}</label>
                      {field.type === 'select' ? (
                        <select
                          value={toolInputs[field.name] || ''}
                          onChange={(e) => handleInputChange(field.name, e.target.value)}
                          required
                        >
                          <option value="">Select {field.label}</option>
                          {field.options.map(opt => (
                            <option key={opt} value={opt}>{opt}</option>
                          ))}
                        </select>
                      ) : (
                        <input
                          type={field.type}
                          value={toolInputs[field.name] || ''}
                          onChange={(e) => handleInputChange(field.name, e.target.value)}
                          placeholder={field.placeholder}
                          required
                        />
                      )}
                    </div>
                  ))}
                  <button type="submit" className="button" disabled={loading}>
                    {loading ? 'Executing...' : 'Execute'}
                  </button>
                </form>

                {result && (
                  <div className="result-panel">
                    <h4>Result:</h4>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                  </div>
                )}
              </>
            ) : (
              <div className="empty-state">
                <p>Select a tool from the list to execute it</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Tools;
