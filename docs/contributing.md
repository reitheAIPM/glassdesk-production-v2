
# GlassDesk - AI Development Guidelines

> **AI AGENT MASTER GUIDE**: This is your primary reference for all GlassDesk development.

## 🎯 **QUICK START FOR AI AGENTS**

### **CRITICAL PRINCIPLES**
- **User is NOT a developer** - Implement comprehensive error handling and self-debugging
- **Always work in Python virtual environment** (venv)
- **Use mock data for development** - Real APIs for production only
- **Current Status**: ✅ **PRODUCTION READY** - Deployed at https://glassdesk-production.up.railway.app
- **Architecture**: Supports both web and desktop clients

### **ENHANCED MODULES (USE THESE)**
- `app/enhanced_oauth_manager.py` (Authlib, PKCE, secure)
- `app/enhanced_ai_interface.py` (LangChain RAG, semantic search)
- See `/auth/*` and `/test/ai/enhanced_query` endpoints for usage
- **Legacy modules** (`app/oauth_manager.py`, `app/ai_interface.py`) are deprecated

---

## AI-ONLY DEVELOPMENT ENVIRONMENT

### IMPERATIVE REQUIREMENTS:
1. **Comprehensive Error Analysis** - Every function must have detailed error logging and recovery
2. **Self-Debugging Systems** - Implement robust debugging tools that can identify and fix issues autonomously
3. **Fail-Safe Operations** - All operations must gracefully handle failures and provide clear error messages
4. **Automated Testing** - Extensive test coverage to catch issues before they reach the user
5. **Detailed Logging** - Every action must be logged for AI analysis and debugging
6. **User-Friendly Error Messages** - Technical errors must be translated into simple, actionable messages
7. **Multi-Platform Support** - Architecture must support both web and desktop clients

### AI DEVELOPMENT GUIDELINES:
- **ENHANCED:** Use `EnhancedAIInterface` (`app/enhanced_ai_interface.py`) for all new AI query logic. See `/test/ai/enhanced_query` endpoint for usage.
- **Assume Zero Technical Knowledge** - User cannot debug code or understand technical errors
- **Implement Self-Healing Systems** - Code should automatically detect and attempt to fix common issues
- **Provide Clear Status Updates** - Always inform user of what's happening in simple terms
- **Create Backup Plans** - Every feature needs fallback options when primary methods fail
- **Design for Multi-Platform** - Backend should work for both web and desktop clients

---

## FOUNDATIONAL SYSTEMS & TOOLS

| System | Purpose | Files | Status |
|--------|---------|-------|---------|
| **Prompt Library** | AI prompt templates | `prompts/summarize_meeting.txt`, `prompts/task_prioritizer.txt` | ✅ Implemented |
| **Mock Data** | Sample JSON data for testing | `mock_data/sample_gmail_messages.json`, `mock_data/sample_zoom_meetings.json` | ✅ Complete |
| **Sandbox Environment** | Isolated testing | `sandbox/enhanced_sandbox.py` | ✅ Enhanced |
| **Self-Healing System** | Auto-detect and fix issues | `app/self_healing.py` | ✅ Implemented |
| **User Communication** | Simple user messages | `app/user_communication.py` | ✅ Complete |
| **Debugging Strategies** | AI debugging guide | `docs/debugging_strategies.md` | ✅ Documented |
| **Project Goals** | Keep development focused | `docs/project_goals.md` | ✅ Updated |
| **OAuth Management** | Multi-platform authentication | `app/services/oauth_manager.py` | ✅ Implemented |

---

## DEVELOPMENT ENVIRONMENT

### SETUP COMMANDS:
```bash
# Create and activate venv
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup development environment
python setup_dev.py

# Test functionality
python sandbox/enhanced_sandbox.py

# Run tests
python -m pytest tests/ -v

# Code quality
black app/ tests/
flake8 app/ tests/ --max-line-length=88
```

---

## FILE & FOLDER STRUCTURE

### **MANDATORY FILE ORGANIZATION PRINCIPLES**
> **AI AGENT**: All newly created files MUST follow these organized and efficient file structure principles to optimize AI workflow.

