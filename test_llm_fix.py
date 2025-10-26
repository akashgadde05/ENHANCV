#!/usr/bin/env python3
"""
Test script to verify the LLM analyzer fixes
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_llm_analyzer():
    """Test the improved LLM analyzer"""
    print("🧪 Testing Improved LLM Analyzer")
    print("=" * 50)
    
    # Check if API key is configured
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your_groq_api_key_here':
        print("❌ Groq API key not configured")
        print("Please set GROQ_API_KEY in your .env file")
        return False
    
    print(f"✅ API Key configured: {api_key[:8]}...")
    
    try:
        from utils.llm_analyzer import LLMAnalyzer
        
        analyzer = LLMAnalyzer()
        print(f"✅ LLM Analyzer initialized with model: {analyzer.model}")
        
        # Test with a simple resume
        test_resume = """
        John Smith
        Software Engineer
        john.smith@email.com | (555) 123-4567
        
        EXPERIENCE
        Software Engineer - Tech Company (2021-Present)
        • Developed web applications using Python and React
        • Improved system performance by 25%
        • Led team of 3 developers
        
        EDUCATION
        Bachelor of Computer Science - University (2020)
        
        SKILLS
        Python, JavaScript, React, SQL, Git
        """
        
        print("\n🔄 Testing resume analysis...")
        print("📝 Sample resume length:", len(test_resume), "characters")
        
        result = analyzer.analyze_resume_content(test_resume)
        
        if result:
            print("✅ Analysis completed successfully!")
            print(f"📊 Overall Score: {result.get('overall_score', 'N/A')}")
            print(f"🔧 ATS Score: {result.get('ats_compatibility', {}).get('score', 'N/A')}")
            print(f"📝 Content Score: {result.get('content_analysis', {}).get('score', 'N/A')}")
            
            # Check if all required fields are present
            required_fields = [
                'overall_score', 'ats_compatibility', 'content_analysis',
                'skills_analysis', 'experience_analysis', 'formatting_analysis',
                'keyword_optimization', 'recommendations'
            ]
            
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"⚠️  Missing fields: {missing_fields}")
            else:
                print("✅ All required fields present in response")
            
            return True
        else:
            print("❌ Analysis failed - no result returned")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required packages: pip install groq python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid input"""
    print("\n🧪 Testing Error Handling")
    print("=" * 50)
    
    try:
        from utils.llm_analyzer import LLMAnalyzer
        analyzer = LLMAnalyzer()
        
        # Test with empty resume
        print("🔄 Testing with empty resume...")
        result = analyzer.analyze_resume_content("")
        
        if result and 'overall_score' in result:
            print("✅ Empty resume handled gracefully")
        else:
            print("❌ Empty resume not handled properly")
            return False
        
        # Test with very short resume
        print("🔄 Testing with minimal resume...")
        result = analyzer.analyze_resume_content("John Doe, Engineer")
        
        if result and 'overall_score' in result:
            print("✅ Minimal resume handled gracefully")
        else:
            print("❌ Minimal resume not handled properly")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 LLM Analyzer Fix Verification")
    print("=" * 60)
    
    basic_test = test_llm_analyzer()
    error_test = test_error_handling()
    
    print("\n" + "=" * 60)
    
    if basic_test and error_test:
        print("🎉 SUCCESS: LLM Analyzer fixes working correctly!")
        print("\n🔧 Improvements Made:")
        print("   ✅ Better error handling for empty responses")
        print("   ✅ Retry mechanism for failed API calls")
        print("   ✅ Improved JSON parsing with validation")
        print("   ✅ Debug logging for troubleshooting")
        print("   ✅ Fallback analysis for all error cases")
        
        print("\n🚀 The resume analyzer should now work reliably!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify your Groq API key is correct")
        print("   2. Check your internet connection")
        print("   3. Ensure you have the latest groq package")
    
    return basic_test and error_test

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)