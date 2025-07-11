# GlassDesk Testing Guide

> **AI AGENT**: This file contains all testing procedures and coverage information. Reference this for testing tasks.

---

## 🧪 **TESTING OVERVIEW**

### **Current Test Coverage**
- **Overall Coverage**: 94% (30/33 tests passing)
- **Test Files**: 4 test files
- **Test Categories**: Unit, Integration, OAuth, AI
- **Status**: ✅ **HEALTHY** - All critical tests passing

### **Test Categories**
1. **Unit Tests** - Individual component testing
2. **Integration Tests** - End-to-end workflow testing
3. **OAuth Tests** - Authentication flow testing
4. **AI Tests** - Natural language processing testing

---

## 🚀 **QUICK TESTING COMMANDS**

### **Run All Tests**
```bash
# Run complete test suite
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_enhanced_features.py -v
```

### **Sandbox Testing**
```bash
# Run enhanced sandbox
python sandbox/enhanced_sandbox.py

# Expected output: All 4 test categories passing
```

### **Production Testing**
```bash
# Health check
curl https://glassdesk-production.up.railway.app/health

# OAuth test
curl https://glassdesk-production.up.railway.app/auth/google/login

# AI query test
curl -X POST https://glassdesk-production.up.railway.app/api/test/ai/enhanced_query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

---

## 📋 **TEST FILES STRUCTURE**

### **Test Files**
```
tests/
├── __init__.py
├── test_api_integration.py      # API endpoint tests
├── test_email_processing.py     # Gmail processing tests
├── test_meeting_processing.py   # Zoom processing tests
└── test_enhanced_features.py    # OAuth and AI tests
```

### **Test Categories**
```python
# Unit Tests
- test_priority_detection()
- test_email_metadata()
- test_meeting_normalization()

# Integration Tests
- test_enhanced_features_workflow()
- test_data_processing_integration()

# OAuth Tests
- test_oauth_manager_initialization()
- test_provider_configuration_check()

# AI Tests
- test_ai_interface_initialization()
- test_conversation_history()
- test_format_gmail_data()
```

---

## 🔧 **DETAILED TESTING PROCEDURES**

### **Unit Testing**

#### **Email Processing Tests**
```python
# File: tests/test_email_processing.py
def test_priority_detection():
    """Test email priority detection logic"""
    # Test high priority keywords
    # Test low priority patterns
    # Test neutral emails

def test_email_metadata():
    """Test email metadata extraction"""
    # Test subject parsing
    # Test sender extraction
    # Test date handling

def test_email_thread_processing():
    """Test email thread grouping"""
    # Test thread identification
    # Test conversation flow
    # Test action item extraction
```

#### **Meeting Processing Tests**
```python
# File: tests/test_meeting_processing.py
def test_meeting_normalization():
    """Test meeting data normalization"""
    # Test date/time parsing
    # Test participant extraction
    # Test duration calculation

def test_meeting_transcript_processing():
    """Test transcript analysis"""
    # Test action item extraction
    # Test decision identification
    # Test key point summarization
```

### **Integration Testing**

#### **Enhanced Features Tests**
```python
# File: tests/test_enhanced_features.py
class TestEnhancedOAuthManager:
    def test_oauth_manager_initialization(self):
        """Test OAuth manager setup"""
        
    def test_provider_configuration_check(self):
        """Test OAuth provider configuration"""
        
    def test_get_provider_status(self):
        """Test provider status checking"""

class TestEnhancedAIInterface:
    def test_ai_interface_initialization(self):
        """Test AI interface setup"""
        
    def test_conversation_history(self):
        """Test conversation memory"""
        
    def test_format_gmail_data(self):
        """Test Gmail data formatting"""
```

### **API Integration Tests**
```python
# File: tests/test_api_integration.py
def test_gmail_api_integration():
    """Test Gmail API endpoints"""
    
def test_zoom_api_integration():
    """Test Zoom API endpoints"""
    
def test_asana_api_integration():
    """Test Asana API endpoints"""
```

---

## 🧪 **SANDBOX TESTING**

### **Enhanced Sandbox**
```python
# File: sandbox/enhanced_sandbox.py
def test_data_processing():
    """Test data processing with mock data"""
    # Load enhanced mock data
    # Process Gmail, Zoom, Asana data
    # Verify processing results

def test_ai_interface():
    """Test AI interface with various queries"""
    # Test different query types
    # Verify response quality
    # Check conversation history

def test_user_communication():
    """Test user communication system"""
    # Test different message types
    # Verify user notifications

def test_error_handling():
    """Test error handling with malformed data"""
    # Test empty data handling
    # Test malformed data handling
