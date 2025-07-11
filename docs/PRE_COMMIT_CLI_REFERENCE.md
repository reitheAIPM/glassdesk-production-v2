# Pre-commit CLI Reference for GlassDesk

> **AI AGENT**: This document provides comprehensive pre-commit commands for GlassDesk code quality, testing automation, and development workflows. Use this to maintain 94% test coverage and code quality.

---

## 🎯 **ESSENTIAL PRE-COMMIT COMMANDS**

### **Installation**
```bash
# Install pre-commit
pip install pre-commit

# Verify installation
pre-commit --version
```

**📚 Official Docs**: https://pre-commit.com/

---

## 🚀 **GLASSDESK PRE-COMMIT SETUP**

### **Initial Setup**
```bash
# Initialize pre-commit in GlassDesk project
pre-commit install

# Install commit-msg hook
pre-commit install --hook-type commit-msg

# Verify hooks are installed
pre-commit run --all-files
```

### **GlassDesk Configuration (.pre-commit-config.yaml)**
```yaml
repos:
  # Code formatting
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=88]

  # Linting
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --ignore=E203,W503]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--ignore-missing-imports]

  # Security checks
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, app/, -f, json, -o, bandit-report.json]

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: check-docstring-first
      - id: check-json
      - id: debug-statements
      - id: name-tests-test
      - id: requirements-txt-fixer

  # Import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  # Test coverage
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests/, -v, --cov=app, --cov-report=term-missing]
```

---

## 🔧 **CODE QUALITY COMMANDS**

### **Run All Hooks**
```bash
# Run all hooks on all files
pre-commit run --all-files

# Run all hooks on staged files only
pre-commit run

# Run specific hook
pre-commit run black
pre-commit run flake8
pre-commit run mypy
pre-commit run bandit
```

### **Individual Hook Commands**
```bash
# Black formatting
pre-commit run black --all-files

# Flake8 linting
pre-commit run flake8 --all-files

# MyPy type checking
pre-commit run mypy --all-files

# Bandit security
pre-commit run bandit --all-files

# Import sorting
pre-commit run isort --all-files
```

### **Testing Commands**
```bash
# Run tests with coverage
pre-commit run pytest

# Run tests on specific files
pre-commit run pytest --files app/ai_interface.py

# Run tests with verbose output
pre-commit run pytest --verbose
```

---

## 🎯 **GLASSDESK-SPECIFIC WORKFLOWS**

### **Daily Development Workflow**
```bash
# 1. Make changes to code
# 2. Stage files
git add .

# 3. Run pre-commit hooks
pre-commit run --all-files

# 4. If hooks pass, commit
git commit -m "Add new feature"

# 5. If hooks fail, fix issues and repeat
```

### **Code Quality Workflow**
```bash
# 1. Check formatting
pre-commit run black --all-files

# 2. Check linting
pre-commit run flake8 --all-files

# 3. Check types
pre-commit run mypy --all-files

# 4. Check security
pre-commit run bandit --all-files

# 5. Run tests
pre-commit run pytest
```

### **Pre-commit Debugging Workflow**
```bash
# 1. Check hook status
pre-commit run --all-files --verbose

# 2. Run specific hook with debug
pre-commit run black --all-files --verbose

# 3. Check hook configuration
pre-commit run --all-files --show-diff-on-failure

# 4. Skip hooks if needed
git commit -m "WIP: skip hooks" --no-verify
```

---

## 🔍 **DEBUGGING COMMANDS**

### **Hook Debugging**
```bash
# Show hook information
pre-commit run --all-files --verbose

# Show hook diff
pre-commit run --all-files --show-diff-on-failure

# Run hook with debug output
pre-commit run black --all-files --verbose

# Check hook configuration
pre-commit run --all-files --verbose --hook-stage manual
```

### **Configuration Debugging**
```bash
# Validate configuration
pre-commit validate-config

# Show installed hooks
pre-commit run --all-files --verbose

# Check hook versions
pre-commit run --all-files --verbose | grep "Using"

# Debug specific hook
pre-commit run black --all-files --verbose --hook-stage manual
```

### **Common Issues**
```bash
# Fix hook installation
pre-commit uninstall
pre-commit install

# Update hooks
pre-commit autoupdate

# Clean hook cache
pre-commit clean

# Reinstall hooks
pre-commit install --overwrite
```

