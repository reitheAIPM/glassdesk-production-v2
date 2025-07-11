# GitHub CLI Reference

> **AI AGENT**: This file contains all GitHub CLI commands and usage. Reference this for repository and project management tasks.

---

## 🚀 **QUICK REFERENCE**

### **Essential Commands**
```bash
# Authentication
gh auth login                    # Login to GitHub
gh auth status                   # Check authentication status

# Repository Management
gh repo create                   # Create new repository
gh repo clone OWNER/REPO         # Clone repository
gh repo view                     # View repository info

# Issue & PR Management
gh issue create                  # Create new issue
gh pr create                     # Create pull request
gh pr list                       # List pull requests
```

---

## 🔐 **AUTHENTICATION**

### **Login & Status**
```bash
# Authentication
gh auth login                    # Interactive login
gh auth login --web              # Web-based login
gh auth login --with-token       # Login with token
gh auth logout                   # Logout from GitHub
gh auth status                   # Check authentication status
gh auth refresh                  # Refresh authentication token
```

### **Token Management**
```bash
# Token operations
gh auth token                    # Print auth token
gh auth setup-git               # Configure git to use GitHub CLI
```

---

## 📁 **REPOSITORY MANAGEMENT**

### **Create & Clone**
```bash
# Create repositories
gh repo create                   # Interactive repository creation
gh repo create NAME              # Create repository with name
gh repo create --public          # Create public repository
gh repo create --private         # Create private repository
gh repo create --source=.        # Create from current directory
gh repo create --template OWNER/REPO  # Create from template

# Clone repositories
gh repo clone OWNER/REPO         # Clone repository
gh repo clone OWNER/REPO -- --depth=1  # Shallow clone
gh repo clone OWNER/REPO PATH    # Clone to specific path
```

### **View & Browse**
```bash
# Repository information
gh repo view                     # View current repository
gh repo view OWNER/REPO          # View specific repository
gh repo view --web               # Open repository in browser
gh repo view --json              # Output as JSON

# Repository browsing
gh repo browse                   # Open repository in browser
gh repo browse --settings        # Open repository settings
gh repo browse --wiki            # Open repository wiki
```

### **Repository Operations**
```bash
# Repository actions
gh repo fork OWNER/REPO          # Fork repository
gh repo sync                     # Sync with upstream
gh repo archive                   # Archive repository
gh repo unarchive                # Unarchive repository
gh repo delete OWNER/REPO        # Delete repository
```

---

## 🔧 **ISSUE MANAGEMENT**

### **Create Issues**
```bash
# Create issues
gh issue create                  # Interactive issue creation
gh issue create --title "Title"  # Create with title
gh issue create --body "Body"    # Create with body
gh issue create --label "bug"    # Create with label
gh issue create --assignee USER   # Assign to user
gh issue create --project "Project"  # Add to project
```

### **View & List Issues**
```bash
# View issues
gh issue view NUMBER             # View specific issue
gh issue view --web              # Open issue in browser
gh issue list                    # List all issues
gh issue list --state open       # List open issues
gh issue list --assignee USER    # List assigned issues
gh issue list --author USER      # List authored issues
gh issue list --label "bug"      # List by label
```

### **Issue Operations**
```bash
# Issue actions
gh issue close NUMBER            # Close issue
gh issue reopen NUMBER           # Reopen issue
gh issue comment NUMBER          # Add comment to issue
gh issue edit NUMBER             # Edit issue
gh issue transfer OWNER/REPO     # Transfer issue
```

---

## 🔄 **PULL REQUEST MANAGEMENT**

### **Create Pull Requests**
```bash
# Create PRs
gh pr create                     # Interactive PR creation
gh pr create --title "Title"     # Create with title
gh pr create --body "Body"       # Create with body
gh pr create --draft             # Create as draft
gh pr create --base main         # Set base branch
gh pr create --head feature      # Set head branch
```

### **View & List PRs**
```bash
# View PRs
gh pr view NUMBER                # View specific PR
gh pr view --web                 # Open PR in browser
gh pr list                       # List all PRs
gh pr list --state open          # List open PRs
gh pr list --author USER         # List authored PRs
gh pr list --assignee USER       # List assigned PRs
gh pr list --label "enhancement" # List by label
```

### **PR Operations**
```bash
# PR actions
gh pr checkout NUMBER            # Checkout PR branch
gh pr checkout --rebase          # Checkout with rebase
gh pr close NUMBER               # Close PR
gh pr reopen NUMBER              # Reopen PR
gh pr merge NUMBER               # Merge PR
gh pr merge --squash            # Merge with squash
gh pr merge --rebase            # Merge with rebase
gh pr comment NUMBER             # Add comment to PR
gh pr review NUMBER              # Review PR
gh pr review --approve          # Approve PR
gh pr review --request-changes  # Request changes
```

---

## 🏷️ **LABELS & MILESTONES**

### **Label Management**
```bash
# Label operations
gh label list                    # List all labels
gh label create NAME             # Create label
gh label create --color COLOR    # Create with color
gh label edit NAME               # Edit label
gh label delete NAME             # Delete label
```

