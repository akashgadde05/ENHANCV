# Smart ATS Resume Builder & Analyzer 🚀

An AI-powered Flask application designed to help job seekers create and optimize their resumes for Applicant Tracking Systems (ATS) using Groq's Llama 3.3 70B Versatile model.

## 🌟 Key Features

### 📝 Resume Builder
- **Interactive Form**: Step-by-step resume creation with guided prompts
- **ATS-Optimized Templates**: Professional layouts that pass through ATS filters
- **Real-time Validation**: Instant feedback on content quality
- **PDF Generation**: High-quality, professional PDF output

### 🔍 Resume Analyzer
- **AI-Powered Analysis**: Advanced algorithms analyze resume content using Groq LLM
- **ATS Compatibility Check**: Identifies potential ATS issues
- **Skills Gap Analysis**: Compares your skills with industry standards
- **Quantitative Scoring**: Detailed scoring across multiple dimensions

### 📚 Course Recommendations
- **Personalized Learning**: Suggests courses based on missing skills
- **Multiple Platforms**: Recommendations from Coursera, Udemy, edX, and more
- **Skill Development**: Focus on in-demand technical skills

### 📦 Bulk Analysis
- **HR-Friendly**: Perfect for recruiters and HR teams
- **Batch Processing**: Analyze multiple resumes simultaneously
- **Comparative Analysis**: Rank and compare candidates

## 🏗️ Technical Architecture

### Backend
- **Framework**: Flask web framework
- **Text Processing**: PyPDF2 and python-docx for document parsing
- **PDF Generation**: ReportLab for professional PDF creation
- **AI Integration**: Groq API with Llama 3.3 70B Versatile model
- **Natural Language Processing**: TextBlob for text analysis

### Frontend
- **UI Framework**: Bootstrap 5 for responsive design
- **JavaScript**: Vanilla JS for interactive features
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome for consistent iconography

## 📊 Analysis Metrics

The system evaluates resumes across multiple dimensions:

- **Content Length**: Optimal word count analysis
- **Skills Assessment**: Technical and soft skills evaluation
- **Experience Analysis**: Professional experience indicators
- **Quantification**: Presence of metrics and achievements
- **ATS Compatibility**: Format and structure optimization
- **Section Completeness**: Essential resume sections check
- **Readability**: Text clarity and structure analysis

## 🎖️ Scoring System

- **85-100**: Excellent - ATS optimized
- **70-84**: Good - Minor improvements needed
- **55-69**: Average - Several areas need attention
- **Below 55**: Needs improvement - Major optimization required

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Groq API key (get from [console.groq.com](https://console.groq.com/))

### 🚀 Quick Start (Choose Your Method)

#### Option 1: One-Click Start (Easiest)
```bash
# Clone and start automatically
git clone https://github.com/akashgadde05/ENHANCV.git
cd ENHANCV
python start.py
```

#### Option 2: Automated Setup
```bash
# Full system check and setup
python check_system.py  # Check what's needed
python setup.py         # Install everything
python start.py         # Start the app
```

#### Option 3: Manual Installation
```bash
# 1. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies (try minimal first)
pip install -r requirements-minimal.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run the application
python run.py
```

#### Option 4: Troubleshooting Installation
```bash
# If you have dependency issues
python install.py        # Smart installer with fallbacks
python app_minimal.py    # Run with whatever works
```

### Environment Configuration

Create a `.env` file with your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DEBUG=True
```

### Get Your Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Go to API Keys section
4. Create a new API key
5. Copy it to your `.env` file

### 🔧 Troubleshooting & System Check

#### Quick Diagnostics:
```bash
python check_system.py   # Complete system analysis
python test_groq.py      # Test Groq API integration
python start.py          # Smart start (auto-detects issues)
```

#### Common Issues & Solutions:

| Issue | Solution |
|-------|----------|
| **Dependency conflicts** | `python install.py` or `pip install -r requirements-minimal.txt` |
| **Missing packages** | `pip install flask groq python-dotenv` (core only) |
| **API errors** | Check Groq API key in `.env` file |
| **Import errors** | `python app_minimal.py` (runs with available packages) |
| **File upload issues** | Run `python check_system.py` to create directories |

#### Feature Availability:
- ✅ **Always Available**: Home page, basic UI
- 🔑 **Needs Groq API**: Resume analysis, AI recommendations  
- 📦 **Needs Packages**: File upload (pypdf, python-docx), PDF generation (reportlab)

#### Run Modes:
```bash
python run.py           # Full version (all features)
python app_minimal.py   # Minimal version (graceful degradation)
python start.py         # Auto-detect best version
```

The application will be available at `http://localhost:5000`

## 📱 Usage Guide

### Resume Builder
1. Navigate to the **Builder** section
2. Fill out the interactive form with your information
3. Use the live preview to see your resume in real-time
4. Generate a professional PDF when ready

### Resume Analyzer
1. Go to the **Analyzer** section
2. Upload your resume (PDF, DOCX, DOC, or TXT)
3. Optionally provide a job description for targeted analysis
4. Review the comprehensive AI-powered analysis
5. Export results for future reference

### Bulk Analysis
1. Access the **Bulk Analysis** section
2. Upload multiple resume files
3. Configure analysis settings
4. Review comparative results and rankings
5. Export batch analysis results

## 💡 Tips for Best Results

- **Use Keywords**: Include relevant industry keywords
- **Quantify Achievements**: Add specific numbers and metrics
- **Standard Formatting**: Avoid complex layouts and graphics
- **Complete Sections**: Include all essential resume sections
- **Proofread**: Ensure error-free content

## 🔒 Privacy & Security

- **No Data Storage**: Files are processed in memory only
- **Local Processing**: Analysis happens on your device
- **Secure**: No resume data is saved or transmitted
- **API Security**: Groq API calls are made securely with proper authentication

## 🛠️ Development

### Project Structure
```
ENHANCV/
├── app.py                 # Main Flask application
├── run.py                 # Application runner
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .env.example          # Environment template
├── README.md             # This file
├── utils/                # Utility modules
│   ├── llm_analyzer.py   # Groq LLM integration
│   ├── resume_analyzer.py # Resume text analysis
│   ├── resume_builder.py  # Resume building logic
│   └── pdf_generator.py   # PDF generation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── builder.html      # Resume builder
│   ├── analyzer.html     # Resume analyzer
│   └── bulk_analyzer.html # Bulk analysis
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # JavaScript functionality
```

### Adding New Features
1. Create utility functions in the `utils/` directory
2. Add new routes in `app.py`
3. Create corresponding templates in `templates/`
4. Update JavaScript in `static/js/main.js`
5. Add styles in `static/css/style.css`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq**: For providing the powerful Llama 3.3 70B Versatile model
- **Bootstrap**: For the responsive UI framework
- **ReportLab**: For PDF generation capabilities
- **Flask**: For the lightweight web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include your environment details and error messages

---

**Made with ❤️ By AKASH GADDE for job seekers worldwide**