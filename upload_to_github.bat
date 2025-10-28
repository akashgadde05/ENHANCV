@echo off
REM Git commands to upload to GitHub (Windows)

echo 🚀 Uploading Smart ATS Resume Builder to GitHub
echo Repository: https://github.com/akashgadde05/ENHANCV
echo.

REM Initialize git if not already done
if not exist ".git" (
    echo 📁 Initializing git repository...
    git init
)

REM Add remote if not exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo 🔗 Adding remote origin...
    git remote add origin https://github.com/akashgadde05/ENHANCV.git
)

REM Add all files
echo 📝 Adding files to git...
git add .

REM Commit
echo 💾 Committing changes...
git commit -m "Initial commit: Smart ATS Resume Builder with Llama 3.3 70B"

REM Push to GitHub
echo 🚀 Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Upload complete!
echo 🌐 Your repository is now available at:
echo    https://github.com/akashgadde05/ENHANCV
pause