### **Milestone Management**
```bash
# Milestone operations
gh milestone list                # List milestones
gh milestone create              # Create milestone
gh milestone view NUMBER         # View milestone
gh milestone edit NUMBER         # Edit milestone
gh milestone delete NUMBER       # Delete milestone
```

---

## 👥 **USER & ORGANIZATION**

### **User Information**
```bash
# User commands
gh user view                     # View current user
gh user view USERNAME            # View specific user
gh user view --web               # Open user profile in browser
gh user list                     # List users (if applicable)
```

### **Organization Management**
```bash
# Organization commands
gh org list                      # List organizations
gh org view ORG                  # View organization
gh org view --web                # Open org in browser
gh org member list ORG           # List org members
gh org member add USER ORG       # Add member to org
gh org member remove USER ORG    # Remove member from org
```

---

## 🔍 **SEARCH & DISCOVERY**

### **Search Commands**
```bash
# Search repositories
gh search repos QUERY            # Search repositories
gh search repos --language js    # Search by language
gh search repos --stars >100     # Search by stars
gh search repos --user USER      # Search user's repos

# Search issues
gh search issues QUERY           # Search issues
gh search issues --repo OWNER/REPO  # Search in repo
gh search issues --state open    # Search open issues

# Search code
gh search code QUERY             # Search code
gh search code --language python # Search by language
gh search code --repo OWNER/REPO # Search in repo
```

---

## 📊 **PROJECTS & BOARDS**

### **Project Management**
```bash
# Project commands
gh project list                  # List projects
gh project create                # Create project
gh project view NUMBER           # View project
gh project edit NUMBER           # Edit project
gh project delete NUMBER         # Delete project
```

### **Project Items**
```bash
# Project item commands
gh project item-list NUMBER      # List project items
gh project item-add NUMBER       # Add item to project
gh project item-remove NUMBER    # Remove item from project
```

---

## 🔧 **WORKFLOW & AUTOMATION**

### **Workflow Commands**
```bash
# Workflow operations
gh workflow list                 # List workflows
gh workflow view NAME            # View workflow
gh workflow run NAME             # Run workflow
gh workflow run --field KEY=VAL  # Run with inputs
gh workflow run --ref BRANCH     # Run on specific branch
```

### **Actions & Secrets**
```bash
# Actions commands
gh secret list                   # List secrets
gh secret set NAME VALUE         # Set secret
gh secret delete NAME            # Delete secret

# Variable commands
gh variable list                 # List variables
gh variable set NAME VALUE       # Set variable
gh variable delete NAME          # Delete variable
```

---

## 📝 **GISTS**

### **Gist Management**
```bash
# Gist commands
gh gist create                   # Create gist
gh gist create FILE              # Create from file
gh gist create --public          # Create public gist
gh gist create --secret          # Create secret gist
gh gist list                     # List gists
gh gist view ID                  # View gist
gh gist edit ID                  # Edit gist
gh gist delete ID                # Delete gist
```

---

## 🎯 **GLASSDESK SPECIFIC COMMANDS**

### **Repository Setup**
```bash
# Clone GlassDesk repository
gh repo clone your-username/glassdesk

# Create new GlassDesk repository
gh repo create glassdesk --public --description "AI-powered personal assistant"

# Fork GlassDesk repository
gh repo fork original-owner/glassdesk
```

### **Issue Management**
```bash
# Create GlassDesk issues
gh issue create --title "Fix OAuth 500 error" --body "Production OAuth endpoint returning 500 error"
gh issue create --title "Add Zoom integration" --label "enhancement"
gh issue create --title "Test OpenAI integration" --assignee your-username

# List GlassDesk issues
gh issue list --label "bug"
gh issue list --state open
```

### **Pull Request Workflow**
```bash
# Create feature branch
git checkout -b feature/oauth-fix

# Make changes and commit
git add .
git commit -m "Fix OAuth environment variables"

# Create pull request
gh pr create --title "Fix OAuth 500 error" --body "Resolves production OAuth issues"

# Review and merge
gh pr review --approve
gh pr merge --squash
```

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues**
```bash
# Authentication issues
gh auth status                   # Check auth status
gh auth login                    # Re-authenticate
gh auth logout && gh auth login  # Clear and re-login

# Repository issues
gh repo view                     # Check current repo
gh repo sync                     # Sync with upstream

# Permission issues
gh auth refresh                  # Refresh token
gh auth setup-git               # Setup git integration
```

### **Debug Commands**
```bash
# Debug information
gh --version                     # Check CLI version
gh config list                   # List configuration
gh config get git_protocol       # Check git protocol
gh config set git_protocol ssh   # Set git protocol
```

---

## 📚 **RESOURCES**

### **Documentation**
- **GitHub CLI Docs**: https://cli.github.com/
- **GitHub CLI Reference**: https://docs.github.com/en/github-cli/github-cli/github-cli-reference
- **GitHub CLI Manual**: https://cli.github.com/manual/

### **Related Files**
- **Project Status**: `docs/PROJECT_STATUS.md`
- **Setup Guide**: `docs/SETUP_GUIDE.md`
- **Railway CLI**: `docs/RAILWAY_CLI_REFERENCE.md`

---

*Last Updated: 2024-07-11*
*AI Agent: Use this reference for all GitHub repository and project management tasks* 