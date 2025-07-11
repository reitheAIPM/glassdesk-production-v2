"""
Minimal GlassDesk FastAPI Application for Railway Testing
"""

from fastapi import FastAPI
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GlassDesk API (Minimal)",
    description="Minimal test version",
    version="1.0.0-minimal",
)

@app.get("/")
async def root():
    """Root endpoint - API status"""
    logger.info("Root endpoint accessed")
    return {
        "message": "GlassDesk API is running! 🚀 (Minimal Version)",
        "version": "1.0.0-minimal",
        "status": "healthy",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    logger.info("Health check accessed")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "glassdesk-api-minimal",
    }

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    logger.info("Test endpoint accessed")
    return {
        "test": "success",
        "message": "This is a test endpoint",
        "timestamp": datetime.now().isoformat(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 