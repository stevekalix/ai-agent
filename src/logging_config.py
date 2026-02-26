"""
Logging configuration for the AI Agent System
"""

import logging
import logging.handlers
from pathlib import Path
from src.config import settings

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure root logger
logger = logging.getLogger("ai_agent")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# File handler
file_handler = logging.handlers.RotatingFileHandler(
    log_dir / "ai_agent.log",
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

