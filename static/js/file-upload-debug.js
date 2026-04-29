// Debug version of file upload handler
console.log('=== FILE UPLOAD DEBUG SCRIPT LOADED ===');

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOM LOADED ===');
    
    // Check if elements exist
    const singleUploadArea = document.getElementById('singleFileUpload');
    const singleFileInput = document.getElementById('singleFileInput');
    const bulkUploadArea = document.getElementById('bulkFileUploadArea');
    const bulkFileInput = document.getElementById('bulkFileInput');
    
    console.log('Single upload area:', singleUploadArea);
    console.log('Single file input:', singleFileInput);
    console.log('Bulk upload area:', bulkUploadArea);
    console.log('Bulk file input:', bulkFileInput);
    
    // Setup single file upload if elements exist
    if (singleUploadArea && singleFileInput) {
        console.log('Setting up SINGLE file upload...');
        
        // Click to upload
        singleUploadArea.addEventListener('click', function(e) {
            console.log('Upload area clicked!');
            e.preventDefault();
            e.stopPropagation();
            singleFileInput.click();
        });
        
        // File input change
        singleFileInput.addEventListener('change', function(e) {
            console.log('File selected:', this.files);
            if (this.files.length > 0) {
                const file = this.files[0];
                console.log('File name:', file.name);
                console.log('File size:', file.size);
                console.log('File type:', file.type);
                
                // Show file in UI
                const container = this.closest('.file-upload-container');
                const fileList = container.querySelector('.file-list');
                if (fileList) {
                    fileList.innerHTML = `
                        <div class="alert alert-success">
                            <i class="fas fa-file me-2"></i>
                            ${file.name} (${formatBytes(file.size)})
                        </div>
                    `;
                }
                
                // Update upload text
                const uploadText = container.querySelector('.upload-text');
                if (uploadText) {
                    uploadText.innerHTML = '<span class="text-success fw-bold">1 file selected</span>';
                }
            }
        });
        
        // Drag and drop
        singleUploadArea.addEventListener('dragover', function(e) {
            console.log('Drag over');
            e.preventDefault();
            e.stopPropagation();
            this.style.borderColor = '#28a745';
            this.style.backgroundColor = '#d4edda';
        });
        
        singleUploadArea.addEventListener('dragleave', function(e) {
            console.log('Drag leave');
            e.preventDefault();
            e.stopPropagation();
            this.style.borderColor = '#dee2e6';
            this.style.backgroundColor = 'transparent';
        });
        
        singleUploadArea.addEventListener('drop', function(e) {
            console.log('File dropped!');
            e.preventDefault();
            e.stopPropagation();
            this.style.borderColor = '#dee2e6';
            this.style.backgroundColor = 'transparent';
            
            const files = e.dataTransfer.files;
            console.log('Dropped files:', files);
            
            if (files.length > 0) {
                // Manually set the files to the input
                singleFileInput.files = files;
                
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                singleFileInput.dispatchEvent(event);
            }
        });
        
        console.log('Single file upload setup COMPLETE');
    } else {
        console.log('Single file upload elements NOT FOUND');
    }
    
    // Setup bulk file upload if elements exist
    if (bulkUploadArea && bulkFileInput) {
        console.log('Setting up BULK file upload...');
        
        // Click to upload
        bulkUploadArea.addEventListener('click', function(e) {
            console.log('Bulk upload area clicked!');
            e.preventDefault();
            e.stopPropagation();
            bulkFileInput.click();
        });
        
        // File input change
        bulkFileInput.addEventListener('change', function(e) {
            console.log('Files selected:', this.files);
            if (this.files.length > 0) {
                const container = this.closest('.file-upload-container');
                const fileList = container.querySelector('.file-list');
                if (fileList) {
                    fileList.innerHTML = '';
                    Array.from(this.files).forEach(file => {
                        const div = document.createElement('div');
                        div.className = 'alert alert-success mb-2';
                        div.innerHTML = `
                            <i class="fas fa-file me-2"></i>
                            ${file.name} (${formatBytes(file.size)})
                        `;
                        fileList.appendChild(div);
                    });
                }
                
                // Update upload text
                const uploadText = container.querySelector('.upload-text');
                if (uploadText) {
                    uploadText.innerHTML = `<span class="text-success fw-bold">${this.files.length} file(s) selected</span>`;
                }
            }
        });
        
        // Drag and drop
        bulkUploadArea.addEventListener('dragover', function(e) {
            console.log('Bulk drag over');
            e.preventDefault();
            e.stopPropagation();
            this.style.borderColor = '#28a745';
            this.style.backgroundColor = '#d4edda';
        });
        
        bulkUploadArea.addEventListener('dragleave', function(e) {
            console.log('Bulk drag leave');
            e.preventDefault();
            e.stopPropagation();
            this.style.borderColor = '#dee2e6';
            this.style.backgroundColor = 'transparent';
        });
        
        bulkUploadArea.addEventListener('drop', function(e) {
            console.log('Bulk files dropped!');
            e.preventDefault();
            e.stopPropagation();
            this.style.borderColor = '#dee2e6';
            this.style.backgroundColor = 'transparent';
            
            const files = e.dataTransfer.files;
            console.log('Dropped files:', files);
            
            if (files.length > 0) {
                bulkFileInput.files = files;
                const event = new Event('change', { bubbles: true });
                bulkFileInput.dispatchEvent(event);
            }
        });
        
        console.log('Bulk file upload setup COMPLETE');
    } else {
        console.log('Bulk file upload elements NOT FOUND');
    }
});

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

console.log('=== FILE UPLOAD DEBUG SCRIPT END ===');
