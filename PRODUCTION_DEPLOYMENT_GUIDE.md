# 🚀 Lexsy Production Deployment Guide

Complete step-by-step guide to deploy Lexsy to production.

**Frontend:** Vercel  
**Backend:** Render  
**Database/Cache:** Render Redis (optional)

---

## 📋 Pre-Deployment Checklist

### ✅ Required Accounts
- [ ] Vercel account (free tier available) - https://vercel.com
- [ ] Render account (free tier available) - https://render.com
- [ ] GitHub/GitLab account (for repository)
- [ ] Groq API key - https://console.groq.com
- [ ] Firebase project (for authentication) - https://console.firebase.google.com

### ✅ Required Files (Already Created)
- [x] `frontend/vercel.json` - Vercel configuration
- [x] `frontend/.vercelignore` - Files to exclude from Vercel
- [x] `render.yaml` - Render configuration
- [x] `backend/requirements.txt` - Python dependencies
- [x] Frontend builds successfully ✓

---

## Part 1: Backend Deployment (Render)

### Step 1: Prepare Backend

1. **Verify requirements.txt has all dependencies:**
   ```bash
   cd backend
   cat requirements.txt
   ```
   
   Should include:
   - flask
   - flask-cors
   - gunicorn
   - groq
   - python-docx
   - firebase-admin
   - redis (optional)

2. **Generate SECRET_KEY:**
   ```bash
   cd backend
   python generate_secret_key.py
   ```
   
   **Copy the generated SECRET_KEY** - you'll need it later!

### Step 2: Push to GitHub

If not already done:

```bash
cd /Users/srinathbegudem/Desktop/Lexsy

# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit - ready for production"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/lexsy.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. **Go to Render Dashboard:**
   - Visit https://dashboard.render.com
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Select **"Build and deploy from a Git repository"**
   - Click **"Connect" next to your GitHub account**
   - Find and select your **lexsy** repository
   - Click **"Connect"**

3. **Configure Service:**
   
   **Basic Settings:**
   - **Name:** `lexsy-backend`
   - **Region:** Ohio (US East) - or closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --worker-class gthread --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT app:app`

   **Plan:**
   - Select **Free** (or paid plan for better performance)

4. **Set Environment Variables:**
   
   Click **"Advanced"** → **"Add Environment Variable"**
   
   Add these (one by one):
   
   ```
   FLASK_ENV=production
   PYTHON_VERSION=3.11.0
   PORT=10000
   
   # REQUIRED - Replace with your actual values
   SECRET_KEY=<paste the key you generated earlier>
   GROQ_API_KEY=<your Groq API key from console.groq.com>
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   
   # Firebase (if using authentication)
   FIREBASE_TYPE=service_account
   FIREBASE_PROJECT_ID=<your-firebase-project-id>
   FIREBASE_PRIVATE_KEY_ID=<your-private-key-id>
   FIREBASE_PRIVATE_KEY=<your-private-key>
   FIREBASE_CLIENT_EMAIL=<your-client-email>
   FIREBASE_CLIENT_ID=<your-client-id>
   FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
   FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
   FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   FIREBASE_CLIENT_X509_CERT_URL=<your-cert-url>
   
   # Optional - If using Redis for sessions
   REDIS_URL=<your-render-redis-url>
   ```

   **⚠️ Important Notes:**
   - Never commit these secrets to git!
   - For `FIREBASE_PRIVATE_KEY`, keep the `\n` characters as-is
   - `CORS_ORIGINS` will be updated later with your Vercel URL

5. **Deploy:**
   - Click **"Create Web Service"**
   - Render will start building and deploying
   - Wait 5-10 minutes for first deployment
   - You'll get a URL like: `https://lexsy-backend.onrender.com`

6. **Verify Backend is Running:**
   ```bash
   curl https://lexsy-backend.onrender.com/api/health
   ```
   
   Should return:
   ```json
   {"status": "healthy"}
   ```

### Step 4: (Optional) Add Redis for Session Management

1. In Render Dashboard:
   - Click **"New +"** → **"Redis"**
   - Name: `lexsy-redis`
   - Plan: Free or paid
   - Click **"Create Redis"**

2. Copy the **Internal Redis URL**

3. Go back to your web service:
   - Settings → Environment
   - Add: `REDIS_URL=<paste-internal-redis-url>`
   - Save Changes

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Environment Variables

