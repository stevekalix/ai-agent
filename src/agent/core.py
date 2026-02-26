"""
Core AI Agent logic and decision-making
"""

import json
import re
from typing import Dict, Any, List, Tuple
from src.logging_config import logger
from src.agent.tools import tool_registry

class AIAgent:
    """Main AI Agent class"""

    def __init__(self):
        self.name = "IntelliBot"
        self.tools = tool_registry
        self.conversation_context = []
        self.max_context = 50

    def process_user_input(self, user_message: str) -> Dict[str, Any]:
        """
        Process user input and generate response
        Returns: {
            "response": str,
            "tool_used": str or None,
            "tool_input": dict or None,
            "tool_output": dict or None,
            "reasoning": str
        }
        """
        logger.info(f"Processing user input: {user_message[:100]}...")

        # Analyze user intent
        intent = self._analyze_intent(user_message)
        logger.debug(f"Detected intent: {intent}")

        # Decide if tool is needed
        tool_to_use = self._select_tool(intent, user_message)

        if tool_to_use:
            logger.info(f"Selected tool: {tool_to_use}")
            # Extract parameters
            params = self._extract_parameters(user_message, tool_to_use)

            # Execute tool
            tool_output = self.tools.execute_tool(tool_to_use, **params)

            # Generate response based on tool output
            response = self._generate_response(user_message, tool_to_use, tool_output, intent)

            return {
                "response": response,
                "tool_used": tool_to_use,
                "tool_input": params,
                "tool_output": tool_output,
                "reasoning": f"Used {tool_to_use} tool to answer your question"
            }
        else:
            # Generate response without tool
            response = self._generate_direct_response(user_message, intent)
            return {
                "response": response,
                "tool_used": None,
                "tool_input": None,
                "tool_output": None,
                "reasoning": "Processed without external tools"
            }

    def _analyze_intent(self, message: str) -> str:
        """Analyze user intent from message"""
        message_lower = message.lower()

        # Intent keywords mapping
        intent_keywords = {
            "math": ["calculate", "compute", "add", "subtract", "multiply", "divide", "math", "+", "-", "*", "/"],
            "weather": ["weather", "temperature", "climate", "rain", "sunny", "cloudy"],
            "search": ["search", "find", "look for", "tell me about", "what is", "how does"],
            "file": ["file", "directory", "list", "folder"],
            "greeting": ["hello", "hi", "hey", "greetings"],
            "help": ["help", "what can you do", "capabilities", "tools"],
        }

        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent

        return "general"

    def _select_tool(self, intent: str, message: str) -> str or None:
        """Select appropriate tool based on intent"""
        tool_selection = {
            "math": "calculator",
            "weather": "weather_lookup",
            "search": "web_search",
            "file": "file_list",
        }

        return tool_selection.get(intent)

    def _extract_parameters(self, message: str, tool_name: str) -> Dict[str, Any]:
        """Extract parameters for tool execution"""
        params = {}

        if tool_name == "calculator":
            # Extract numbers and operation
            numbers = re.findall(r'-?\d+\.?\d*', message)
            if len(numbers) >= 2:
                params["a"] = float(numbers[0])
                params["b"] = float(numbers[1])

            # Detect operation
            if "add" in message.lower() or "+" in message:
                params["operation"] = "add"
            elif "subtract" in message.lower() or "-" in message:
                params["operation"] = "subtract"
            elif "multiply" in message.lower() or "*" in message:
                params["operation"] = "multiply"
            elif "divide" in message.lower() or "/" in message:
                params["operation"] = "divide"
            else:
                params["operation"] = "add"

        elif tool_name == "weather_lookup":
            # Extract city name
            cities = ["new york", "london", "tokyo", "paris", "sydney", "berlin", "toronto", "mumbai"]
            for city in cities:
                if city in message.lower():
                    params["city"] = city
                    break
            if not params:
                # Try to extract any word as city
                words = message.split()
                if len(words) > 0:
                    params["city"] = words[-1]

        elif tool_name == "web_search":
            # Use the entire message as search query
            params["query"] = message.replace("search", "").replace("find", "").strip()

        elif tool_name == "file_list":
            # Extract directory path
            params["directory"] = "."

        return params

    def _generate_response(self, user_message: str, tool_used: str, tool_output: Dict, intent: str) -> str:
        """Generate human-friendly response based on tool output"""

        if not tool_output.get("success"):
            return f"I encountered an error while using the {tool_used} tool: {tool_output.get('error', 'Unknown error')}"

        if tool_used == "calculator":
            op = tool_output.get("operation", "")
            result = tool_output.get("result", "")
            a = tool_output.get("operands", {}).get("a", "")
            b = tool_output.get("operands", {}).get("b", "")
            return f"The result of {a} {op} {b} is {result}"

        elif tool_used == "weather_lookup":
            city = tool_output.get("city", "")
            weather = tool_output.get("weather", {})
            return f"Weather in {city}: {weather.get('condition', 'Unknown')}, Temperature: {weather.get('temp', 'N/A')}°F, Humidity: {weather.get('humidity', 'N/A')}%"

        elif tool_used == "web_search":
            query = tool_output.get("query", "")
            results = tool_output.get("results", [])
            response = f"Search results for '{query}':\n"
            for i, result in enumerate(results[:3], 1):
                response += f"{i}. {result.get('title')}: {result.get('snippet')}\n"
            return response.strip()

        elif tool_used == "file_list":
            directory = tool_output.get("directory", ".")
            files = tool_output.get("files", [])
            response = f"Files in {directory}:\n"
            for file in files[:10]:
                file_type = "[DIR]" if file.get("is_directory") else "[FILE]"
                response += f"  {file_type} {file.get('name')}\n"
            return response.strip()

        return f"Tool {tool_used} executed successfully"

    def _generate_direct_response(self, message: str, intent: str) -> str:
        """Generate response without using tools"""

        if intent == "greeting":
            greetings = [
                "Hello! I'm IntelliBot, your AI assistant. How can I help you?",
                "Hi there! What can I do for you today?",
                "Greetings! I'm ready to assist you."
            ]
            return greetings[hash(message) % len(greetings)]

        elif intent == "help":
            tools_info = self.tools.get_all_tools_info()
            response = "I can help you with the following:\n"
            for tool_name, description in tools_info.items():
                response += f"• {tool_name}: {description}\n"
            return response.strip()

        else:
            return "I understand your question. I can assist you better if you ask me to search, calculate, check weather, or list files. Type 'help' to see my capabilities."

class ConversationManager:
    """Manages conversation state and history"""

    def __init__(self):
        self.agent = AIAgent()

    def add_to_context(self, role: str, content: str):
        """Add message to conversation context"""
        self.agent.conversation_context.append({
            "role": role,
            "content": content
        })

        # Keep context size manageable
        if len(self.agent.conversation_context) > self.agent.max_context:
            self.agent.conversation_context = self.agent.conversation_context[-self.agent.max_context:]

    def process_message(self, user_message: str) -> Dict[str, Any]:
        """Process user message and maintain context"""
        # Add user message to context
        self.add_to_context("user", user_message)

        # Get agent response
        agent_response = self.agent.process_user_input(user_message)

        # Add agent response to context
        self.add_to_context("assistant", agent_response["response"])

        return agent_response

    def get_context(self) -> List[Dict[str, str]]:
        """Get current conversation context"""
        return self.agent.conversation_context

    def clear_context(self):
        """Clear conversation context"""
        self.agent.conversation_context = []

# Global conversation manager
conversation_manager = ConversationManager()

