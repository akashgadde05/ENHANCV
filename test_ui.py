#!/usr/bin/env python3
"""
Simple test to check if the new UI works
"""

import os
import webbrowser
import threading
import time
from app import app

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

def main():
    """Test the new UI"""
    print("🎨 Testing New Modern UI")
    print("=" * 40)
    
    print("🚀 Starting Flask app with new design...")
    print("📱 Features:")
    print("   ✅ Tailwind CSS integration")
    print("   ✅ Modern gradient navigation")
    print("   ✅ Improved hero section")
    print("   ✅ Better feature cards")
    print("   ✅ Enhanced forms and buttons")
    print("   ✅ Responsive design")
    
    print("\n🌐 Opening browser...")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the app
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 UI test completed!")

if __name__ == "__main__":
    main()