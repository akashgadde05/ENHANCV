#!/usr/bin/env python3
"""
System check script for Smart ATS Resume Builder
Verifies all components and provides detailed status
"""

import os
import sys
import platform
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print('='*50)

def check_python():
    """Check Python version and environment"""
    print_header("Python Environment")
    
    print(f"🐍 Python Version: {sys.version}")
    print(f"💻 Platform: {platform.system()} {platform.release()}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version compatible")
        return True

def check_files():
    """Check if required files exist"""
    print_header("Required Files")
    
    required_files = [
        'app.py',
        'app_minimal.py', 
        'run.py',
        'requirements.txt',
        'requirements-minimal.txt',
        '.env.example'
    ]
    
    optional_files = [
        '.env',
        'utils/llm_analyzer.py',
        'utils/resume_analyzer.py',
        'utils/pdf_generator.py',
        'templates/index.html',
        'static/css/style.css'
    ]
    
    all_good = True
    
    print("📋 Required Files:")
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            all_good = False
    
    print("\n📋 Optional Files:")
    for file in optional_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️  {file} - Missing (some features may not work)")
    
    return all_good

def check_dependencies():
    """Check Python package dependencies"""
    print_header("Python Dependencies")
    
    # Core dependencies
    core_deps = {
        'flask': 'Flask web framework',
        'groq': 'Groq LLM API client',
        'dotenv': 'Environment variable loader',
    }
    
    # Optional dependencies
    optional_deps = {
        'pypdf': 'PDF file processing',
        'docx': 'Word document processing', 
        'reportlab': 'PDF generation',
        'textblob': 'Text analysis',
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'requests': 'HTTP requests'
    }
    
    print("🔧 Core Dependencies:")
    core_ok = True
    for package, description in core_deps.items():
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} - MISSING")
            core_ok = False
    
    print("\n🔧 Optional Dependencies:")
    optional_count = 0
    for package, description in optional_deps.items():
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
            optional_count += 1
        except ImportError:
            print(f"   ⚠️  {package} - {description} - Missing")
    
    print(f"\n📊 Optional packages available: {optional_count}/{len(optional_deps)}")
    
    return core_ok, optional_count

def check_environment():
    """Check environment configuration"""
    print_header("Environment Configuration")
    
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("💡 Copy .env.example to .env and configure your API key")
        return False
    
    print("✅ .env file exists")
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Check for API key
        if 'GROQ_API_KEY=' in content:
            if 'your_groq_api_key_here' in content:
                print("⚠️  Groq API key not configured (using placeholder)")
                print("💡 Get your API key from https://console.groq.com/")
                return False
            else:
                print("✅ Groq API key configured")
                return True
        else:
            print("❌ GROQ_API_KEY not found in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print_header("Directory Structure")
    
    required_dirs = ['utils', 'templates', 'static']
    optional_dirs = ['uploads', 'static/css', 'static/js']
    
    print("📁 Required Directories:")
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"   ✅ {directory}/")
        else:
            print(f"   ❌ {directory}/ - MISSING")
            # Create missing directory
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   🔧 Created {directory}/")
    
    print("\n📁 Optional Directories:")
    for directory in optional_dirs:
        if Path(directory).exists():
            print(f"   ✅ {directory}/")
        else:
            print(f"   ⚠️  {directory}/ - Missing")
            # Create missing directory
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   🔧 Created {directory}/")

def test_imports():
    """Test importing main modules"""
    print_header("Module Import Test")
    
    modules_to_test = [
        ('app', 'Main Flask application'),
        ('app_minimal', 'Minimal Flask application'),
        ('utils.llm_analyzer', 'LLM analyzer (optional)'),
        ('utils.resume_analyzer', 'Resume analyzer (optional)'),
        ('utils.pdf_generator', 'PDF generator (optional)')
    ]
    
    import_results = {}
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {module_name} - {description}")
            import_results[module_name] = True
        except ImportError as e:
            print(f"   ❌ {module_name} - {description} - Import failed: {e}")
            import_results[module_name] = False
        except Exception as e:
            print(f"   ⚠️  {module_name} - {description} - Error: {e}")
            import_results[module_name] = False
    
    return import_results

def provide_recommendations(core_ok, optional_count, env_ok, import_results):
    """Provide recommendations based on system check"""
    print_header("Recommendations")
    
    if not core_ok:
        print("🚨 CRITICAL: Core dependencies missing")
        print("   Run: pip install flask groq python-dotenv")
        print("   Or: python install.py")
    
    if not env_ok:
        print("⚠️  Environment not configured")
        print("   1. Copy .env.example to .env")
        print("   2. Get API key from https://console.groq.com/")
        print("   3. Add your API key to .env file")
    
    if optional_count < 3:
        print("💡 Limited functionality due to missing packages")
        print("   Install more features: pip install -r requirements.txt")
        print("   Or minimal set: pip install -r requirements-minimal.txt")
    
    # Determine best way to run
    print("\n🚀 How to run the application:")
    
    if core_ok and import_results.get('app', False):
        if env_ok and optional_count >= 5:
            print("   ✅ Full version: python run.py")
        else:
            print("   ⚠️  Limited version: python app_minimal.py")
    elif core_ok and import_results.get('app_minimal', False):
        print("   ⚠️  Minimal version only: python app_minimal.py")
    else:
        print("   ❌ Cannot run - fix critical issues first")
    
    print("\n🔧 Quick fixes:")
    print("   • Auto setup: python setup.py")
    print("   • Smart start: python start.py")
    print("   • Test system: python test_groq.py")

def main():
    """Main system check function"""
    print("🔍 Smart ATS Resume Builder - System Check")
    print("This will verify your installation and configuration")
    
    # Run all checks
    python_ok = check_python()
    files_ok = check_files()
    core_ok, optional_count = check_dependencies()
    env_ok = check_environment()
    check_directories()
    import_results = test_imports()
    
    # Summary
    print_header("Summary")
    
    total_score = sum([
        python_ok,
        files_ok, 
        core_ok,
        env_ok,
        import_results.get('app', False) or import_results.get('app_minimal', False)
    ])
    
    if total_score >= 4:
        print("🎉 System Status: GOOD")
        print("   Your system is ready to run the application!")
    elif total_score >= 3:
        print("⚠️  System Status: PARTIAL")
        print("   Some features may not work, but basic functionality available")
    else:
        print("❌ System Status: NEEDS ATTENTION")
        print("   Several issues need to be resolved")
    
    # Provide recommendations
    provide_recommendations(core_ok, optional_count, env_ok, import_results)
    
    return total_score >= 3

if __name__ == "__main__":
    success = main()
    print(f"\n{'='*50}")
    print("🏁 System check complete!")
    sys.exit(0 if success else 1)