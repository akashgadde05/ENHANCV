#!/usr/bin/env python3
"""
Simple installation script for Smart ATS Resume Builder
Handles common dependency issues
"""

import os
import sys
import subprocess
import platform

def get_python_info():
    """Get Python version and platform info"""
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Platform: {platform.system()} {platform.release()}")
    print(f"📦 Pip: ", end="")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        print(result.stdout.strip())
    except:
        print("Not available")

def install_package(package_name, alternative_name=None):
    """Install a package with fallback options"""
    packages_to_try = [package_name]
    if alternative_name:
        packages_to_try.append(alternative_name)
    
    for pkg in packages_to_try:
        try:
            print(f"📦 Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {pkg} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {pkg}")
            continue
    
    return False

def main():
    """Main installation function"""
    print("🚀 Smart ATS Resume Builder - Installation")
    print("=" * 50)
    
    get_python_info()
    print()
    
    # Core packages with alternatives
    packages = [
        ("Flask", None),
        ("groq", None),
        ("python-dotenv", "python_dotenv"),
        ("pypdf", "PyPDF2"),
        ("python-docx", "python_docx"),
        ("reportlab", None),
        ("textblob", None),
        ("requests", None),
        ("Pillow", "PIL")
    ]
    
    print("📦 Installing core packages...")
    failed_packages = []
    
    for package, alternative in packages:
        if not install_package(package, alternative):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    
    if not failed_packages:
        print("🎉 All packages installed successfully!")
        print("\n🚀 You can now run:")
        print("   python run.py")
    else:
        print(f"⚠️  Some packages failed to install: {failed_packages}")
        print("\n🔧 Try these solutions:")
        print("   1. Update pip: python -m pip install --upgrade pip")
        print("   2. Use virtual environment: python -m venv venv")
        print("   3. Install manually: pip install <package-name>")
        
        # Create a minimal requirements file for failed packages
        with open("requirements-failed.txt", "w") as f:
            for pkg in failed_packages:
                f.write(f"{pkg}\n")
        print(f"   4. Try: pip install -r requirements-failed.txt")

if __name__ == "__main__":
    main()