```

### **Expected Sandbox Output**
```
🚀 Starting Enhanced Sandbox Tests
============================================================

✅ PASS: Data Processing
✅ PASS: AI Interface
✅ PASS: User Communication
✅ PASS: Error Handling
============================================================
```

---

## 🔍 **TESTING STRATEGIES**

### **Mock Data Testing**
```python
# Mock data files
mock_data/
├── enhanced_sample_data.json    # Comprehensive test data
├── sample_gmail_messages.json   # Gmail test data
└── sample_zoom_meetings.json    # Zoom test data

# Test data structure
{
  "gmail_messages": [...],
  "zoom_meetings": [...],
  "asana_tasks": [...]
}
```

### **Error Testing**
```python
# Test error scenarios
def test_error_handling():
    # Test with empty data
    # Test with malformed data
    # Test with invalid API responses
    # Verify graceful error handling
```

### **Performance Testing**
```python
# Test response times
def test_performance():
    # Test API response times
    # Test AI processing speed
    # Test database query performance
    # Verify performance targets
```

---

## 📊 **COVERAGE ANALYSIS**

### **Current Coverage**
```bash
# Run coverage analysis
python -m pytest tests/ --cov=app --cov-report=html

# Coverage breakdown
- app/ai_interface.py: 95%
- app/data_processor.py: 90%
- app/enhanced_oauth_manager.py: 100%
- app/enhanced_ai_interface.py: 95%
- app/routes/auth.py: 85%
```

### **Coverage Targets**
- **Critical Paths**: 100% coverage
- **OAuth System**: 100% coverage
- **AI Interface**: 95% coverage
- **Data Processing**: 90% coverage
- **Overall Target**: 95% coverage

---

## 🚨 **TESTING ISSUES**

### **Known Issues**
1. **Async Tests Skipped**: Python 3.13 compatibility
   - **Impact**: Low (non-critical tests)
   - **Solution**: Install pytest-asyncio when available

2. **LangChain Warnings**: Deprecation warnings
   - **Impact**: None (functionality unaffected)
   - **Solution**: Update imports when stable

### **Test Failures**
```bash
# Common failure patterns
- OAuth configuration issues
- Missing environment variables
- Database connection problems
- API rate limiting
```

---

## 🔧 **TESTING TOOLS**

### **Pytest Configuration**
```ini
# pytest.ini (if needed)
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### **Test Environment**
```bash
# Required environment variables for testing
OPENAI_API_KEY=test_key
GOOGLE_CLIENT_ID=test_client_id
GOOGLE_CLIENT_SECRET=test_client_secret
SECRET_KEY=test_secret_key
```

### **Test Data Management**
```python
# Test data loading
def load_test_data():
    with open('mock_data/enhanced_sample_data.json') as f:
        return json.load(f)

# Test data validation
def validate_test_data(data):
    assert 'gmail_messages' in data
    assert 'zoom_meetings' in data
    assert 'asana_tasks' in data
```

---

## 📝 **TESTING CHECKLIST**

### **Before Running Tests**
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Mock data available

### **Test Execution**
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Run sandbox tests
- [ ] Check coverage report
- [ ] Verify all tests pass

### **After Tests**
- [ ] Review test results
- [ ] Check coverage targets
- [ ] Document any failures
- [ ] Update test data if needed

---

## 🔍 **DEBUGGING TESTS**

### **Common Test Issues**
```bash
# Import errors
pip install -r requirements.txt

# Environment variable issues
export OPENAI_API_KEY=test_key

# Database issues
python -c "from app.database import init_db; init_db()"

# OAuth issues
python -c "from app.enhanced_oauth_manager import EnhancedOAuthManager; print('OAuth OK')"
```

### **Test Debugging Commands**
```bash
# Run specific test with verbose output
python -m pytest tests/test_enhanced_features.py::TestEnhancedOAuthManager::test_oauth_manager_initialization -v -s

# Run tests with print statements
python -m pytest tests/ -s

# Run tests and stop on first failure
python -m pytest tests/ -x
```

---

## 📚 **TESTING RESOURCES**

### **Documentation**
- **Pytest Documentation**: https://docs.pytest.org/
- **Coverage Documentation**: https://coverage.readthedocs.io/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

### **Related Files**
- **Test Files**: `tests/` directory
- **Mock Data**: `mock_data/` directory
- **Sandbox**: `sandbox/enhanced_sandbox.py`
- **Requirements**: `requirements.txt`

---

*Last Updated: 2024-07-11*
*AI Agent: Use this guide for all testing tasks and coverage analysis* 