# GlassDesk CLI Tools Reference

> **AI AGENT**: This document lists all CLI tools essential for GlassDesk development. Install these tools for maximum development efficiency.

---

## 🎯 **ESSENTIAL CLI TOOLS**

### **1. Database & Migration Tools**

#### **Alembic CLI** (Already in stack)
```bash
# Install
pip install alembic

# Usage
alembic init alembic
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
alembic downgrade -1
alembic current
alembic history
```

**📚 Official Docs**: https://alembic.sqlalchemy.org/en/latest/api/commands.html

#### **PostgreSQL CLI (psql)** - Railway Managed PostgreSQL
```bash
# Install (Windows)
# Download from https://www.postgresql.org/download/windows/

# Usage (Railway PostgreSQL)
psql -h localhost -U username -d glassdesk
psql -h glassdesk-production.up.railway.app -U $DATABASE_USERNAME -d $DATABASE_NAME

# Common commands
\dt                    # List tables
\d table_name         # Describe table
SELECT * FROM users;  # Query data
\q                    # Quit
```

**📚 Official Docs**: https://www.postgresql.org/docs/current/app-psql.html
**💡 Note**: GlassDesk uses Railway's managed PostgreSQL, not Supabase

#### **SQLite CLI**
```bash
# Install (usually comes with Python)
# Usage
sqlite3 glassdesk.db
.tables               # List tables
.schema users         # Show table schema
SELECT * FROM users;  # Query data
.quit                # Quit
```

### **2. API Testing & Development**

#### **HTTPie** (Better than curl)
```bash
# Install
pip install httpie

# Usage
http GET https://glassdesk-production.up.railway.app/health
http POST https://glassdesk-production.up.railway.app/auth/google/login
http GET https://glassdesk-production.up.railway.app/ai/query q=="summarize my emails"

# With authentication
http GET https://api.example.com/users Authorization:"Bearer token"
```

**📚 Official Docs**: https://httpie.io/docs/cli/request-url

#### **jq** (JSON Processing)
```bash
# Install (Windows)
# Download from https://stedolan.github.io/jq/download/

# Usage
curl -s https://glassdesk-production.up.railway.app/health | jq .
curl -s https://api.example.com/users | jq '.[0].name'
curl -s https://api.example.com/users | jq '.[] | select(.active == true)'
```

**📚 Official Docs**: https://jqlang.org/manual/?utm_source=chatgpt.com

### **3. Code Quality & Development**

#### **pre-commit** (Git Hooks)
```bash
# Install
pip install pre-commit

# Setup
pre-commit install
pre-commit install --hook-type commit-msg

# Usage
pre-commit run --all-files
pre-commit run black
pre-commit run flake8
```

**📚 Official Docs**: https://pre-commit.com/

#### **mypy** (Static Type Checking)
```bash
# Install
pip install mypy

# Usage
mypy app/
mypy --ignore-missing-imports app/
mypy --strict app/
```

**📚 Official Docs**: https://mypy.readthedocs.io/en/stable/command_line.html

#### **bandit** (Security Linting)
```bash
# Install
pip install bandit

# Usage
bandit -r app/
bandit -f json -o bandit-report.json app/
```

**📚 Official Docs**: https://github.com/PyCQA/bandit

#### **safety** (Dependency Security)
```bash
# Install
pip install safety

# Usage
safety check
safety check --json
safety check --output json > safety-report.json
```

**📚 Official Docs**: https://github.com/pyupio/safety (GitHub repository)

### **4. Environment & Configuration**

#### **direnv** (Auto Environment Loading)
```bash
# Install (Windows - via chocolatey)
choco install direnv

# Usage
# Create .envrc file in project root
echo "export DATABASE_URL=postgresql://..." > .envrc
direnv allow
```

#### **dotenv-cli**
```bash
# Install
npm install -g dotenv-cli

# Usage
dotenv -e .env python main.py
dotenv -e .env.test pytest tests/
```

### **5. Monitoring & Debugging**

#### **htop** (System Monitoring)
```bash
# Install (Windows - via WSL or alternative)
# Alternative: Use Windows Task Manager or Process Explorer

# Usage (Linux/WSL)
htop
htop -p $(pgrep python)
```

#### **lsof** (Network Connections)
```bash
# Install (Windows - via WSL)
# Alternative: netstat on Windows

# Usage
lsof -i :8000
lsof -i tcp
```

