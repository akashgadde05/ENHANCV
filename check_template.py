#!/usr/bin/env python3
"""
Check what's in the analyzer.html template
"""

with open('templates/analyzer.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
print("=" * 80)
print("CHECKING ANALYZER.HTML TEMPLATE")
print("=" * 80)

# Check for the upload area ID
if 'id="singleFileUpload"' in content:
    print("✓ Found: id='singleFileUpload'")
else:
    print("✗ MISSING: id='singleFileUpload'")

# Check for the file input ID
if 'id="singleFileInput"' in content:
    print("✓ Found: id='singleFileInput'")
else:
    print("✗ MISSING: id='singleFileInput'")

# Check for the onclick handler
if 'uploadArea.onclick' in content:
    print("✓ Found: uploadArea.onclick handler")
else:
    print("✗ MISSING: uploadArea.onclick handler")

# Check for the ondrop handler
if 'uploadArea.ondrop' in content:
    print("✓ Found: uploadArea.ondrop handler")
else:
    print("✗ MISSING: uploadArea.ondrop handler")

# Check for console.log statements
if 'console.log' in content:
    print("✓ Found: console.log statements")
    # Count them
    count = content.count('console.log')
    print(f"  Total console.log statements: {count}")
else:
    print("✗ MISSING: console.log statements")

# Check for the window.addEventListener('load')
if "window.addEventListener('load'" in content:
    print("✓ Found: window.addEventListener('load')")
else:
    print("✗ MISSING: window.addEventListener('load')")

print("\n" + "=" * 80)
print("SCRIPT BLOCK CONTENT:")
print("=" * 80)

# Extract and show the script block
import re
script_match = re.search(r'{% block scripts %}(.*?){% endblock %}', content, re.DOTALL)
if script_match:
    script_content = script_match.group(1)
    print(script_content[:500])  # First 500 chars
    print("\n... (truncated)")
else:
    print("✗ No script block found!")

print("\n" + "=" * 80)
print("FILE SIZE:", len(content), "bytes")
print("=" * 80)
