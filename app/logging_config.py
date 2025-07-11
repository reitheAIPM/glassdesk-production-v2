"""
Centralized logging configuration for GlassDesk
Follows the contributing guidelines for logging all errors and AI outputs
"""

import logging
import os
from datetime import datetime


def setup_logging():
    """Configure logging for the entire application"""

    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # File handler for glassdesk.log
            logging.FileHandler("glassdesk.log", mode="a"),
            # Console handler for development
            logging.StreamHandler(),
        ],
    )

    # Create application logger
    logger = logging.getLogger("glassdesk")
    logger.setLevel(logging.INFO)

    return logger


def log_ai_output(ai_model: str, prompt: str, response: str, metadata: dict = None):
    """Log AI interactions as specified in contributing guidelines"""
    logger = logging.getLogger("glassdesk.ai")

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": ai_model,
        "prompt": prompt,
        "response": response,
        "metadata": metadata or {},
    }

    logger.info(f"AI Output: {log_entry}")


def log_api_error(service: str, error: Exception, context: dict = None):
    """Log API errors with context"""
    logger = logging.getLogger("glassdesk.api")

    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "service": service,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {},
    }

    logger.error(f"API Error: {error_entry}")


def log_data_ingestion(
    source: str, record_count: int, success: bool, errors: list = None
):
    """Log data ingestion results"""
    logger = logging.getLogger("glassdesk.ingestion")

    ingestion_entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "record_count": record_count,
        "success": success,
        "errors": errors or [],
    }

    if success:
        logger.info(f"Data Ingestion Success: {ingestion_entry}")
    else:
        logger.error(f"Data Ingestion Failed: {ingestion_entry}")
