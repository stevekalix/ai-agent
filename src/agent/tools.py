"""
Tool execution module - Core tools available to the AI agent
"""

import json
import time
from typing import Dict, Any, Callable
from abc import ABC, abstractmethod
from src.logging_config import logger

class Tool(ABC):
    """Base class for all tools"""

    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool"""
        pass

class CalculatorTool(Tool):
    """Simple calculator tool"""

    name = "calculator"
    description = "Performs mathematical calculations (add, subtract, multiply, divide)"

    def execute(self, operation: str, a: float, b: float) -> Dict[str, Any]:
        """Execute calculator operation"""
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    raise ValueError("Cannot divide by zero")
                result = a / b
            else:
                raise ValueError(f"Unknown operation: {operation}")

            return {
                "success": True,
                "result": result,
                "operation": operation,
                "operands": {"a": a, "b": b}
            }
        except Exception as e:
            logger.error(f"Calculator error: {str(e)}")
            return {"success": False, "error": str(e)}

class WeatherLookupTool(Tool):
    """Weather lookup tool (simulated)"""

    name = "weather_lookup"
    description = "Looks up weather information for a given city"

    # Simulated weather data
    WEATHER_DATA = {
        "new york": {"temp": 72, "condition": "Partly Cloudy", "humidity": 65},
        "london": {"temp": 55, "condition": "Rainy", "humidity": 80},
        "tokyo": {"temp": 68, "condition": "Sunny", "humidity": 55},
        "paris": {"temp": 64, "condition": "Cloudy", "humidity": 70},
        "sydney": {"temp": 75, "condition": "Sunny", "humidity": 50},
    }

    def execute(self, city: str) -> Dict[str, Any]:
        """Get weather for a city"""
        try:
            city_lower = city.lower().strip()

            if city_lower in self.WEATHER_DATA:
                weather = self.WEATHER_DATA[city_lower]
                return {
                    "success": True,
                    "city": city,
                    "weather": weather
                }
            else:
                return {
                    "success": True,
                    "city": city,
                    "weather": {
                        "temp": 70,
                        "condition": "Unknown",
                        "humidity": 60
                    },
                    "note": "Weather data not available for this city"
                }
        except Exception as e:
            logger.error(f"Weather lookup error: {str(e)}")
            return {"success": False, "error": str(e)}

class WebSearchTool(Tool):
    """Web search tool (simulated)"""

    name = "web_search"
    description = "Searches the web for information on a given topic"

    # Simulated search results
    SEARCH_DATA = {
        "python": "Python is a high-level programming language known for simplicity and readability.",
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "machine learning": "Machine Learning is a subset of AI that enables systems to learn from data.",
        "web development": "Web development involves building and maintaining websites and web applications.",
    }

    def execute(self, query: str) -> Dict[str, Any]:
        """Search for information"""
        try:
            query_lower = query.lower().strip()

            # Find matching results
            results = []
            for key, value in self.SEARCH_DATA.items():
                if key in query_lower or query_lower in key:
                    results.append({"title": key.title(), "snippet": value})

            if not results:
                results.append({
                    "title": query,
                    "snippet": f"No specific results found for '{query}', but this could be researched further."
                })

            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            logger.error(f"Web search error: {str(e)}")
            return {"success": False, "error": str(e)}

class FileListTool(Tool):
    """File listing tool"""

    name = "file_list"
    description = "Lists files in a specified directory"

    def execute(self, directory: str = ".") -> Dict[str, Any]:
        """List files in directory"""
        try:
            import os

            if not os.path.isdir(directory):
                return {"success": False, "error": f"Directory not found: {directory}"}

            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                files.append({
                    "name": item,
                    "is_directory": os.path.isdir(item_path)
                })

            return {
                "success": True,
                "directory": directory,
                "files": files,
                "count": len(files)
            }
        except Exception as e:
            logger.error(f"File list error: {str(e)}")
            return {"success": False, "error": str(e)}

class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools"""
        self.register(CalculatorTool())
        self.register(WeatherLookupTool())
        self.register(WebSearchTool())
        self.register(FileListTool())
        logger.info(f"Registered {len(self.tools)} default tools")

    def register(self, tool: Tool):
        """Register a tool"""
        self.tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Tool:
        """Get a tool by name"""
        return self.tools.get(name)

    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool"""
        tool = self.get_tool(name)
        if not tool:
            return {"success": False, "error": f"Tool not found: {name}"}

        logger.info(f"Executing tool: {name} with params: {kwargs}")
        start_time = time.time()

        try:
            result = tool.execute(**kwargs)
            execution_time = int((time.time() - start_time) * 1000)
            result["execution_time_ms"] = execution_time
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_all_tools_info(self) -> Dict[str, str]:
        """Get info about all registered tools"""
        return {
            name: tool.description
            for name, tool in self.tools.items()
        }

# Global registry instance
tool_registry = ToolRegistry()

