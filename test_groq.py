#!/usr/bin/env python3
"""
Test script to verify Groq API integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_connection():
    """Test Groq API connection"""
    print("🧪 Testing Groq API Connection")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your_groq_api_key_here':
        print("❌ Groq API key not found or not configured")
        print("Please set GROQ_API_KEY in your .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    try:
        # Import and test LLM analyzer
        from utils.llm_analyzer import LLMAnalyzer
        
        analyzer = LLMAnalyzer()
        print("✅ LLMAnalyzer initialized successfully")
        
        # Test with a simple resume text
        test_resume = """
        John Doe
        Software Engineer
        john.doe@email.com | (555) 123-4567
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 5 years of experience in web development.
        
        EXPERIENCE
        Senior Software Engineer - Tech Corp (2020-Present)
        • Developed web applications using Python and JavaScript
        • Led a team of 3 developers
        • Improved system performance by 30%
        
        EDUCATION
        Bachelor of Science in Computer Science - University XYZ (2018)
        
        SKILLS
        Python, JavaScript, React, SQL, AWS
        """
        
        print("🔄 Testing resume analysis...")
        result = analyzer.analyze_resume_content(test_resume)
        
        if result and 'overall_score' in result:
            print(f"✅ Analysis successful! Overall score: {result['overall_score']}/100")
            print(f"📊 ATS Compatibility: {result.get('ats_compatibility', {}).get('score', 'N/A')}/100")
            return True
        else:
            print("❌ Analysis failed - no valid result returned")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n🔍 Testing Dependencies")
    print("=" * 40)
    
    required_packages = [
        'flask',
        'groq',
        'dotenv',
        'pypdf',
        'docx',
        'reportlab',
        'textblob',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main test function"""
    print("🧪 Smart ATS Resume Builder - System Test")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n❌ Dependency test failed")
        return False
    
    # Test Groq connection
    groq_ok = test_groq_connection()
    
    print("\n" + "=" * 50)
    if groq_ok:
        print("🎉 All tests passed! Your system is ready.")
        print("\n🚀 You can now run the application:")
        print("   python run.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common solutions:")
        print("   1. Make sure your Groq API key is correct")
        print("   2. Check your internet connection")
        print("   3. Verify all dependencies are installed")
    
    return groq_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)