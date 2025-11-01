# 🚀 Render Deployment - Environment Variables Setup Guide

## Quick Start

Your Vercel frontend is deployed at: **https://lexsy-web-app.vercel.app/**

Now set up your Render backend environment variables to connect everything together.

---

## 📋 Step-by-Step Setup

### 1. Go to Render Dashboard
- Navigate to: https://dashboard.render.com
- Open your **lexsy-backend** service
- Go to **Settings** → **Environment**

### 2. Add These REQUIRED Variables

Copy and paste these variables one by one into Render:

#### 🔒 Flask Configuration
```
FLASK_ENV=production
PORT=10000
```

#### 🔑 Secret Key (Generate a NEW one!)

**Choose one of these methods:**

**Method 1 - Node.js:**
```bash
node -e "const crypto = require('crypto'); console.log(crypto.randomBytes(32).toString('hex'))"
```

**Method 2 - Anaconda Python:**
```bash
/opt/anaconda3/bin/python -c "import secrets; print(secrets.token_hex(32))"
```

**Method 3 - Online Generator:**
Visit: https://randomkeygen.com/

Then add:
```
SECRET_KEY=<paste_your_generated_key_here>
```

**⚠️ IMPORTANT:** Generate a NEW secret key for production. Don't use the development one!

#### 🌐 CORS Configuration (Your Frontend URL)
```
CORS_ORIGINS=https://lexsy-web-app.vercel.app,https://www.lexsy-web-app.vercel.app
```

This allows your Vercel frontend to make API calls to Render backend.

#### 🤖 AI Service (Groq API)
```
GROQ_API_KEY=your_groq_api_key_here
```

---

### 3. Optional But Recommended

#### 📁 File Upload Settings (defaults work, but you can customize)
```
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed
```

#### 💾 Redis (Optional - for session management)
If you're using Redis on Render:
```
REDIS_URL=<your_redis_url_from_render>
```

Or configure manually:
```
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_password
```

---

### 4. Firebase Authentication Setup

Firebase requires uploading a **file**, not setting an environment variable:

1. Go to Render Dashboard → Your Service → Settings → **Environment Files**
2. Click **Add Environment File**
3. Name: `firebase-service-account.json`
4. Upload your `backend/firebase-service-account.json` file
5. Click **Save**

**Note:** Make sure your `firebase-service-account.json` file exists in your `backend/` directory before uploading.

---

## ✅ Complete Environment Variables List

Here's the complete list for easy copy-paste:

```
FLASK_ENV=production
PORT=10000
SECRET_KEY=<GENERATE_NEW_ONE>
CORS_ORIGINS=https://lexsy-web-app.vercel.app,https://www.lexsy-web-app.vercel.app
GROQ_API_KEY=your_groq_api_key_here
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed
```

---

## 🔄 After Adding Variables

1. Click **Save Changes**
2. Go to **Manual Deploy** → **Deploy latest commit**
3. Wait for deployment to complete
4. Check the logs to ensure everything starts correctly

---

## 🧪 Testing Your Deployment

Once deployed, test these endpoints:

1. **Health Check:**
   ```
   https://your-backend-url.onrender.com/api/health
   ```
   Should return: `{"status": "ok"}`

2. **CORS Test:**
   Open your Vercel frontend (https://lexsy-web-app.vercel.app/) and try uploading a document. It should connect to your Render backend.

---

## 🐛 Troubleshooting

### CORS Errors
- Make sure `CORS_ORIGINS` includes your exact Vercel URL (no trailing slash)
- Check both `https://lexsy-web-app.vercel.app` and `https://www.lexsy-web-app.vercel.app`

### Firebase Auth Not Working
- Verify `firebase-service-account.json` is uploaded as an environment file
- Check file path in logs (should be in backend/ directory)

### Secret Key Issues
- Generate a NEW secret key for production
- Must be at least 32 characters long
- Never commit secret keys to git

### Backend Not Starting
- Check Render logs for errors
- Verify all required environment variables are set
- Ensure PORT is set to 10000 (or let Render auto-set it)

---

## 📚 Additional Resources

- Render Docs: https://render.com/docs/environment-variables
- Groq API: https://console.groq.com/
- Vercel Deployment: https://lexsy-web-app.vercel.app/

---

## 🔐 Security Checklist

- [ ] SECRET_KEY is a newly generated random string (32+ chars)
- [ ] GROQ_API_KEY is set correctly
- [ ] CORS_ORIGINS only includes your frontend URLs
- [ ] firebase-service-account.json is uploaded (not in git)
- [ ] No sensitive keys are committed to git
- [ ] All environment variables marked as "Secret" in Render (optional but recommended)

---

**Need Help?** Check the logs in Render Dashboard → Your Service → Logs

