# GlassDesk FastAPI Application
# Based on research/railway_deployment.md patterns

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import logging

# Import routes
from app.routes.auth import router as auth_router
from app.routes.test_routes import router as test_router
from app.routes.gmail_routes import router as gmail_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting GlassDesk Backend...")
    print("🚀 Starting GlassDesk Backend...")
    yield
    # Shutdown
    logger.info("🛑 Shutting down GlassDesk Backend...")
    print("🛑 Shutting down GlassDesk Backend...")


app = FastAPI(
    title="GlassDesk API",
    description="Privacy-first AI assistant for work data",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://glassdesk.vercel.app",  # Production frontend
        "http://localhost:3000",  # Development frontend
        "http://localhost:8000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "GlassDesk API is running! 🚀",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "glassdesk-api",
    }


@app.get("/api/status")
async def api_status():
    """API status with more details"""
    return {
        "service": "GlassDesk API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "oauth": "planned",
            "gmail": "planned",
            "zoom": "planned",
            "asana": "planned",
            "ai_processing": "planned",
        },
    }


# Include routes
app.include_router(auth_router)
app.include_router(test_router)
app.include_router(gmail_router)

# TODO: Add Gmail API routes
# TODO: Add Zoom API routes
# TODO: Add Asana API routes
# TODO: Add AI processing routes

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