Have these ready from your `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://lexsy-backend.onrender.com
NEXT_PUBLIC_FIREBASE_API_KEY=<your-firebase-api-key>
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=<your-project>.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=<your-project-id>
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=<your-project>.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=<your-sender-id>
NEXT_PUBLIC_FIREBASE_APP_ID=<your-app-id>
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=<your-measurement-id>
```

### Step 2: Deploy to Vercel

**Option A: Using Vercel CLI (Recommended)**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy Frontend:**
   ```bash
   cd /Users/srinathbegudem/Desktop/Lexsy/frontend
   vercel
   ```
   
   Follow the prompts:
   - **Set up and deploy?** Y
   - **Which scope?** Select your account
   - **Link to existing project?** N
   - **Project name?** lexsy (or your preferred name)
   - **Directory?** `./` (current)
   - **Override settings?** N

4. **Add Environment Variables:**
   ```bash
   vercel env add NEXT_PUBLIC_API_URL production
   # Paste: https://lexsy-backend.onrender.com
   
   vercel env add NEXT_PUBLIC_FIREBASE_API_KEY production
   # Paste your Firebase API key
   
   # Repeat for all Firebase environment variables...
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

**Option B: Using Vercel Dashboard**

1. **Go to Vercel:**
   - Visit https://vercel.com/dashboard
   - Click **"Add New..."** → **"Project"**

2. **Import Repository:**
   - Click **"Import Git Repository"**
   - Select your **lexsy** repository
   - Click **"Import"**

3. **Configure Project:**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (auto)
   - **Output Directory:** `.next` (auto)
   - **Install Command:** `npm install` (auto)

4. **Add Environment Variables:**
   
   Click **"Environment Variables"** and add:
   
   ```
   NEXT_PUBLIC_API_URL=https://lexsy-backend.onrender.com
   NEXT_PUBLIC_FIREBASE_API_KEY=<your-key>
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=<your-domain>
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=<your-id>
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=<your-bucket>
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=<your-sender-id>
   NEXT_PUBLIC_FIREBASE_APP_ID=<your-app-id>
   NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=<your-measurement-id>
   ```
   
   Make sure to select **"Production"** environment for each!

5. **Deploy:**
   - Click **"Deploy"**
   - Wait 2-3 minutes
   - You'll get a URL like: `https://lexsy-abc123.vercel.app`

### Step 3: Update Backend CORS

Now that you have your Vercel URL:

1. Go to **Render Dashboard**
2. Select your **lexsy-backend** service
3. Go to **Environment**
4. Find `CORS_ORIGINS` and update it:
   ```
   CORS_ORIGINS=https://your-actual-url.vercel.app
   ```
5. **Save Changes**
6. Render will automatically redeploy

---

## Part 3: Post-Deployment Configuration

### Step 1: Configure Firebase

1. **Add Authorized Domains:**
   - Go to Firebase Console
   - Select your project
   - **Authentication** → **Settings** → **Authorized domains**
   - Add your Vercel domain: `your-app.vercel.app`
   - Click **"Add domain"**

### Step 2: Test the Deployment

1. **Visit your Vercel URL:**
   ```
   https://your-app.vercel.app
   ```

2. **Test Authentication:**
   - Click **"Sign in with Google"**
   - Should redirect to Google OAuth
   - After signing in, should return to your app

3. **Test Document Upload:**
   - Upload a SAFE.docx document
   - Fill in a few fields
   - Check if AI Assistant works
   - Complete and download the document

4. **Check Backend Health:**
   ```bash
   curl https://lexsy-backend.onrender.com/api/health
   ```

### Step 3: Monitor Your Apps

**Vercel:**
- Dashboard: https://vercel.com/dashboard
- View deployment logs
- Check performance metrics
- Monitor errors

**Render:**
- Dashboard: https://dashboard.render.com
- View service logs
- Check resource usage
- Monitor uptime

---

## 🔧 Troubleshooting

### Issue: "CORS Error" in browser console

**Solution:**
1. Check `CORS_ORIGINS` in Render includes your exact Vercel URL
2. Make sure there are no trailing slashes
3. Restart the backend service after updating

### Issue: "Firebase Authentication Failed"

**Solution:**
1. Verify all Firebase env vars are set correctly in Vercel
2. Check Firebase authorized domains include your Vercel domain
3. Verify Firebase API key is correct

### Issue: "Backend not responding"

**Solution:**
1. Check Render service logs for errors
2. Verify `GROQ_API_KEY` is set correctly
3. Check health endpoint: `/api/health`
4. Free tier spins down after inactivity - first request takes 30-60s

