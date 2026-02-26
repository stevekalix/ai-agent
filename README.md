# AI Agent System - Student Project

A comprehensive, production-ready AI agent system built with Python that demonstrates modern software architecture, multi-tool integration, and conversation management.

## 📋 Features

### Core Features
- ✅ **Multi-Tool AI Agent**: Intelligent tool selection and execution
- ✅ **Conversation Management**: Persistent conversation storage and history
- ✅ **REST API**: FastAPI-based HTTP endpoints
- ✅ **Database Integration**: SQLAlchemy ORM with SQLite
- ✅ **Logging System**: Comprehensive logging with file rotation
- ✅ **Configuration Management**: Environment-based settings
- ✅ **Error Handling**: Proper exception handling and validation

### Available Tools
1. **Calculator Tool** - Basic arithmetic operations (add, subtract, multiply, divide)
2. **Weather Lookup** - Get weather information for cities
3. **Web Search** - Search for information on topics
4. **File List** - List files in directories

### Advanced Features
- Conversation memory and context management
- Intent analysis for smart tool selection
- Parameter extraction from natural language
- Execution logging and statistics
- API testing suite
- Docker containerization

## 🏗️ Architecture

### Project Structure
```
Ai-Agent/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
├── docker-compose.yml              # Docker Compose setup
├── .env                            # Environment variables
├── src/
│   ├── config.py                   # Configuration settings
│   ├── logging_config.py           # Logging setup
│   ├── agent/
│   │   ├── core.py                # AI agent logic
│   │   └── tools.py               # Tool implementations
│   ├── api/
│   │   ├── schemas.py             # Request/Response models
│   │   └── routes/
│   │       ├── agent_routes.py    # Agent endpoints
│   │       └── health_routes.py   # Health check endpoints
│   └── database/
│       ├── models.py              # SQLAlchemy models
│       ├── init_db.py             # Database initialization
│       └── repository.py          # Data access layer
├── tests/
│   └── test_agent.py              # Unit and integration tests
├── examples/
│   └── api_usage.py               # API usage examples
└── logs/
    └── ai_agent.log               # Application logs
```

### Architecture Diagram
```
┌─────────────────────────────────────────────────┐
│            FastAPI Application                  │
├─────────────────────────────────────────────────┤
│  Routes (Agent, Health, Tools)                  │
├─────────────────────────────────────────────────┤
│  AI Agent Core Logic                            │
│  ├─ Intent Analysis                             │
│  ├─ Tool Selection                              │
│  └─ Conversation Management                     │
├─────────────────────────────────────────────────┤
│  Tool Registry                                  │
│  ├─ Calculator Tool                             │
│  ├─ Weather Tool                                │
│  ├─ Search Tool                                 │
│  └─ File List Tool                              │
├─────────────────────────────────────────────────┤
│  Database Layer (SQLAlchemy)                    │
│  ├─ Conversations                               │
│  ├─ Messages                                    │
│  └─ Agent Logs                                  │
└─────────────────────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Docker & Docker Compose (optional)

### Local Installation

1. **Clone the repository**
```bash
cd E:\Vibe-Coding-AI\Ai-Agent
```

2. **Create a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Docker Installation

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access the application**
```
http://localhost:8000
```

3. **View logs**
```bash
docker-compose logs -f ai-agent
```

4. **Stop the application**
```bash
docker-compose down
```

## 📚 API Documentation

### Interactive API Docs
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Health Check
```
GET /api/v1/health
```
**Response**: Health status and version

#### Create Conversation
```
POST /api/v1/agent/conversation
Body: {
    "user_id": "user123",
    "title": "My Conversation"
}
```
**Response**: Conversation details with ID

#### Send Message
```
POST /api/v1/agent/message
Body: {
    "conversation_id": "conv_id",
    "content": "What is 5 plus 3?",
    "user_id": "user123"
}
```
**Response**: Agent response with tool usage

#### Get Conversation History
```
GET /api/v1/agent/conversation/{conversation_id}/history?limit=50
```
**Response**: Message history for conversation

#### List Available Tools
```
GET /api/v1/agent/tools
```
**Response**: Available tools and descriptions

#### Get Conversation Statistics
```
GET /api/v1/agent/conversation/{conversation_id}/stats
```
**Response**: Conversation statistics

## 💻 Code Examples

### Using the API with Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create conversation
conv_response = requests.post(
    f"{BASE_URL}/agent/conversation",
    json={"user_id": "user123", "title": "Test"}
)
conversation_id = conv_response.json()["id"]

# Send message
message_response = requests.post(
    f"{BASE_URL}/agent/message",
    json={
        "conversation_id": conversation_id,
        "content": "What is 10 plus 5?",
        "user_id": "user123"
    }
)
print(message_response.json()["response"])

# Get history
history = requests.get(
    f"{BASE_URL}/agent/conversation/{conversation_id}/history"
)
print(history.json()["messages"])
```

