"""
Minimal version of Smart ATS Resume Builder
Works with basic dependencies only
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import tempfile
from datetime import datetime

# Try to import optional dependencies
try:
    from utils.llm_analyzer import LLMAnalyzer
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("⚠️  LLM analyzer not available - install groq package")

try:
    from utils.resume_analyzer import ResumeAnalyzer
    HAS_ANALYZER = True
except ImportError:
    HAS_ANALYZER = False
    print("⚠️  Resume analyzer not available - install pypdf and python-docx")

try:
    from utils.pdf_generator import PDFGenerator
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("⚠️  PDF generator not available - install reportlab")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components if available
llm_analyzer = LLMAnalyzer() if HAS_LLM else None
resume_analyzer = ResumeAnalyzer() if HAS_ANALYZER else None
pdf_generator = PDFGenerator() if HAS_PDF else None

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', 
                         has_llm=HAS_LLM, 
                         has_analyzer=HAS_ANALYZER, 
                         has_pdf=HAS_PDF)

@app.route('/builder')
def builder():
    if not HAS_PDF:
        return render_template('error.html', 
                             message="PDF generation not available. Please install reportlab package.")
    return render_template('builder.html')

@app.route('/analyzer')
def analyzer():
    if not HAS_LLM or not HAS_ANALYZER:
        return render_template('error.html', 
                             message="Resume analyzer not available. Please install required packages.")
    return render_template('analyzer.html')

@app.route('/bulk-analyzer')
def bulk_analyzer():
    if not HAS_LLM or not HAS_ANALYZER:
        return render_template('error.html', 
                             message="Bulk analyzer not available. Please install required packages.")
    return render_template('bulk_analyzer.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    if not HAS_LLM or not HAS_ANALYZER:
        return jsonify({'error': 'Analysis features not available'}), 503
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file temporarily
        filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text from resume
            resume_text = resume_analyzer.extract_text_from_file(filepath)
            
            # Analyze with LLM
            analysis = llm_analyzer.analyze_resume_content(resume_text, job_description)
            
            return jsonify({
                'success': True,
                'analysis': analysis,
                'resume_text': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
            })
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/build-resume', methods=['POST'])
def build_resume():
    if not HAS_PDF:
        return jsonify({'error': 'PDF generation not available'}), 503
    
    try:
        resume_data = request.json
        
        if not resume_data:
            return jsonify({'error': 'No resume data provided'}), 400
        
        # Generate PDF
        pdf_buffer = pdf_generator.create_resume(resume_data)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(pdf_buffer.getvalue())
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """API endpoint to check which features are available"""
    return jsonify({
        'llm_available': HAS_LLM,
        'analyzer_available': HAS_ANALYZER,
        'pdf_available': HAS_PDF,
        'features': {
            'resume_analysis': HAS_LLM and HAS_ANALYZER,
            'resume_building': HAS_PDF,
            'bulk_analysis': HAS_LLM and HAS_ANALYZER
        }
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="Internal server error"), 500

if __name__ == '__main__':
    print("🚀 Starting Smart ATS Resume Builder (Minimal Version)")
    print(f"📍 Running on http://localhost:5000")
    
    if HAS_LLM:
        print("✅ LLM Analysis: Available")
    else:
        print("❌ LLM Analysis: Not available (install groq)")
    
    if HAS_ANALYZER:
        print("✅ File Processing: Available") 
    else:
        print("❌ File Processing: Not available (install pypdf, python-docx)")
    
    if HAS_PDF:
        print("✅ PDF Generation: Available")
    else:
        print("❌ PDF Generation: Not available (install reportlab)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)