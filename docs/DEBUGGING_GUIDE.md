# GlassDesk Debugging Guide

> **AI AGENT**: This file contains all debugging strategies and error handling. Reference this for troubleshooting issues.

---

## 🚨 **QUICK DEBUGGING CHECKLIST**

### **Production Issues**
1. **Check Health**: https://glassdesk-production.up.railway.app/health
2. **Check Logs**: Railway dashboard logs
3. **Test OAuth**: https://glassdesk-production.up.railway.app/auth/google/login
4. **Test AI**: POST to `/api/test/ai/enhanced_query`

### **Development Issues**
1. **Run Tests**: `python -m pytest tests/ -v`
2. **Check Sandbox**: `python sandbox/enhanced_sandbox.py`
3. **Check Logs**: `logs/glassdesk.log`
4. **Verify Environment**: Check `.env` file

---

## 🔍 **COMMON ISSUES & SOLUTIONS**

### **OAuth Authentication Issues**

#### **Problem**: OAuth callback errors
```bash
# Symptoms
- "redirect_uri_mismatch" error
- OAuth flow fails to complete
- Tokens not stored properly

# Solutions
1. Check Google Cloud Console redirect URIs
2. Verify environment variables
3. Test with production URLs
```

#### **Problem**: Token refresh failures
```bash
# Symptoms
- "invalid_grant" errors
- Expired tokens not refreshed
- API calls failing

# Solutions
1. Check token storage in database
2. Verify refresh token logic
3. Test token refresh manually
```

### **AI Processing Issues**

#### **Problem**: OpenAI API errors
```bash
# Symptoms
- "invalid_api_key" errors
- Rate limit exceeded
- Model not found errors

# Solutions
1. Verify OPENAI_API_KEY in environment
2. Check API key permissions
3. Monitor token usage
4. Switch to GPT-3.5 if needed
```

#### **Problem**: LangChain import errors
```bash
# Symptoms
- ImportError for langchain modules
- Deprecation warnings
- Missing dependencies

# Solutions
1. Update to langchain_community imports
2. Install missing dependencies
3. Check requirements.txt
```

### **Database Issues**

#### **Problem**: Database connection errors
```bash
# Symptoms
- "database is locked" errors
- Connection timeout
- Schema migration failures

# Solutions
1. Check DATABASE_URL environment variable
2. Verify database permissions
3. Run migrations manually
4. Check Railway database status
```

### **Deployment Issues**

#### **Problem**: Railway deployment failures
```bash
# Symptoms
- Build failures
- Environment variable errors
- Service not starting

# Solutions
1. Check Railway logs
2. Verify environment variables
3. Test locally first
4. Check requirements.txt
```

---

## 🛠️ **DEBUGGING TOOLS**

### **Health Check Endpoints**
```bash
# Production health check
curl https://glassdesk-production.up.railway.app/health

# Development health check
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-07-11T09:06:28.923Z",
  "version": "1.0.0"
}
```

### **Log Analysis**
```bash
# Check application logs
tail -f logs/glassdesk.log

# Check Railway logs
railway logs

# Search for errors
grep "ERROR" logs/glassdesk.log
grep "Exception" logs/glassdesk.log
```

### **Environment Verification**
```bash
# Check environment variables
python -c "import os; print('OPENAI_API_KEY:', bool(os.getenv('OPENAI_API_KEY')))"
python -c "import os; print('GOOGLE_CLIENT_ID:', bool(os.getenv('GOOGLE_CLIENT_ID')))"

# Test database connection
python -c "from app.database import get_db; print(get_db())"
```

### **API Testing**
```bash
# Test OAuth flow
curl https://glassdesk-production.up.railway.app/auth/google/login

# Test AI query
curl -X POST https://glassdesk-production.up.railway.app/api/test/ai/enhanced_query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'

# Test data processing
curl -X POST https://glassdesk-production.up.railway.app/api/gmail/process \
  -H "Content-Type: application/json" \
  -d '{"emails": []}'
```

---

## 🔧 **SELF-HEALING SYSTEMS**

### **Automatic Error Recovery**
```python
# Pattern: Safe API calls
def safe_api_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_api_error(func.__name__, e, {'args': args, 'kwargs': kwargs})
        return None

# Pattern: User-friendly error messages
def translate_error(error):
    if "connection" in str(error).lower():
        return "I'm having trouble connecting. I'll keep trying."
    elif "permission" in str(error).lower():
        return "I need your permission to access this data."
    else:
        return "Something went wrong, but I'm working to fix it automatically."
```

