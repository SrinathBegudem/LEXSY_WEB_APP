# Vercel Deployment Configuration

## ⚙️ Required Vercel Project Settings

Your Next.js app is in the `frontend/` subdirectory. You MUST configure Vercel to use this as the root:

### Steps to Configure:

1. Go to your Vercel project: https://vercel.com/dashboard
2. Select your `lexsy-web-app` project
3. Go to **Settings** → **General**
4. Find **"Root Directory"** section
5. Click **"Edit"**
6. Set Root Directory to: `frontend`
7. Click **"Save"**
8. **Redeploy** your project

### Environment Variables

Make sure these are set in Vercel Settings → Environment Variables:

#### Required:
- `NEXT_PUBLIC_API_URL` - Your Render backend URL (e.g., `https://lexsy-backend.onrender.com`)

#### Firebase (Required):
- `NEXT_PUBLIC_FIREBASE_API_KEY`
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID`
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`
- `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`
- `NEXT_PUBLIC_FIREBASE_APP_ID`
- `NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID`

## 🔄 After Configuration

After setting the Root Directory to `frontend`, Vercel will:
- ✅ Automatically detect Next.js
- ✅ Use the correct build commands
- ✅ Properly route all pages
- ✅ Serve your app from the root URL (not /frontend)

## 🚀 Deploy

After making these changes:
```bash
git add .
git commit -m "Update Vercel configuration"
git push
```

Vercel will automatically redeploy with the correct settings.

