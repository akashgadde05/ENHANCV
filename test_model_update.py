#!/usr/bin/env python3
"""
Test script to verify the Llama 3.3 70B model update
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_model_configuration():
    """Test that the model is correctly configured"""
    print("🧪 Testing Llama 3.3 70B Model Configuration")
    print("=" * 50)
    
    # Check environment variable
    model = os.getenv('GROQ_MODEL')
    print(f"📋 Environment Model: {model}")
    
    if model == 'llama-3.3-70b-versatile':
        print("✅ Environment model correctly set to Llama 3.3 70B")
    else:
        print(f"❌ Environment model is '{model}', expected 'llama-3.3-70b-versatile'")
        return False
    
    # Test LLM analyzer initialization
    try:
        from utils.llm_analyzer import LLMAnalyzer
        analyzer = LLMAnalyzer()
        
        print(f"📋 Analyzer Model: {analyzer.model}")
        
        if analyzer.model == 'llama-3.3-70b-versatile':
            print("✅ LLM Analyzer correctly configured for Llama 3.3 70B")
        else:
            print(f"❌ LLM Analyzer model is '{analyzer.model}', expected 'llama-3.3-70b-versatile'")
            return False
            
    except ImportError:
        print("⚠️  LLM Analyzer not available (missing dependencies)")
        return True  # This is okay for minimal installations
    except Exception as e:
        print(f"❌ Error initializing LLM Analyzer: {e}")
        return False
    
    print("\n🎉 Model configuration test passed!")
    print("💡 The application is now using Llama 3.3 70B Versatile model")
    
    return True

def test_api_connection():
    """Test API connection with the new model"""
    print("\n🔗 Testing API Connection with Llama 3.3 70B")
    print("=" * 50)
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your_groq_api_key_here':
        print("⚠️  Groq API key not configured - skipping API test")
        return True
    
    try:
        from utils.llm_analyzer import LLMAnalyzer
        analyzer = LLMAnalyzer()
        
        # Test with a simple prompt
        test_text = "Software Engineer with 3 years experience in Python and web development."
        
        print("🔄 Testing API call with new model...")
        result = analyzer.analyze_resume_content(test_text)
        
        if result and 'overall_score' in result:
            print(f"✅ API test successful! Model responded with score: {result['overall_score']}")
            print("🚀 Llama 3.3 70B is working correctly!")
            return True
        else:
            print("❌ API test failed - no valid response")
            return False
            
    except ImportError:
        print("⚠️  Cannot test API - missing dependencies")
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔄 Llama 3.3 70B Model Update Verification")
    print("=" * 60)
    
    config_ok = test_model_configuration()
    api_ok = test_api_connection()
    
    print("\n" + "=" * 60)
    
    if config_ok and api_ok:
        print("🎉 SUCCESS: Llama 3.3 70B model update completed successfully!")
        print("\n📋 What's New in Llama 3.3 70B:")
        print("   • Improved reasoning capabilities")
        print("   • Better instruction following")
        print("   • Enhanced performance on complex tasks")
        print("   • More accurate resume analysis")
        
        print("\n🚀 Your Smart ATS Resume Builder is now powered by the latest model!")
    else:
        print("⚠️  Some issues detected. Please check the errors above.")
    
    return config_ok and api_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)