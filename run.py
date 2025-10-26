#!/usr/bin/env python3
"""
Smart ATS Resume Builder & Analyzer
Main application runner
"""

import os
from app import app

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment variable
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting Smart ATS Resume Builder & Analyzer")
    print(f"📍 Running on http://localhost:{port}")
    print("💡 Powered by Groq's Llama 3.3 70B Versatile model")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )