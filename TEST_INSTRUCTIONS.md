# File Upload Testing Instructions

## What Was Fixed

1. **Removed conflicting event listeners** - The analyzer.html and bulk_analyzer.html had inline scripts that were adding duplicate event listeners to the file inputs, causing conflicts.

2. **Created debug version** - A simplified debug version of the file upload handler (`file-upload-debug.js`) that logs everything to the console for easier debugging.

3. **Proper element IDs** - Ensured all upload areas and inputs have the correct IDs:
   - Analyzer: `singleFileUpload` and `singleFileInput`
   - Bulk Analyzer: `bulkFileUploadArea` and `bulkFileInput`

## How to Test

### Step 1: Start the Application
```bash
python app.py
```

### Step 2: Open Browser Console
- Press F12 to open Developer Tools
- Go to the Console tab

### Step 3: Test Analyzer Page
1. Navigate to: http://localhost:5000/analyzer
2. Check console for these messages:
   - "=== FILE UPLOAD DEBUG SCRIPT LOADED ==="
   - "=== DOM LOADED ==="
   - "Setting up SINGLE file upload..."
   - "Single file upload setup COMPLETE"

3. **Test Click Upload:**
   - Click on the upload area
   - Console should show: "Upload area clicked!"
   - File picker should open
   - Select a file
   - Console should show: "File selected:" with file details
   - File should appear in the file list below

4. **Test Drag & Drop:**
   - Drag a file over the upload area
   - Console should show: "Drag over"
   - Area should turn green
   - Drop the file
   - Console should show: "File dropped!" and "Dropped files:"
   - File should appear in the file list

### Step 4: Test Bulk Analyzer Page
1. Navigate to: http://localhost:5000/bulk-analyzer
2. Check console for:
   - "Setting up BULK file upload..."
   - "Bulk file upload setup COMPLETE"

3. **Test Multiple Files:**
   - Click upload area or drag multiple files
   - All files should appear in the list
   - Console should show file count and details

## Expected Console Output

When working correctly, you should see:
```
=== FILE UPLOAD DEBUG SCRIPT LOADED ===
=== DOM LOADED ===
Single upload area: <div id="singleFileUpload">
Single file input: <input id="singleFileInput">
Setting up SINGLE file upload...
Single file upload setup COMPLETE
Analyzer page script loaded
```

## Troubleshooting

### If nothing happens when clicking:
- Check console for errors
- Verify elements exist (should see them logged)
- Check if JavaScript is enabled

### If drag & drop doesn't work:
- Check console for "Drag over" messages
- Verify browser supports drag & drop
- Try a different browser

### If files don't appear in list:
- Check console for file details
- Verify .file-list element exists
- Check for JavaScript errors

## Next Steps

Once you confirm it's working with the debug version:
1. We can switch back to the production version (file-upload.js)
2. Add back validation and error handling
3. Test the full upload and analysis flow
