#!/usr/bin/env python3
"""
Prepare Smart ATS Resume Builder for GitHub upload
"""

import os
import shutil
from pathlib import Path

def clean_sensitive_data():
    """Remove sensitive data before GitHub upload"""
    print("🔒 Cleaning sensitive data...")
    
    # Read .env file and create a clean version
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Check if it contains real API key
        if 'gsk_' in content:
            print("⚠️  Found real API key in .env file")
            
            # Create backup
            shutil.copy('.env', '.env.backup')
            print("📋 Created .env.backup with your real API key")
            
            # Replace with placeholder
            clean_content = content.replace(
                content.split('GROQ_API_KEY=')[1].split('\n')[0],
                'your_groq_api_key_here'
            )
            
            with open('.env', 'w') as f:
                f.write(clean_content)
            
            print("✅ Cleaned .env file for GitHub")
        else:
            print("✅ .env file already clean")
    
    # Remove any temporary files
    temp_files = [
        '*.pyc', '__pycache__', '*.log', 'temp_*', 
        'uploads/*', '*.pdf', '*.docx'
    ]
    
    for pattern in temp_files:
        for file in Path('.').glob(pattern):
            if file.is_file():
                file.unlink()
                print(f"🗑️  Removed {file}")
            elif file.is_dir():
                shutil.rmtree(file)
                print(f"🗑️  Removed directory {file}")

