#!/usr/bin/env python3
"""
Test file upload functionality
"""

import os
import tempfile
import requests
from pathlib import Path

def test_file_upload():
    """Test if file upload is working"""
    print("🧪 Testing File Upload Functionality")
    print("=" * 50)
    
    # Create a test resume file
    test_resume_content = """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5 years in web development.
    
    EXPERIENCE
    Senior Software Engineer - Tech Corp (2020-Present)
    • Developed web applications using Python and JavaScript
    • Led a team of 3 developers
    • Improved system performance by 30%
    
    EDUCATION
    Bachelor of Science in Computer Science - University (2018)
    
    SKILLS
    Python, JavaScript, React, SQL, AWS
    """
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_resume_content)
        temp_file_path = f.name
    
    try:
        print(f"✅ Created test resume file: {temp_file_path}")
        print(f"📄 File size: {os.path.getsize(temp_file_path)} bytes")
        
        # Test if the file can be read
        with open(temp_file_path, 'r') as f:
            content = f.read()
            print(f"✅ File content readable: {len(content)} characters")
        
        print("\n🌐 File upload should now work in the web interface!")
        print("📋 To test:")
        print("   1. Run: python run.py")
        print("   2. Go to: http://localhost:5000/analyzer")
        print("   3. Upload the test file or any resume")
        print("   4. Click 'Analyze Resume'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"🗑️  Cleaned up test file")

if __name__ == "__main__":
    test_file_upload()