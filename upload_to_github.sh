#!/bin/bash
# Git commands to upload to GitHub

echo "🚀 Uploading Smart ATS Resume Builder to GitHub"
echo "Repository: https://github.com/akashgadde05/ENHANCV"
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add remote if not exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Adding remote origin..."
    git remote add origin https://github.com/akashgadde05/ENHANCV.git
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Initial commit: Smart ATS Resume Builder with Llama 3.3 70B

Features:
- AI-powered resume analysis using Groq's Llama 3.3 70B Versatile
- Interactive resume builder with real-time preview
- ATS compatibility scoring and recommendations
- Bulk resume analysis for HR teams
- Professional PDF generation
- Course recommendations based on skill gaps
- Responsive web interface with Bootstrap 5
- Comprehensive error handling and fallback systems
- Multiple installation options for different environments

Tech Stack:
- Backend: Flask, Python 3.8+
- AI: Groq API with Llama 3.3 70B Versatile
- Frontend: Bootstrap 5, JavaScript, Jinja2
- PDF: ReportLab
- Text Processing: pypdf, python-docx
- Testing: Comprehensive test suite"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Upload complete!"
echo "🌐 Your repository is now available at:"
echo "   https://github.com/akashgadde05/ENHANCV"
echo ""
echo "📋 Next steps:"
echo "   1. Go to your GitHub repository"
echo "   2. Add a description and topics"
echo "   3. Enable GitHub Pages if desired"
echo "   4. Set up branch protection rules"
echo "   5. Add collaborators if needed"
