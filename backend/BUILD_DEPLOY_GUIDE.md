# 🔨 Build & Deployment Scripts Guide

## Overview

Your Lexsy backend now has automated build scripts for Render deployment:

```
backend/
├── build.sh                 ← Main build script (runs on Render)
├── pre-deploy-check.sh      ← Local pre-deployment checker
└── render.yaml              ← Legacy config (not used if root render.yaml exists)
```

---

## ✅ What You Have

### 1. `build.sh` - Production Build Script

**Purpose:** Runs automatically on Render during deployment

**What it does:**
- ✅ Upgrades pip
- ✅ Installs all Python dependencies from requirements.txt
- ✅ Creates necessary directories (uploads/, processed/, logs/)
- ✅ Verifies critical dependencies are installed
- ✅ Checks Python version
- ✅ Validates Firebase and Redis (optional)

**Usage:** Automatically executed by Render (no manual action needed)

### 2. `pre-deploy-check.sh` - Local Validation Script

**Purpose:** Run locally BEFORE pushing to GitHub to catch issues early

**What it checks:**
- ✅ All required files exist (app.py, requirements.txt, services/)
- ✅ build.sh is executable
- ✅ Critical dependencies in requirements.txt
- ✅ .gitignore has sensitive files
- ✅ Firebase config is secure
- ✅ Environment setup is correct

**Usage:**
```bash
cd backend
bash pre-deploy-check.sh
```

---

## 🚀 Deployment Workflow

### Option 1: Using render.yaml (Automated) ✅ RECOMMENDED

**This is what you have configured:**

```yaml
buildCommand: bash build.sh
```

**Steps:**
1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to dashboard.render.com
   - Create New Web Service
   - Connect GitHub repository
   - Root Directory: `backend`
   - **Build automatically uses build.sh** ✓
   - Add environment variables
   - Click Deploy

3. **Render automatically:**
   - Detects Python environment
   - Runs `bash build.sh`
   - Creates directories
   - Installs dependencies
   - Starts your app with gunicorn

**That's it!** No manual build.sh or deploy.sh needed!

---

### Option 2: Manual Testing (Local)

**Before deploying, test locally:**

1. **Run pre-deployment check:**
   ```bash
   cd backend
   bash pre-deploy-check.sh
   ```

2. **Test build script locally:**
   ```bash
   cd backend
   bash build.sh
   ```

3. **Test app locally:**
   ```bash
   cd backend
   source venv/bin/activate  # If using venv
   gunicorn --bind 0.0.0.0:5001 app:app
   ```

---

## 📋 Pre-Deployment Checklist

Run this before every deployment:

```bash
cd backend
bash pre-deploy-check.sh
```

**Should pass:**
- ✓ All required files exist
- ✓ Dependencies in requirements.txt
- ✓ build.sh is executable
- ✓ .gitignore configured correctly
- ✓ No secrets committed to git

---

## 🔧 Do You Need deploy.sh?

**Short answer: NO!**

You **don't need** a separate `deploy.sh` because:

1. ✅ **render.yaml handles deployment** - Points to build.sh
2. ✅ **Render automates the process** - Detects changes and redeploys
3. ✅ **build.sh covers everything** - Build + setup in one script

**When you WOULD need deploy.sh:**
- Database migrations (you're using in-memory/Redis)
- Complex multi-step deployments
- Custom deployment logic
- Multiple environments

**For Lexsy:** `render.yaml` + `build.sh` is perfect! ✓

---

## 🎯 Current Setup Summary

### What Happens on Render Deploy:

```
1. Render detects push to main branch
   ↓
2. Reads render.yaml
   ↓
3. Sets root directory to backend/
   ↓
4. Runs: bash build.sh
   ├── Upgrades pip
   ├── Installs requirements.txt
   ├── Creates directories (uploads/, processed/, logs/)
   └── Verifies dependencies
   ↓
5. Starts app: gunicorn --worker-class gthread --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT app:app
   ↓
6. ✅ App is live!
```

**Total time:** 5-10 minutes

---

## 🛠️ Troubleshooting

### Build fails on Render

**Check:**
1. Is build.sh executable? (Should be ✓)
2. Are all dependencies in requirements.txt?
3. Check Render build logs for specific errors

**Fix:**
```bash
# Make sure build.sh is executable
chmod +x backend/build.sh
git add backend/build.sh
git commit -m "Make build.sh executable"
git push
```

### Dependencies not installing

**Check build.sh output in Render logs:**
- Python version correct? (3.11.0)
- pip upgrading successfully?
- Any package conflicts?

### Directories not created

**build.sh already handles this:**
```bash
mkdir -p uploads
mkdir -p processed
mkdir -p logs
```

Should work automatically on Render!

---

## 📊 Comparison: With vs Without Build Scripts

### Without build.sh (Simple):
```yaml
buildCommand: pip install -r requirements.txt
```
❌ No directory creation  
❌ No dependency verification  
❌ No error handling  
❌ Hard to debug issues  

### With build.sh (Professional): ✅
```yaml
buildCommand: bash build.sh
```
✅ Creates all necessary directories  
✅ Verifies dependencies installed correctly  
✅ Better error messages  
✅ Easy to add future steps  
✅ Production-ready  

---

## ✅ Final Answer

**Do you need build.sh?** → **YES! (You have it ✓)**  
**Do you need deploy.sh?** → **NO! (render.yaml handles it ✓)**

Your current setup is **optimal for Render deployment**:
- ✓ render.yaml → Points to build.sh
- ✓ build.sh → Handles build process
- ✓ pre-deploy-check.sh → Validates before push
- ✓ Fully automated deployment

---

## 🚀 Quick Deploy Commands

**Before deploying:**
```bash
cd backend
bash pre-deploy-check.sh
```

**Deploy:**
```bash
cd /Users/srinathbegudem/Desktop/Lexsy
git add .
git commit -m "Deploy to production"
git push origin main
```

**Render automatically:**
- Detects the push
- Runs build.sh
- Deploys your app

**No manual build or deploy scripts needed!** ✅

---

## 📚 Additional Resources

- **Render Build Docs:** https://render.com/docs/builds
- **Render Deploy Docs:** https://render.com/docs/deploys
- **Python on Render:** https://render.com/docs/deploy-flask

---

## ✨ Your Setup is Production-Ready!

With `build.sh` and `render.yaml`:
- ✅ Automated deployments
- ✅ Proper directory setup
- ✅ Dependency verification
- ✅ Easy debugging
- ✅ Professional workflow

**You're ready to deploy!** 🚀

