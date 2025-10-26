from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
from utils.llm_analyzer import LLMAnalyzer
from utils.resume_analyzer import ResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.pdf_generator import PDFGenerator
import tempfile
import zipfile
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize analyzers
llm_analyzer = LLMAnalyzer()
resume_analyzer = ResumeAnalyzer()
resume_builder = ResumeBuilder()
pdf_generator = PDFGenerator()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/builder')
def builder():
    return render_template('builder.html')

@app.route('/analyzer')
def analyzer():
    return render_template('analyzer.html')

@app.route('/bulk-analyzer')
def bulk_analyzer():
    return render_template('bulk_analyzer.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
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
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from resume
        resume_text = resume_analyzer.extract_text_from_file(filepath)
        
        # Analyze with LLM 
        analysis = llm_analyzer.analyze_resume_content(resume_text, job_description)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'resume_text': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk-analyze', methods=['POST'])
def bulk_analyze():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                # Save file temporarily
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{i}_{filename}")
                file.save(filepath)
                
                # Extract and analyze
                resume_text = resume_analyzer.extract_text_from_file(filepath)
                analysis = llm_analyzer.analyze_resume_content(resume_text)
                
                results.append({
                    'filename': filename,
                    'analysis': analysis,
                    'resume_preview': resume_text[:200] + '...' if len(resume_text) > 200 else resume_text
                })
                
                # Clean up
                os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_analyzed': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/build-resume', methods=['POST'])
def build_resume():
    try:
        resume_data = request.json
        
        if not resume_data:
            return jsonify({'error': 'No resume data provided'}), 400
        
        # Generate PDF
        pdf_path = pdf_generator.generate_resume_pdf(resume_data)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-suggestions', methods=['POST'])
def get_suggestions():
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        target_role = data.get('target_role', '')
        
        if not resume_text:
            return jsonify({'error': 'No resume text provided'}), 400
        
        suggestions = llm_analyzer.generate_resume_suggestions(resume_text, target_role)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-analysis', methods=['POST'])
def export_analysis():
    try:
        analysis_data = request.json
        
        if not analysis_data:
            return jsonify({'error': 'No analysis data provided'}), 400
        
        # Create temporary file for export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(analysis_data, f, indent=2)
            temp_path = f.name
        
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)