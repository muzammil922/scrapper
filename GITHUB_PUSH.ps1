# GitHub Push Script for Windows PowerShell
# Usage: .\GITHUB_PUSH.ps1

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "📦 GitHub Push Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "🔧 Initializing git..." -ForegroundColor Yellow
    git init
}

# Check if remote exists
$remoteExists = git remote | Select-String -Pattern "origin"
if ($remoteExists) {
    Write-Host "ℹ️  Remote 'origin' already exists" -ForegroundColor Yellow
    $remove = Read-Host "Remove and add new? (y/n) [n]"
    if ($remove -eq "y" -or $remove -eq "Y") {
        git remote remove origin
    } else {
        Write-Host "Using existing remote..." -ForegroundColor Green
        git remote -v
        $continue = Read-Host "Continue with push? (y/n) [y]"
        if ($continue -ne "n" -and $continue -ne "N") {
            # Add, commit, and push
            Write-Host "📝 Adding files..." -ForegroundColor Yellow
            git add .
            
            Write-Host "💾 Committing files..." -ForegroundColor Yellow
            git commit -m "Update: Universal Data Scraper with all features"
            
            Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
            git branch -M main 2>$null
            git push -u origin main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
            } else {
                Write-Host ""
                Write-Host "❌ Push failed!" -ForegroundColor Red
            }
            exit
        }
    }
}

# Get repository URL from user
Write-Host "📋 GitHub Repository Setup" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you haven't created a repository yet:" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "2. Enter repository name (e.g., universal-data-scraper)" -ForegroundColor White
Write-Host "3. Choose Public or Private" -ForegroundColor White
Write-Host "4. DON'T initialize with README" -ForegroundColor White
Write-Host "5. Click 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "Then enter your repository URL below:" -ForegroundColor Yellow
Write-Host "Example: https://github.com/username/repo-name.git" -ForegroundColor Gray
Write-Host ""

$repo_url = Read-Host "GitHub Repository URL"

if ([string]::IsNullOrWhiteSpace($repo_url)) {
    Write-Host "❌ Repository URL is required!" -ForegroundColor Red
    exit 1
}

# Add remote
Write-Host ""
Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
git remote add origin $repo_url

# Add all files
Write-Host "📝 Adding files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "💾 Committing files..." -ForegroundColor Yellow
$commit_msg = Read-Host "Commit message [Initial commit: Universal Data Scraper]"
if ([string]::IsNullOrWhiteSpace($commit_msg)) {
    $commit_msg = "Initial commit: Universal Data Scraper with all features"
}
git commit -m $commit_msg

# Set branch to main
git branch -M main

# Push
Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  You may be asked for GitHub credentials" -ForegroundColor Red
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "🔗 Repository: $repo_url" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Your project is now on GitHub!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host "💡 Make sure:" -ForegroundColor Yellow
    Write-Host "   1. Repository URL is correct" -ForegroundColor White
    Write-Host "   2. You have access to the repository" -ForegroundColor White
    Write-Host "   3. GitHub credentials are correct" -ForegroundColor White
    Write-Host ""
    Write-Host "For authentication:" -ForegroundColor Yellow
    Write-Host "   - Use Personal Access Token as password" -ForegroundColor White
    Write-Host "   - Or use SSH key" -ForegroundColor White
}

