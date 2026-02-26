# 🚀 Running Frontend & Backend Together

## Quick Summary

You now have:
- **Backend**: Python FastAPI server (port 8000)
- **Frontend**: React web application (port 3000)

This guide shows you how to run both simultaneously.

---

## ⚡ Fastest Way to Get Started (5 minutes)

### Terminal 1: Start Backend
```bash
cd E:\Vibe-Coding-AI\Ai-Agent
python startup.py
```

### Terminal 2: Start Frontend
```bash
cd E:\Vibe-Coding-AI\Ai-Agent\frontend
npm install
npm start
```

### Then Visit
```
http://localhost:3000
```

**That's it!** The React app will automatically connect to the backend.

---

## 📋 Step-by-Step Setup

### Step 1: Install Frontend Dependencies

```bash
cd E:\Vibe-Coding-AI\Ai-Agent\frontend
npm install
```

This installs all required packages:
- React
- React Router
- Axios
- And other dependencies

**Expected Output:**
```
added 1500+ packages in X minutes
```

### Step 2: Setup Backend (if not done already)

```bash
cd E:\Vibe-Coding-AI\Ai-Agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Start Backend in Terminal 1

```bash
cd E:\Vibe-Coding-AI\Ai-Agent
python startup.py
```

**Expected Output:**
```
============================================================
🚀 Starting AI Agent System...
============================================================
📍 Server: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
🔄 ReDoc: http://localhost:8000/redoc
============================================================
```

### Step 4: Start Frontend in Terminal 2

```bash
cd E:\Vibe-Coding-AI\Ai-Agent\frontend
npm start
```

**Expected Output:**
```
On Your Network: http://192.168.x.x:3000

Local:   http://localhost:3000
```

The React app will automatically open in your browser.

---

## 🏠 Frontend Pages

### 1. **Dashboard** (http://localhost:3000)
- System status
- Available tools
- Quick info

### 2. **Chat** (http://localhost:3000/chat)
- Create conversations
- Send messages to AI agent
- View conversation history
- See which tools were used

### 3. **Tools** (http://localhost:3000/tools)
- List of available tools
- Execute tools directly
- View results

---

## 🔌 API Endpoints Connected

The frontend connects to these backend endpoints:

```
GET  /api/v1/health                    ✅ Health check
GET  /api/v1/agent/tools               ✅ List tools
POST /api/v1/agent/conversation        ✅ Create chat
GET  /api/v1/agent/conversations/{uid} ✅ Get conversations
POST /api/v1/agent/message             ✅ Send message
GET  /api/v1/agent/conversation/{id}/history  ✅ Get history
POST /api/v1/agent/tools/{name}/execute       ✅ Execute tool
```

---

## 🖼️ Frontend Features

### Dashboard
- ✅ Shows backend health status
- ✅ Lists all available tools
- ✅ Quick info and links

### Chat Interface
- ✅ Create new conversations
- ✅ Send messages to AI agent
- ✅ View conversation history
- ✅ See which tools were used
- ✅ Auto-scroll to latest messages
- ✅ Persistent conversation list

### Tools Page
- ✅ Interactive tool explorer
- ✅ Execute tools with custom inputs
- ✅ View tool results in JSON format
- ✅ Easy input forms for each tool

---

## 🎯 What Happens When You Use the Frontend

### When you send a chat message:
1. React sends POST request to backend
2. Backend processes with AI agent
3. Agent selects appropriate tool
4. Tool executes and returns result
5. Response sent back to frontend
6. Message and response displayed in chat

Example:
```
You:    "What is 5 plus 3?"
        ↓ (API call)
Backend: Uses calculator tool
        ↓ (Process)
Agent:   "The result of 5 add 3 is 8"
        ↓ (Response)