### **Error Categories**
1. **Connection Errors**: Network or API connectivity issues
2. **Authentication Errors**: OAuth or API key problems
3. **Data Processing Errors**: Invalid data or processing failures
4. **AI Processing Errors**: OpenAI or LangChain issues
5. **Database Errors**: Connection or schema issues

---

## 📊 **PERFORMANCE DEBUGGING**

### **Response Time Analysis**
```bash
# Test response times
time curl https://glassdesk-production.up.railway.app/health
time curl -X POST https://glassdesk-production.up.railway.app/api/test/ai/enhanced_query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### **Memory Usage Monitoring**
```bash
# Check memory usage (Railway)
# Monitor in Railway dashboard

# Local memory check
python -c "import psutil; print(psutil.virtual_memory())"
```

### **Error Rate Monitoring**
```bash
# Check error logs
grep -c "ERROR" logs/glassdesk.log
grep -c "Exception" logs/glassdesk.log

# Calculate error rate
# (Error count / Total requests) * 100
```

---

## 🧪 **TESTING STRATEGIES**

### **Unit Testing**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_enhanced_features.py -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### **Integration Testing**
```bash
# Run sandbox tests
python sandbox/enhanced_sandbox.py

# Test OAuth flow
python test_oauth.py

# Test AI interface
python -c "from app.enhanced_ai_interface import EnhancedAIInterface; print('AI Interface OK')"
```

### **End-to-End Testing**
```bash
# Test complete workflow
1. Start development server
2. Test OAuth login
3. Test data processing
4. Test AI queries
5. Verify responses
```

---

## 🔍 **DIAGNOSTIC COMMANDS**

### **System Health Check**
```bash
# Check Python environment
python --version
pip list | grep -E "(fastapi|langchain|openai)"

# Check file permissions
ls -la logs/
ls -la .env

# Check disk space
df -h
```

### **Network Connectivity**
```bash
# Test external APIs
curl -I https://api.openai.com/v1/models
curl -I https://www.googleapis.com/oauth2/v1/tokeninfo

# Test Railway connectivity
curl -I https://glassdesk-production.up.railway.app/health
```

### **Database Diagnostics**
```bash
# Check database connection
python -c "from app.database import get_db; db = get_db(); print('DB OK')"

# Check database schema
python -c "from app.database import get_db; db = get_db(); print(db.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())"
```

---

## 📝 **ERROR LOGGING PATTERNS**

### **Structured Error Logging**
```python
import logging
from datetime import datetime

def log_error(error_type, error_message, context=None):
    logging.error(f"""
    ERROR TYPE: {error_type}
    MESSAGE: {error_message}
    TIMESTAMP: {datetime.now().isoformat()}
    CONTEXT: {context}
    """)

# Usage
log_error("oauth_error", "Invalid redirect URI", {"uri": redirect_uri})
log_error("ai_error", "OpenAI API error", {"query": user_query})
```

### **Error Recovery Strategies**
1. **Retry Logic**: Automatic retry for transient errors
2. **Fallback Responses**: Graceful degradation
3. **User Notification**: Clear error messages
4. **Logging**: Comprehensive error tracking

---

## 🚨 **EMERGENCY PROCEDURES**

### **Production Issues**
1. **Check Railway Status**: Verify service is running
2. **Review Recent Logs**: Look for error patterns
3. **Test Critical Endpoints**: Health, OAuth, AI
4. **Rollback if Necessary**: Revert to last working version

### **Data Loss Prevention**
1. **Backup Database**: Export critical data
2. **Preserve Logs**: Keep error logs for analysis
3. **Document Changes**: Record what was modified
4. **Test Recovery**: Verify backup restoration

---

## 📚 **DEBUGGING RESOURCES**

### **Documentation References**
- **API Reference**: `docs/API_REFERENCE.md`
- **Setup Guide**: `docs/SETUP_GUIDE.md`
- **Deployment Status**: `docs/DEPLOYMENT_STATUS.md`
- **Project Status**: `docs/PROJECT_STATUS.md`

### **External Resources**
- **Railway Docs**: https://docs.railway.app/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangChain Docs**: https://python.langchain.com/
- **OpenAI Docs**: https://platform.openai.com/docs

---

*Last Updated: 2024-07-11*
*AI Agent: Use this guide for all debugging and troubleshooting tasks* 