# GlassDesk OAuth Setup Guide

> **AI AGENT**: This file contains all OAuth configuration and setup information. Reference this for OAuth-related tasks.

---

## 🎯 **OAUTH OVERVIEW**

### **Current Status**
- **Production**: ✅ **CONFIGURED** - Live at https://glassdesk-production.up.railway.app
- **Web OAuth**: ✅ **ACTIVE** - Google OAuth 2.0
- **Desktop OAuth**: ✅ **ACTIVE** - PKCE security enabled
- **Token Storage**: ✅ **SECURE** - Encrypted server-side storage

### **OAuth Providers**
1. **Google (Gmail)** - Primary authentication and data source
2. **Zoom** - Meeting data integration (Phase 2)
3. **Asana** - Task management integration (Phase 2)

---

## 🔐 **GOOGLE OAUTH CONFIGURATION**

### **Production Credentials**
```env
# Web Application OAuth
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI=https://glassdesk-production.up.railway.app/auth/google/callback

# Desktop Application OAuth (PKCE)
GOOGLE_DESKTOP_CLIENT_ID=YOUR_GOOGLE_DESKTOP_CLIENT_ID
GOOGLE_DESKTOP_CLIENT_SECRET=YOUR_GOOGLE_DESKTOP_CLIENT_SECRET
OAUTH_ENABLE_PKCE=true
OAUTH_DESKTOP_REDIRECT_URI=https://glassdesk-production.up.railway.app/auth/desktop/callback
```

### **Development Credentials**
```env
# Web Application OAuth
GOOGLE_CLIENT_ID=your_development_client_id
GOOGLE_CLIENT_SECRET=your_development_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Desktop Application OAuth
GOOGLE_DESKTOP_CLIENT_ID=your_desktop_client_id
GOOGLE_DESKTOP_CLIENT_SECRET=your_desktop_client_secret
OAUTH_ENABLE_PKCE=true
OAUTH_DESKTOP_REDIRECT_URI=http://localhost:3000/callback
```

---

## 🚀 **GOOGLE CLOUD CONSOLE SETUP**

### **Step 1: Create Project**
1. Go to https://console.cloud.google.com/
2. Create new project: "GlassDesk API"
3. Enable billing (required for API usage)

### **Step 2: Enable APIs**
```bash
# Required APIs
- Gmail API
- Google+ API
- Google OAuth2 API
```

### **Step 3: Create OAuth Credentials**

#### **Web Application OAuth**
1. Go to APIs & Services > Credentials
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Application type: "Web application"
4. Name: "GlassDesk Web OAuth"
5. Authorized redirect URIs:
   ```
   https://glassdesk-production.up.railway.app/auth/google/callback
   http://localhost:8000/auth/google/callback
   ```

#### **Desktop Application OAuth**
1. Create another OAuth 2.0 Client ID
2. Application type: "Desktop application"
3. Name: "GlassDesk Desktop OAuth"
4. No redirect URIs needed (PKCE handles this)

### **Step 4: Configure OAuth Consent Screen**
1. Go to OAuth consent screen
2. User type: "External"
3. App name: "GlassDesk"
4. User support email: [your email]
5. Developer contact information: [your email]
6. Scopes to add:
   ```
   https://www.googleapis.com/auth/gmail.readonly
   https://www.googleapis.com/auth/userinfo.email
   https://www.googleapis.com/auth/userinfo.profile
   ```

---

## 🔧 **OAUTH IMPLEMENTATION**

### **Enhanced OAuth Manager**
```python
# File: app/enhanced_oauth_manager.py
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.httpx_client import OAuth2Client

class EnhancedOAuthManager:
    def __init__(self):
        self.oauth = OAuth()
        self.setup_providers()
    
    def setup_providers(self):
        # Google OAuth configuration
        self.oauth.register(
            name='google',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
            server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
            client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/gmail.readonly'}
        )
```

### **OAuth Endpoints**
```python
# Web OAuth Flow
@router.get("/auth/google/login")
async def google_oauth_login(request: Request):
    redirect_uri = request.url_for('google_oauth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_oauth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    # Store token securely
    return {"message": "OAuth successful"}

# Desktop OAuth Flow (PKCE)
@router.get("/auth/desktop/login")
async def desktop_oauth_login(request: Request):
    # PKCE implementation
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    # Store code_verifier for later verification
```

---

## 🔒 **SECURITY CONSIDERATIONS**

### **PKCE (Proof Key for Code Exchange)**
```python
# Desktop OAuth with PKCE
import secrets
import base64
import hashlib

def generate_code_verifier():
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

def generate_code_challenge(code_verifier):
    sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
```

