"""
Example API usage and testing script
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

class APITester:
    """Helper class for testing API endpoints"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.conversation_id = None
        self.user_id = "student_user"

    def print_response(self, title: str, response: dict):
        """Pretty print response"""
        print(f"\n{'='*60}")
        print(f"📌 {title}")
        print(f"{'='*60}")
        print(json.dumps(response, indent=2, default=str))

    # ==================== Health & Tools ====================

    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.base_url}/health")
        self.print_response("Health Check", response.json())

    def list_available_tools(self):
        """List all available tools"""
        response = requests.get(f"{self.base_url}/agent/tools")
        self.print_response("Available Tools", response.json())
        return response.json()

    # ==================== Conversation Management ====================

    def create_conversation(self, title: str = "AI Agent Test Session"):
        """Create a new conversation"""
        payload = {
            "user_id": self.user_id,
            "title": title
        }
        response = requests.post(f"{self.base_url}/agent/conversation", json=payload)
        data = response.json()
        self.print_response("Create Conversation", data)
        self.conversation_id = data.get("id")
        return data

    def get_conversation(self):
        """Get conversation details"""
        response = requests.get(f"{self.base_url}/agent/conversation/{self.conversation_id}")
        self.print_response("Get Conversation", response.json())
        return response.json()

    def get_user_conversations(self):
        """Get all user conversations"""
        response = requests.get(f"{self.base_url}/agent/conversations/{self.user_id}")
        self.print_response("User Conversations", response.json())
        return response.json()

    # ==================== Message Processing ====================

    def send_message(self, content: str):
        """Send message to agent"""
        if not self.conversation_id:
            self.create_conversation()

        payload = {
            "conversation_id": self.conversation_id,
            "content": content,
            "user_id": self.user_id
        }
        response = requests.post(f"{self.base_url}/agent/message", json=payload)
        data = response.json()
        self.print_response(f"User: {content}", data)
        return data

    def get_conversation_history(self):
        """Get conversation history"""
        response = requests.get(f"{self.base_url}/agent/conversation/{self.conversation_id}/history")
        self.print_response("Conversation History", response.json())
        return response.json()

    def get_conversation_stats(self):
        """Get conversation statistics"""
        response = requests.get(f"{self.base_url}/agent/conversation/{self.conversation_id}/stats")
        self.print_response("Conversation Stats", response.json())
        return response.json()

    # ==================== Test Scenarios ====================

    def test_math_conversation(self):
        """Test math calculations"""
        print("\n" + "🔢 MATH CONVERSATION TEST".center(60, "="))
        self.create_conversation("Math Test Session")

        messages = [
            "What is 15 plus 25?",
            "Now multiply that result by 2",
            "Divide the result by 5"
        ]

        for msg in messages:
            self.send_message(msg)
            time.sleep(0.5)

    def test_weather_conversation(self):
        """Test weather lookups"""
        print("\n" + "🌤️  WEATHER CONVERSATION TEST".center(60, "="))
        self.create_conversation("Weather Test Session")

        messages = [
            "What's the weather in London?",
            "How about in New York?",
            "Tell me about Tokyo weather"
        ]

        for msg in messages:
            self.send_message(msg)
            time.sleep(0.5)

    def test_search_conversation(self):
        """Test web searches"""
        print("\n" + "🔍 SEARCH CONVERSATION TEST".center(60, "="))
        self.create_conversation("Search Test Session")

        messages = [
            "Search for information about Python",
            "What can you tell me about Machine Learning?",
            "Find info on Web Development"
        ]

        for msg in messages:
            self.send_message(msg)
            time.sleep(0.5)

    def test_greeting_and_help(self):
        """Test greeting and help"""
        print("\n" + "👋 GREETING & HELP TEST".center(60, "="))
        self.create_conversation("Help Test Session")

        self.send_message("Hi, what can you do?")
        time.sleep(0.5)
        self.send_message("Tell me about your capabilities")
        time.sleep(0.5)

    def run_all_tests(self):
        """Run all test scenarios"""
        print("\n" + "🤖 AI AGENT SYSTEM - COMPREHENSIVE TEST".center(60, "="))

        try:
            self.test_health_check()
            self.list_available_tools()
            self.test_greeting_and_help()
            self.test_math_conversation()
            self.test_weather_conversation()
            self.test_search_conversation()
            self.get_user_conversations()
            self.get_conversation_stats()

            print("\n" + "✅ ALL TESTS COMPLETED".center(60, "="))

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            print("Make sure the API server is running on http://localhost:8000")

# ==================== Example Usage ====================

if __name__ == "__main__":
    tester = APITester()

    # Run all tests
    tester.run_all_tests()

    # Or run individual tests:
    # tester.create_conversation("My First Conversation")
    # tester.send_message("What is 5 plus 3?")
    # tester.get_conversation_history()

