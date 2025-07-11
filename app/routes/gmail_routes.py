"""
Gmail API Routes for GlassDesk

Real Gmail API integration endpoints for fetching and processing emails.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

# Import with error handling
try:
    from ..gmail_integration import gmail_integration
    gmail_integration_available = True
except Exception as e:
    gmail_integration_available = False
    gmail_integration = None
    logging.getLogger(__name__).warning(f"Gmail integration not available: {e}")

try:
    from ..enhanced_oauth_manager import enhanced_oauth_manager
    oauth_manager_available = True
except Exception as e:
    oauth_manager_available = False
    enhanced_oauth_manager = None
    logging.getLogger(__name__).warning(f"Enhanced OAuth manager not available: {e}")

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gmail", tags=["gmail"])

def _check_services():
    """Check if required services are available"""
    if not oauth_manager_available:
        raise HTTPException(
            status_code=503,
            detail="OAuth service temporarily unavailable. Please check server configuration."
        )
    if not gmail_integration_available:
        raise HTTPException(
            status_code=503,
            detail="Gmail integration service temporarily unavailable. Please check server configuration."
        )

@router.get("/status")
async def gmail_status():
    """Check Gmail OAuth status and connectivity"""
    try:
        if not oauth_manager_available:
            return {
                "status": "service_unavailable",
                "message": "OAuth service temporarily unavailable",
                "authenticated": False
            }
        
        # Check if user is authenticated with Gmail
        tokens = enhanced_oauth_manager.token_manager.get_tokens("google")
        
        if not tokens:
            return {
                "status": "not_authenticated",
                "message": "Gmail access not configured. Please authenticate first.",
                "authenticated": False
            }
        
        return {
            "status": "authenticated",
            "message": "Gmail access is configured and ready.",
            "authenticated": True,
            "has_access_token": bool(tokens.get("access_token")),
            "has_refresh_token": bool(tokens.get("refresh_token"))
        }
        
    except Exception as e:
        logger.error(f"Error checking Gmail status: {e}")
        raise HTTPException(status_code=500, detail=f"Error checking Gmail status: {str(e)}")


@router.post("/fetch-emails")
async def fetch_gmail_emails(max_results: Optional[int] = Query(50, description="Maximum number of emails to fetch")):
    """Fetch real emails from Gmail API"""
    _check_services()
    try:
        # Check authentication first
        tokens = enhanced_oauth_manager.token_manager.get_tokens("google")
        if not tokens:
            raise HTTPException(
                status_code=401, 
                detail="Gmail access not configured. Please authenticate with Gmail first."
            )
        
        # Fetch emails using real Gmail API
        emails = gmail_integration.get_user_emails(max_results=max_results)
        
        return {
            "success": True,
            "message": f"Successfully fetched {len(emails)} emails from Gmail",
            "email_count": len(emails),
            "emails": emails[:5] if emails else []  # Return first 5 emails for preview
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching Gmail emails: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching emails: {str(e)}")


@router.post("/process-emails")
async def process_gmail_emails(max_results: Optional[int] = Query(50, description="Maximum number of emails to process")):
    """Fetch and process real Gmail data"""
    _check_services()
    try:
        # Check authentication first
        tokens = enhanced_oauth_manager.token_manager.get_tokens("google")
        if not tokens:
            raise HTTPException(
                status_code=401, 
                detail="Gmail access not configured. Please authenticate with Gmail first."
            )
        
        # Process emails using real Gmail API
        processed_data = gmail_integration.process_gmail_data(max_results=max_results)
        
        return {
            "success": True,
            "message": "Successfully processed Gmail data",
            "processed_data": processed_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing Gmail data: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Gmail data: {str(e)}")


@router.get("/test-connection")
async def test_gmail_connection():
    """Test Gmail API connection and authentication"""
    try:
        if not oauth_manager_available:
            return {
                "status": "service_unavailable",
                "message": "OAuth service temporarily unavailable",
                "authenticated": False,
                "connection_test": "failed"
            }
        
        # Check authentication
        tokens = enhanced_oauth_manager.token_manager.get_tokens("google")
        if not tokens:
            return {
                "status": "not_authenticated",
                "message": "Gmail access not configured",
                "authenticated": False
            }
        
        if not gmail_integration_available:
            return {
                "status": "service_unavailable",
                "message": "Gmail integration service temporarily unavailable",
                "authenticated": True,
                "connection_test": "failed"
            }
        
        # Test fetching a small number of emails
        emails = gmail_integration.get_user_emails(max_results=1)
        
        return {
            "status": "connected",
            "message": "Gmail API connection successful",
            "authenticated": True,
            "connection_test": "passed",
            "email_count": len(emails)
        }
        
    except Exception as e:
        logger.error(f"Error testing Gmail connection: {e}")
        return {
            "status": "error",
            "message": f"Gmail API connection failed: {str(e)}",
            "authenticated": bool(tokens) if 'tokens' in locals() else False,
            "connection_test": "failed"
        } 