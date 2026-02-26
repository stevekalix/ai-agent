#!/usr/bin/env python
"""
Startup script for AI Agent System
Handles initialization and application startup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_virtual_env():
    """Check if virtual environment is activated"""
    if sys.prefix == sys.base_prefix:
        print("⚠️  Virtual environment not detected!")
        print("Please activate virtual environment:")
        print("  Windows: venv\\Scripts\\activate")
        print("  Linux/Mac: source venv/bin/activate")
        return False
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def initialize_database():
    """Initialize the database"""
    try:
        from src.database.init_db import init_db
        print("🗄️  Initializing database...")
        init_db()
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def create_logs_directory():
    """Create logs directory if it doesn't exist"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    print(f"📁 Logs directory ready: {log_dir.absolute()}")

def start_server():
    """Start the FastAPI server"""
    print("\n" + "="*60)
    print("🚀 Starting AI Agent System...")
    print("="*60)
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔄 ReDoc: http://localhost:8000/redoc")
    print("="*60 + "\n")

    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutdown requested")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

def main():
    """Main startup routine"""
    print("\n" + "="*60)
    print("AI AGENT SYSTEM - STARTUP")
    print("="*60 + "\n")

    # Check virtual environment
    if not check_virtual_env():
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Create logs directory
    create_logs_directory()

    # Initialize database
    if not initialize_database():
        sys.exit(1)

    # Start server
    start_server()

if __name__ == "__main__":
    main()

