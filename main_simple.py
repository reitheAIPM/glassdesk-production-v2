"""
Simple GlassDesk FastAPI Application for Railway Testing
Bypasses all complex imports to isolate the issue
"""

from fastapi import FastAPI
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GlassDesk API (Simple)",
    description="Simple test version without complex imports",
    version="1.0.0-simple",
)

@app.get("/")
async def root():
    """Root endpoint - API status"""
    logger.info("Root endpoint accessed")
    return {
        "message": "GlassDesk API is running! 🚀 (Simple Version)",
        "version": "1.0.0-simple",
        "status": "healthy",
        "note": "Complex imports bypassed for testing"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    logger.info("Health check accessed")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "glassdesk-api-simple",
        "note": "Basic FastAPI working"
    }

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    logger.info("Test endpoint accessed")
    return {
        "test": "success",
        "message": "This is a test endpoint",
        "timestamp": datetime.now().isoformat(),
        "note": "No complex dependencies"
    }

@app.get("/debug")
async def debug_info():
    """Debug information"""
    import os
    return {
        "environment_variables": {
            "SECRET_KEY": "SET" if os.getenv("SECRET_KEY") else "NOT SET",
            "OPENAI_API_KEY": "SET" if os.getenv("OPENAI_API_KEY") else "NOT SET",
            "GOOGLE_CLIENT_ID": "SET" if os.getenv("GOOGLE_CLIENT_ID") else "NOT SET",
            "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT", "NOT SET"),
            "PORT": os.getenv("PORT", "NOT SET"),
        },
        "python_version": "3.12",
        "fastapi_version": "0.104.1",
        "note": "Debug information for deployment troubleshooting"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 