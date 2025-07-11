"""
OAuth Authentication Routes for GlassDesk
Handles Gmail, Zoom, and Asana OAuth flows using EnhancedOAuthManager
"""

from fastapi import APIRouter, HTTPException, Request, Response, Query
from fastapi.responses import RedirectResponse
import logging
from typing import Optional
from app.enhanced_oauth_manager import enhanced_oauth_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

def _check_oauth_manager():
    """Check if OAuth manager is available"""
    if enhanced_oauth_manager is None:
        raise HTTPException(
            status_code=503, 
            detail="OAuth service temporarily unavailable. Please check server configuration."
        )

# --- GOOGLE OAUTH (WEB) ---
@router.get("/google/login")
async def google_login():
    """Initiate Google OAuth flow for Gmail access (web)"""
    _check_oauth_manager()
    try:
        result = await enhanced_oauth_manager.initiate_oauth_flow("google", is_desktop=False)
        return RedirectResponse(url=result["auth_url"])
    except Exception as e:
        logger.error(f"Error initiating Google OAuth: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Google OAuth flow")

@router.get("/google/callback")
async def google_callback(code: str = Query(...), state: Optional[str] = None):
    """Handle Google OAuth callback and exchange code for tokens (web)"""
    _check_oauth_manager()
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    try:
        result = await enhanced_oauth_manager.handle_oauth_callback("google", code, state, is_desktop=False)
        return result
    except Exception as e:
        logger.error(f"Error handling Google OAuth callback: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete OAuth flow")

# --- GOOGLE OAUTH (DESKTOP/PKCE) ---
@router.get("/google/desktop/login")
async def google_desktop_login():
    """Initiate Google OAuth flow for Gmail access (desktop/PKCE)"""
    _check_oauth_manager()
    try:
        result = await enhanced_oauth_manager.initiate_oauth_flow("google", is_desktop=True)
        return {"auth_url": result["auth_url"]}
    except Exception as e:
        logger.error(f"Error initiating Google Desktop OAuth: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Google Desktop OAuth flow")

@router.get("/google/desktop/callback")
async def google_desktop_callback(code: str = Query(...), state: Optional[str] = None):
    """Handle Google OAuth callback and exchange code for tokens (desktop/PKCE)"""
    _check_oauth_manager()
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    try:
        result = await enhanced_oauth_manager.handle_oauth_callback("google", code, state, is_desktop=True)
        return result
    except Exception as e:
        logger.error(f"Error handling Google Desktop OAuth callback: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete Desktop OAuth flow")

# --- STATUS & LOGOUT ---
@router.get("/status")
async def auth_status():
    """Check authentication status for all services"""
    if enhanced_oauth_manager is None:
        return {
            "status": "OAuth service unavailable",
            "providers": {
                "google": {"configured": False, "connected": False, "oauth_flow": True},
                "zoom": {"configured": False, "connected": False, "oauth_flow": True},
                "asana": {"configured": False, "connected": False, "oauth_flow": False}
            }
        }
    return enhanced_oauth_manager.get_provider_status()

@router.post("/logout")
async def logout():
    """Logout and revoke access tokens"""
    _check_oauth_manager()
    providers = ["google", "zoom", "asana"]
    revoked = []
    for provider in providers:
        if enhanced_oauth_manager.token_manager.revoke_tokens(provider):
            revoked.append(provider)
    logger.info(f"User logged out, revoked tokens for: {revoked}")
    return {"message": "Logged out successfully", "revoked_providers": revoked}
