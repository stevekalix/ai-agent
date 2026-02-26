# Quick Start Guide - AI Agent System

## ⚡ 5-Minute Quick Start

### 1. Install Dependencies (1 minute)
```bash
cd E:\Vibe-Coding-AI\Ai-Agent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Start the Server (30 seconds)
```bash
python startup.py
```

**Output should show:**
```
============================================================
AI AGENT SYSTEM - STARTUP
============================================================

✅ All dependencies installed
📁 Logs directory ready: ...
🗄️  Initializing database...
✅ Database initialized

============================================================
🚀 Starting AI Agent System...
============================================================
📍 Server: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
🔄 ReDoc: http://localhost:8000/redoc
============================================================
```

### 3. Test the API (1 minute)
Open browser and visit: **http://localhost:8000/docs**

Click "Try it out" on any endpoint to test!

---

## 🎯 Common First Steps

### Create Your First Conversation
```bash
curl -X POST http://localhost:8000/api/v1/agent/conversation \
  -H "Content-Type: application/json" \
  -d '{"user_id":"student","title":"My First Chat"}'
```

Response will include `conversation_id` - copy it!

### Send Your First Message
Replace `CONVERSATION_ID` with the ID from above:
```bash
curl -X POST http://localhost:8000/api/v1/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id":"CONVERSATION_ID",
    "content":"What is 5 plus 3?",
    "user_id":"student"
  }'
```

### View Conversation History
```bash
curl http://localhost:8000/api/v1/agent/conversation/CONVERSATION_ID/history
```

---

## 📝 Example Interactions

### Math Conversation
```
User: "What is 15 times 3?"
Agent: Uses calculator tool → "The result of 15 multiply 3 is 45"
```

### Weather Query
```
User: "What's the weather in London?"
Agent: Uses weather_lookup tool → "Weather in London: Rainy, Temperature: 55°F"
```

### Information Search
```
User: "Search for information about Python"
Agent: Uses web_search tool → Lists relevant results
```

---

## 🧪 Run Tests

```bash
# Run all tests
pytest tests/test_agent.py -v

# Run comprehensive API testing
python examples/api_usage.py
```

---

## 📚 Project Structure

```
Ai-Agent/
├── main.py                    # Application entry
├── startup.py                 # Startup script
├── requirements.txt           # Dependencies
├── src/
│   ├── config.py             # Settings
│   ├── agent/
│   │   ├── core.py          # Agent logic
│   │   └── tools.py         # Available tools
│   ├── api/
│   │   ├── schemas.py       # Data models
│   │   └── routes/          # API endpoints
│   └── database/
│       ├── models.py        # DB tables
│       └── repository.py    # Data access
├── tests/                     # Test suite
├── examples/                  # Usage examples
└── logs/                      # Application logs
```

---

## 🔧 Available Tools

The agent can use these tools automatically:

### 1. **Calculator Tool**
- Performs: add, subtract, multiply, divide
- Example: "What is 100 divided by 5?"

### 2. **Weather Lookup Tool**
- Get weather for cities
- Example: "Weather in New York"

### 3. **Web Search Tool**
- Search for information
- Example: "Tell me about machine learning"

### 4. **File List Tool**
- List directory files
- Example: "List files in current directory"

---

## 🐛 If Something Goes Wrong

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# If in use, kill the process or use different port
# Edit main.py and change port=8000 to port=8001
```

### Database error
```bash
# Reset database
del ai_agent.db
python -c "from src.database.init_db import init_db; init_db()"
```

### Import errors
```bash
# Make sure you're in the right directory
cd E:\Vibe-Coding-AI\Ai-Agent

# Verify virtual environment is activated
# Should see (venv) in terminal

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📖 Full Documentation

- **README.md** - Complete overview and architecture
- **DEPLOYMENT.md** - Production deployment guide
- **API Docs** - http://localhost:8000/docs (interactive)
- **Code Comments** - Inline documentation in all files

---

## 🚀 Next: Customize It!

To add your own tool:

1. Edit `src/agent/tools.py`
2. Create a new class extending `Tool`
3. Implement the `execute()` method
4. Register it in `ToolRegistry`

Example:
```python
class MyCustomTool(Tool):
    name = "my_tool"
    description = "What my tool does"
    
    def execute(self, **kwargs):
        # Your implementation
        return {"success": True, "result": "..."}
```

---

## ✅ You're All Set!

Start the server with `python startup.py` and explore the API!

Questions? Check the test files for usage examples.

Happy coding! 🎉

