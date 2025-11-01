# ⚡ Deployment Quick Start

**5-minute guide to deploy Lexsy to production**

---

## 🎯 Prerequisites (5 minutes)

1. **Create Accounts:**
   - [ ] Vercel: https://vercel.com/signup
   - [ ] Render: https://dashboard.render.com/register
   - [ ] GitHub: https://github.com/join (if not done)

2. **Get API Keys:**
   - [ ] Groq API: https://console.groq.com → Create API Key
   - [ ] Firebase: Already set up ✓

3. **Generate SECRET_KEY:**
   ```bash
   cd backend
   python generate_secret_key.py
   ```
   Copy the output - you'll need it!

---

## 🚀 Deploy Backend to Render (10 minutes)

### Step 1: Push to GitHub
```bash
cd /Users/srinathbegudem/Desktop/Lexsy
git add .
git commit -m "Ready for production deployment"
git push origin main
```

### Step 2: Deploy on Render

1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. **Settings:**
   - Name: `lexsy-backend`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --worker-class gthread --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT app:app`

5. **Environment Variables** (click Add Environment Variable):
   ```
   FLASK_ENV=production
   SECRET_KEY=<paste your generated key>
   GROQ_API_KEY=<your Groq API key>
   CORS_ORIGINS=https://your-app.vercel.app
   ```
   
   Add Firebase vars (copy from your .env file):
   ```
   FIREBASE_TYPE=service_account
   FIREBASE_PROJECT_ID=<your-id>
   FIREBASE_PRIVATE_KEY_ID=<your-key-id>
   FIREBASE_PRIVATE_KEY=<your-key>
   FIREBASE_CLIENT_EMAIL=<your-email>
   FIREBASE_CLIENT_ID=<your-id>
   FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
   FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
   FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   FIREBASE_CLIENT_X509_CERT_URL=<your-url>
   ```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes
8. Note your backend URL: `https://lexsy-backend.onrender.com`

---

## 🌐 Deploy Frontend to Vercel (5 minutes)

### Option A: CLI (Fastest)
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod
```

### Option B: Dashboard
1. Go to: https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. **Settings:**
   - Root Directory: `frontend`
   - Framework: Next.js (auto-detected)

5. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://lexsy-backend.onrender.com
   NEXT_PUBLIC_FIREBASE_API_KEY=<from .env.local>
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=<from .env.local>
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=<from .env.local>
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=<from .env.local>
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=<from .env.local>
   NEXT_PUBLIC_FIREBASE_APP_ID=<from .env.local>
   NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=<from .env.local>
   ```

6. Click **"Deploy"**
7. Wait 2-3 minutes
8. Note your frontend URL: `https://your-app.vercel.app`

---

## 🔄 Update CORS (2 minutes)

1. Go back to **Render Dashboard**
2. Select **lexsy-backend**
3. Go to **Environment**
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-actual-vercel-url.vercel.app
   ```
5. Save (backend will auto-redeploy)

---

## ✅ Verify Deployment (2 minutes)

### 1. Test Backend
```bash
curl https://lexsy-backend.onrender.com/api/health
```
Should return: `{"status": "healthy"}`

### 2. Test Frontend
- Visit: `https://your-app.vercel.app`
- Click "Sign in with Google"
- Upload a test document
- Try the AI Assistant
- Complete and download

---

## 🎉 You're Live!

**Frontend:** https://your-app.vercel.app  
**Backend:** https://lexsy-backend.onrender.com

### Common Issues

**Issue:** CORS error in console  
**Fix:** Update `CORS_ORIGINS` in Render with exact Vercel URL

**Issue:** "Backend not responding"  
**Fix:** Free tier spins down - wait 30-60s for cold start

**Issue:** Firebase auth fails  
**Fix:** Add Vercel domain to Firebase authorized domains

---

## 📊 Free Tier Limits

**Vercel:**
- 100GB bandwidth/month
- 100 build hours/month
- Unlimited projects

**Render:**
- 750 hours/month (enough for 1 service)
- Spins down after 15 min inactivity
- 30-60s cold start time

**Upgrade:** $37/month for always-on production service

---

## 🔗 Quick Links

- Full Guide: `PRODUCTION_DEPLOYMENT_GUIDE.md`
- Vercel Dashboard: https://vercel.com/dashboard
- Render Dashboard: https://dashboard.render.com
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs

---

**Total Deployment Time: ~25 minutes** ⚡

Need help? Check the full deployment guide for detailed troubleshooting!

