// Main JavaScript for Smart ATS Resume Builder

// Global variables
let currentAnalysis = null;
let uploadedFiles = [];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUploads();
    initializeFormValidation();
    initializeTooltips();
});

// File Upload Functionality
function initializeFileUploads() {
    const fileUploadAreas = document.querySelectorAll('.file-upload-area');
    
    fileUploadAreas.forEach(area => {
        const input = area.querySelector('input[type="file"]');
        
        // Click to upload
        area.addEventListener('click', () => input.click());
        
        // Drag and drop
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                handleFileSelection(input);
            }
        });
        
        // File selection
        input.addEventListener('change', () => handleFileSelection(input));
    });
}

function handleFileSelection(input) {
    const files = Array.from(input.files);
    const fileList = input.closest('.file-upload-container').querySelector('.file-list');
    
    if (fileList) {
        fileList.innerHTML = '';
        files.forEach((file, index) => {
            const fileItem = createFileItem(file, index);
            fileList.appendChild(fileItem);
        });
    }
    
    // Update upload area text
    const uploadArea = input.closest('.file-upload-area');
    const uploadText = uploadArea.querySelector('.upload-text');
    if (uploadText) {
        uploadText.textContent = `${files.length} file(s) selected`;
    }
}

function createFileItem(file, index) {
    const div = document.createElement('div');
    div.className = 'file-item d-flex justify-content-between align-items-center p-2 border rounded mb-2';
    div.innerHTML = `
        <div>
            <i class="fas fa-file-alt me-2"></i>
            <span>${file.name}</span>
            <small class="text-muted ms-2">(${formatFileSize(file.size)})</small>
        </div>
        <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeFile(${index})">
            <i class="fas fa-times"></i>
        </button>
    `;
    return div;
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

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
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
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Analyzing...';
    resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p class="mt-2">Analyzing your resume with AI...</p></div>';
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAnalysis = data.analysis;
            displayAnalysisResults(data.analysis);
        } else {
            throw new Error(data.error || 'Analysis failed');
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
        submitBtn.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Resume';
    }
}

function displayAnalysisResults(analysis) {
    const resultsDiv = document.getElementById('analysisResults');
    
    const html = `
        <div class="analysis-results fade-in">
            <!-- Overall Score -->
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card ${getScoreCardClass(analysis.overall_score)}">
                        <div class="card-body text-center">
                            <h2 class="display-4 mb-0">${analysis.overall_score}/100</h2>
                            <p class="mb-0">Overall ATS Score</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Detailed Scores -->
            <div class="row mb-4">
                ${createScoreCard('ATS Compatibility', analysis.ats_compatibility.score)}
                ${createScoreCard('Content Quality', analysis.content_analysis.score)}
                ${createScoreCard('Skills Analysis', analysis.skills_analysis.score)}
                ${createScoreCard('Experience', analysis.experience_analysis.score)}
                ${createScoreCard('Formatting', analysis.formatting_analysis.score)}
                ${createScoreCard('Keywords', analysis.keyword_optimization.score)}
            </div>
            
            <!-- Recommendations -->
            <div class="card mb-4">
                <div class="card-header">
                    <h4 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Recommendations</h4>
                </div>
                <div class="card-body">
                    ${createRecommendationsList(analysis.recommendations)}
                </div>
            </div>
            
            <!-- Skills Analysis -->
            <div class="card mb-4">
                <div class="card-header">
                    <h4 class="mb-0"><i class="fas fa-cogs me-2"></i>Skills Analysis</h4>
                </div>
                <div class="card-body">
                    ${createSkillsAnalysis(analysis.skills_analysis)}
                </div>
            </div>
            
            <!-- Course Recommendations -->
            ${analysis.course_recommendations.length > 0 ? createCourseRecommendations(analysis.course_recommendations) : ''}
            
            <!-- Export Options -->
            <div class="text-center mt-4">
                <button class="btn btn-primary me-2" onclick="exportAnalysis()">
                    <i class="fas fa-download me-2"></i>Export Analysis
                </button>
                <button class="btn btn-outline-primary" onclick="getSuggestions()">
                    <i class="fas fa-magic me-2"></i>Get Improvement Suggestions
                </button>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

function getScoreCardClass(score) {
    if (score >= 85) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 55) return 'score-average';
    return 'score-poor';
}

function createScoreCard(title, score) {
    return `
        <div class="col-md-4 col-lg-2 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">${score}</h5>
                    <p class="card-text small">${title}</p>
                    <div class="progress" style="height: 5px;">
                        <div class="progress-bar ${getProgressBarClass(score)}" 
                             style="width: ${score}%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function getProgressBarClass(score) {
    if (score >= 85) return 'bg-success';
    if (score >= 70) return 'bg-primary';
    if (score >= 55) return 'bg-warning';
    return 'bg-danger';
}

