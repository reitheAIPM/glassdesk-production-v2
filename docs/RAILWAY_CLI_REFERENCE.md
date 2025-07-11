# Railway CLI Reference

> **AI AGENT**: This file contains all Railway CLI commands and usage. Reference this for deployment and management tasks.

---

## 🚀 **QUICK REFERENCE**

### **Essential Commands**
```bash
# Project Management
railway login                    # Login to Railway account
railway link                     # Link current directory to project
railway status                   # Show project status
railway up                       # Deploy current directory

# Environment Variables
railway variables                # Show all variables
railway variables --set KEY=VAL  # Set environment variable

# Monitoring
railway logs                     # View deployment logs
railway open                     # Open project dashboard
```

---

## 📋 **PROJECT MANAGEMENT**

### **Authentication & Linking**
```bash
# Authentication
railway login                    # Login to Railway account
railway logout                   # Logout of Railway account
railway whoami                   # Show current user

# Project Linking
railway link [PROJECT_ID]        # Link directory to project
railway unlink                   # Unlink current directory
railway list                     # List all projects
```

### **Project Status & Information**
```bash
# Status Commands
railway status                   # Show current project info
railway docs                     # Open Railway documentation
railway open                     # Open project dashboard
```

---

## 🚀 **DEPLOYMENT COMMANDS**

### **Deploy Applications**
```bash
# Deploy from current directory
railway up                       # Deploy current directory
railway up [PATH]               # Deploy specific path
railway up --detach             # Deploy without log streaming
railway up --ci                 # CI mode (build logs only)

# Deploy Templates
railway deploy --template TEMPLATE  # Deploy template
railway deploy -t postgres -v "VAR=value"  # Deploy with variables

# Redeploy
railway redeploy                # Redeploy latest deployment
railway down                    # Remove most recent deployment
```

### **Service Management**
```bash
# Service Operations
railway service [SERVICE]        # Link service to project
railway add --service NAME       # Add new service
railway add --database TYPE      # Add database (postgres, mysql, redis, mongo)
```

---

## 🔧 **ENVIRONMENT VARIABLES**

### **View Variables**
```bash
# Show all variables
railway variables                # Show variables for active environment
railway variables --service SERVICE  # Show variables for specific service
railway variables --environment ENV  # Show variables for specific environment
railway variables --kv           # Show in key-value format
```

### **Set Variables**
```bash
# Set single variable
railway variables --set "KEY=value"

# Set multiple variables
railway variables --set "KEY1=value1" --set "KEY2=value2"

# Set service-specific variables
railway variables --set "SERVICE.KEY=value"
```

### **Environment Management**
```bash
# Environment operations
railway environment              # Show environment selector
railway environment ENV         # Link to specific environment
railway environment new NAME    # Create new environment
railway environment delete ENV  # Delete environment
railway environment new foo --duplicate bar  # Duplicate environment
```

---

## 📊 **MONITORING & LOGS**

### **View Logs**
```bash
# Log commands
railway logs                    # View deployment logs
railway logs --service SERVICE  # View service-specific logs
```

### **Database Connections**
```bash
# Connect to databases
railway connect                 # Connect to database shell
railway connect SERVICE_NAME    # Connect to specific database

# Available database shells:
# - Postgres: psql
# - Redis: redis-cli  
# - MongoDB: mongosh
# - MySQL: mysql
```

---

## 🌐 **DOMAIN & NETWORKING**

### **Domain Management**
```bash
# Domain commands
railway domain                  # Generate Railway domain
railway domain CUSTOM_DOMAIN    # Add custom domain
railway domain --port PORT      # Specify port for domain
railway domain --service SERVICE # Domain for specific service
```

---

## 🛠️ **DEVELOPMENT TOOLS**

### **Local Development**
```bash
# Run commands with Railway environment
railway run COMMAND             # Run command with Railway variables
railway run --service SERVICE   # Run with specific service variables
railway run --environment ENV   # Run with specific environment

# Shell with Railway variables
railway shell                   # Open subshell with Railway variables
railway shell --service SERVICE # Shell with service variables
```

