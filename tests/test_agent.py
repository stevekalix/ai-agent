"""
Unit and integration tests for AI Agent System
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from src.agent.core import AIAgent, ConversationManager
from src.agent.tools import tool_registry
from src.database.models import Base
from src.database.init_db import SessionLocal, engine

# Test client
client = TestClient(app)

# ==================== Tool Tests ====================

class TestCalculatorTool:
    """Test calculator tool"""

    def test_add(self):
        result = tool_registry.execute_tool("calculator", operation="add", a=5, b=3)
        assert result["success"] == True
        assert result["result"] == 8

    def test_subtract(self):
        result = tool_registry.execute_tool("calculator", operation="subtract", a=10, b=4)
        assert result["success"] == True
        assert result["result"] == 6

    def test_multiply(self):
        result = tool_registry.execute_tool("calculator", operation="multiply", a=6, b=7)
        assert result["success"] == True
        assert result["result"] == 42

    def test_divide(self):
        result = tool_registry.execute_tool("calculator", operation="divide", a=10, b=2)
        assert result["success"] == True
        assert result["result"] == 5

    def test_divide_by_zero(self):
        result = tool_registry.execute_tool("calculator", operation="divide", a=10, b=0)
        assert result["success"] == False
        assert "divide by zero" in result["error"].lower()

class TestWeatherTool:
    """Test weather lookup tool"""

    def test_weather_known_city(self):
        result = tool_registry.execute_tool("weather_lookup", city="new york")
        assert result["success"] == True
        assert "weather" in result
        assert "temp" in result["weather"]

    def test_weather_unknown_city(self):
        result = tool_registry.execute_tool("weather_lookup", city="unknown_city_xyz")
        assert result["success"] == True

class TestWebSearchTool:
    """Test web search tool"""

    def test_search_python(self):
        result = tool_registry.execute_tool("web_search", query="python")
        assert result["success"] == True
        assert "results" in result
        assert len(result["results"]) > 0

    def test_search_ai(self):
        result = tool_registry.execute_tool("web_search", query="artificial intelligence")
        assert result["success"] == True
        assert "results" in result

class TestFileListTool:
    """Test file list tool"""

    def test_list_current_directory(self):
        result = tool_registry.execute_tool("file_list", directory=".")
        assert result["success"] == True
        assert "files" in result
        assert "count" in result

# ==================== Agent Tests ====================

class TestAIAgent:
    """Test AI Agent core logic"""

    def setup_method(self):
        """Setup for each test"""
        self.agent = AIAgent()

    def test_agent_initialization(self):
        assert self.agent.name == "IntelliBot"
        assert self.agent.tools is not None

    def test_intent_analysis_math(self):
        intent = self.agent._analyze_intent("calculate 5 plus 3")
        assert intent == "math"

    def test_intent_analysis_weather(self):
        intent = self.agent._analyze_intent("what's the weather in london")
        assert intent == "weather"

    def test_intent_analysis_search(self):
        intent = self.agent._analyze_intent("search for information about python")
        assert intent == "search"

    def test_tool_selection(self):
        tool = self.agent._select_tool("math", "calculate 5 + 3")
        assert tool == "calculator"

    def test_parameter_extraction_calculator(self):
        params = self.agent._extract_parameters("add 5 and 3", "calculator")
        assert params["a"] == 5
        assert params["b"] == 3
        assert params["operation"] == "add"

    def test_process_user_input(self):
        result = self.agent.process_user_input("what is 5 plus 3")
        assert "response" in result
        assert "tool_used" in result
        assert result["tool_used"] == "calculator"

    def test_greeting(self):
        result = self.agent.process_user_input("hello")
        assert "response" in result
        assert result["tool_used"] is None

class TestConversationManager:
    """Test conversation manager"""

    def setup_method(self):
        """Setup for each test"""
        self.manager = ConversationManager()

    def test_add_to_context(self):
        self.manager.add_to_context("user", "Hello")
        assert len(self.manager.agent.conversation_context) == 1
        assert self.manager.agent.conversation_context[0]["role"] == "user"

    def test_process_message(self):
        response = self.manager.process_message("what is 10 plus 5")
        assert response["response"] is not None
        assert len(self.manager.agent.conversation_context) == 2

    def test_get_context(self):
        self.manager.add_to_context("user", "Test message")
        context = self.manager.get_context()
        assert len(context) == 1
        assert context[0]["content"] == "Test message"

    def test_clear_context(self):
        self.manager.add_to_context("user", "Message 1")
        self.manager.add_to_context("user", "Message 2")
        self.manager.clear_context()
        assert len(self.manager.agent.conversation_context) == 0

# ==================== API Tests ====================

class TestAPIEndpoints:
    """Test API endpoints"""

    def test_health_check(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_list_tools(self):
        response = client.get("/api/v1/agent/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert data["total_tools"] > 0

    def test_create_conversation(self):
        response = client.post(
            "/api/v1/agent/conversation",
            json={"user_id": "test_user", "title": "Test Conversation"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["user_id"] == "test_user"
        assert data["title"] == "Test Conversation"

    def test_process_message(self):
        # Create conversation first
        conv_response = client.post(
            "/api/v1/agent/conversation",
            json={"user_id": "test_user", "title": "Test"}
        )
        conversation_id = conv_response.json()["id"]

        # Process message
        response = client.post(
            "/api/v1/agent/message",
            json={
                "conversation_id": conversation_id,
                "content": "calculate 5 plus 3",
                "user_id": "test_user"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["tool_used"] == "calculator"

    def test_get_conversation_history(self):
        # Create conversation
        conv_response = client.post(
            "/api/v1/agent/conversation",
            json={"user_id": "test_user", "title": "Test"}
        )
        conversation_id = conv_response.json()["id"]

        # Add message
        client.post(
            "/api/v1/agent/message",
            json={
                "conversation_id": conversation_id,
                "content": "hello",
                "user_id": "test_user"
            }
        )

        # Get history
        response = client.get(f"/api/v1/agent/conversation/{conversation_id}/history")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert data["total_messages"] > 0

    def test_invalid_conversation_id(self):
        response = client.get("/api/v1/agent/conversation/invalid_id")
        assert response.status_code == 404

# ==================== Run Tests ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

