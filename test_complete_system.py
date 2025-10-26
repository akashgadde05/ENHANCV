#!/usr/bin/env python3
"""
Complete system test for Smart ATS Resume Builder
Tests all components including the fixed LLM analyzer
"""

import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_llm_analyzer():
    """Test the LLM analyzer with Llama 3.3 70B"""
    print("🤖 Testing LLM Analyzer (Llama 3.3 70B)")
    print("-" * 40)
    
    try:
        from utils.llm_analyzer import LLMAnalyzer
        
        analyzer = LLMAnalyzer()
        print(f"✅ Model: {analyzer.model}")
        
        # Test analysis
        test_resume = """
        Sarah Johnson
        Senior Software Engineer
        sarah.johnson@email.com | (555) 987-6543
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 5+ years developing scalable web applications.
        
        EXPERIENCE
        Senior Software Engineer - TechCorp (2020-Present)
        • Led development of microservices architecture serving 1M+ users
        • Improved system performance by 40% through optimization
        • Mentored team of 4 junior developers
        
        Software Engineer - StartupXYZ (2019-2020)
        • Built REST APIs using Python and Django
        • Implemented CI/CD pipelines reducing deployment time by 60%
        
        EDUCATION
        Bachelor of Science in Computer Science - State University (2019)
        GPA: 3.8/4.0
        
        SKILLS
        Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL
        """
        
        result = analyzer.analyze_resume_content(test_resume)
        
        if result and result.get('overall_score', 0) > 0:
            print(f"✅ Analysis successful - Score: {result['overall_score']}/100")
            return True
        else:
            print("❌ Analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ LLM Analyzer error: {e}")
        return False

def test_resume_analyzer():
    """Test the resume text extraction"""
    print("\n📄 Testing Resume Text Analyzer")
    print("-" * 40)
    
    try:
        from utils.resume_analyzer import ResumeAnalyzer
        
        analyzer = ResumeAnalyzer()
        
        # Test basic analysis
        test_text = "John Doe, Software Engineer with Python and JavaScript experience."
        analysis = analyzer.basic_analysis(test_text)
        
        if analysis and 'word_count' in analysis:
            print(f"✅ Text analysis successful - {analysis['word_count']} words")
            return True
        else:
            print("❌ Text analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Resume Analyzer error: {e}")
        return False

def test_pdf_generator():
    """Test PDF generation"""
    print("\n📑 Testing PDF Generator")
    print("-" * 40)
    
    try:
        from utils.pdf_generator import PDFGenerator
        
        generator = PDFGenerator()
        
        # Test data
        test_data = {
            'personal_info': {
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '(555) 123-4567'
            },
            'summary': 'Test professional summary',
            'experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Test Company',
                    'duration': '2020-Present',
                    'responsibilities': ['Developed applications', 'Led team projects']
                }
            ],
            'education': [
                {
                    'degree': 'Bachelor of Science',
                    'institution': 'Test University',
                    'year': '2020'
                }
            ],
            'skills': {
                'technical': ['Python', 'JavaScript'],
                'soft': ['Communication', 'Leadership']
            }
        }
        
        # Generate PDF
        pdf_path = generator.generate_resume_pdf(test_data)
        
        if pdf_path and Path(pdf_path).exists():
            print("✅ PDF generation successful")
            # Clean up
            os.remove(pdf_path)
            return True
        else:
            print("❌ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"❌ PDF Generator error: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization"""
    print("\n🌐 Testing Flask Application")
    print("-" * 40)
    
    try:
        import app
        
        # Test app creation
        if hasattr(app, 'app') and app.app:
            print("✅ Flask app initialized successfully")
            
            # Test routes exist
            routes = [rule.rule for rule in app.app.url_map.iter_rules()]
            expected_routes = ['/', '/builder', '/analyzer', '/api/analyze']
            
            missing_routes = [route for route in expected_routes if route not in routes]
            
            if not missing_routes:
                print("✅ All expected routes available")
                return True
            else:
                print(f"❌ Missing routes: {missing_routes}")
                return False
        else:
            print("❌ Flask app not properly initialized")
            return False
            
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n⚙️  Testing Environment Configuration")
    print("-" * 40)
    
    # Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if api_key and api_key != 'your_groq_api_key_here':
        print("✅ Groq API key configured")
    else:
        print("❌ Groq API key not configured")
        return False
    
    # Check model
    model = os.getenv('GROQ_MODEL')
    if model == 'llama-3.3-70b-versatile':
        print("✅ Model set to Llama 3.3 70B Versatile")
    else:
        print(f"⚠️  Model is '{model}', expected 'llama-3.3-70b-versatile'")
    
    return True

def main():
    """Run complete system test"""
    print("🧪 Smart ATS Resume Builder - Complete System Test")
    print("=" * 60)
    
    tests = [
        ("Environment", test_environment),
        ("LLM Analyzer", test_llm_analyzer),
        ("Resume Analyzer", test_resume_analyzer),
        ("PDF Generator", test_pdf_generator),
        ("Flask App", test_flask_app)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Your Smart ATS Resume Builder is fully functional!")
        print("\n📋 What's working:")
        print("   ✅ Llama 3.3 70B AI analysis")
        print("   ✅ Resume text processing")
        print("   ✅ PDF generation")
        print("   ✅ Web application")
        print("   ✅ Environment configuration")
        
        print("\n🏃 Ready to run:")
        print("   python run.py")
        
    elif passed >= 3:
        print("\n⚠️  PARTIAL SUCCESS")
        print("Most features are working. Check failed tests above.")
        
        print("\n🏃 You can still run:")
        print("   python app_minimal.py  # Runs with available features")
        
    else:
        print("\n❌ MULTIPLE FAILURES")
        print("Several components need attention. Check the errors above.")
        
        print("\n🔧 Try:")
        print("   python install.py      # Fix dependencies")
        print("   python check_system.py # Detailed diagnosis")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)