---

## 📊 **TESTING AUTOMATION**

### **Test Coverage Commands**
```bash
# Run tests with coverage
pre-commit run pytest

# Run tests on specific modules
pre-commit run pytest --files app/ai_interface.py app/oauth_manager.py

# Run tests with coverage report
pre-commit run pytest --args="--cov=app --cov-report=html"

# Run tests with coverage threshold
pre-commit run pytest --args="--cov=app --cov-fail-under=94"
```

### **Test Configuration**
```yaml
# Add to .pre-commit-config.yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest
      entry: pytest
      language: system
      pass_filenames: false
      always_run: true
      args: [tests/, -v, --cov=app, --cov-report=term-missing, --cov-fail-under=94]
```

### **Test Workflows**
```bash
# Quick test run
pre-commit run pytest

# Full test suite
pre-commit run pytest --all-files

# Test with coverage
pre-commit run pytest --args="--cov=app --cov-report=html"

# Test specific test file
pre-commit run pytest --files tests/test_ai_interface.py
```

---

## 🔐 **SECURITY CHECKS**

### **Bandit Security Scanning**
```bash
# Run security scan
pre-commit run bandit --all-files

# Run security scan with JSON output
pre-commit run bandit --all-files --args="-f json -o bandit-report.json"

# Run security scan on specific directories
pre-commit run bandit --files app/oauth_manager.py app/ai_interface.py

# Run security scan with custom config
pre-commit run bandit --args="-c .bandit -r app/"
```

### **Security Configuration**
```yaml
# Add to .pre-commit-config.yaml
- repo: https://github.com/PyCQA/bandit
  rev: 1.7.5
  hooks:
    - id: bandit
      args: [-r, app/, -f, json, -o, bandit-report.json, -c, .bandit]
```

### **Security Workflows**
```bash
# Daily security check
pre-commit run bandit --all-files

# Security check on OAuth files
pre-commit run bandit --files app/oauth_manager.py

# Security check with custom config
pre-commit run bandit --args="-c .bandit -r app/ -f json"
```

---

## 📝 **CODE FORMATTING**

### **Black Formatting**
```bash
# Format all files
pre-commit run black --all-files

# Format specific files
pre-commit run black --files app/ai_interface.py

# Format with custom line length
pre-commit run black --args="--line-length=88"

# Check formatting without changes
pre-commit run black --args="--check"
```

### **Import Sorting**
```bash
# Sort imports
pre-commit run isort --all-files

# Sort imports with Black profile
pre-commit run isort --args="--profile=black"

# Check import sorting
pre-commit run isort --args="--check-only"
```

### **Formatting Workflows**
```bash
# Format all code
pre-commit run black --all-files
pre-commit run isort --all-files

# Check formatting
pre-commit run black --args="--check"
pre-commit run isort --args="--check-only"

# Format specific modules
pre-commit run black --files app/ai_interface.py app/oauth_manager.py
pre-commit run isort --files app/ai_interface.py app/oauth_manager.py
```

---

## 🔍 **LINTING AND TYPE CHECKING**

### **Flake8 Linting**
```bash
# Run linting
pre-commit run flake8 --all-files

# Run linting with custom config
pre-commit run flake8 --args="--max-line-length=88 --ignore=E203,W503"

# Run linting on specific files
pre-commit run flake8 --files app/ai_interface.py
```

### **MyPy Type Checking**
```bash
# Run type checking
pre-commit run mypy --all-files

# Run type checking with ignore missing imports
pre-commit run mypy --args="--ignore-missing-imports"

# Run strict type checking
pre-commit run mypy --args="--strict"

# Run type checking on specific files
pre-commit run mypy --files app/ai_interface.py
```

### **Linting Workflows**
```bash
# Run all linting
pre-commit run flake8 --all-files
pre-commit run mypy --all-files

# Check specific modules
pre-commit run flake8 --files app/ai_interface.py app/oauth_manager.py
pre-commit run mypy --files app/ai_interface.py app/oauth_manager.py
```

---

## 🚀 **ADVANCED FEATURES**

### **Custom Hooks**
```yaml
# Add custom hook to .pre-commit-config.yaml
- repo: local
  hooks:
    - id: glassdesk-tests
      name: GlassDesk Tests
      entry: python -m pytest
      language: system
      pass_filenames: false
      always_run: true
      args: [tests/, -v, --cov=app]
```