#### **📁 DOCUMENTATION STRUCTURE**
- **`docs/`** - All documentation files
  - **Master Index**: `docs/README.md` - Primary reference for AI agents
  - **Status Files**: `docs/PROJECT_STATUS.md`, `docs/DEPLOYMENT_STATUS.md`
  - **Technical Reference**: `docs/TECH_STACK.md`, `docs/API_REFERENCE.md`
  - **CLI References**: `docs/HTTPIE_CLI_REFERENCE.md`, `docs/PRE_COMMIT_CLI_REFERENCE.md`
  - **Guides**: `docs/SETUP_GUIDE.md`, `docs/TESTING_GUIDE.md`, `docs/DEBUGGING_GUIDE.md`
  - **Research**: `docs/RESEARCH_SUMMARY.md` - Consolidated research findings

#### **📁 CODE STRUCTURE**
- **`app/`** - Core application logic
  - **Enhanced Modules**: `app/enhanced_oauth_manager.py`, `app/enhanced_ai_interface.py`
  - **Services**: `app/services/` - Service layer components
  - **Routes**: `app/routes/` - API endpoint handlers
- **`database/`** - Database schema and migrations
- **`config/`** - Configuration management
- **`tests/`** - Comprehensive test suite (94% coverage)
- **`sandbox/`** - Isolated testing environment

#### **📁 DEVELOPMENT TOOLS**
- **`mock_data/`** - Sample JSON data for testing
- **`prompts/`** - AI prompt templates
- **`docs/`** - Complete documentation hub

#### **📁 ROOT FILES**
- **`main.py`** - FastAPI application entry point
- **`requirements.txt`** - Python dependencies
- **`.env_template.env`** - Environment variable template

### **FILE ORGANIZATION RULES**
1. **✅ DO**: Keep documentation in `docs/` folder with clear naming
2. **✅ DO**: Use consistent naming conventions (snake_case for files)
3. **✅ DO**: Cross-reference related files in documentation
4. **✅ DO**: Update status files when making changes
5. **✅ DO**: Consolidate redundant information
6. **❌ DON'T**: Create redundant documentation
7. **❌ DON'T**: Leave outdated information
8. **❌ DON'T**: Scatter related info across multiple files
9. **❌ DON'T**: Use vague or ambiguous language
10. **❌ DON'T**: Keep research files separate from implementation docs

### **AI-OPTIMIZED FILE STRUCTURE**
| Folder/File | Purpose | AI Optimization | Status |
|-------------|---------|-----------------|---------|
| `docs/README.md` | Master documentation index | Primary AI reference | ✅ Complete |
| `docs/PROJECT_STATUS.md` | Current project state | AI agent reference | ✅ Complete |
| `docs/CLI_TOOLS_REFERENCE.md` | Essential CLI tools | AI development efficiency | ✅ Complete |
| `docs/HTTPIE_CLI_REFERENCE.md` | API testing commands | GlassDesk-specific examples | ✅ Complete |
| `docs/PRE_COMMIT_CLI_REFERENCE.md` | Code quality automation | GlassDesk workflows | ✅ Complete |
| `app/enhanced_oauth_manager.py` | OAuth management | Enhanced with PKCE | ✅ Complete |
| `app/enhanced_ai_interface.py` | AI interface | LangChain RAG implementation | ✅ Complete |
| `tests/` | Test suite | 94% coverage maintained | ✅ Complete |
| `sandbox/enhanced_sandbox.py` | Testing environment | Isolated validation | ✅ Complete |

---

## ADDING NEW INTEGRATION (AI CHECKLIST)

To add new data source (e.g., Slack):

1. ✅ Create `app/slack_integration.py`
2. ✅ Add ingestion function
3. ✅ Normalize data and validate schema
4. ✅ Store result via SQL or database
5. ✅ Log errors using `safe_api_call()`
6. ✅ Add sample data to `mock_data/sample_slack_messages.json`
7. ✅ Create prompt template in `prompts/slack_processor.txt`
8. ✅ Update `sandbox/enhanced_sandbox.py` to test new integration
9. ✅ Add to `docs/mock_data_guidelines.md` reference

---

## OAUTH CONFIGURATION FOR MULTI-PLATFORM

