# GlassDesk API Reference

> **AI AGENT**: This file contains all API endpoint information. Update when adding new endpoints.

---

## 🚀 **BASE URL**
- **Production**: https://glassdesk-production.up.railway.app
- **Development**: http://localhost:8000

---

## 📋 **CORE ENDPOINTS**

### **Health & Status**
```http
GET /
GET /health
GET /docs
```

### **OAuth Authentication**
```http
GET /auth/google/login
GET /auth/google/callback
GET /auth/desktop/login
GET /auth/desktop/callback
GET /auth/status
```

### **Data Processing**
```http
POST /api/gmail/process
POST /api/zoom/process
POST /api/asana/process
GET /api/data/summary
```

### **AI Interface**
```http
POST /api/ai/query
GET /api/ai/history
POST /api/test/ai/enhanced_query
```

---

## 🔧 **DETAILED ENDPOINT SPECIFICATIONS**

### **Health Check**
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-07-11T09:06:28.923Z",
  "version": "1.0.0"
}
```

### **OAuth Login**
```http
GET /auth/google/login
```
**Response:** Redirects to Google OAuth

### **OAuth Callback**
```http
GET /auth/google/callback?code={code}&state={state}
```
**Response:** Redirects to success/error page

### **AI Query**
```http
POST /api/ai/query
Content-Type: application/json

{
  "query": "What are my action items?",
  "context": "gmail"
}
```
**Response:**
```json
{
  "response": "Based on your data...",
  "type": "action_items",
  "confidence": 0.95
}
```

### **Enhanced AI Query**
```http
POST /api/test/ai/enhanced_query
Content-Type: application/json

{
  "query": "What did I accomplish today?",
  "include_history": true
}
```
**Response:**
```json
{
  "response": "Here's what you accomplished...",
  "type": "daily_summary",
  "sources": ["gmail", "zoom", "asana"],
  "confidence": 0.92
}
```

---

## 📊 **DATA PROCESSING ENDPOINTS**

### **Gmail Processing**
```http
POST /api/gmail/process
Content-Type: application/json

{
  "emails": [
    {
      "id": "email_id",
      "subject": "Meeting Follow-up",
      "body": "Email content...",
      "from": "sender@example.com",
      "date": "2024-07-11T09:00:00Z"
    }
  ]
}
```

### **Zoom Processing**
```http
POST /api/zoom/process
Content-Type: application/json

{
  "meetings": [
    {
      "id": "meeting_id",
      "topic": "Project Review",
      "start_time": "2024-07-11T10:00:00Z",
      "duration": 60,
      "participants": ["user1@example.com"],
      "transcript": "Meeting transcript..."
    }
  ]
}
```

### **Asana Processing**
```http
POST /api/asana/process
Content-Type: application/json

{
  "tasks": [
    {
      "id": "task_id",
      "name": "Complete project proposal",
      "status": "in_progress",
      "due_date": "2024-07-15T23:59:59Z",
      "project": "Project Alpha"
    }
  ]
}
```

---

## 🔍 **QUERY TYPES**

### **Supported Query Categories**
1. **Action Items**: "What are my action items?"
2. **Daily Summary**: "What did I accomplish today?"
3. **Priorities**: "What are my priorities?"
4. **Deadlines**: "What are my deadlines?"
5. **Meeting Info**: "What was discussed in the meeting?"
6. **Email Analysis**: "How many emails do I have?"
7. **General Summary**: "Give me a summary of my work"

### **Response Types**
- `action_items`: List of tasks and follow-ups
- `daily_summary`: Overview of daily activities
- `priorities`: High-priority items
- `deadlines`: Upcoming due dates
- `meeting_summary`: Meeting insights and decisions
- `email_summary`: Email statistics and highlights
- `general_summary`: Overall work summary

---

## 🔐 **AUTHENTICATION**

### **OAuth Flow**
1. **Initiate**: `GET /auth/google/login`
2. **Callback**: `GET /auth/google/callback`
3. **Status**: `GET /auth/status`

### **Token Management**
- **Storage**: Encrypted server-side storage
- **Refresh**: Automatic token refresh
- **Security**: PKCE for desktop flows

---

## 📝 **ERROR RESPONSES**

### **Standard Error Format**
```json
{
  "error": "error_type",
  "message": "Human-readable error message",
  "details": "Technical details",
  "timestamp": "2024-07-11T09:06:28.923Z"
}
```

### **Common Error Types**
- `oauth_error`: OAuth authentication failed
- `api_error`: External API call failed
- `validation_error`: Invalid request data
- `processing_error`: Data processing failed
- `ai_error`: AI processing failed

---

## 🧪 **TESTING ENDPOINTS**

### **Mock Data Testing**
```http
GET /test/gmail/mock
GET /test/zoom/mock
GET /test/asana/mock
POST /test/ai/enhanced_query
```

### **Sandbox Testing**
```http
POST /sandbox/test
Content-Type: application/json

{
  "test_type": "data_processing",
  "data": {...}
}
```

---

## 📊 **MONITORING ENDPOINTS**

### **System Status**
```http
GET /health
GET /status
GET /metrics
```

### **Logs**
```http
GET /logs
GET /logs/errors
GET /logs/performance
```

---

## 🔗 **QUICK REFERENCE**

### **Most Used Endpoints**
- **Health Check**: `GET /health`
- **OAuth Login**: `GET /auth/google/login`
- **AI Query**: `POST /api/ai/query`
- **Data Summary**: `GET /api/data/summary`

### **Development Endpoints**
- **API Docs**: `GET /docs`
- **Test AI**: `POST /api/test/ai/enhanced_query`
- **Mock Data**: `GET /test/*/mock`

---

*Last Updated: 2024-07-11*
*AI Agent: Update this file when adding new endpoints or changing existing ones* 