# HTTPie CLI Reference for GlassDesk

> **AI AGENT**: This document provides comprehensive HTTPie commands for GlassDesk API testing, debugging, and monitoring. Use this for all HTTP requests to the GlassDesk API.

---

## 🎯 **ESSENTIAL HTTPIE COMMANDS**

### **Installation**
```bash
# Install HTTPie
pip install httpie

# Verify installation
http --version
```

**📚 Official Docs**: https://httpie.io/docs/cli/request-url

---

## 🚀 **GLASSDESK API TESTING**

### **Health Check Endpoints**
```bash
# Production health check
http GET https://glassdesk-production.up.railway.app/health

# Local development health check
http GET http://localhost:8000/health

# Health check with verbose output
http GET https://glassdesk-production.up.railway.app/health -v

# Health check with timing
http GET https://glassdesk-production.up.railway.app/health --timeout 10
```

### **OAuth Endpoints**
```bash
# Test OAuth login endpoint
http GET https://glassdesk-production.up.railway.app/auth/google/login

# Test OAuth callback (simulate)
http GET https://glassdesk-production.up.railway.app/auth/google/callback?code=test_code

# Test desktop OAuth
http GET https://glassdesk-production.up.railway.app/auth/desktop/login

# Test OAuth with headers
http GET https://glassdesk-production.up.railway.app/auth/google/login \
  User-Agent:"GlassDesk/1.0" \
  Accept:"application/json"
```

### **AI Query Endpoints**
```bash
# Test AI query endpoint
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="summarize my recent emails"

# Test AI query with JSON body
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="analyze my meeting schedule" \
  source=="gmail"

# Test AI query with authentication
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="find important tasks" \
  Authorization:"Bearer your_token_here"

# Test AI query with multiple parameters
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="summarize my week" \
  source=="all" \
  format=="detailed"
```

### **Data Processing Endpoints**
```bash
# Test Gmail data processing
http POST https://glassdesk-production.up.railway.app/process/gmail \
  Authorization:"Bearer token"

# Test Zoom data processing
http POST https://glassdesk-production.up.railway.app/process/zoom \
  Authorization:"Bearer token"

# Test Asana data processing
http POST https://glassdesk-production.up.railway.app/process/asana \
  Authorization:"Bearer token"
```

---

## 🔍 **DEBUGGING COMMANDS**

### **Verbose Output for Debugging**
```bash
# Full request/response debugging
http GET https://glassdesk-production.up.railway.app/health -v

# Extra verbose (includes intermediary requests)
http GET https://glassdesk-production.up.railway.app/auth/google/login -vv

# Show request headers only
http GET https://glassdesk-production.up.railway.app/health --print=H

# Show response headers only
http GET https://glassdesk-production.up.railway.app/health --print=h

# Show both request and response headers
http GET https://glassdesk-production.up.railway.app/health --print=Hh
```

### **Error Handling**
```bash
# Test with timeout
http GET https://glassdesk-production.up.railway.app/health --timeout 5

# Test with retry
http GET https://glassdesk-production.up.railway.app/health --max-redirects 3

# Test with custom user agent
http GET https://glassdesk-production.up.railway.app/health \
  User-Agent:"GlassDesk-Debug/1.0"

# Test with custom headers
http GET https://glassdesk-production.up.railway.app/health \
  X-Debug:true \
  X-Request-ID:test-123
```

---

## 🔐 **AUTHENTICATION TESTING**

### **Bearer Token Authentication**
```bash
# Test with Bearer token
http GET https://glassdesk-production.up.railway.app/user/profile \
  Authorization:"Bearer your_oauth_token"

# Test with custom auth header
http GET https://glassdesk-production.up.railway.app/user/profile \
  X-Auth-Token:"your_token"

# Test OAuth token validation
http POST https://glassdesk-production.up.railway.app/auth/validate \
  token=="your_oauth_token"
```