> **ENHANCED:** Use `EnhancedOAuthManager` (`app/enhanced_oauth_manager.py`) for all new OAuth flows. See `/auth/google/login` and `/auth/google/desktop/login` endpoints.

### Web Application OAuth (Current)
- **Redirect URIs**: `http://localhost:8000/auth/google/callback` (dev), `https://your-app.railway.app/auth/google/callback` (prod)
- **Client Type**: Web application
- **Token Storage**: Server-side encrypted storage
- **Security**: Standard OAuth 2.0 flow

### Desktop Application OAuth (Planned)
- **Redirect URIs**: `http://localhost:3000/callback` (dev), `https://your-app.railway.app/auth/desktop/callback` (prod)
- **Client Type**: Desktop application
- **Token Storage**: Local encrypted storage with PKCE
- **Security**: PKCE (Proof Key for Code Exchange) for enhanced security

### OAuth Implementation Strategy
1. **Backend Remains Unchanged** - FastAPI serves both web and desktop
2. **Client-Specific OAuth Flows** - Different OAuth configurations for web vs desktop
3. **Unified Token Management** - Same backend token storage for both clients
4. **Platform-Specific Features** - Desktop gets system integration, web gets sharing features

---

## CONTRIBUTING PROCESS (AI REQUIREMENTS)

### MANDATORY PRACTICES:
1. ✅ Use TODO and FIXME comments to track uncertain logic
2. ✅ Log all errors and AI outputs to `glassdesk.log`
3. ✅ Write readable and comment-rich code for AI assistance
4. ✅ Use test files in `tests/` and log summaries for AI-assisted debugging
5. ✅ **Work inside a venv for all development and testing**
6. ✅ **Implement comprehensive error handling and self-debugging systems**
7. ✅ **Provide user-friendly error messages and status updates**
8. ✅ **Use AI-friendly markers in code** (`CLAUDE_TODO`, `CURSOR_NOTE`, `AI_FIXME`)
9. ✅ **Test with mock data** before using real API tokens (see `docs/mock_data_guidelines.md`)
10. ✅ **Run sandbox tests** to validate functionality in isolation
11. ✅ **Design for multi-platform** - Backend should support both web and desktop clients
12. ✅ **AI must take initiative: constantly update `docs/TASK_LIST.md`, proactively add/fix tasks for any issues, opportunities, or improvements, and never mark a task as complete unless it is truly fixed.**
13. ✅ **Always use CLI commands (as documented in CLI references) for all project actions whenever possible. Only use direct file edits or manual steps when CLI commands are not available or appropriate. Document all CLI commands used in the task list and status updates.**

### AI-FRIENDLY CODE MARKERS:
```python
# CLAUDE_TODO: Implement OAuth flow for Slack integration
# CURSOR_NOTE: This function needs better error handling
# AI_FIXME: Add rate limiting to prevent API abuse
# DESKTOP_TODO: Add desktop-specific OAuth flow
```

### TASK LIST MANAGEMENT:
- **✅ DO**: Update `docs/TASK_LIST.md` when tasks are completed or new ones are added
- **✅ DO**: Use priority levels (🔴 HIGH, 🟡 MEDIUM, 🟢 LOW) for task organization
- **✅ DO**: Include specific action items and file references for each task
- **✅ DO**: Update task status (⏳ PENDING, 🔄 IN PROGRESS, ✅ COMPLETE)
- **✅ DO**: Add GlassDesk-specific examples and workflows to task descriptions
- **❌ DON'T**: Leave tasks without clear action items or file references
- **❌ DON'T**: Create tasks without priority levels or status tracking

---

## ERROR HANDLING PATTERNS (AI IMPLEMENTATION)

### PATTERN 1: Safe API Calls
```python
def safe_api_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_api_error(func.__name__, e, {'args': args, 'kwargs': kwargs})
        return None
```

### PATTERN 2: User-Friendly Error Messages
```python
def translate_error(error):
    if "connection" in str(error).lower():
        return "I'm having trouble connecting. I'll keep trying."
    elif "permission" in str(error).lower():
        return "I need your permission to access this data."
    else:
        return "Something went wrong, but I'm working to fix it automatically."
```