### **6. AI Development Specific**

#### **OpenAI CLI**
```bash
# Install
pip install openai

# Usage
openai api chat.completions.create --model gpt-4 --message "Hello"
openai api models.list
```

#### **LangChain CLI** (if available)
```bash
# Install
pip install langchain-cli

# Usage
langchain app new my-app
langchain app serve
```

### **7. Deployment & Infrastructure**

#### **Docker CLI**
```bash
# Install
# Download from https://www.docker.com/products/docker-desktop/

# Usage
docker build -t glassdesk .
docker run -p 8000:8000 glassdesk
docker-compose up -d
```

---

## 🚀 **GLASSDESK-SPECIFIC CLI WORKFLOWS**

### **Development Workflow**
```bash
# 1. Start development environment
direnv allow
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
alembic upgrade head

# 4. Run tests
pytest tests/ -v --cov=app

# 5. Start development server
uvicorn main:app --reload
```

### **API Testing Workflow**
```bash
# 1. Test health endpoint
http GET https://glassdesk-production.up.railway.app/health

# 2. Test OAuth endpoint
http GET https://glassdesk-production.up.railway.app/auth/google/login

# 3. Test AI endpoint
http POST https://glassdesk-production.up.railway.app/ai/query \
  q=="summarize my recent emails"

# 4. Check response with jq
http GET https://glassdesk-production.up.railway.app/health | jq .
```

### **Database Management Workflow**
```bash
# 1. Check current migration
alembic current

# 2. Create new migration
alembic revision --autogenerate -m "Add new feature"

# 3. Apply migration
alembic upgrade head

# 4. Check database (local)
sqlite3 glassdesk.db ".tables"

# 5. Check database (production)
psql -h glassdesk-production.up.railway.app -U $DATABASE_USERNAME -d $DATABASE_NAME -c "\dt"
```

### **Code Quality Workflow**
```bash
# 1. Run pre-commit hooks
pre-commit run --all-files

# 2. Run type checking
mypy app/

# 3. Run security checks
bandit -r app/
safety check

# 4. Run tests with coverage
pytest tests/ -v --cov=app --cov-report=html
```

---

## 📦 **INSTALLATION SCRIPTS**

### **Windows Installation Script**
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install CLI tools
choco install git postgresql jq direnv

# Install Python tools
pip install pre-commit mypy bandit safety httpie
```

### **Linux/macOS Installation Script**
```bash
# Install CLI tools
sudo apt-get update
sudo apt-get install -y postgresql-client jq direnv htop

# Install Python tools
pip install pre-commit mypy bandit safety httpie
```

---

## 🔧 **CONFIGURATION FILES**

### **.pre-commit-config.yaml**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### **mypy.ini**
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### **.envrc**
```bash
export DATABASE_URL="postgresql://user:pass@localhost/glassdesk"
export OPENAI_API_KEY="your-key-here"
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
```

---

## 📊 **MONITORING COMMANDS**

### **Production Monitoring**
```bash
# Check Railway deployment
railway status

# Check application health
http GET https://glassdesk-production.up.railway.app/health

# Check logs
railway logs

# Monitor database connections
psql -h glassdesk-production.up.railway.app -U $DATABASE_USERNAME -d $DATABASE_NAME -c "SELECT count(*) FROM pg_stat_activity;"
```

### **Local Development Monitoring**
```bash
# Monitor Python processes
htop -p $(pgrep python)

# Monitor network connections
lsof -i :8000

# Monitor file changes
watch -n 1 "find app/ -name '*.py' -mtime -1"
```

---

## 🎯 **AI AGENT EFFICIENCY TIPS**

### **For AI Development**
1. **Use HTTPie** for API testing - more readable than curl
2. **Use jq** for JSON processing - essential for API responses
3. **Use pre-commit** for code quality - prevents issues before commit
4. **Use mypy** for type checking - catches errors early
5. **Use bandit** for security - prevents vulnerabilities

### **For Database Management**
1. **Use Alembic** for migrations - version control for database
2. **Use psql** for direct queries - faster than GUI tools
3. **Use SQLite CLI** for local development - lightweight and fast

### **For Deployment**
1. **Use Railway CLI** for deployment management
2. **Use Docker** for containerization (future)
3. **Use direnv** for environment management

---

*Last Updated: 2024-07-11*
*AI Agent: Install these tools for maximum development efficiency* 