### **OAuth Flow Testing**
```bash
# Test OAuth state parameter
http GET https://glassdesk-production.up.railway.app/auth/google/login \
  state=="test_state_123"

# Test OAuth with PKCE
http GET https://glassdesk-production.up.railway.app/auth/desktop/login \
  code_challenge=="test_challenge" \
  code_challenge_method=="S256"

# Test OAuth callback with all parameters
http GET https://glassdesk-production.up.railway.app/auth/google/callback \
  code=="test_auth_code" \
  state=="test_state" \
  scope=="email profile"
```

---

## 📊 **PRODUCTION MONITORING**

### **Health Monitoring**
```bash
# Quick health check
http GET https://glassdesk-production.up.railway.app/health

# Health check with response time
time http GET https://glassdesk-production.up.railway.app/health

# Health check with JSON output
http GET https://glassdesk-production.up.railway.app/health --json

# Health check with custom format
http GET https://glassdesk-production.up.railway.app/health --format=json
```

### **Performance Testing**
```bash
# Test response time
http GET https://glassdesk-production.up.railway.app/health --timeout 10

# Test with compression
http GET https://glassdesk-production.up.railway.app/health --compress

# Test with different user agents
http GET https://glassdesk-production.up.railway.app/health \
  User-Agent:"GlassDesk-Monitor/1.0"
```

### **Error Monitoring**
```bash
# Test 404 endpoint
http GET https://glassdesk-production.up.railway.app/nonexistent

# Test 500 error simulation
http POST https://glassdesk-production.up.railway.app/test/error

# Test malformed requests
http POST https://glassdesk-production.up.railway.app/ai/query \
  invalid_field=="test"
```

---

## 🎯 **GLASSDESK-SPECIFIC WORKFLOWS**

### **Daily Development Workflow**
```bash
# 1. Check production health
http GET https://glassdesk-production.up.railway.app/health

# 2. Test local development
http GET http://localhost:8000/health

# 3. Test OAuth flow
http GET https://glassdesk-production.up.railway.app/auth/google/login

# 4. Test AI query
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="test query"

# 5. Check API documentation
http GET https://glassdesk-production.up.railway.app/docs
```

### **OAuth Debugging Workflow**
```bash
# 1. Test OAuth login endpoint
http GET https://glassdesk-production.up.railway.app/auth/google/login -v

# 2. Test OAuth callback (simulate)
http GET https://glassdesk-production.up.railway.app/auth/google/callback \
  code=="test_code" \
  state=="test_state" \
  -v

# 3. Test token validation
http POST https://glassdesk-production.up.railway.app/auth/validate \
  token=="test_token" \
  -v

# 4. Test user profile with token
http GET https://glassdesk-production.up.railway.app/user/profile \
  Authorization:"Bearer test_token" \
  -v
```

### **AI Testing Workflow**
```bash
# 1. Test basic AI query
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="summarize my emails"

# 2. Test AI query with source
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="analyze my meetings" \
  source=="zoom"

# 3. Test AI query with authentication
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="find important tasks" \
  Authorization:"Bearer token"

# 4. Test AI query with complex parameters
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="summarize my week" \
  source=="all" \
  format=="detailed" \
  limit=="10"
```

### **Production Monitoring Workflow**
```bash
# 1. Check all endpoints health
http GET https://glassdesk-production.up.railway.app/health
http GET https://glassdesk-production.up.railway.app/docs
http GET https://glassdesk-production.up.railway.app/auth/google/login

# 2. Test AI functionality
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="test query"

# 3. Test error handling
http GET https://glassdesk-production.up.railway.app/nonexistent

# 4. Check response times
time http GET https://glassdesk-production.up.railway.app/health
```

---

## 🔧 **ADVANCED FEATURES**

### **Session Management**
```bash
# Create a session for authenticated requests
http --session=glassdesk https://glassdesk-production.up.railway.app/auth/google/login

# Use session for subsequent requests
http --session=glassdesk https://glassdesk-production.up.railway.app/ai/query \
  q=="test query"

# Save session to file
http --session=glassdesk.json https://glassdesk-production.up.railway.app/auth/google/login
```

### **File Upload Testing**
```bash
# Test file upload (if implemented)
http POST https://glassdesk-production.up.railway.app/upload \
  file@/path/to/file.txt

# Test multiple file uploads
http POST https://glassdesk-production.up.railway.app/upload \
  file1@/path/to/file1.txt \
  file2@/path/to/file2.txt
```