### **Token Storage Security**
```python
# Secure token storage
from cryptography.fernet import Fernet

class SecureTokenStorage:
    def __init__(self):
        self.cipher = Fernet(os.getenv('SECRET_KEY').encode())
    
    def store_token(self, user_id, provider, token_data):
        encrypted_token = self.cipher.encrypt(json.dumps(token_data).encode())
        # Store in database
        return encrypted_token
    
    def retrieve_token(self, user_id, provider):
        encrypted_token = # Get from database
        decrypted_token = self.cipher.decrypt(encrypted_token)
        return json.loads(decrypted_token.decode())
```

### **Token Refresh Logic**
```python
# Automatic token refresh
async def refresh_token_if_needed(user_id, provider):
    token_data = get_stored_token(user_id, provider)
    if is_token_expired(token_data):
        new_token = await refresh_oauth_token(token_data['refresh_token'])
        store_token(user_id, provider, new_token)
        return new_token
    return token_data
```

---

## 🧪 **TESTING OAUTH**

### **Production Testing**
```bash
# Test OAuth login
curl -L https://glassdesk-production.up.railway.app/auth/google/login

# Test callback handling
curl https://glassdesk-production.up.railway.app/auth/google/callback?code=test&state=test

# Test OAuth status
curl https://glassdesk-production.up.railway.app/auth/status
```

### **Development Testing**
```bash
# Start development server
uvicorn main:app --reload

# Test OAuth flow
python test_oauth.py

# Test with real Google account
# Visit: http://localhost:8000/auth/google/login
```

### **OAuth Test Script**
```python
# File: test_oauth.py
import requests

def test_oauth_flow():
    # Test OAuth endpoints
    base_url = "https://glassdesk-production.up.railway.app"
    
    # Test login endpoint
    response = requests.get(f"{base_url}/auth/google/login", allow_redirects=False)
    print(f"Login redirect: {response.status_code}")
    
    # Test callback endpoint
    response = requests.get(f"{base_url}/auth/google/callback?code=test&state=test")
    print(f"Callback response: {response.status_code}")
```

---

## 🔍 **TROUBLESHOOTING OAUTH**

### **Common Issues**

#### **Problem**: "redirect_uri_mismatch"
```bash
# Solution
1. Check Google Cloud Console redirect URIs
2. Verify environment variables
3. Ensure exact URI match (including protocol)
```

#### **Problem**: "invalid_client"
```bash
# Solution
1. Verify client ID and secret
2. Check OAuth consent screen configuration
3. Ensure APIs are enabled
```

#### **Problem**: "invalid_grant"
```bash
# Solution
1. Check token expiration
2. Verify refresh token logic
3. Test token refresh manually
```

### **Debugging Commands**
```bash
# Check OAuth configuration
python -c "import os; print('GOOGLE_CLIENT_ID:', os.getenv('GOOGLE_CLIENT_ID')[:20] + '...')"

# Test OAuth endpoints
curl -I https://glassdesk-production.up.railway.app/auth/google/login

# Check Railway environment variables
railway variables list | grep GOOGLE
```

---

## 📊 **OAUTH MONITORING**

### **Health Checks**
```bash
# OAuth health check
curl https://glassdesk-production.up.railway.app/auth/status

# Expected response
{
  "status": "healthy",
  "providers": {
    "google": "active",
    "zoom": "inactive",
    "asana": "inactive"
  }
}
```

### **Log Monitoring**
```bash
# Check OAuth logs
grep "oauth" logs/glassdesk.log
grep "google" logs/glassdesk.log

# Monitor Railway logs
railway logs | grep oauth
```

---

## 🔄 **OAUTH WORKFLOW**

### **Web OAuth Flow**
1. **User clicks login** → `/auth/google/login`
2. **Redirect to Google** → Google OAuth consent screen
3. **User authorizes** → Google redirects with code
4. **Callback processing** → `/auth/google/callback`
5. **Token exchange** → Exchange code for tokens
6. **Token storage** → Encrypt and store tokens
7. **Success response** → Redirect to success page

### **Desktop OAuth Flow (PKCE)**
1. **Generate PKCE** → Code verifier and challenge
2. **User clicks login** → `/auth/desktop/login`
3. **Redirect to Google** → With code challenge
4. **User authorizes** → Google redirects with code
5. **Callback processing** → `/auth/desktop/callback`
6. **Token exchange** → With code verifier
7. **Token storage** → Encrypt and store tokens
8. **Success response** → Return to desktop app

---

## 📚 **OAUTH RESOURCES**

### **Documentation**
- **Google OAuth 2.0**: https://developers.google.com/identity/protocols/oauth2
- **Authlib Documentation**: https://authlib.org/
- **PKCE Specification**: https://tools.ietf.org/html/rfc7636

### **Related Files**
- **OAuth Manager**: `app/enhanced_oauth_manager.py`
- **OAuth Routes**: `app/routes/auth.py`
- **OAuth Tests**: `test_oauth.py`
- **Environment**: `.env` and Railway variables

---

*Last Updated: 2024-07-11*
*AI Agent: Use this guide for all OAuth-related tasks and troubleshooting* 