"""
Health check routes
"""

from fastapi import APIRouter, HTTPException
from src.config import settings
from src.api.schemas import HealthResponse
from src.logging_config import logger
from datetime import datetime

router = APIRouter()

@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        logger.info("Health check performed")
        return HealthResponse(
            status="healthy",
            version=settings.APP_VERSION,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