### Issue: "Document upload fails"

**Solution:**
1. Check backend logs for errors
2. Verify `SECRET_KEY` is set
3. Check file size limits (10MB max)
4. Ensure `uploads/` and `processed/` folders are created automatically

### Issue: "Build fails on Vercel"

**Solution:**
1. Check TypeScript errors: `npm run type-check`
2. Verify all dependencies are in `package.json`
3. Check Node version compatibility (14.x or higher)

---

## 📊 Performance Optimization

### Vercel (Frontend)

1. **Enable Vercel Analytics:**
   ```bash
   npm install @vercel/analytics
   ```
   
   Add to `app/layout.tsx`:
   ```tsx
   import { Analytics } from '@vercel/analytics/react';
   
   export default function RootLayout({ children }) {
     return (
       <html>
         <body>
           {children}
           <Analytics />
         </body>
       </html>
     );
   }
   ```

2. **Enable Caching:**
   - Vercel automatically caches static assets
   - Configure in `vercel.json` if needed

### Render (Backend)

1. **Upgrade Plan:**
   - Free tier spins down after 15 min inactivity
   - Paid plan ($7/mo) keeps service always running
   - Better for production use

2. **Enable Persistent Disk:**
   - For storing uploaded documents longer
   - Add in Render Dashboard under service settings

3. **Scale Workers:**
   - Increase workers/threads in start command
   - Example: `--workers 4 --threads 8`

---

## 🔒 Security Checklist

- [ ] SECRET_KEY is strong (64+ characters)
- [ ] All API keys stored as environment variables
- [ ] Never commit .env files to git
- [ ] CORS configured to only allow your frontend domain
- [ ] Firebase security rules are properly configured
- [ ] HTTPS enforced on both frontend and backend
- [ ] Rate limiting enabled (if using paid tier)
- [ ] Regular security updates for dependencies

---

## 💰 Cost Estimate

### Free Tier (Good for MVP/Testing)

**Vercel:**
- Hosting: Free
- Bandwidth: 100GB/month
- Builds: 100 hours/month
- **Cost: $0/month**

**Render:**
- Web Service: Free (spins down after 15 min)
- Redis: Free (25MB)
- Bandwidth: Limited
- **Cost: $0/month**

**Total: $0/month** ✅

### Production Tier (Recommended)

**Vercel Pro:**
- Unlimited bandwidth
- Priority builds
- Advanced analytics
- **Cost: $20/month**

**Render Starter:**
- Always-on service
- 512MB RAM
- 0.5 CPU
- **Cost: $7/month**

**Render Redis:**
- 256MB RAM
- **Cost: $10/month**

**Total: $37/month**

---

## 🎯 Quick Start Summary

### 1. Backend (Render)
```bash
# Push to GitHub
git push origin main

# Deploy on Render
# 1. Connect GitHub repo
# 2. Set root dir to 'backend'
# 3. Add environment variables
# 4. Click Deploy
```

### 2. Frontend (Vercel)
```bash
# CLI deploy
cd frontend
vercel --prod

# Or use Vercel Dashboard
# 1. Import GitHub repo
# 2. Set root dir to 'frontend'
# 3. Add environment variables
# 4. Click Deploy
```

### 3. Update CORS
```
# In Render, update CORS_ORIGINS with Vercel URL
CORS_ORIGINS=https://your-app.vercel.app
```

### 4. Test
```
# Visit your app
https://your-app.vercel.app

# Test health endpoint
curl https://lexsy-backend.onrender.com/api/health
```

---

## 📚 Useful Links

- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **Next.js Deploy Guide:** https://nextjs.org/docs/deployment
- **Flask on Render:** https://render.com/docs/deploy-flask
- **Vercel CLI:** https://vercel.com/docs/cli

---

## 🆘 Support

If you encounter issues:

1. Check service logs (Vercel/Render dashboards)
2. Verify environment variables are set correctly
3. Test API endpoints directly with curl
4. Check Firebase console for auth errors
5. Review this guide's troubleshooting section

---

## ✅ Deployment Complete!

Your Lexsy app is now live in production! 🎉

- **Frontend:** https://your-app.vercel.app
- **Backend:** https://lexsy-backend.onrender.com
- **Status:** Production-ready with all features working

**Next Steps:**
- Set up custom domain (optional)
- Enable monitoring and alerts
- Configure automatic deployments
- Set up CI/CD pipeline
- Add analytics and tracking

Good luck with your launch! 🚀

