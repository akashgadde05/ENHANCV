// Main JavaScript for Smart ATS Resume Builder

// Global variables
let currentAnalysis = null;
let uploadedFiles = [];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initializeFormValidation();
    initializeTooltips();
});

// File upload functionality is now handled by file-upload.js

function handleFileSelection(input) {
    const files = Array.from(input.files);
    console.log(`Files selected: ${files.length}`);

    // Validate files
    const validFiles = [];
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'text/plain'];

    for (let file of files) {
        if (file.size > maxSize) {
            showAlert(`File "${file.name}" is too large. Maximum size is 16MB.`, 'error');
            continue;
        }

        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(pdf|docx|doc|txt)$/i)) {
            showAlert(`File "${file.name}" has an unsupported format. Please use PDF, DOCX, DOC, or TXT.`, 'error');
            continue;
        }

        validFiles.push(file);
    }

    if (validFiles.length === 0) {
        return;
    }

    // Update file list display
    const fileList = input.closest('.file-upload-container').querySelector('.file-list');
    if (fileList) {
        fileList.innerHTML = '';
        validFiles.forEach((file, index) => {
            const fileItem = createFileItem(file, index, input);
            fileList.appendChild(fileItem);
        });
    }

    // Update upload area text
    const uploadArea = input.closest('.file-upload-modern') || input.closest('.file-upload-area');
    const uploadText = uploadArea.querySelector('.upload-text');
    if (uploadText) {
        uploadText.innerHTML = `<span class="text-green-600 font-semibold">${validFiles.length} file(s) selected</span>`;
    }

    // Show success message
    if (typeof showAlert === 'function') {
        showAlert(`${validFiles.length} file(s) selected successfully!`, 'success');
    }
}

function createFileItem(file, index, input) {
    const div = document.createElement('div');
    div.className = 'file-item flex justify-between items-center p-3 bg-gray-50 border border-gray-200 rounded-lg mb-2 hover:bg-gray-100 transition-colors';
    div.setAttribute('data-file-index', index);

    // Get file type icon
    const fileIcon = getFileIcon(file.name);

    div.innerHTML = `
        <div class="flex items-center">
            <i class="${fileIcon} text-indigo-600 mr-3"></i>
            <div>
                <span class="font-medium text-gray-800">${file.name}</span>
                <div class="text-sm text-gray-500">${formatFileSize(file.size)}</div>
            </div>
        </div>
        <button type="button" class="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-50 transition-colors" onclick="removeFileItem(this)">
            <i class="fas fa-times"></i>
        </button>
    `;
    return div;
}

