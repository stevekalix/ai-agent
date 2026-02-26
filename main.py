"""
AI Agent System - Main Application Entry Point
A comprehensive multi-tool intelligent agent system for educational purposes.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import settings
from src.api.routes import agent_routes, health_routes
from src.database.init_db import init_db
from src.logging_config import logger

# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("Starting AI Agent System")
    init_db()
    yield
    logger.info("Shutting down AI Agent System")

# Create FastAPI app
app = FastAPI(
    title="Intelligent Multi-Tool AI Agent",
    description="A comprehensive AI agent system with tool execution capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health_routes.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(agent_routes.router, prefix="/api/v1/agent", tags=["Agent"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