React:   Displays message with tool info
```

---

## 🐛 Troubleshooting

### Frontend won't connect to backend
**Problem:** "Cannot connect to backend"
**Solution:**
1. Make sure backend is running: `python startup.py`
2. Check backend is on port 8000
3. Try refreshing the page

### "npm install" fails
**Problem:** npm not found
**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart your terminal
3. Try again

### Port 3000 already in use
**Problem:** "Something is already running on port 3000"
**Solution:**
```bash
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
PORT=3001 npm start
```

### Messages not showing up
**Problem:** Sent message but no response
**Solution:**
1. Check backend is running
2. Check browser console (F12) for errors
3. Look at backend terminal for error messages

---

## 📁 Frontend File Structure

```
frontend/
├── package.json              # Dependencies
├── public/
│   └── index.html           # Main HTML
├── src/
│   ├── index.js             # Entry point
│   ├── App.js               # Main app
│   ├── App.css              # Styles
│   ├── components/
│   │   └── Navbar.js        # Navigation bar
│   └── pages/
│       ├── Dashboard.js     # Dashboard page
│       ├── Chat.js          # Chat page
│       ├── Tools.js         # Tools page
│       └── *.css            # Page styles
└── node_modules/            # Dependencies (auto-created)
```

---

## 🔧 Configuration

### Change Backend URL
If backend is on different URL, edit `frontend/src/App.js`:

```javascript
const [apiUrl] = useState('http://your-backend-url:8000/api/v1');
```

### Change Frontend Port
```bash
PORT=3001 npm start  # Use port 3001 instead
```

---

## 📊 Running Both Together (Recommended Setup)

### Using 2 Terminals (Best Way)

**Terminal 1 - Backend:**
```bash
cd E:\Vibe-Coding-AI\Ai-Agent
python startup.py
```

**Terminal 2 - Frontend:**
```bash
cd E:\Vibe-Coding-AI\Ai-Agent\frontend
npm start
```

**Open Browser:**
```
http://localhost:3000
```

### Using Docker (Alternative)

```bash
# Build frontend
cd E:\Vibe-Coding-AI\Ai-Agent\frontend
npm run build

# Build and run with docker-compose (when available)
cd ..
docker-compose up
```

---

## ✅ How to Know Everything Works

1. ✅ Backend running:
   - Terminal shows "🚀 Starting AI Agent System..."
   - Visit http://localhost:8000/docs (Swagger UI)

2. ✅ Frontend running:
   - Browser opens to http://localhost:3000
   - Page shows "Welcome to AI Agent"

3. ✅ Connection working:
   - Dashboard shows system status
   - No red error banner

4. ✅ Chat working:
   - Can create new conversation
   - Can send messages
   - Responses appear

---

## 🚀 Next Steps

1. **Open Browser:**
   ```
   http://localhost:3000
   ```

2. **Explore Dashboard:**
   - See system status
   - View available tools

3. **Try Chat:**
   - Click "Chat" in menu
   - Click "+ New Chat"
   - Type: "What is 5 plus 3?"
   - See response with calculator tool

4. **Explore Tools:**
   - Click "Tools" in menu
   - Select "calculator"
   - Enter numbers
   - Click Execute
   - See result

---

## 💡 Pro Tips

### Keep terminals organized
1. Use different terminal windows/tabs
2. Label them: "Backend" and "Frontend"
3. Keep them side by side

### Quick restart
```bash
# Restart backend (Ctrl+C then)
python startup.py

# Restart frontend (Ctrl+C then)
npm start
```

### Debug issues
1. **Browser console:** Press F12
2. **Backend logs:** Check terminal output
3. **Network tab:** See API calls
4. **Check health:** http://localhost:8000/api/v1/health

---

## 🎯 Common Commands

| What | Command |
|------|---------|
| Start backend | `python startup.py` |
| Start frontend | `npm start` |
| Stop server | `Ctrl+C` |
| Install deps | `npm install` |
| Build frontend | `npm run build` |
| View API docs | http://localhost:8000/docs |
| View frontend | http://localhost:3000 |
| Check health | http://localhost:8000/api/v1/health |

---

## ✨ Summary

```
Terminal 1:  python startup.py
Terminal 2:  npm start
Browser:     http://localhost:3000
```

That's all you need! Happy coding! 🎉

---

**Need help?**
- Backend logs: Check Terminal 1
- Frontend logs: Check Terminal 2 / Browser Console (F12)
- API docs: http://localhost:8000/docs