function getFileIcon(filename) {
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

function removeFileItem(button) {
    const fileItem = button.closest('.file-item');
    const fileList = button.closest('.file-list');

    if (fileItem) {
        fileItem.remove();

        // Update the file count display
        const remainingFiles = fileList.querySelectorAll('.file-item').length;
        const uploadArea = fileList.closest('.file-upload-container').querySelector('.file-upload-modern, .file-upload-area');
        const uploadText = uploadArea.querySelector('.upload-text');

        if (remainingFiles === 0) {
            uploadText.innerHTML = 'Click to upload or drag & drop';
            uploadText.classList.remove('text-green-600', 'font-semibold');
        } else {
            uploadText.innerHTML = `<span class="text-green-600 font-semibold">${remainingFiles} file(s) selected</span>`;
        }
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function removeFile(index) {
    // Implementation for removing files from selection
    console.log('Remove file at index:', index);
}

// Specific file upload handlers
function setupFileUploadHandlers() {
    // Single file upload for analyzer
    const analyzerUpload = document.getElementById('fileUploadArea');
    const analyzerInput = document.getElementById('fileInput');

    if (analyzerUpload && analyzerInput) {
        console.log('Setting up analyzer file upload...');

        // Click handler
        analyzerUpload.addEventListener('click', function (e) {
            e.preventDefault();
            analyzerInput.click();
        });

        // Drag and drop handlers
        analyzerUpload.addEventListener('dragover', function (e) {
            e.preventDefault();
            e.stopPropagation();
            analyzerUpload.classList.add('border-green-400', 'bg-green-50');
        });

        analyzerUpload.addEventListener('dragleave', function (e) {
            e.preventDefault();
            e.stopPropagation();
            analyzerUpload.classList.remove('border-green-400', 'bg-green-50');
        });

        analyzerUpload.addEventListener('drop', function (e) {
            e.preventDefault();
            e.stopPropagation();
            analyzerUpload.classList.remove('border-green-400', 'bg-green-50');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                analyzerInput.files = files;
                handleFileSelection(analyzerInput);
            }
        });

        // File input change handler
        analyzerInput.addEventListener('change', function () {
            handleFileSelection(analyzerInput);
        });
    }

    // Multiple file upload for bulk analyzer
    const bulkUpload = document.getElementById('bulkFileUploadArea');
    const bulkInput = document.getElementById('bulkFileInput');

    if (bulkUpload && bulkInput) {
        console.log('Setting up bulk analyzer file upload...');

        // Click handler
        bulkUpload.addEventListener('click', function (e) {
            e.preventDefault();
            bulkInput.click();
        });

        // Drag and drop handlers
        bulkUpload.addEventListener('dragover', function (e) {
            e.preventDefault();
            e.stopPropagation();
            bulkUpload.classList.add('border-green-400', 'bg-green-50');
        });

        bulkUpload.addEventListener('dragleave', function (e) {
            e.preventDefault();
            e.stopPropagation();
            bulkUpload.classList.remove('border-green-400', 'bg-green-50');
        });

        bulkUpload.addEventListener('drop', function (e) {
            e.preventDefault();
            e.stopPropagation();
            bulkUpload.classList.remove('border-green-400', 'bg-green-50');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                bulkInput.files = files;
                handleFileSelection(bulkInput);
            }
        });

        // File input change handler
        bulkInput.addEventListener('change', function () {
            handleFileSelection(bulkInput);
        });
    }
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Resume Analysis Functions
async function analyzeResume() {
    const form = document.getElementById('analyzeForm');
    const formData = new FormData(form);
    const submitBtn = document.getElementById('analyzeBtn');
    const resultsDiv = document.getElementById('analysisResults');

    // Validate file selection
    const fileInput = form.querySelector('input[type="file"]');
    if (!fileInput.files || fileInput.files.length === 0) {
        showAlert('Please select a resume file to analyze.', 'error');
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner mr-2"></span>Analyzing...';

    // Show loading in results area
    resultsDiv.innerHTML = `
        <div class="card-modern">
            <div class="text-center py-16">
                <div class="w-16 h-16 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <div class="loading-spinner"></div>
                </div>
                <h3 class="text-2xl font-semibold text-gray-800 mb-4">Analyzing Your Resume</h3>
                <p class="text-gray-600 max-w-md mx-auto">Our AI is examining your resume for ATS compatibility and providing detailed recommendations...</p>
            </div>
        </div>
    `;

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            currentAnalysis = data.analysis;
            displayAnalysisResults(data.analysis);
            showAlert('Resume analysis completed successfully!', 'success');
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        resultsDiv.innerHTML = `
            <div class="card-modern">
                <div class="text-center py-16">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="fas fa-exclamation-triangle text-2xl text-red-600"></i>
                    </div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-4">Analysis Failed</h3>
                    <p class="text-gray-600 max-w-md mx-auto mb-6">${error.message}</p>
                    <button onclick="analyzeResume()" class="btn-modern btn-primary-modern">
                        <i class="fas fa-redo mr-2"></i>Try Again
                    </button>
                </div>
            </div>
        `;
        showAlert(`Error: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-search mr-2"></i>Analyze Resume';
    }
}

// Bulk Analysis Functions
async function bulkAnalyze() {
    const form = document.getElementById('bulkAnalyzeForm');
    const formData = new FormData(form);
    const submitBtn = document.getElementById('bulkAnalyzeBtn');
    const resultsDiv = document.getElementById('bulkResults');

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Analyzing...';
    resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p class="mt-2">Analyzing multiple resumes...</p></div>';

    try {
        const response = await fetch('/api/bulk-analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayBulkResults(data.results);
        } else {
            throw new Error(data.error || 'Bulk analysis failed');
        }
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error: ${error.message}
            </div>
        `;
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-layer-group me-2"></i>Analyze All Resumes';
    }
}

function displayBulkResults(results) {
    const resultsDiv = document.getElementById('bulkResults');

    // Sort results by overall score
    results.sort((a, b) => b.analysis.overall_score - a.analysis.overall_score);

    let html = `
        <div class="bulk-results fade-in">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4><i class="fas fa-chart-bar me-2"></i>Analysis Results (${results.length} resumes)</h4>
                <button class="btn btn-outline-primary" onclick="exportBulkResults()">
                    <i class="fas fa-download me-2"></i>Export All Results
                </button>
            </div>
            
            <div class="row">
    `;

    results.forEach((result, index) => {
        html += `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">#${index + 1} ${result.filename}</h6>
                        <span class="badge ${getScoreBadgeClass(result.analysis.overall_score)}">
                            ${result.analysis.overall_score}/100
                        </span>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <small class="text-muted">Preview:</small>
                            <p class="small">${result.resume_preview}</p>
                        </div>
                        
                        <div class="row text-center">
                            <div class="col-6">
                                <small class="text-muted">ATS Score</small>
                                <div class="fw-bold">${result.analysis.ats_compatibility.score}</div>
                            </div>
                            <div class="col-6">
                                <small class="text-muted">Content</small>
                                <div class="fw-bold">${result.analysis.content_analysis.score}</div>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-sm btn-outline-primary w-100" 
                                onclick="viewDetailedAnalysis(${index})">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div></div>';
    resultsDiv.innerHTML = html;

    // Store results for export
    window.bulkAnalysisResults = results;
}

function getScoreBadgeClass(score) {
    if (score >= 85) return 'bg-success';
    if (score >= 70) return 'bg-primary';
    if (score >= 55) return 'bg-warning';
    return 'bg-danger';
}

function viewDetailedAnalysis(index) {
    const result = window.bulkAnalysisResults[index];
    // Create modal or new page to show detailed analysis
    console.log('View detailed analysis for:', result.filename);
}

function exportBulkResults() {
    if (!window.bulkAnalysisResults) {
        alert('No bulk analysis results to export');
        return;
    }

    const dataStr = JSON.stringify(window.bulkAnalysisResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `bulk_analysis_results_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Validate file selection
const fileInput = form.querySelector('input[type="file"]');
if (!fileInput.files || fileInput.files.length === 0) {
    showAlert('Please select a resume file to analyze.', 'error');
    return;
}

// Show loading state
submitBtn.disabled = true;
submitBtn.innerHTML = '<span class="loading-spinner mr-2"></span>Analyzing...';

// Show loading in results area
resultsDiv.innerHTML = `
        <div class="card-modern">
            <div class="text-center py-16">
                <div class="w-16 h-16 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <div class="loading-spinner"></div>
                </div>
                <h3 class="text-2xl font-semibold text-gray-800 mb-4">Analyzing Your Resume</h3>
                <p class="text-gray-600 max-w-md mx-auto">Our AI is examining your resume for ATS compatibility and providing detailed recommendations...</p>
            </div>
        </div>
    `;

try {
    const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    if (data.success) {
        currentAnalysis = data.analysis;
        displayAnalysisResults(data.analysis);
        showAlert('Resume analysis completed successfully!', 'success');
    } else {
        throw new Error(data.error || 'Analysis failed');
    }
} catch (error) {
    console.error('Analysis error:', error);
    resultsDiv.innerHTML = `
            <div class="card-modern">
                <div class="text-center py-16">
                    <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="fas fa-exclamation-triangle text-2xl text-red-600"></i>
                    </div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-4">Analysis Failed</h3>
                    <p class="text-gray-600 max-w-md mx-auto mb-6">${error.message}</p>
                    <button onclick="analyzeResume()" class="btn-modern btn-primary-modern">
                        <i class="fas fa-redo mr-2"></i>Try Again
                    </button>
                </div>
            </div>
        `;
    showAlert(`Error: ${error.message}`, 'error');
} finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="fas fa-search mr-2"></i>Analyze Resume';
}


// Display analysis results with modern styling
function displayAnalysisResults(analysis) {
    const resultsDiv = document.getElementById('analysisResults');

    const html = `
        <div class="analysis-results space-y-6 fade-in">
            <!-- Overall Score -->
            <div class="card-modern">
                <div class="text-center p-8">
                    <div class="w-32 h-32 mx-auto mb-6 relative">
                        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="#e5e7eb" stroke-width="8"/>
                            <circle cx="50" cy="50" r="45" fill="none" stroke="url(#scoreGradient)" stroke-width="8" 
                                    stroke-dasharray="${analysis.overall_score * 2.83} 283" stroke-linecap="round"/>
                            <defs>
                                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" style="stop-color:#667eea"/>
                                    <stop offset="100%" style="stop-color:#764ba2"/>
                                </linearGradient>
                            </defs>
                        </svg>
                        <div class="absolute inset-0 flex items-center justify-center">
                            <div class="text-center">
                                <div class="text-3xl font-bold text-gray-800">${analysis.overall_score}</div>
                                <div class="text-sm text-gray-500">/ 100</div>
                            </div>
                        </div>
                    </div>
                    <h2 class="text-2xl font-bold text-gray-800 mb-2">Overall ATS Score</h2>
                    <p class="text-gray-600">${getScoreDescription(analysis.overall_score)}</p>
                </div>
            </div>
            
            <!-- Detailed Scores -->
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${createScoreCard('ATS Compatibility', analysis.ats_compatibility.score, 'fas fa-robot')}
                ${createScoreCard('Content Quality', analysis.content_analysis.score, 'fas fa-file-text')}
                ${createScoreCard('Skills Analysis', analysis.skills_analysis.score, 'fas fa-cogs')}
                ${createScoreCard('Experience', analysis.experience_analysis.score, 'fas fa-briefcase')}
                ${createScoreCard('Formatting', analysis.formatting_analysis.score, 'fas fa-align-left')}
                ${createScoreCard('Keywords', analysis.keyword_optimization.score, 'fas fa-key')}
            </div>
            
            <!-- Recommendations -->
            <div class="card-modern">
                <div class="p-6">
                    <h3 class="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                        <i class="fas fa-lightbulb text-yellow-500 mr-3"></i>
                        Recommendations
                    </h3>
                    ${createRecommendationsList(analysis.recommendations)}
                </div>
            </div>
            
            <!-- Skills Analysis -->
            <div class="card-modern">
                <div class="p-6">
                    <h3 class="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                        <i class="fas fa-cogs text-blue-500 mr-3"></i>
                        Skills Analysis
                    </h3>
                    ${createSkillsAnalysis(analysis.skills_analysis)}
                </div>
            </div>
            
            <!-- Course Recommendations -->
            ${analysis.course_recommendations && analysis.course_recommendations.length > 0 ? createCourseRecommendations(analysis.course_recommendations) : ''}
            
            <!-- Export Options -->
            <div class="text-center space-x-4">
                <button class="btn-modern btn-primary-modern" onclick="exportAnalysis()">
                    <i class="fas fa-download mr-2"></i>Export Analysis
                </button>
                <button class="btn-modern btn-secondary-modern" onclick="getSuggestions()">
                    <i class="fas fa-magic mr-2"></i>Get Improvement Suggestions
                </button>
            </div>
        </div>
    `;

    resultsDiv.innerHTML = html;
}

function getScoreDescription(score) {
    if (score >= 85) return "Excellent! Your resume is well-optimized for ATS systems.";
    if (score >= 70) return "Good! Minor improvements could enhance your ATS compatibility.";
    if (score >= 55) return "Average. Several areas need attention for better ATS performance.";
    return "Needs improvement. Major optimization required for ATS compatibility.";
}

function createScoreCard(title, score, icon) {
    const colorClass = getScoreColorClass(score);
    return `
        <div class="card-modern p-6 text-center">
            <div class="w-12 h-12 ${colorClass} rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="${icon} text-white"></i>
            </div>
            <h4 class="font-semibold text-gray-800 mb-2">${title}</h4>
            <div class="text-2xl font-bold ${getScoreTextClass(score)} mb-2">${score}</div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="${getProgressBarClass(score)} h-2 rounded-full" style="width: ${score}%"></div>
            </div>
        </div>
    `;
}

function getScoreColorClass(score) {
    if (score >= 85) return 'bg-green-500';
    if (score >= 70) return 'bg-blue-500';
    if (score >= 55) return 'bg-yellow-500';
    return 'bg-red-500';
}

function getScoreTextClass(score) {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 55) return 'text-yellow-600';
    return 'text-red-600';
}

function getProgressBarClass(score) {
    if (score >= 85) return 'bg-green-500';
    if (score >= 70) return 'bg-blue-500';
    if (score >= 55) return 'bg-yellow-500';
    return 'bg-red-500';
}

function createRecommendationsList(recommendations) {
    let html = '';

    if (recommendations.high_priority && recommendations.high_priority.length > 0) {
        html += '<div class="mb-6">';
        html += '<h4 class="text-lg font-semibold text-red-600 mb-3 flex items-center">';
        html += '<i class="fas fa-exclamation-circle mr-2"></i>High Priority</h4>';
        recommendations.high_priority.forEach(rec => {
            html += `<div class="bg-red-50 border-l-4 border-red-400 p-4 mb-2 rounded-r-lg">${rec}</div>`;
        });
        html += '</div>';
    }

    if (recommendations.medium_priority && recommendations.medium_priority.length > 0) {
        html += '<div class="mb-6">';
        html += '<h4 class="text-lg font-semibold text-yellow-600 mb-3 flex items-center">';
        html += '<i class="fas fa-exclamation-triangle mr-2"></i>Medium Priority</h4>';
        recommendations.medium_priority.forEach(rec => {
            html += `<div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-2 rounded-r-lg">${rec}</div>`;
        });
        html += '</div>';
    }

    if (recommendations.low_priority && recommendations.low_priority.length > 0) {
        html += '<div class="mb-6">';
        html += '<h4 class="text-lg font-semibold text-blue-600 mb-3 flex items-center">';
        html += '<i class="fas fa-info-circle mr-2"></i>Low Priority</h4>';
        recommendations.low_priority.forEach(rec => {
            html += `<div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-2 rounded-r-lg">${rec}</div>`;
        });
        html += '</div>';
    }

    return html || '<p class="text-gray-500">No specific recommendations available.</p>';
}

function createSkillsAnalysis(skillsAnalysis) {
    let html = '<div class="grid md:grid-cols-2 gap-6">';

    if (skillsAnalysis.technical_skills && skillsAnalysis.technical_skills.length > 0) {
        html += `
            <div>
                <h4 class="font-semibold text-gray-800 mb-3 flex items-center">
                    <i class="fas fa-code text-blue-500 mr-2"></i>Technical Skills Found
                </h4>
                <div class="flex flex-wrap gap-2">
                    ${skillsAnalysis.technical_skills.map(skill =>
            `<span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">${skill}</span>`
        ).join('')}
                </div>
            </div>
        `;
    }

    if (skillsAnalysis.soft_skills && skillsAnalysis.soft_skills.length > 0) {
        html += `
            <div>
                <h4 class="font-semibold text-gray-800 mb-3 flex items-center">
                    <i class="fas fa-users text-green-500 mr-2"></i>Soft Skills Found
                </h4>
                <div class="flex flex-wrap gap-2">
                    ${skillsAnalysis.soft_skills.map(skill =>
            `<span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">${skill}</span>`
        ).join('')}
                </div>
            </div>
        `;
    }

    if (skillsAnalysis.missing_skills && skillsAnalysis.missing_skills.length > 0) {
        html += `
            <div class="md:col-span-2">
                <h4 class="font-semibold text-gray-800 mb-3 flex items-center">
                    <i class="fas fa-plus-circle text-yellow-500 mr-2"></i>Recommended Skills to Add
                </h4>
                <div class="flex flex-wrap gap-2">
                    ${skillsAnalysis.missing_skills.map(skill =>
            `<span class="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">${skill}</span>`
        ).join('')}
                </div>
            </div>
        `;
    }

    html += '</div>';
    return html;
}

function createCourseRecommendations(courseRecommendations) {
    let html = `
        <div class="card-modern">
            <div class="p-6">
                <h3 class="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                    <i class="fas fa-graduation-cap text-purple-500 mr-3"></i>
                    Course Recommendations
                </h3>
                <div class="space-y-6">
    `;

    courseRecommendations.forEach(skillGroup => {
        html += `<div>`;
        html += `<h4 class="text-lg font-semibold text-purple-600 mb-3">${skillGroup.skill}</h4>`;
        html += `<div class="grid md:grid-cols-2 gap-4">`;

        skillGroup.courses.forEach(course => {
            html += `
                <div class="course-card">
                    <div class="flex justify-between items-start mb-2">
                        <h5 class="font-semibold text-gray-800">${course.title}</h5>
                        <span class="platform-badge">${course.platform}</span>
                    </div>
                    <p class="text-sm text-gray-600 mb-2">${course.reason}</p>
                    <div class="text-xs text-gray-500">Level: ${course.level}</div>
                </div>
            `;
        });

        html += `</div></div>`;
    });

    html += '</div></div></div>';
    return html;
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-modern alert-${type} fixed top-4 right-4 z-50 max-w-md`;
    alertDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'} mr-3"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-auto">
                <i class="fas fa-times"></i>
            </button>
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

// Export and other functions
async function exportAnalysis() {
    if (!currentAnalysis) {
        showAlert('No analysis data to export', 'error');
        return;
    }

    try {
        const response = await fetch('/api/export-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentAnalysis)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `resume_analysis_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showAlert('Analysis exported successfully!', 'success');
        } else {
            throw new Error('Export failed');
        }
    } catch (error) {
        showAlert('Error exporting analysis: ' + error.message, 'error');
    }
}

async function getSuggestions() {
    showAlert('Getting improvement suggestions...', 'info');
    // Implementation for getting suggestions would go here
}