#!/usr/bin/env python3
"""
Development setup script for GlassDesk
Helps new contributors set up their development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    try:
        # Use the virtual environment's pip
        if os.name == 'nt':  # Windows
            pip_path = "venv\\Scripts\\pip"
        else:  # Unix/Linux/Mac
            pip_path = "venv/bin/pip"
        
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment_file():
    """Create .env file from template"""
    env_file = Path(".env")
    template_file = Path("env_template.env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if template_file.exists():
        print("📝 Creating .env file from template...")
        shutil.copy(template_file, env_file)
        print("✅ .env file created (please update with your actual values)")
        return True
    else:
        print("❌ env_template.env not found")
        return False

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    try:
        # Use the virtual environment's python
        if os.name == 'nt':  # Windows
            python_path = "venv\\Scripts\\python"
        else:  # Unix/Linux/Mac
            python_path = "venv/bin/python"
        
        result = subprocess.run([python_path, "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print("❌ Tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up GlassDesk development environment...")
    print()
    print("📋 Note: This project uses mock data for development.")
    print("   See docs/mock_data_guidelines.md for usage rules and transition plans.")
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup completed")
    
    print()
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\Activate.ps1")
    else:
        print("   source venv/bin/activate")
    print("2. Update .env file with your API keys")
    print("3. Run the application: python main.py")
    print("4. Check the documentation in docs/")

if __name__ == "__main__":
    main() 