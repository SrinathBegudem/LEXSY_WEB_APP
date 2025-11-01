## Lexsy Deployment Guide (Vercel + Render)

This guide gets your project deployed with:
- Frontend (Next.js) → Vercel
- Backend (Flask) → Render

Follow the steps exactly and copy the provided environment variable templates.

---

### 1) Prerequisites
- GitHub repository connected with this code
- Accounts on Vercel and Render
- Optional: Firebase project for Google Auth (see `FIREBASE_SETUP_GUIDE.md`)

---

### 2) Backend on Render (Flask)

1. Push latest code to GitHub.
2. In Render, click “New +” → “Web Service”.
3. Connect your repo.
4. Set these options:
   - Root Directory: `backend`
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app`
5. Add Environment Variables (see copy-paste below). You can start with just `SECRET_KEY` and `CORS_ORIGINS` and add others as you need.
6. Deploy. Note your Render URL, e.g. `https://lexsy-backend.onrender.com`.

Recommended networking/CORS on Render:
- Set `CORS_ORIGINS` to your Vercel domain once the frontend is deployed
- Or temporarily set `CORS_ALLOW_ALL=true` during initial testing

Health check: `GET https://<your-render-url>/api/health`

---

### 3) Frontend on Vercel (Next.js)

1. In Vercel, “Add New Project” → import the `frontend` directory from your repo.
2. Framework is auto-detected (Next.js). No custom build settings required.
3. Add Environment Variables (below). The most important is `NEXT_PUBLIC_API_URL` pointing to your Render backend.
4. Deploy.

After the first deploy, update `CORS_ORIGINS` on Render to include your final Vercel domain (e.g., `https://lexsy-1234.vercel.app`). Redeploy if needed.

---

### 4) Environment Variables (Copy-Paste)

Create `backend/.env` locally (or use Render dashboard):

```env
# Flask / Server
FLASK_ENV=production
PORT=5001
SECRET_KEY=replace_with_strong_random_value
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed

# CORS (recommended: restrict to your Vercel domain)
CORS_ALLOW_ALL=false
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# AI Provider (optional; enables real Groq responses)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

# Firebase Admin (optional; enables token verification)
# If the JSON is in the backend folder on Render, use the absolute path Render assigns.
FIREBASE_SERVICE_ACCOUNT=/opt/render/project/src/backend/firebase-service-account.json

# Redis (optional; improves session persistence)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
SESSION_TIMEOUT_HOURS=168
```

Create `frontend/.env.local` (or use Vercel dashboard):

```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com

# Optional if you move Firebase config to env vars
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

Tip: You can test locally with:
- Backend: `cd backend && python app.py` (uses `PORT` from `.env`, default 5001)
- Frontend: `cd frontend && npm run dev` (`NEXT_PUBLIC_API_URL` should point to the backend)

---

### 5) Post-Deploy Checklist
- Backend health endpoint returns `200 OK`
- Upload works from Vercel to Render (if not, double-check CORS settings and `NEXT_PUBLIC_API_URL`)
- If using Firebase Auth, verify sign-in works and the token is sent in requests

---

### 6) Troubleshooting
- Upload fails on Vercel: ensure `CORS_ORIGINS` includes your exact Vercel domain and that `NEXT_PUBLIC_API_URL` uses `https://`.
- 403 CORS error: confirm your Origin matches one of `CORS_ORIGINS` exactly. You may temporarily set `CORS_ALLOW_ALL=true` to validate.
- 502/Timeout on Render free tier: try again or upgrade plan; ensure `gunicorn` command is used.

For deeper setup info, see `FIREBASE_SETUP_GUIDE.md` and `PORT_CONFIG.md`.


