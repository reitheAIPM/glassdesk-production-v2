
# GlassDesk AI Assistant

## Project Description

GlassDesk is an AI-powered personal assistant designed to aggregate, organize, and contextualize a user's daily digital work life by connecting to various data sources such as Gmail, Zoom, and Asana. Instead of continuously running expensive AI models on raw data, GlassDesk leverages existing AI services for transcription and summarization, then acts as a meta-orchestrator that compiles, stores, and intelligently queries the aggregated data to answer user queries and provide actionable insights.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (for production) or SQLite (for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd glassdesk
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env_template.env .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Development Setup

For development with mock data:
```bash
python setup_dev.py
python sandbox/enhanced_sandbox.py
```

---

## 🎯 Current Status

### ✅ Completed Features
- **Mock Data Processing**: Complete Gmail, Zoom, and Asana data processors
- **AI Interface**: Natural language query processing with intelligent responses
- **Error Handling**: Comprehensive error handling and self-healing mechanisms
- **Testing**: 94% test coverage with automated test suite
- **Code Quality**: Black formatting and flake8 linting
- **Database Schema**: PostgreSQL/SQLite migrations ready
- **Documentation**: Comprehensive docs and contributing guidelines

### 🔄 In Progress
- **OAuth Integration**: Google OAuth setup for Gmail access
- **Production Deployment**: Railway deployment configuration
- **Security Hardening**: Token encryption and secure storage

### 📋 Next Steps
1. **Google OAuth Setup** (User action required)
2. **Production Deployment** to Railway
3. **Real API Integration** (Gmail → Zoom → Asana)
4. **User Interface Development**

---

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run with Coverage
```bash
python -m coverage run -m pytest tests/
python -m coverage report
```

### Enhanced Sandbox Testing
```bash
python sandbox/enhanced_sandbox.py
```

---

## 📊 Usage Examples

### Natural Language Queries
```python
from app.ai_interface import AIInterface
from app.data_processor import DataProcessor

# Initialize
processor = DataProcessor()
ai = AIInterface(processor)

# Ask questions
response = ai.process_query("How many emails do I have?")
response = ai.process_query("What are my action items?")
response = ai.process_query("Show me my priorities")
```

### Data Processing
```python
from app.data_processor import DataProcessor
from mock_data.sample_gmail_messages import sample_emails

processor = DataProcessor()
processed = processor.process_gmail_data(sample_emails)
summary = processor.create_daily_summary()
```

---

## 🚀 Enhanced Features (2024)

### Enhanced OAuth (PKCE, Secure)
- All authentication now uses Authlib for secure OAuth 2.0 flows (web and desktop)
- Endpoints:
  - `/auth/google/login` (web)
  - `/auth/google/desktop/login` (desktop/PKCE)
  - `/auth/google/callback` and `/auth/google/desktop/callback`
  - `/auth/status` for provider status

### Enhanced AI Querying (LangChain RAG)
- Context-aware, semantic search and retrieval-augmented generation
- Endpoint:
  - `POST /test/ai/enhanced_query` with `{ "query": "What did I accomplish today?" }`
- Returns:
  - Intelligent, context-aware answers
  - Source document snippets for transparency

---

## 🧪 API Usage Examples (Enhanced)

### Enhanced AI Query
```python
import requests

response = requests.post(
    "http://localhost:8000/test/ai/enhanced_query",
    json={"query": "What did I accomplish today?"}
)
print(response.json())
```

### OAuth Flow (Web)
- Visit `/auth/google/login` in your browser to start Google OAuth
- Complete the flow and check `/auth/status` for connection

### OAuth Flow (Desktop/PKCE)
- Call `/auth/google/desktop/login` to get the auth URL
- Complete the flow and call `/auth/google/desktop/callback` with the code

---

## 🔧 Configuration

### Environment Variables
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `ZOOM_CLIENT_ID`: Zoom OAuth client ID
- `ASANA_PERSONAL_ACCESS_TOKEN`: Asana API token
- `OPENAI_API_KEY`: OpenAI API key for AI processing
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key

### Feature Flags
- `ENABLE_GMAIL`: Enable Gmail integration
- `ENABLE_ZOOM`: Enable Zoom integration
- `ENABLE_ASANA`: Enable Asana integration
- `ENABLE_AI_PROCESSING`: Enable AI processing

---

## 🏗️ Architecture

### Core Components
- **Data Processor**: Handles data ingestion and processing
- **AI Interface**: Natural language query processing
- **OAuth Manager**: Secure token management
- **Error Handler**: Comprehensive error handling
- **User Communication**: User-friendly messaging

### Data Flow
1. **Ingestion**: Collect data from APIs (Gmail, Zoom, Asana)
2. **Processing**: Extract key information and action items
3. **Storage**: Store processed data in database
4. **Query**: Process natural language queries
5. **Response**: Generate intelligent responses

---

## 🔒 Security & Privacy

### Data Protection
- All data encrypted at rest and in transit
- Secure OAuth 2.0 flows with token encryption
- User data isolation and anonymization
- GDPR and CCPA compliance planning

### Access Control
- Role-based access control (RBAC)
- Row-level security (RLS) for database
- Secure token storage and refresh

---

## 💰 Cost Optimization

### AI Usage Strategies
- **Batch Processing**: Process data in batches instead of real-time
- **Selective Ingestion**: Only process relevant data
- **Hybrid AI**: Use cheaper models for routine tasks
- **Optimized Prompts**: Reduce token usage through efficient prompts
- **Local Processing**: Use local tools where possible

### Cost-Saving Measures
- Leverage existing AI services (Gmail's Smart Compose, Zoom's transcription)
- Implement intelligent data filtering
- Use caching for repeated queries
- Optimize API call frequency

---

## 📚 Documentation

- **`docs/contributing.md`**: AI development guidelines and processes
- **`docs/project_goals.md`**: Detailed project objectives
- **`docs/tech_stack.md`**: Technology stack and architecture
- **`docs/deployment_architecture.md`**: Deployment strategies
- **`PROJECT_ROADMAP.md`**: Active project task list

---

## 🤝 Contributing

Please read `docs/contributing.md` for development guidelines, AI development patterns, and contribution processes.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For issues, questions, or contributions:
1. Check the documentation in `docs/`
2. Review `PROJECT_ROADMAP.md` for current status
3. Run the enhanced sandbox for testing: `python sandbox/enhanced_sandbox.py`
4. Open an issue with detailed information
#   g l a s s d e s k - p r o d u c t i o n  
 