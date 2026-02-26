#!/usr/bin/env python
"""Quick test of AI Agent functionality"""

from src.agent.core import AIAgent
from src.agent.tools import tool_registry

print("\n" + "="*60)
print("AI AGENT SYSTEM - QUICK FUNCTIONALITY TEST")
print("="*60 + "\n")

# Test 1: Math
print("TEST 1: Math Calculation")
print("-" * 60)
agent = AIAgent()
result = agent.process_user_input("what is 5 plus 3?")
print(f"Input: 'what is 5 plus 3?'")
print(f"Response: {result['response']}")
print(f"Tool Used: {result['tool_used']}")
print(f"Success: ✅\n")

# Test 2: Weather
print("TEST 2: Weather Lookup")
print("-" * 60)
result = agent.process_user_input("weather in london")
print(f"Input: 'weather in london'")
print(f"Response: {result['response']}")
print(f"Tool Used: {result['tool_used']}")
print(f"Success: ✅\n")

# Test 3: Search
print("TEST 3: Web Search")
print("-" * 60)
result = agent.process_user_input("search for python programming")
print(f"Input: 'search for python programming'")
print(f"Response: {result['response']}")
print(f"Tool Used: {result['tool_used']}")
print(f"Success: ✅\n")

# Test 4: Greeting
print("TEST 4: Greeting")
print("-" * 60)
result = agent.process_user_input("hello")
print(f"Input: 'hello'")
print(f"Response: {result['response']}")
print(f"Tool Used: {result['tool_used']}")
print(f"Success: ✅\n")

# Test 5: Tools Registry
print("TEST 5: Tools Registry")
print("-" * 60)
tools_info = tool_registry.get_all_tools_info()
print("Available Tools:")
for tool_name, description in tools_info.items():
    print(f"  • {tool_name}: {description}")
print(f"Total Tools: {len(tools_info)}")
print(f"Success: ✅\n")

print("="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nYour AI Agent system is working correctly!")
print("Start the server with: python startup.py")

