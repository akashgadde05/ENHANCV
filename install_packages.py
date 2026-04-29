#!/usr/bin/env python3
"""
Complete package installation script for Smart ATS Resume Builder
Installs all required packages and sets up the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_packages():
    """Install all required packages"""
    print("🚀 Smart ATS Resume Builder - Package Installation")
    print("=" * 60)
    
    if not check_python_version():
        return False
    
    # Core packages
    core_packages = [
        "Flask==3.0.0",
        "groq==0.4.2",
        "python-dotenv==1.0.1",
        "pypdf==3.17.4",
        "python-docx==1.1.0",
        "reportlab==4.2.2",
        "requests==2.32.3"
    ]
    
    # Optional packages for enhanced functionality
    optional_packages = [
        "textblob==0.18.0",
        "pandas==2.2.0",
        "numpy==1.26.4",
        "Pillow==10.2.0",
        "nltk==3.8.1",
        "wordcloud==1.9.3",
        "plotly==5.18.0",
        "gunicorn==21.2.0"
    ]
    
    print("📋 Installing core packages...")
    failed_core = []
    for package in core_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            failed_core.append(package)
    
    print("\n📋 Installing optional packages...")
    failed_optional = []
    for package in optional_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            failed_optional.append(package)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Installation Summary")
    print("=" * 60)
    
    total_core = len(core_packages)
    success_core = total_core - len(failed_core)
    
    total_optional = len(optional_packages)
    success_optional = total_optional - len(failed_optional)
    
    print(f"Core packages: {success_core}/{total_core} installed")
    print(f"Optional packages: {success_optional}/{total_optional} installed")
    
    if failed_core:
        print(f"\n❌ Failed core packages: {', '.join(failed_core)}")
        print("⚠️  Some core functionality may not work")
    
    if failed_optional:
        print(f"\n⚠️  Failed optional packages: {', '.join(failed_optional)}")
        print("💡 These are optional - basic functionality will still work")
    
    if not failed_core:
        print("\n🎉 All core packages installed successfully!")
        print("🚀 You can now run the application!")
        
        # Check if .env file exists
        if not Path('.env').exists():
            print("\n📝 Next steps:")
            print("   1. Copy .env.example to .env")
            print("   2. Add your Groq API key to .env")
            print("   3. Run: python run.py")
        else:
            print("\n🏃 Ready to run:")
            print("   python run.py")
        
        return True
    else:
        print("\n❌ Some core packages failed to install")
        print("🔧 Try running: pip install --upgrade pip")
        return False

def create_venv_and_install():
    """Create virtual environment and install packages"""
    print("🔧 Creating virtual environment and installing packages...")
    
    commands = [
        ("python -m venv venv", "Creating virtual environment"),
        ("venv\\Scripts\\activate && pip install --upgrade pip", "Upgrading pip"),
        ("venv\\Scripts\\activate && pip install -r requirements.txt", "Installing from requirements.txt")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"❌ Failed at: {description}")
            return False
    
    print("✅ Virtual environment created and packages installed!")
    print("\n🏃 To activate the virtual environment:")
    print("   venv\\Scripts\\activate")
    print("   python run.py")
    
    return True

def main():
    """Main installation function"""
    print("🎯 Choose installation method:")
    print("1. Install in current environment")
    print("2. Create new virtual environment and install")
    print("3. Install core packages only")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            return install_packages()
        elif choice == "2":
            return create_venv_and_install()
        elif choice == "3":
            # Install only core packages
            core_only = [
                "Flask==3.0.0",
                "groq==0.4.2", 
                "python-dotenv==1.0.1",
                "pypdf==3.17.4",
                "python-docx==1.1.0",
                "reportlab==4.2.2"
            ]
            
            print("📦 Installing core packages only...")
            failed = []
            for package in core_only:
                if not run_command(f"pip install {package}", f"Installing {package}"):
                    failed.append(package)
            
            if not failed:
                print("✅ Core packages installed successfully!")
                return True
            else:
                print(f"❌ Failed packages: {', '.join(failed)}")
                return False
        else:
            print("❌ Invalid choice")
            return False
            
    except KeyboardInterrupt:
        print("\n👋 Installation cancelled")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)