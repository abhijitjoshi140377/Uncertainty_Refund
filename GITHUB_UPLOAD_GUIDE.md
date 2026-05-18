# How to Upload This Project to GitHub

This guide will help you upload the Travel Refund Uncertainty Estimation System to GitHub.

## Prerequisites

1. **GitHub Account**: Create one at [github.com](https://github.com) if you don't have one
2. **Git Installed**: Verify with `git --version` in terminal
   - If not installed, download from [git-scm.com](https://git-scm.com/)

## Method 1: Using GitHub Desktop (Easiest for Beginners)

### Step 1: Install GitHub Desktop
1. Download from [desktop.github.com](https://desktop.github.com/)
2. Install and sign in with your GitHub account

### Step 2: Create Repository
1. Open GitHub Desktop
2. Click **File** → **Add Local Repository**
3. Click **Choose...** and select: `C:\Users\AbhijitJoshi\Uncertainty_Refund`
4. Click **Create Repository** (if prompted)
5. Click **Publish repository**
6. Set repository name: `Uncertainty_Refund`
7. Add description: "AI-Powered Travel Refund Prediction System"
8. Uncheck "Keep this code private" (if you want it public)
9. Click **Publish repository**

### Step 3: Update README with Your Repository URL
1. After publishing, GitHub Desktop will show your repository URL
2. Open `README.md` in VS Code
3. Find line 11: `**GitHub**: https://github.com/your-username/Uncertainty_Refund`
4. Replace `your-username` with your actual GitHub username
5. Save the file
6. In GitHub Desktop, you'll see the change
7. Add commit message: "Update repository URL"
8. Click **Commit to main**
9. Click **Push origin**

Done! Your project is now on GitHub.

---

## Method 2: Using Command Line (Git Bash/PowerShell)

### Step 1: Create Repository on GitHub Website
1. Go to [github.com](https://github.com)
2. Click the **+** icon (top right) → **New repository**
3. Repository name: `Uncertainty_Refund`
4. Description: "AI-Powered Travel Refund Prediction System"
5. Choose **Public** or **Private**
6. **DO NOT** check "Initialize with README" (we already have one)
7. Click **Create repository**
8. **Keep this page open** - you'll need the commands shown

### Step 2: Initialize Git in Your Project
Open PowerShell or Git Bash in your project directory:

```bash
# Navigate to your project
cd C:\Users\AbhijitJoshi\Uncertainty_Refund

# Initialize git (if not already done)
git init

# Check status
git status
```

### Step 3: Configure Git (First Time Only)
```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Add Files and Commit
```bash
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status

# Create first commit
git commit -m "Initial commit: Travel Refund Uncertainty Estimation System"
```

### Step 5: Connect to GitHub and Push
```bash
# Add remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/Uncertainty_Refund.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 6: Update README with Repository URL
```bash
# Open README.md and update line 11 with your actual GitHub username
# Then commit and push the change:

git add README.md
git commit -m "Update repository URL in README"
git push
```

---

## Method 3: Using VS Code (Integrated Git)

### Step 1: Initialize Git Repository
1. Open VS Code in your project folder
2. Click **Source Control** icon (left sidebar) or press `Ctrl+Shift+G`
3. Click **Initialize Repository**

### Step 2: Stage and Commit Files
1. You'll see all files listed
2. Click **+** next to "Changes" to stage all files
3. Enter commit message: "Initial commit: Travel Refund Uncertainty Estimation System"
4. Click **✓ Commit**

### Step 3: Create GitHub Repository
1. Click **Publish to GitHub** button
2. Sign in to GitHub if prompted
3. Choose repository name: `Uncertainty_Refund`
4. Select **Public** or **Private**
5. Click **Publish**

### Step 4: Update README
1. Open `README.md`
2. Update line 11 with your GitHub username
3. Save, commit, and push the change

---

## What Gets Uploaded?

The `.gitignore` file ensures these are **NOT** uploaded:
- ❌ `node_modules/` (frontend dependencies)
- ❌ `venv/` (Python virtual environment)
- ❌ `__pycache__/` (Python cache)
- ❌ `.env` files (if any)
- ❌ `*.db` files (database)
- ❌ IDE settings

What **WILL** be uploaded:
- ✅ All source code (backend & frontend)
- ✅ Documentation (README, guides)
- ✅ Configuration files (package.json, requirements.txt)
- ✅ Helper scripts (start.bat, start.ps1)

---

## After Upload - Verify Your Repository

1. Go to `https://github.com/YOUR-USERNAME/Uncertainty_Refund`
2. Check that all files are there
3. Click on `README.md` - it should display nicely
4. Verify the repository URL in README is correct

---

## Common Issues and Solutions

### Issue: "Git is not recognized"
**Solution**: Install Git from [git-scm.com](https://git-scm.com/) and restart terminal

### Issue: "Permission denied (publickey)"
**Solution**: 
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR-USERNAME/Uncertainty_Refund.git
```

### Issue: "Repository already exists"
**Solution**: Either:
- Delete the repository on GitHub and try again
- Or use a different repository name

### Issue: Files not showing up
**Solution**: Check `.gitignore` - make sure important files aren't ignored

### Issue: "Large files" error
**Solution**: 
```bash
# Remove large files from git
git rm --cached path/to/large/file
git commit -m "Remove large file"
```

---

## Next Steps After Upload

1. **Share Your Repository**
   - Share the URL: `https://github.com/YOUR-USERNAME/Uncertainty_Refund`
   - Others can now clone it: `git clone <your-repo-url>`

2. **Add a License**
   - Go to your repository on GitHub
   - Click **Add file** → **Create new file**
   - Name it `LICENSE`
   - Choose a license template (MIT is common)

3. **Enable GitHub Pages** (Optional)
   - For project documentation website
   - Go to Settings → Pages
   - Select source branch

4. **Add Topics/Tags**
   - On your repository page, click ⚙️ next to "About"
   - Add topics: `machine-learning`, `fastapi`, `react`, `ibm-carbon`, `travel`, `refund-prediction`

5. **Create Releases**
   - Go to **Releases** → **Create a new release**
   - Tag: `v1.0.0`
   - Title: "Initial Release"

---

## Keeping Your Repository Updated

### After Making Changes Locally

**Using GitHub Desktop:**
1. Open GitHub Desktop
2. Review changes
3. Add commit message
4. Click **Commit to main**
5. Click **Push origin**

**Using Command Line:**
```bash
git add .
git commit -m "Description of changes"
git push
```

**Using VS Code:**
1. Go to Source Control
2. Stage changes (+)
3. Enter commit message
4. Click ✓ Commit
5. Click **Sync Changes**

---

## Cloning Your Repository (For Others)

Once uploaded, anyone can clone your project:

```bash
git clone https://github.com/YOUR-USERNAME/Uncertainty_Refund.git
cd Uncertainty_Refund
```

Then follow the installation instructions in README.md.

---

## Need Help?

- **GitHub Docs**: [docs.github.com](https://docs.github.com)
- **Git Tutorial**: [git-scm.com/doc](https://git-scm.com/doc)
- **GitHub Desktop Guide**: [docs.github.com/desktop](https://docs.github.com/en/desktop)

---

**Recommended Method**: Use **GitHub Desktop** (Method 1) if you're new to Git. It's the easiest and most visual way to manage your repository.

**Last Updated**: May 18, 2026