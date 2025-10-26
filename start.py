#!/usr/bin/env python3
"""
Quick start script for Smart ATS Resume Builder
Automatically detects available dependencies and runs the best version
"""

import os
import sys
import subprocess
from pathlib import Path

def check_package(package_name):
    """Check if a package is available"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_dependencies():
    """Check which dependencies are available"""
    deps = {
        'flask': check_package('flask'),
        'groq': check_package('groq'),
        'dotenv': check_package('dotenv'),
        'pypdf': check_package('pypdf'),
        'docx': check_package('docx'),
        'reportlab': check_package('reportlab'),
    }
    return deps

def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path('.env')
    if not env_path.exists():
        return False, "No .env file found"
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
            if 'your_groq_api_key_here' in content or 'GROQ_API_KEY=' not in content:
                return False, "Groq API key not configured"
        return True, "Environment configured"
    except Exception as e:
        return False, f"Error reading .env: {e}"

def main():
    """Main function to start the application"""
    print("🚀 Smart ATS Resume Builder - Quick Start")
    print("=" * 50)
    
    # Check dependencies
    deps = check_dependencies()
    missing_deps = [name for name, available in deps.items() if not available]
    
    print("📦 Dependency Status:")
    for name, available in deps.items():
        status = "✅" if available else "❌"
        print(f"   {status} {name}")
    
    # Check environment
    env_ok, env_msg = check_env_file()
    print(f"\n🔧 Environment: {'✅' if env_ok else '❌'} {env_msg}")
    
    print("\n" + "=" * 50)
    
    # Decide which version to run
    if not deps['flask']:
        print("❌ Flask is required but not installed")
        print("💡 Run: pip install flask")
        return False
    
    if missing_deps:
        print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("🔄 Starting minimal version...")
        
        if not env_ok:
            print("⚠️  Some features may not work without proper configuration")
        
        # Run minimal version
        try:
            os.system("python app_minimal.py")
        except KeyboardInterrupt:
            print("\n👋 Application stopped")
        except Exception as e:
            print(f"❌ Error running minimal app: {e}")
            return False
    else:
        print("✅ All dependencies available!")
        
        if not env_ok:
            print("⚠️  Environment not configured - some features may not work")
        
        print("🚀 Starting full application...")
        
        # Run full version
        try:
            os.system("python run.py")
        except KeyboardInterrupt:
            print("\n👋 Application stopped")
        except Exception as e:
            print(f"❌ Error running app: {e}")
            return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)