# GlassDesk Setup Guide

> **AI AGENT**: This file contains all setup and configuration instructions. Update when setup procedures change.

---

## 🚀 **QUICK START**

### **For AI Agents**
1. **Read**: `docs/README.md` (master index)
2. **Check**: `docs/PROJECT_STATUS.md` (current state)
3. **Follow**: `docs/CONTRIBUTING.md` (development guidelines)

### **For Users**
1. **Production**: https://glassdesk-production.up.railway.app
2. **OAuth Login**: https://glassdesk-production.up.railway.app/auth/google/login
3. **API Docs**: https://glassdesk-production.up.railway.app/docs

---

## 🔧 **DEVELOPMENT ENVIRONMENT SETUP**

### **Prerequisites**
- Python 3.11+ (3.13 recommended)
- Git
- Virtual environment tool

### **Local Setup**
```bash
# Clone repository
git clone <repository-url>
cd glassdesk

# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup development environment
python setup_dev.py

# Run tests
python -m pytest tests/ -v

# Start development server
uvicorn main:app --reload
```

### **Environment Variables**
Copy `env_template.env` to `.env` and configure:
```env
# OAuth Configuration
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# AI Configuration
OPENAI_API_KEY=your_openai_api_key

# Security
SECRET_KEY=your_generated_secret_key

# Database
DATABASE_URL=sqlite:///./glassdesk.db

# Environment
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 🚀 **PRODUCTION DEPLOYMENT**

### **Railway Deployment**
- **Status**: ✅ **LIVE**
- **URL**: https://glassdesk-production.up.railway.app
- **Platform**: Railway
- **Environment**: Production

### **Environment Variables (Production)**
```env
# OAuth Configuration
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI=https://glassdesk-production.up.railway.app/auth/google/callback

GOOGLE_DESKTOP_CLIENT_ID=YOUR_GOOGLE_DESKTOP_CLIENT_ID
GOOGLE_DESKTOP_CLIENT_SECRET=YOUR_GOOGLE_DESKTOP_CLIENT_SECRET
OAUTH_ENABLE_PKCE=true
OAUTH_DESKTOP_REDIRECT_URI=https://glassdesk-production.up.railway.app/auth/desktop/callback

# AI Configuration
OPENAI_API_KEY=sk-... # Configured

# Security
SECRET_KEY=... # Generated

# Database
DATABASE_URL=postgresql://... # Railway managed

# Environment
LOG_LEVEL=INFO
ENVIRONMENT=production
```

---

## 🔐 **OAUTH CONFIGURATION**

### **Google Cloud Console Setup**
1. **Create Project**: https://console.cloud.google.com/
2. **Enable APIs**: Gmail API, Google+ API
3. **Create Credentials**: OAuth 2.0 Client IDs
4. **Configure Redirect URIs**:

#### **Development URIs**
```
http://localhost:8000/auth/google/callback
http://localhost:3000/callback
```

#### **Production URIs**
```
https://glassdesk-production.up.railway.app/auth/google/callback
https://glassdesk-production.up.railway.app/auth/desktop/callback
```

### **OAuth Client Types**
- **Web Application**: For web interface
- **Desktop Application**: For desktop client (with PKCE)

---

## 🧪 **TESTING SETUP**

### **Run All Tests**
```bash
# Run test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_enhanced_features.py -v
```

### **Sandbox Testing**
```bash
# Run enhanced sandbox
python sandbox/enhanced_sandbox.py

# Test specific components
python sandbox/test_oauth.py
python sandbox/test_ai.py
```

### **API Testing**
```bash
# Test health endpoint
curl https://glassdesk-production.up.railway.app/health

# Test OAuth login
curl https://glassdesk-production.up.railway.app/auth/google/login

# Test AI query
curl -X POST https://glassdesk-production.up.railway.app/api/test/ai/enhanced_query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

---

## 📊 **MONITORING SETUP**

### **Health Checks**
- **Production**: https://glassdesk-production.up.railway.app/health
- **Development**: http://localhost:8000/health

### **Logs**
- **Development**: `logs/glassdesk.log`
- **Production**: Railway dashboard logs

### **Metrics**
- **Response Time**: < 2 seconds
- **Error Rate**: < 1%
- **Uptime**: 99.9%

---

## 🔧 **CONFIGURATION FILES**

### **Railway Configuration**
```json
// railway.json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### **Requirements**
- `requirements.txt` - Production dependencies
- `requirements_minimal.txt` - Minimal dependencies
- `requirements_full.txt` - All dependencies

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

#### **OAuth Errors**
```bash
# Check redirect URIs
curl https://glassdesk-production.up.railway.app/auth/google/login

# Verify Google Cloud Console configuration
# Check environment variables
```

#### **Database Issues**
```bash
# Check database connection
python -c "from app.database import get_db; print(get_db())"

# Verify DATABASE_URL
echo $DATABASE_URL
```

#### **AI Processing Errors**
```bash
# Test OpenAI connection
curl -X POST https://glassdesk-production.up.railway.app/api/test/ai/enhanced_query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Check OpenAI API key
echo $OPENAI_API_KEY
```

#### **Deployment Issues**
```bash
# Check Railway logs
railway logs

# Verify environment variables
railway variables list

# Test deployment
curl https://glassdesk-production.up.railway.app/health
```

---

## 📋 **SETUP CHECKLIST**

### **Development Environment**
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Tests passing
- [ ] Development server running

### **Production Environment**
- [ ] Railway deployment active
- [ ] Environment variables set
- [ ] OAuth credentials configured
- [ ] Database connected
- [ ] Health checks passing
- [ ] OAuth flow working

### **OAuth Configuration**
- [ ] Google Cloud Console project created
- [ ] APIs enabled (Gmail, Google+)
- [ ] OAuth credentials created
- [ ] Redirect URIs configured
- [ ] Production URIs added
- [ ] OAuth flow tested

---

## 🔗 **QUICK REFERENCE**

### **Development Commands**
```bash
# Start development
uvicorn main:app --reload

# Run tests
python -m pytest tests/ -v

# Run sandbox
python sandbox/enhanced_sandbox.py

# Format code
black app/ tests/
flake8 app/ tests/
```

### **Production URLs**
- **Main App**: https://glassdesk-production.up.railway.app
- **Health Check**: https://glassdesk-production.up.railway.app/health
- **API Docs**: https://glassdesk-production.up.railway.app/docs
- **OAuth Login**: https://glassdesk-production.up.railway.app/auth/google/login

### **Key Files**
- **Main App**: `main.py`
- **OAuth Manager**: `app/enhanced_oauth_manager.py`
- **AI Interface**: `app/enhanced_ai_interface.py`
- **Tests**: `tests/` directory
- **Documentation**: `docs/` directory

---

*Last Updated: 2024-07-11*
*AI Agent: Update this file when setup procedures change* 

## Getting Real Google OAuth Credentials

### For Development:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Replace placeholders in your local `.env` file with real values

### For Production:
The real credentials are already set in Railway environment variables:
- `GOOGLE_CLIENT_ID` - Real production client ID
- `GOOGLE_CLIENT_SECRET` - Real production client secret
- `GOOGLE_DESKTOP_CLIENT_ID` - Real desktop client ID
- `GOOGLE_DESKTOP_CLIENT_SECRET` - Real desktop client secret

### Security Best Practices:
- ✅ **Repository**: Use placeholders (`YOUR_GOOGLE_CLIENT_ID`)
- ✅ **Environment Variables**: Use real values (Railway, local `.env`)
- ✅ **Documentation**: Show examples with placeholders
- ❌ **Never commit real secrets to git** 