### PATTERN 3: Self-Healing Implementation
```python
def auto_fix_common_issues(issue_type, context):
    if issue_type == "database_connection":
        return reconnect_database()
    elif issue_type == "oauth_token_expired":
        return refresh_oauth_token()
    elif issue_type == "rate_limited":
        return wait_and_retry(context)
    else:
        log_unknown_error(issue_type, context)
        return False
```

---

## TESTING REQUIREMENTS (AI VALIDATION)

### MOCK DATA TESTING:
- ✅ Test all features with mock data
- ✅ Validate data schemas and structures
- ✅ Test error handling with malformed data
- ✅ Test user communication systems

### REAL API TESTING:
- ✅ Test OAuth flows and token management
- ✅ Test rate limiting and error handling
- ✅ Test data validation against real APIs
- ✅ Test production deployment scenarios

### SANDBOX TESTING:
- ✅ Run `python sandbox/enhanced_sandbox.py` to validate functionality
- ✅ Test all integrations in isolation
- ✅ Validate user communication and error handling
- ✅ Test self-healing systems

### MULTI-PLATFORM TESTING:
- ✅ Test OAuth flows for both web and desktop clients
- ✅ Validate token storage for different platforms
- ✅ Test API communication from different client types
- ✅ Verify security measures for each platform

---

## SUCCESS METRICS (AI VALIDATION)

### DEVELOPMENT PHASE:
- ✅ All features work with mock data
- ✅ OAuth flows work for both web and desktop
- ✅ Backend serves multiple client types
- ✅ Security measures implemented for all platforms

### PRODUCTION PHASE:
- ✅ Real API integrations functional
- ✅ Multi-platform OAuth working
- ✅ Error handling works with real APIs
- ✅ User experience consistent across platforms

---

## DESKTOP APPLICATION PLANNING

### Architecture Benefits:
1. **Backend-Heavy Design** - FastAPI serves both web and desktop
2. **Unified Data Processing** - Same AI and processing logic
3. **Platform-Specific Features** - Desktop gets system integration, web gets sharing
4. **Cost Efficiency** - Single backend reduces maintenance overhead

### Desktop Implementation Plan:
1. **Phase 1**: Desktop OAuth with PKCE security
2. **Phase 2**: Electron/Tauri desktop client
3. **Phase 3**: System integration (notifications, file access)
4. **Phase 4**: Offline capability and enhanced features

### OAuth Configuration Strategy:
- **Web**: Standard OAuth 2.0 with server-side token storage
- **Desktop**: PKCE flow with local token storage
- **Backend**: Unified token management for both platforms
- **Security**: Enhanced security for desktop with PKCE

---

## CURRENT PROJECT STATUS

### ✅ **COMPLETED FOUNDATION:**
- **Mock Data Processing**: Complete Gmail, Zoom, and Asana processors
- **AI Interface**: Natural language query processing with intelligent responses
- **Error Handling**: Comprehensive error handling and self-healing mechanisms
- **Testing**: 94% test coverage with automated test suite
- **Code Quality**: Black formatting and flake8 linting
- **Database Schema**: PostgreSQL/SQLite migrations ready
- **Documentation**: Comprehensive docs and contributing guidelines
- **Deployment**: Railway deployment configuration ready
- **Security**: Token encryption and secure patterns implemented
- **Multi-Platform Architecture**: Backend designed for both web and desktop

### 🔄 **NEXT IMMEDIATE STEPS:**
1. **Google OAuth Setup** (User action required)
2. **Production Deployment** to Railway
3. **Real API Integration** (Gmail → Zoom → Asana)
4. **Desktop OAuth Implementation** (PKCE flow)
5. **Desktop Client Development** (Electron/Tauri)

### 📊 **TECHNICAL ACHIEVEMENTS:**
- **Test Coverage**: 94%
- **Files Formatted**: 22
- **Security**: Verified (no hardcoded secrets)
- **Deployment**: Production-ready
- **Documentation**: Complete
- **Multi-Platform**: Architecture ready for desktop

## Secret Management
- Never commit real secrets or credentials to the repository.
- Use placeholders in all documentation and template files.
- Always add `.env` and any real secret files to `.gitignore`.
- If a secret is accidentally committed, remove it from history and rotate the secret immediately.