def create_github_files():
    """Create GitHub-specific files"""
    print("\n📝 Creating GitHub files...")
    
    # Create CONTRIBUTING.md
    contributing_content = """# Contributing to Smart ATS Resume Builder

Thank you for your interest in contributing! Here's how you can help:

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ENHANCV.git`
3. Create a virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file with your Groq API key

## Development Setup

```bash
# Install development dependencies
pip install -r requirements-minimal.txt

# Run tests
python test_complete_system.py

# Start development server
python run.py
```

## Making Changes

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes: `python test_complete_system.py`
4. Commit your changes: `git commit -m "Add your feature"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Update tests when adding new features

## Reporting Issues

Please use the GitHub issue tracker to report bugs or request features.
Include:
- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior

## Questions?

Feel free to open an issue for questions or join our discussions!
"""
    
    with open('CONTRIBUTING.md', 'w', encoding='utf-8') as f:
        f.write(contributing_content)
    print("✅ Created CONTRIBUTING.md")
    
    # Create LICENSE
    license_content = """MIT License

Copyright (c) 2024 Akash Gadde

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content)
    print("✅ Created LICENSE")
    
    # Create GitHub workflow for CI
    github_dir = Path('.github/workflows')
    github_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: CI Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-minimal.txt
    
    - name: Run basic tests
      run: |
        python -c "import app; print('App imports successfully')"
        python -c "import utils.resume_analyzer; print('Resume analyzer imports successfully')"
        python -c "import utils.pdf_generator; print('PDF generator imports successfully')"
    
    - name: Test Flask app
      run: |
        python -c "
        import app
        with app.app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            print('Flask app test passed')
        "
"""
    
    with open(github_dir / 'ci.yml', 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    print("✅ Created GitHub Actions workflow")

def create_project_structure_doc():
    """Create a detailed project structure document"""
    print("\n📁 Creating project structure documentation...")
    
    structure_content = """# Project Structure

```
ENHANCV/
├── 📄 README.md                    # Main documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 .gitignore                   # Git ignore rules
├── 📄 requirements.txt             # Full dependencies
├── 📄 requirements-minimal.txt     # Core dependencies only
├── 📄 .env.example                 # Environment template
├── 📄 .env                         # Your environment (not in git)
│
├── 🚀 Main Application Files
│   ├── 📄 app.py                   # Main Flask application
│   ├── 📄 app_minimal.py           # Minimal version with graceful degradation
│   ├── 📄 run.py                   # Application runner
│   └── 📄 start.py                 # Smart launcher
│
├── 🛠️ Setup & Installation
│   ├── 📄 setup.py                 # Automated setup script
│   ├── 📄 install.py               # Smart installer with fallbacks
│   └── 📄 prepare_for_github.py    # GitHub preparation script
│
├── 🧪 Testing & Verification
│   ├── 📄 test_groq.py             # Test Groq API integration
│   ├── 📄 test_llm_fix.py          # Test LLM analyzer fixes
│   ├── 📄 test_model_update.py     # Test model update
│   ├── 📄 test_complete_system.py  # Complete system test
│   └── 📄 check_system.py          # System health check
│
├── 🔧 Utilities
│   └── utils/
│       ├── 📄 llm_analyzer.py      # Groq LLM integration
│       ├── 📄 resume_analyzer.py   # Resume text processing
│       ├── 📄 resume_builder.py    # Resume building logic
│       └── 📄 pdf_generator.py     # PDF generation
│
├── 🎨 Frontend
│   ├── templates/
│   │   ├── 📄 base.html            # Base template
│   │   ├── 📄 index.html           # Home page
│   │   ├── 📄 builder.html         # Resume builder
│   │   ├── 📄 analyzer.html        # Resume analyzer
│   │   ├── 📄 bulk_analyzer.html   # Bulk analysis
│   │   └── 📄 error.html           # Error pages
│   │
│   └── static/
│       ├── css/
│       │   └── 📄 style.css        # Custom styles
│       └── js/
│           └── 📄 main.js          # JavaScript functionality
│
├── 📁 uploads/                     # Temporary file uploads (not in git)
│
└── 🔄 GitHub Integration
    └── .github/
        └── workflows/
            └── 📄 ci.yml           # GitHub Actions CI
```

## Key Components

### Core Application
- **app.py**: Main Flask application with all routes and API endpoints
- **app_minimal.py**: Fallback version that works with missing dependencies
- **run.py**: Production-ready application runner

### AI & Analysis
- **utils/llm_analyzer.py**: Groq API integration with Llama 3.3 70B Versatile
- **utils/resume_analyzer.py**: Text extraction and basic analysis
- **utils/pdf_generator.py**: Professional PDF generation

### User Interface
- **templates/**: Jinja2 templates for all pages
- **static/**: CSS, JavaScript, and other static assets
- Responsive Bootstrap 5 design

### Testing & Setup
- Multiple test scripts for different components
- Smart installation scripts with fallback options
- System health checks and diagnostics

### GitHub Integration
- CI/CD pipeline with GitHub Actions
- Comprehensive documentation
- Contribution guidelines
"""
    
    with open('PROJECT_STRUCTURE.md', 'w', encoding='utf-8') as f:
        f.write(structure_content)
    print("✅ Created PROJECT_STRUCTURE.md")

def create_deployment_guide():
    """Create deployment guide"""
    print("\n🚀 Creating deployment guide...")
    
    deployment_content = """# Deployment Guide

## Local Development

### Quick Start
```bash
git clone https://github.com/akashgadde05/ENHANCV.git
cd ENHANCV
python start.py
```

### Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run the application
python run.py
```

## Production Deployment

### Using Gunicorn (Recommended)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables
```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
DEBUG=False
SECRET_KEY=your_production_secret_key
```

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku create your-app-name

# Set environment variables
heroku config:set GROQ_API_KEY=your_api_key
heroku config:set GROQ_MODEL=llama-3.3-70b-versatile
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

### Vercel Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## Configuration

### Required Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_MODEL`: Model to use (default: llama-3.3-70b-versatile)

### Optional Environment Variables
- `DEBUG`: Enable debug mode (default: True)
- `SECRET_KEY`: Flask secret key (auto-generated if not set)
- `PORT`: Port to run on (default: 5000)

## Monitoring & Maintenance

### Health Checks
```bash
# System health check
python check_system.py

# Complete system test
python test_complete_system.py

# API test
python test_groq.py
```

### Logs
- Application logs are printed to stdout
- Use log aggregation services in production
- Monitor API usage and rate limits

### Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Test after updates
python test_complete_system.py
```
"""
    
    with open('DEPLOYMENT.md', 'w', encoding='utf-8') as f:
        f.write(deployment_content)
    print("✅ Created DEPLOYMENT.md")

def create_git_commands():
    """Create a script with git commands for upload"""
    print("\n📋 Creating git commands...")
    
    git_commands = """#!/bin/bash
# Git commands to upload to GitHub

echo "🚀 Uploading Smart ATS Resume Builder to GitHub"
echo "Repository: https://github.com/akashgadde05/ENHANCV"
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add remote if not exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Adding remote origin..."
    git remote add origin https://github.com/akashgadde05/ENHANCV.git
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Initial commit: Smart ATS Resume Builder with Llama 3.3 70B

Features:
- AI-powered resume analysis using Groq's Llama 3.3 70B Versatile
- Interactive resume builder with real-time preview
- ATS compatibility scoring and recommendations
- Bulk resume analysis for HR teams
- Professional PDF generation
- Course recommendations based on skill gaps
- Responsive web interface with Bootstrap 5
- Comprehensive error handling and fallback systems
- Multiple installation options for different environments

Tech Stack:
- Backend: Flask, Python 3.8+
- AI: Groq API with Llama 3.3 70B Versatile
- Frontend: Bootstrap 5, JavaScript, Jinja2
- PDF: ReportLab
- Text Processing: pypdf, python-docx
- Testing: Comprehensive test suite"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Upload complete!"
echo "🌐 Your repository is now available at:"
echo "   https://github.com/akashgadde05/ENHANCV"
echo ""
echo "📋 Next steps:"
echo "   1. Go to your GitHub repository"
echo "   2. Add a description and topics"
echo "   3. Enable GitHub Pages if desired"
echo "   4. Set up branch protection rules"
echo "   5. Add collaborators if needed"
"""
    
    with open('upload_to_github.sh', 'w', encoding='utf-8') as f:
        f.write(git_commands)
    
    # Make it executable
    os.chmod('upload_to_github.sh', 0o755)
    print("✅ Created upload_to_github.sh")
    
    # Also create Windows batch file
    windows_commands = """@echo off
REM Git commands to upload to GitHub (Windows)

echo 🚀 Uploading Smart ATS Resume Builder to GitHub
echo Repository: https://github.com/akashgadde05/ENHANCV
echo.

REM Initialize git if not already done
if not exist ".git" (
    echo 📁 Initializing git repository...
    git init
)

REM Add remote if not exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo 🔗 Adding remote origin...
    git remote add origin https://github.com/akashgadde05/ENHANCV.git
)

REM Add all files
echo 📝 Adding files to git...
git add .

REM Commit
echo 💾 Committing changes...
git commit -m "Initial commit: Smart ATS Resume Builder with Llama 3.3 70B"

REM Push to GitHub
echo 🚀 Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Upload complete!
echo 🌐 Your repository is now available at:
echo    https://github.com/akashgadde05/ENHANCV
pause
"""
    
    with open('upload_to_github.bat', 'w', encoding='utf-8') as f:
        f.write(windows_commands)
    print("✅ Created upload_to_github.bat")

def main():
    """Main preparation function"""
    print("🔧 Preparing Smart ATS Resume Builder for GitHub")
    print("=" * 60)
    
    clean_sensitive_data()
    create_github_files()
    create_project_structure_doc()
    create_deployment_guide()
    create_git_commands()
    
    print("\n" + "=" * 60)
    print("🎉 GitHub preparation complete!")
    print("\n📋 Files created:")
    print("   ✅ CONTRIBUTING.md - Contribution guidelines")
    print("   ✅ LICENSE - MIT License")
    print("   ✅ PROJECT_STRUCTURE.md - Project documentation")
    print("   ✅ DEPLOYMENT.md - Deployment guide")
    print("   ✅ .github/workflows/ci.yml - GitHub Actions")
    print("   ✅ upload_to_github.sh/.bat - Upload scripts")
    
    print("\n🚀 Ready to upload to GitHub!")
    print("   Repository: https://github.com/akashgadde05/ENHANCV")
    
    print("\n📋 Upload options:")
    print("   1. Run: ./upload_to_github.sh (Linux/Mac)")
    print("   2. Run: upload_to_github.bat (Windows)")
    print("   3. Manual git commands:")
    print("      git init")
    print("      git remote add origin https://github.com/akashgadde05/ENHANCV.git")
    print("      git add .")
    print("      git commit -m 'Initial commit'")
    print("      git branch -M main")
    print("      git push -u origin main")
    
    print("\n⚠️  Important:")
    print("   • Your real API key is backed up in .env.backup")
    print("   • .env file now contains placeholder for GitHub")
    print("   • Remember to set up your API key after cloning")

if __name__ == "__main__":
    main()