### **SSH Access**
```bash
# SSH into services
railway ssh                     # SSH into service
railway ssh --service SERVICE   # SSH into specific service
railway ssh --project PROJECT   # SSH into specific project
railway ssh COMMAND             # Execute command via SSH
```

---

## 📦 **SERVICE MANAGEMENT**

### **Add Services**
```bash
# Add different service types
railway add --service NAME      # Add application service
railway add --database postgres # Add PostgreSQL database
railway add --database mysql    # Add MySQL database
railway add --database redis    # Add Redis database
railway add --database mongo    # Add MongoDB database

# Add with variables
railway add --service NAME --variables "KEY=value"
```

### **Service Variables**
```bash
# Set service variables during creation
railway add --service NAME --variables "PORT=3000" --variables "NODE_ENV=production"

# Set variables for specific service
railway variables --service SERVICE --set "KEY=value"
```

---

## 💾 **VOLUME MANAGEMENT**

### **Volume Operations**
```bash
# Volume commands
railway volume list             # List all volumes
railway volume add              # Add new volume
railway volume delete VOLUME    # Delete volume
railway volume update VOLUME    # Update volume
railway volume attach VOLUME    # Attach volume to service
railway volume detach VOLUME    # Detach volume from service
```

---

## 🔍 **TROUBLESHOOTING COMMANDS**

### **Common Debugging**
```bash
# Check project status
railway status                  # Verify project linking
railway whoami                  # Check authentication
railway list                    # List available projects

# Check environment
railway variables               # Verify environment variables
railway logs                    # Check for errors
railway open                    # Open dashboard for manual check
```

### **Deployment Issues**
```bash
# Redeploy if issues
railway redeploy               # Redeploy latest version
railway down                   # Rollback to previous deployment
railway up --verbose           # Deploy with verbose output
```

---

## 📝 **USAGE EXAMPLES**

### **Complete Deployment Workflow**
```bash
# 1. Login and link project
railway login
railway link

# 2. Set environment variables
railway variables --set "GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID"
railway variables --set "GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET"
railway variables --set "OPENAI_API_KEY=your_openai_key"

# 3. Deploy application
railway up

# 4. Check deployment
railway logs
railway open
```

### **Database Setup**
```bash
# Add PostgreSQL database
railway add --database postgres

# Connect to database
railway connect

# Set database variables
railway variables --set "DATABASE_URL=postgresql://..."
```

### **Environment Management**
```bash
# Create production environment
railway environment new production

# Switch to production
railway environment production

# Set production variables
railway variables --set "NODE_ENV=production"
railway variables --set "LOG_LEVEL=info"
```

---

## 🎯 **GLASSDESK SPECIFIC COMMANDS**

### **Production Deployment**
```bash
# Deploy GlassDesk to production
railway up

# Set GlassDesk environment variables
railway variables --set "GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID"
railway variables --set "GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET"
railway variables --set "OPENAI_API_KEY=your_openai_key"
railway variables --set "SECRET_KEY=your_secret_key"

# Check deployment status
railway status
railway logs
```

### **Database Management**
```bash
# Add PostgreSQL for GlassDesk
railway add --database postgres

# Connect to database for debugging
railway connect

# Check database variables
railway variables | grep DATABASE
```

---

## 📚 **RESOURCES**

### **Documentation**
- **Railway Docs**: https://docs.railway.app/
- **CLI Reference**: https://docs.railway.com/reference/cli-api
- **Deployment Guide**: https://docs.railway.app/deploy/deployments

### **Related Files**
- **Deployment Status**: `docs/DEPLOYMENT_STATUS.md`
- **Setup Guide**: `docs/SETUP_GUIDE.md`
- **Project Status**: `docs/PROJECT_STATUS.md`

---

*Last Updated: 2024-07-11*
*AI Agent: Use this reference for all Railway deployment and management tasks* 