### **Hook Stages**
```bash
# Run hooks at different stages
pre-commit run --all-files --hook-stage commit
pre-commit run --all-files --hook-stage push
pre-commit run --all-files --hook-stage manual
```

### **Hook Filtering**
```bash
# Run hooks on specific file types
pre-commit run --all-files --files "*.py"

# Run hooks on specific directories
pre-commit run --all-files --files app/

# Run hooks excluding certain files
pre-commit run --all-files --files "*.py" --exclude "tests/"
```

---

## 📊 **MONITORING AND REPORTING**

### **Coverage Reports**
```bash
# Generate coverage report
pre-commit run pytest --args="--cov=app --cov-report=html"

# Generate coverage report with threshold
pre-commit run pytest --args="--cov=app --cov-report=html --cov-fail-under=94"

# Generate coverage report for specific modules
pre-commit run pytest --args="--cov=app --cov-report=html --cov=app/ai_interface.py"
```

### **Security Reports**
```bash
# Generate security report
pre-commit run bandit --args="-r app/ -f json -o bandit-report.json"

# Generate security report with custom config
pre-commit run bandit --args="-c .bandit -r app/ -f json -o bandit-report.json"
```

### **Quality Reports**
```bash
# Generate all reports
pre-commit run --all-files --verbose

# Generate specific reports
pre-commit run black --all-files --verbose
pre-commit run flake8 --all-files --verbose
pre-commit run mypy --all-files --verbose
```

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**
```bash
# Hook installation issues
pre-commit uninstall
pre-commit install --overwrite

# Hook update issues
pre-commit autoupdate

# Hook cache issues
pre-commit clean

# Hook configuration issues
pre-commit validate-config
```

### **Debugging Commands**
```bash
# Show hook information
pre-commit run --all-files --verbose

# Show hook diff
pre-commit run --all-files --show-diff-on-failure

# Debug specific hook
pre-commit run black --all-files --verbose --hook-stage manual

# Check hook versions
pre-commit run --all-files --verbose | grep "Using"
```

### **Performance Issues**
```bash
# Run hooks in parallel
pre-commit run --all-files --parallel

# Run hooks with timeout
pre-commit run --all-files --timeout 300

# Run hooks with memory limit
pre-commit run --all-files --memory-limit 1G
```

---

## 📝 **CONFIGURATION FILES**

### **.pre-commit-config.yaml**
```yaml
# GlassDesk pre-commit configuration
repos:
  # Code formatting
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3
        args: [--line-length=88]

  # Linting
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --ignore=E203,W503]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--ignore-missing-imports]

  # Security checks
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, app/, -f, json, -o, bandit-report.json]

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: check-docstring-first
      - id: check-json
      - id: debug-statements
      - id: name-tests-test
      - id: requirements-txt-fixer

  # Import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  # Test coverage
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [tests/, -v, --cov=app, --cov-report=term-missing, --cov-fail-under=94]
```

### **.bandit**
```ini
# Bandit security configuration
[bandit]
exclude_dirs = tests
skips = B101,B601
```

### **.flake8**
```ini
# Flake8 configuration
[flake8]
max-line-length = 88
extend-ignore = E203,W503
exclude = .git,__pycache__,build,dist
```

---

## 🎯 **AI AGENT EFFICIENCY TIPS**

### **For Code Quality**
1. **Run `pre-commit run --all-files`** before commits - catches issues early
2. **Use `pre-commit run black`** for formatting - maintains consistent style
3. **Use `pre-commit run flake8`** for linting - catches style issues
4. **Use `pre-commit run mypy`** for type checking - catches type errors

### **For Testing**
1. **Use `pre-commit run pytest`** for test automation - maintains 94% coverage
2. **Use `--cov=app`** for coverage tracking - monitors test coverage
3. **Use `--cov-fail-under=94`** for coverage threshold - enforces quality
4. **Use `--verbose`** for detailed output - helps debugging

### **For Security**
1. **Use `pre-commit run bandit`** for security scanning - catches vulnerabilities
2. **Use `-f json`** for structured reports - easier to parse
3. **Use `-r app/`** for specific directories - focused scanning
4. **Use custom config** for project-specific rules - tailored security

---

*Last Updated: 2024-07-11*
*AI Agent: Use this reference for all pre-commit commands in GlassDesk development* 