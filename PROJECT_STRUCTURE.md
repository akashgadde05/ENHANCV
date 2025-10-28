# Project Structure

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