function createRecommendationsList(recommendations) {
    let html = '';
    
    if (recommendations.high_priority && recommendations.high_priority.length > 0) {
        html += '<h6 class="text-danger"><i class="fas fa-exclamation-circle me-2"></i>High Priority</h6>';
        recommendations.high_priority.forEach(rec => {
            html += `<div class="recommendation-item recommendation-high">${rec}</div>`;
        });
    }
    
    if (recommendations.medium_priority && recommendations.medium_priority.length > 0) {
        html += '<h6 class="text-warning mt-3"><i class="fas fa-exclamation-triangle me-2"></i>Medium Priority</h6>';
        recommendations.medium_priority.forEach(rec => {
            html += `<div class="recommendation-item recommendation-medium">${rec}</div>`;
        });
    }
    
    if (recommendations.low_priority && recommendations.low_priority.length > 0) {
        html += '<h6 class="text-info mt-3"><i class="fas fa-info-circle me-2"></i>Low Priority</h6>';
        recommendations.low_priority.forEach(rec => {
            html += `<div class="recommendation-item recommendation-low">${rec}</div>`;
        });
    }
    
    return html || '<p class="text-muted">No specific recommendations available.</p>';
}

function createSkillsAnalysis(skillsAnalysis) {
    let html = '<div class="row">';
    
    if (skillsAnalysis.technical_skills && skillsAnalysis.technical_skills.length > 0) {
        html += `
            <div class="col-md-6 mb-3">
                <h6><i class="fas fa-code me-2"></i>Technical Skills Found</h6>
                <div class="d-flex flex-wrap gap-1">
                    ${skillsAnalysis.technical_skills.map(skill => 
                        `<span class="badge bg-primary">${skill}</span>`
                    ).join('')}
                </div>
            </div>
        `;
    }
    
    if (skillsAnalysis.soft_skills && skillsAnalysis.soft_skills.length > 0) {
        html += `
            <div class="col-md-6 mb-3">
                <h6><i class="fas fa-users me-2"></i>Soft Skills Found</h6>
                <div class="d-flex flex-wrap gap-1">
                    ${skillsAnalysis.soft_skills.map(skill => 
                        `<span class="badge bg-success">${skill}</span>`
                    ).join('')}
                </div>
            </div>
        `;
    }
    
    if (skillsAnalysis.missing_skills && skillsAnalysis.missing_skills.length > 0) {
        html += `
            <div class="col-12 mb-3">
                <h6><i class="fas fa-plus-circle me-2"></i>Recommended Skills to Add</h6>
                <div class="d-flex flex-wrap gap-1">
                    ${skillsAnalysis.missing_skills.map(skill => 
                        `<span class="badge bg-warning text-dark">${skill}</span>`
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
        <div class="card mb-4">
            <div class="card-header">
                <h4 class="mb-0"><i class="fas fa-graduation-cap me-2"></i>Course Recommendations</h4>
            </div>
            <div class="card-body">
    `;
    
    courseRecommendations.forEach(skillGroup => {
        html += `<h6 class="text-primary">${skillGroup.skill}</h6>`;
        skillGroup.courses.forEach(course => {
            html += `
                <div class="course-card">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="mb-1">${course.title}</h6>
                            <p class="mb-1 small text-muted">${course.reason}</p>
                        </div>
                        <div class="text-end">
                            <span class="platform-badge bg-light text-dark">${course.platform}</span>
                            <br>
                            <small class="text-muted">${course.level}</small>
                        </div>
                    </div>
                </div>
            `;
        });
    });
    
    html += '</div></div>';
    return html;
}

// Export and Suggestions Functions
async function exportAnalysis() {
    if (!currentAnalysis) {
        alert('No analysis data to export');
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
        } else {
            throw new Error('Export failed');
        }
    } catch (error) {
        alert('Error exporting analysis: ' + error.message);
    }
}

async function getSuggestions() {
    // Implementation for getting improvement suggestions
    console.log('Getting suggestions...');
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
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `bulk_analysis_results_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}