### Running the Test Suite

```bash
# Run all tests
pytest tests/test_agent.py -v

# Run specific test class
pytest tests/test_agent.py::TestCalculatorTool -v

# Run with coverage
pytest tests/test_agent.py --cov=src
```

### Using the API Testing Script

```bash
# Run comprehensive API tests
python examples/api_usage.py
```

## 🧪 Testing

### Test Coverage
- **Tool Tests**: All tool implementations
- **Agent Tests**: Intent analysis, tool selection, parameter extraction
- **API Tests**: Endpoint functionality and error handling
- **Integration Tests**: End-to-end conversation flow

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# App Configuration
APP_NAME=AI Agent System
DEBUG=True
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///./ai_agent.db

# Agent Configuration
MAX_CONVERSATION_HISTORY=50
AGENT_TIMEOUT=30
```

## 📊 Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(50),
    title VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    is_active BOOLEAN
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) FOREIGN KEY,
    role VARCHAR(20),
    content TEXT,
    tool_used VARCHAR(100),
    created_at DATETIME
);
```

### Agent Logs Table
```sql
CREATE TABLE agent_logs (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) FOREIGN KEY,
    action VARCHAR(100),
    tool_name VARCHAR(100),
    input_data TEXT,
    output_data TEXT,
    execution_time INTEGER,
    status VARCHAR(20),
    error_message TEXT,
    created_at DATETIME
);
```

## 🔐 Security Considerations

- Input validation using Pydantic
- Error messages don't expose internal details
- SQL injection prevention via SQLAlchemy ORM
- CORS configuration for API access
- Environment-based sensitive configuration
- Logging for audit trails

## 📈 Scalability Features

- Database abstraction for easy migration to PostgreSQL
- Repository pattern for data access
- Stateless API for horizontal scaling
- Connection pooling for database
- Logging with file rotation
- Tool registry for easy extension

## 🎓 Learning Outcomes

This project demonstrates:

1. **Software Architecture**
   - Clean architecture principles
   - Repository pattern
   - Dependency injection

2. **Python Best Practices**
   - Type hints
   - Exception handling
   - Logging configuration
   - Configuration management

3. **FastAPI Development**
   - REST API design
   - Request/Response validation
   - Error handling
   - Middleware

4. **Database Management**
   - SQLAlchemy ORM
   - Database migrations
   - Relationship modeling

5. **Testing**
   - Unit testing
   - Integration testing
   - Test fixtures
   - Mock objects

6. **DevOps**
   - Docker containerization
   - Docker Compose
   - Environment configuration

## 🚀 Future Enhancements

1. **Advanced Features**
   - LLM integration (OpenAI API)
   - Multi-user authentication
   - Real database (PostgreSQL)
   - Caching layer (Redis)
   - Queue system (Celery)

2. **ML Integration**
   - Intent classification model
   - Entity extraction
   - Sentiment analysis
   - Custom tool training

3. **Frontend**
   - Web UI (React/Vue)
   - Chat interface
   - Dashboard

4. **DevOps**
   - CI/CD pipeline
   - Kubernetes deployment
   - Monitoring (Prometheus/Grafana)
   - APM (Application Performance Monitoring)

## 📖 Documentation

- API documentation: Swagger UI at `/docs`
- Code comments throughout
- Example scripts in `examples/`
- Test cases as documentation

## 🤝 Contributing

To extend the system:

1. **Add a new tool**: Create a class in `src/agent/tools.py` extending `Tool`
2. **Add new routes**: Create file in `src/api/routes/`
3. **Add tests**: Update `tests/test_agent.py`
4. **Update docs**: Modify this README

## 📝 License

This is an educational project for student learning.

## 👨‍💼 Author

Built as a comprehensive AI agent system for learning software architecture and Python development.

## 📞 Support

For issues or questions:
1. Check the test suite for examples
2. Review API documentation at `/docs`
3. Check logs in `logs/ai_agent.log`

---

**Happy Learning! 🚀**

