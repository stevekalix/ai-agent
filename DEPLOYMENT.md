# Installation & Deployment Guide

## Local Development Setup

### Step 1: Clone and Navigate to Project
```bash
cd E:\Vibe-Coding-AI\Ai-Agent
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python -c "from src.database.init_db import init_db; init_db()"
```

### Step 5: Run the Application
```bash
python main.py
```

The server will start at: **http://localhost:8000**

### Step 6: Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f ai-agent

# Stop services
docker-compose down
```

### Option 2: Docker Manual Build
```bash
# Build image
docker build -t ai-agent:latest .

# Run container
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/logs:/app/logs \
  ai-agent:latest

# On Windows PowerShell
docker run -p 8000:8000 `
  -e DEBUG=False `
  -e LOG_LEVEL=INFO `
  -v ${pwd}\logs:/app/logs `
  ai-agent:latest
```

---

## Testing the Installation

### Quick Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### List Available Tools
```bash
curl http://localhost:8000/api/v1/agent/tools
```

### Run Test Suite
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/test_agent.py --cov=src --cov-report=html
```

### Run API Usage Examples
```bash
python examples/api_usage.py
```

---

## Troubleshooting

### Port 8000 Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process (Windows)
taskkill /PID <PID> /F
```

### Database Issues
```bash
# Reset database
rm ai_agent.db
python -c "from src.database.init_db import init_db; init_db()"
```

### Module Not Found Error
```bash
# Ensure you're in the correct directory
cd E:\Vibe-Coding-AI\Ai-Agent

# Verify virtual environment is activated
# Should see (venv) in your terminal

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn main:app -w 4 -b 0.0.0.0:8000 --access-logfile - --error-logfile -
```

### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=8000 main:app
```

### Environment Variables for Production
```env
DEBUG=False
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://user:password@localhost/ai_agent
CORS_ORIGINS=["https://yourdomain.com"]
```

### Docker Deployment to Production
```bash
# Build with production tag
docker build -t myregistry/ai-agent:1.0.0 .

# Push to registry
docker push myregistry/ai-agent:1.0.0

# Deploy with docker-compose in production
docker-compose -f docker-compose.prod.yml up -d
```

---

## Monitoring

### View Logs
```bash
# Local
tail -f logs/ai_agent.log

# Docker
docker-compose logs -f ai-agent
```

### Health Check Endpoint
```bash
# Runs automatically every 30 seconds in Docker
curl http://localhost:8000/api/v1/health
```

### Performance Monitoring
```bash
# Check container stats (Docker)
docker stats ai-agent-app
```

---

## Database Maintenance

### Backup Database
```bash
# Create backup
cp ai_agent.db ai_agent.db.backup

# Docker backup
docker-compose exec ai-agent cp ai_agent.db ai_agent.db.backup
```

### Reset All Data
```bash
rm ai_agent.db
python -c "from src.database.init_db import init_db; init_db()"
```

---

## Next Steps

1. ✅ Start the server
2. 📚 Review API documentation at `/docs`
3. 🧪 Run tests to verify installation
4. 🔧 Customize tools in `src/agent/tools.py`
5. 🚀 Deploy to production when ready


