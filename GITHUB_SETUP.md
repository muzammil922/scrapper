# 📦 GitHub Setup Guide

## 🎯 Steps to Push Project to GitHub

### Step 1: Create GitHub Repository

1. Go to: https://github.com
2. Click **"+"** → **"New repository"**
3. Repository name: `universal-data-scraper` (or any name you like)
4. Description: `🌍 Universal Data Scraper - Scrape data from anywhere, anytime, automatically!`
5. Choose **Public** or **Private**
6. **DON'T** initialize with README (we already have one)
7. Click **"Create repository"**

### Step 2: Initialize Git (If Not Done)

```bash
# Check if git is initialized
git status

# If not initialized, run:
git init
```

### Step 3: Add All Files

```bash
# Add all files
git add .

# Check what will be committed
git status
```

### Step 4: Commit Files

```bash
# First commit
git commit -m "Initial commit: Universal Data Scraper with all features"
```

### Step 5: Connect to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/universal-data-scraper.git

# Verify remote
git remote -v
```

### Step 6: Push to GitHub

```bash
# Push to GitHub (first time)
git branch -M main
git push -u origin main
```

### Step 7: Verify

1. Go to your GitHub repository
2. Refresh the page
3. All files should be there!

---

## 🔐 Authentication

### Option A: Personal Access Token (Recommended)

If asked for password:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (all repo permissions)
4. Copy token
5. Use token as password when pushing

### Option B: SSH Key

```bash
# Generate SSH key (if not exists)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Copy public key: cat ~/.ssh/id_ed25519.pub

# Use SSH URL:
git remote set-url origin git@github.com:YOUR_USERNAME/universal-data-scraper.git
```

---

## 📝 Quick Commands

```bash
# Initial setup (one time)
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main

# Future updates
git add .
git commit -m "Update: Added new features"
git push
```

---

## ✅ What Gets Pushed

**Included:**
- ✅ All Python files
- ✅ Configuration files
- ✅ Documentation
- ✅ Requirements.txt
- ✅ README.md

**Excluded (via .gitignore):**
- ❌ `__pycache__/`
- ❌ `*.csv`, `*.xlsx`, `*.json` (scraped data)
- ❌ `venv/`, `env/`
- ❌ `.env` files
- ❌ IDE files

---

## 🎯 After Pushing

### Next Steps:

1. **Deploy to Railway:**
   - Go to railway.app
   - Connect GitHub repo
   - Auto-deploys!

2. **Deploy to Vercel:**
   - Go to vercel.com
   - Import GitHub repo
   - Auto-deploys!

3. **Share:**
   - Share repo link
   - Collaborate
   - Accept contributions!

---

## 🔄 Updating Repository

```bash
# After making changes
git add .
git commit -m "Description of changes"
git push
```

---

## 📋 Checklist

- [ ] GitHub account created
- [ ] New repository created
- [ ] Git initialized locally
- [ ] Files added and committed
- [ ] Remote added
- [ ] Pushed to GitHub
- [ ] Verified on GitHub website

---

## 🎉 Done!

Your project is now on GitHub! 🚀

**Next:** Deploy to Railway or Vercel for cloud hosting!