### **Custom Headers and Cookies**
```bash
# Test with custom headers
http GET https://glassdesk-production.up.railway.app/health \
  X-Custom-Header:"test_value" \
  X-Request-ID:"test-123"

# Test with cookies
http GET https://glassdesk-production.up.railway.app/health \
  Cookie:"session=test_session"

# Test with multiple headers
http GET https://glassdesk-production.up.railway.app/health \
  User-Agent:"GlassDesk-Test/1.0" \
  Accept:"application/json" \
  X-Debug:"true"
```

---

## 📝 **OUTPUT FORMATTING**

### **JSON Output**
```bash
# Pretty JSON output (default)
http GET https://glassdesk-production.up.railway.app/health

# Compact JSON output
http GET https://glassdesk-production.up.railway.app/health --format=json

# Raw JSON output
http GET https://glassdesk-production.up.railway.app/health --print=b
```

### **Custom Output**
```bash
# Show only response body
http GET https://glassdesk-production.up.railway.app/health --print=b

# Show only status code
http GET https://glassdesk-production.up.railway.app/health --print=S

# Show only headers
http GET https://glassdesk-production.up.railway.app/health --print=h

# Show custom format
http GET https://glassdesk-production.up.railway.app/health --print="S {body}"
```

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**
```bash
# Connection timeout
http GET https://glassdesk-production.up.railway.app/health --timeout 30

# SSL certificate issues
http GET https://glassdesk-production.up.railway.app/health --verify=no

# Proxy issues
http GET https://glassdesk-production.up.railway.app/health --proxy=http://proxy:8080

# Authentication issues
http GET https://glassdesk-production.up.railway.app/health --auth=user:pass
```

### **Debugging Commands**
```bash
# Full debugging output
http GET https://glassdesk-production.up.railway.app/health -vvv

# Show request only
http GET https://glassdesk-production.up.railway.app/health --print=H

# Show response only
http GET https://glassdesk-production.up.railway.app/health --print=h

# Test with different HTTP versions
http GET https://glassdesk-production.up.railway.app/health --http1.1
```

---

## 📊 **MONITORING SCRIPTS**

### **Health Check Script**
```bash
#!/bin/bash
# health_check.sh

echo "Checking GlassDesk production health..."

# Check main health endpoint
response=$(http GET https://glassdesk-production.up.railway.app/health --print=b)
if [[ $response == *"status"*"ok"* ]]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Check OAuth endpoint
oauth_response=$(http GET https://glassdesk-production.up.railway.app/auth/google/login --print=S)
if [[ $oauth_response == "200" ]]; then
    echo "✅ OAuth endpoint accessible"
else
    echo "❌ OAuth endpoint failed: $oauth_response"
fi
```

### **API Test Script**
```bash
#!/bin/bash
# api_test.sh

echo "Testing GlassDesk API endpoints..."

# Test health
echo "Testing health endpoint..."
http GET https://glassdesk-production.up.railway.app/health

# Test OAuth
echo "Testing OAuth endpoint..."
http GET https://glassdesk-production.up.railway.app/auth/google/login

# Test AI query
echo "Testing AI query endpoint..."
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="test query"

echo "API testing complete"
```

---

## 🎯 **AI AGENT EFFICIENCY TIPS**

### **For API Testing**
1. **Use `-v` flag** for debugging - shows full request/response
2. **Use `--print=b`** for JSON responses - easier to parse
3. **Use sessions** for authenticated requests - saves tokens
4. **Use `--timeout`** for production testing - prevents hanging

### **For OAuth Debugging**
1. **Test login endpoint first** - verify OAuth flow starts
2. **Test callback with parameters** - simulate OAuth response
3. **Test token validation** - verify token processing
4. **Use verbose output** - see all OAuth parameters

### **For Production Monitoring**
1. **Check health endpoint** - quick status check
2. **Test AI queries** - verify core functionality
3. **Monitor response times** - performance tracking
4. **Test error endpoints** - verify error handling

---

*Last Updated: 2024-07-11*
*AI Agent: Use this reference for all HTTPie commands in GlassDesk development* 