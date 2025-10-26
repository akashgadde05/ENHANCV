#!/usr/bin/env python3
"""
Setup script for Smart ATS Resume Builder & Analyzer
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Try minimal requirements first
    requirements_files = ["requirements-minimal.txt", "requirements.txt"]
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"📋 Trying {req_file}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
                print("✅ Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Failed with {req_file}: {e}")
                continue
    
    # If both fail, try installing core packages individually
    print("📦 Trying individual package installation...")
    core_packages = [
        "Flask>=3.0.0",
        "groq>=0.4.0", 
        "python-dotenv>=1.0.0",
        "pypdf>=3.17.0",
        "python-docx>=1.1.0",
        "reportlab>=4.2.0",
        "requests>=2.32.0"
    ]
    
    failed_packages = []
    for package in core_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package}")
        except subprocess.CalledProcessError:
            print(f"❌ {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"⚠️  Some packages failed to install: {failed_packages}")
        print("You may need to install them manually or use a different Python environment")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("📝 Creating .env file from template...")
        
        # Copy from .env.example
        example_path = Path(".env.example")
        if example_path.exists():
            with open(example_path, 'r') as src, open(env_path, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created from template")
        else:
            # Create basic .env file
            with open(env_path, 'w') as f:
                f.write("""# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Application Settings
APP_NAME=Smart ATS Resume Builder & Analyzer
DEBUG=True
SECRET_KEY=your-secret-key-here
""")
            print("✅ Basic .env file created")
    
    # Check if API key is set
    with open(env_path, 'r') as f:
        content = f.read()
        if "your_groq_api_key_here" in content:
            print("⚠️  Please update your Groq API key in the .env file")
            print("🔗 Get your API key from: https://console.groq.com/")
            return False
    
    print("✅ .env file configured")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "static/css", "static/js", "templates", "utils"]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def main():
    """Main setup function"""
    print("🚀 Smart ATS Resume Builder & Analyzer Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check environment file
    env_configured = check_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if env_configured:
        print("\n🚀 You can now run the application:")
        print("   python run.py")
    else:
        print("\n⚠️  Before running the application:")
        print("   1. Update your Groq API key in .env file")
        print("   2. Then run: python run.py")
    
    print("\n📖 For more information, check README.md")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)