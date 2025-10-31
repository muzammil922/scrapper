#!/bin/bash

# Quick script to push project to GitHub
# Usage: bash QUICK_PUSH.sh

echo "======================================"
echo "📦 GitHub Push Script"
echo "======================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git..."
    git init
fi

# Get repository URL from user
echo "Enter your GitHub repository URL:"
echo "Example: https://github.com/username/repo-name.git"
read -r repo_url

if [ -z "$repo_url" ]; then
    echo "❌ Repository URL is required!"
    exit 1
fi

# Add remote
echo ""
echo "🔗 Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin "$repo_url"

# Add all files
echo "📝 Adding files..."
git add .

# Commit
echo "💾 Committing files..."
git commit -m "Initial commit: Universal Data Scraper with all features"

# Set branch to main
git branch -M main

# Push
echo ""
echo "🚀 Pushing to GitHub..."
echo "⚠️  You may be asked for GitHub credentials"
echo ""
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🔗 Repository: $repo_url"
else
    echo ""
    echo "❌ Push failed!"
    echo "💡 Make sure:"
    echo "   1. Repository URL is correct"
    echo "   2. You have access to the repository"
    echo "   3. GitHub credentials are correct"
fi

