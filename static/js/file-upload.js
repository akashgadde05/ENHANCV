// Dedicated File Upload Handler
class FileUploadHandler {
    constructor() {
        this.init();
    }

    init() {
        console.log('Initializing file upload handlers...');
        this.setupSingleFileUpload();
        this.setupBulkFileUpload();
    }

    setupSingleFileUpload() {
        const uploadArea = document.getElementById('singleFileUpload');
        const fileInput = document.getElementById('singleFileInput');
        
        if (!uploadArea || !fileInput) {
            console.log('Single file upload elements not found');
            return;
        }

        console.log('Setting up single file upload...');

        // Click handler
        uploadArea.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            fileInput.click();
        });

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => this.highlight(uploadArea), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => this.unhighlight(uploadArea), false);
        });

        // Handle dropped files
        uploadArea.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            this.handleFiles(files, fileInput, false);
        }, false);

        // Handle selected files
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files, fileInput, false);
        });
    }

    setupBulkFileUpload() {
        const uploadArea = document.getElementById('bulkFileUploadArea');
        const fileInput = document.getElementById('bulkFileInput');
        
        if (!uploadArea || !fileInput) {
            console.log('Bulk file upload elements not found');
            return;
        }

        console.log('Setting up bulk file upload...');

        // Click handler
        uploadArea.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            fileInput.click();
        });

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => this.highlight(uploadArea), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => this.unhighlight(uploadArea), false);
        });

        // Handle dropped files
        uploadArea.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            this.handleFiles(files, fileInput, true);
        }, false);

        // Handle selected files
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files, fileInput, true);
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    highlight(element) {
        element.style.borderColor = '#28a745';
        element.style.backgroundColor = '#d4edda';
        element.style.borderStyle = 'solid';
    }

    unhighlight(element) {
        element.style.borderColor = '#dee2e6';
        element.style.backgroundColor = 'transparent';
        element.style.borderStyle = 'dashed';
    }

    handleFiles(files, input, isMultiple) {
        console.log(`Handling ${files.length} files (multiple: ${isMultiple})`);
        
        const validFiles = this.validateFiles(files);
        
        if (validFiles.length === 0) {
            return;
        }

        // Update the input files
        const dt = new DataTransfer();
        validFiles.forEach(file => dt.items.add(file));
        input.files = dt.files;

        // Update UI
        this.updateFileList(validFiles, input);
        this.updateUploadText(validFiles.length, input);
        
        // Show success message
        this.showMessage(`${validFiles.length} file(s) selected successfully!`, 'success');
    }

    validateFiles(files) {
        const validFiles = [];
        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedExtensions = ['pdf', 'docx', 'doc', 'txt'];

        Array.from(files).forEach(file => {
            // Check file size
            if (file.size > maxSize) {
                this.showMessage(`File "${file.name}" is too large. Maximum size is 16MB.`, 'error');
                return;
            }

            // Check file extension
            const extension = file.name.split('.').pop().toLowerCase();
            if (!allowedExtensions.includes(extension)) {
                this.showMessage(`File "${file.name}" has an unsupported format. Please use PDF, DOCX, DOC, or TXT.`, 'error');
                return;
            }

            validFiles.push(file);
        });

        return validFiles;
    }

    updateFileList(files, input) {
        const container = input.closest('.file-upload-container');
        const fileList = container.querySelector('.file-list');
        
        if (!fileList) return;

        fileList.innerHTML = '';
        
        files.forEach((file, index) => {
            const fileItem = this.createFileItem(file, index, input);
            fileList.appendChild(fileItem);
        });
    }

    createFileItem(file, index, input) {
        const div = document.createElement('div');
        div.className = 'file-item d-flex justify-content-between align-items-center p-3 bg-light border rounded mb-2';
        div.style.transition = 'all 0.3s';
        
        const fileIcon = this.getFileIcon(file.name);
        
        div.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="${fileIcon} text-primary me-3"></i>
                <div>
                    <span class="fw-medium">${file.name}</span>
                    <div class="small text-muted">${this.formatFileSize(file.size)}</div>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger remove-file-btn" data-index="${index}">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Add remove functionality
        const removeBtn = div.querySelector('.remove-file-btn');
        removeBtn.addEventListener('click', () => {
            this.removeFile(index, input);
        });

        return div;
    }

    removeFile(index, input) {
        const files = Array.from(input.files);
        files.splice(index, 1);

        // Update input files
        const dt = new DataTransfer();
        files.forEach(file => dt.items.add(file));
        input.files = dt.files;

        // Update UI
        this.updateFileList(files, input);
        this.updateUploadText(files.length, input);
    }

    updateUploadText(fileCount, input) {
        const container = input.closest('.file-upload-container');
        const uploadText = container.querySelector('.upload-text');
        
        if (!uploadText) return;

        if (fileCount === 0) {
            uploadText.innerHTML = input.multiple ? 
                'Click to upload or drag & drop multiple files' : 
                'Click to upload or drag & drop';
            uploadText.className = 'mb-0';
        } else {
            uploadText.innerHTML = `<span class="text-success fw-bold">${fileCount} file(s) selected</span>`;
        }
    }

    getFileIcon(filename) {
        const extension = filename.split('.').pop().toLowerCase();
        switch (extension) {
            case 'pdf':
                return 'fas fa-file-pdf';
            case 'docx':
            case 'doc':
                return 'fas fa-file-word';
            case 'txt':
                return 'fas fa-file-alt';
            default:
                return 'fas fa-file';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showMessage(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${this.getAlertClass(type)} alert-dismissible fade show`;
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.maxWidth = '400px';
        alertDiv.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        
        alertDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentElement) {
                alertDiv.remove();
            }
        }, 5000);
    }

    getAlertClass(type) {
        switch (type) {
            case 'success':
                return 'alert-success';
            case 'error':
                return 'alert-danger';
            case 'warning':
                return 'alert-warning';
            default:
                return 'alert-info';
        }
    }

    getAlertIcon(type) {
        switch (type) {
            case 'success':
                return 'check-circle';
            case 'error':
                return 'exclamation-triangle';
            case 'warning':
                return 'exclamation-circle';
            default:
                return 'info-circle';
        }
    }
}

// Initialize file upload when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing file upload...');
    new FileUploadHandler();
});