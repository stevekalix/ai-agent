#!/usr/bin/env python
"""
Interactive CLI client for AI Agent System
Test the agent without using the API
"""

import sys
from pathlib import Path
from src.agent.core import conversation_manager
from src.agent.tools import tool_registry

def print_header():
    """Print welcome header"""
    print("\n" + "="*70)
    print("AI AGENT SYSTEM - INTERACTIVE CLI CLIENT".center(70))
    print("="*70)
    print("\nType 'help' for available commands")
    print("Type 'exit' to quit\n")

def print_help():
    """Print help information"""
    print("\nAvailable Commands:")
    print("-" * 70)
    print("  help              - Show this help message")
    print("  tools             - List available tools")
    print("  stats             - Show conversation statistics")
    print("  history           - Show conversation history")
    print("  clear             - Clear conversation history")
    print("  exit              - Exit the application")
    print("\nOr just type a message to chat with the agent!\n")

def print_tools():
    """Print available tools"""
    print("\nAvailable Tools:")
    print("-" * 70)
    tools_info = tool_registry.get_all_tools_info()
    for i, (name, desc) in enumerate(tools_info.items(), 1):
        print(f"  {i}. {name:<20} - {desc}")
    print()

def print_history():
    """Print conversation history"""
    context = conversation_manager.get_context()
    if not context:
        print("\nNo messages yet. Start chatting!\n")
        return

    print("\nConversation History:")
    print("-" * 70)
    for msg in context:
        role = "👤 You" if msg["role"] == "user" else "🤖 Agent"
        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"{role:12} | {content}")
    print()

def print_stats():
    """Print conversation statistics"""
    context = conversation_manager.get_context()
    user_msgs = sum(1 for m in context if m["role"] == "user")
    agent_msgs = sum(1 for m in context if m["role"] == "assistant")

    print("\nConversation Statistics:")
    print("-" * 70)
    print(f"  Total Messages    : {len(context)}")
    print(f"  User Messages     : {user_msgs}")
    print(f"  Agent Messages    : {agent_msgs}")
    print(f"  Available Tools   : {len(tool_registry.tools)}")
    print()

def format_response(result):
    """Format agent response for display"""
    response = result["response"]
    tool_used = result.get("tool_used")
    reasoning = result.get("reasoning")

    print("\n" + "-" * 70)
    print("Agent Response:")
    print("-" * 70)
    print(f"\n{response}\n")

    if tool_used:
        print(f"Tool Used: {tool_used}")
        print(f"Reasoning: {reasoning}")
    else:
        print(f"Reasoning: {reasoning}")

    print("-" * 70 + "\n")

def main():
    """Main CLI loop"""
    print_header()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "exit":
                print("\n👋 Goodbye!\n")
                break

            elif user_input.lower() == "help":
                print_help()

            elif user_input.lower() == "tools":
                print_tools()

            elif user_input.lower() == "history":
                print_history()

            elif user_input.lower() == "stats":
                print_stats()

            elif user_input.lower() == "clear":
                conversation_manager.clear_context()
                print("\n✅ Conversation history cleared.\n")

            else:
                # Process as user message
                print("\n⏳ Processing...", end="", flush=True)
                result = conversation_manager.process_message(user_input)
                print("\b" * 14 + " " * 14 + "\b" * 14, end="", flush=True)
                format_response(result)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break

        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            continue

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

