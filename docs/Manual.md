# 📖 Complete Manual - From Setup to Deployment

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Frontend Development](#frontend-development)
4. [Backend Development](#backend-development)
5. [Integration](#integration)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## **Prerequisites**

### **What You Need Before Starting**

1. **A Mac Computer** (with macOS 10.15 or later)
2. **Internet Connection** (for downloading tools and deploying)
3. **2-4 hours** of focused time
4. **Basic knowledge** of terminal commands (we'll guide you!)

### **Software to Install**

#### **1. Homebrew** (Package Manager for Mac)
```bash
# Open Terminal (Cmd + Space, type "Terminal")
# Paste this command and press Enter:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Wait for it to finish (takes 2-3 minutes)
# Then verify it worked:
brew --version
# Should show: Homebrew 4.x.x
```

**What is Homebrew?** Think of it as an "App Store" for developer tools. It helps you install software easily from the terminal.

#### **2. Node.js** (For Frontend)
```bash
# Install Node.js:
brew install node

# Verify installation:
node --version
# Should show: v20.x.x

npm --version
# Should show: 10.x.x
```

**What is Node.js?** It's what lets you run JavaScript on your computer (not just in browsers). npm is the "App Store" for JavaScript packages.

#### **3. Python 3.11** (For Backend)
```bash
# Install Python:
brew install python@3.11

# Verify installation:
python3 --version
# Should show: Python 3.11.x

pip3 --version
# Should show: pip 23.x.x
```

**What is Python?** A programming language. We use it for the backend (server) part of our app.

#### **4. Git** (Version Control)
```bash
# Usually pre-installed on Mac, verify:
git --version
# Should show: git version 2.x.x

# If not installed:
brew install git
```

**What is Git?** It tracks changes to your code, like "Track Changes" in Word, but for code.

#### **5. Code Editor - Cursor**

1. Go to https://cursor.sh
2. Download Cursor for Mac
3. Install it (drag to Applications folder)
4. Open Cursor

**What is Cursor?** It's like VS Code (a code editor) but with built-in AI to help you write code faster.

---

## **Project Setup**

### **Step 1: Create Project Folder**

```bash
# Open Terminal
# Go to your Desktop:
cd ~/Desktop

# Create project folder:
mkdir lexsy-assignment

# Go into it:
cd lexsy-assignment

# Create frontend and backend folders:
mkdir frontend backend docs

# Verify structure:
ls -l
# Should show: frontend, backend, docs folders
```

**What we just did:** Created a folder on your Desktop called "lexsy-assignment" with three sub-folders for organizing our code.

### **Step 2: Initialize Git Repository**

```bash
# Make sure you're in lexsy-assignment folder:
pwd
# Should show: /Users/yourname/Desktop/lexsy-assignment

# Initialize Git:
git init

# Verify:
ls -la
# Should see a .git folder (might be hidden)
```

**What we just did:** Told Git to start tracking changes in this folder.

### **Step 3: Create GitHub Repository**

1. Go to https://github.com
2. Log in (or create account if you don't have one)
3. Click the **"+"** button (top right) → **"New repository"**
4. Repository name: `lexsy-doc-automation`
5. Description: "AI-powered legal document automation for Lexsy"
6. Make it **Public**
7. **Don't** check any boxes (no README, no .gitignore yet)
8. Click **"Create repository"**

9. You'll see a page with commands. Copy the "push an existing repository" section:
```bash
git remote add origin https://github.com/YOUR_USERNAME/lexsy-doc-automation.git
git branch -M main
```

10. Run those commands in your Terminal (make sure you're still in lexsy-assignment folder)

**What we just did:** Created a place on GitHub to store and share our code.

---

## **Frontend Development**

### **Step 1: Create Next.js App**

```bash
# Go to frontend folder:
cd frontend

# Create Next.js app with TypeScript and Tailwind:
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*"

# Answer the prompts:
# ✔ Would you like to use ESLint? › Yes
# ✔ Would you like to use App Router? › Yes
# ✔ Would you like to customize the default import alias? › No

# This takes 2-3 minutes
```

**What we just did:** Created a new Next.js project with TypeScript and Tailwind CSS pre-configured.

**What is Next.js?** A React framework that makes building web apps easier. It's what companies like Netflix and TikTok use.

### **Step 2: Install shadcn/ui**

```bash
# Make sure you're in frontend folder:
pwd
# Should show: .../lexsy-assignment/frontend

# Initialize shadcn/ui:
npx shadcn-ui@latest init

# Answer prompts:
# ✔ Which style would you like to use? › Default
# ✔ Which color would you like to use as base color? › Slate
# ✔ Where is your global CSS file? › app/globals.css
# ✔ Would you like to use CSS variables for colors? › Yes
# ✔ Are you using a custom tailwind prefix? › No
# ✔ Where is your tailwind.config.js? › tailwind.config.ts
# ✔ Configure the import alias for components? › @/components
# ✔ Configure the import alias for utils? › @/lib/utils
# ✔ Are you using React Server Components? › Yes
```

**What we just did:** Set up a component library that gives us beautiful, pre-built UI components.

### **Step 3: Add Components**

```bash
# Add the components we'll need:
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add scroll-area

# Each command takes a few seconds
```

**What we just did:** Downloaded pre-built, customizable components (buttons, cards, inputs, etc.) into our project.

### **Step 4: Install Additional Packages**

```bash
# Still in frontend folder, install these:
npm install framer-motion lucide-react

# framer-motion: for animations
# lucide-react: for icons
```

### **Step 5: Test Frontend**

```bash
# Start development server:
npm run dev

# You should see:
# ✓ Ready in 2.3s
# ○ Local: http://localhost:3000

# Open your browser to: http://localhost:3000
# You should see the default Next.js page
```

**Stop the server:** Press `Ctrl + C` in terminal

**What we just did:** Verified that Next.js is working correctly.

### **Step 6: Project Structure**

Your frontend folder should now look like this:
```
frontend/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   └── ui/
│       ├── button.tsx
│       ├── card.tsx
│       └── ... (other components)
├── lib/
│   └── utils.ts
├── node_modules/
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## **Backend Development**

### **Step 1: Create Python Virtual Environment**

```bash
# Go to backend folder:
cd ../backend
# (We're now in .../lexsy-assignment/backend)

# Create virtual environment:
python3 -m venv venv

# Activate it:
source venv/bin/activate

# You should see (venv) at the start of your terminal prompt
```

**What is a virtual environment?** Like a separate "workspace" for Python packages, so they don't interfere with other projects.

### **Step 2: Install Python Packages**

```bash
# Make sure venv is activated (you should see (venv) in prompt)

# Upgrade pip first:
pip install --upgrade pip

# Install packages:
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install python-docx==1.1.0
pip install groq==0.4.1
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0

# For development/testing:
pip install pytest==7.4.3
pip install pytest-flask==1.3.0

# Save to requirements.txt:
pip freeze > requirements.txt
```

### **Step 3: Get Groq API Key (FREE)**

1. **Open browser** and go to: https://console.groq.com
2. **Sign up** using your Google account (fastest)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**
5. Give it a name: "Lexsy Assignment"
6. Click **"Submit"**
7. **Copy the key** (starts with `gsk_...`)
8. Save it somewhere safe temporarily

**What is Groq?** A company that provides FREE AI models. We'll use their AI to power the conversational interface.

### **Step 4: Create Environment File**

```bash
# Still in backend folder, create .env file:
touch .env

# Open it in Cursor:
cursor .env

# Or use nano:
nano .env
```

**Add this content** (paste your actual Groq API key):
```bash
# AI Provider (FREE)
GROQ_API_KEY=gsk_paste_your_actual_key_here

# Flask Configuration
SECRET_KEY=your-super-secret-random-string-12345
FLASK_ENV=development

# CORS (frontend URL)
CORS_ORIGIN=http://localhost:3000

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed
```

**Save and close** (if using nano: Ctrl+X, then Y, then Enter)

### **Step 5: Create Folders**

```bash
# Create necessary folders:
mkdir services
mkdir uploads
mkdir processed
mkdir tests

# Create __init__.py files:
touch services/__init__.py
touch tests/__init__.py
```

### **Step 6: Backend Structure**

Your backend folder should now look like this:
```
backend/
├── venv/
├── services/
│   └── __init__.py
├── uploads/
├── processed/
├── tests/
│   └── __init__.py
├── .env
├── requirements.txt
└── (we'll create app.py and service files next)
```

---

## **Integration**

### **Step 1: Connect Frontend to Backend**

**Create `.env.local` in frontend folder:**

```bash
# Go to frontend folder:
cd ../frontend

# Create environment file:
touch .env.local

# Open it:
cursor .env.local
```

**Add this:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_NAME=Lexsy Doc Automation
NEXT_PUBLIC_MAX_FILE_SIZE=10485760
```

**What this does:** Tells the frontend where to find the backend API.

### **Step 2: Create API Client**

**Create `lib/api.ts` in frontend:**

```bash
# In frontend folder:
mkdir -p lib
touch lib/api.ts
```

**Open `lib/api.ts` and add:**
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append('document', file);
  
  const response = await fetch(`${API_URL}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Upload failed');
  }
  
  return response.json();
}

export async function sendMessage(message: string, sessionId: string) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to send message');
  }
  
  return response.json();
}

// Add more API functions as needed...
```

**What this does:** Creates functions to communicate with the backend.

---

## **Testing**

### **Test Frontend**

```bash
# In frontend folder:
npm run dev

# Open: http://localhost:3000
# Should see your app running
```

### **Test Backend**

```bash
# In backend folder (in a NEW terminal tab):
cd backend
source venv/bin/activate
python app.py

# Should see:
# * Running on http://127.0.0.1:5000
```

### **Test Integration**

With both frontend and backend running:
1. Open http://localhost:3000 in browser
2. Try uploading a document
3. Check if it communicates with backend
4. Look at terminal outputs for errors

---

## **Deployment**

### **Part 1: Deploy Frontend to Vercel**

#### **Step 1: Prepare Frontend**

```bash
# In frontend folder:
cd frontend

# Build to check for errors:
npm run build

# If build succeeds, you're ready!
```

#### **Step 2: Deploy to Vercel**

**Option A: Using Vercel CLI (Recommended)**

```bash
# Install Vercel CLI:
npm install -g vercel

# Login:
vercel login
# Follow the prompts

# Deploy:
vercel --prod

# Answer prompts:
# ? Set up and deploy "~/Desktop/lexsy-assignment/frontend"? › Yes
# ? Which scope? › Your Account
# ? Link to existing project? › No
# ? What's your project's name? › lexsy-doc-automation
# ? In which directory is your code located? › ./
# ? Want to override the settings? › No

# Wait 2-3 minutes for deployment
# You'll get a URL: https://lexsy-doc-automation.vercel.app
```

**Option B: Using Vercel Website**

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Configure:
   - Framework Preset: Next.js
   - Root Directory: frontend
   - Build Command: (auto-detected)
   - Output Directory: (auto-detected)
6. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL` = (we'll add this after backend is deployed)
7. Click "Deploy"

#### **Step 3: Save Frontend URL**

Copy your frontend URL. It will look like:
```
https://lexsy-doc-automation.vercel.app
```

We'll need this for the backend CORS configuration.

---

### **Part 2: Deploy Backend to Render**

#### **Step 1: Prepare Backend**

```bash
# In backend folder:
cd ../backend

# Create .gitignore:
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
uploads/
processed/
*.log
EOF

# Verify requirements.txt exists:
cat requirements.txt
# Should list all packages
```

#### **Step 2: Push to GitHub**

```bash
# Go to root folder:
cd ..

# Add all files:
git add .

# Commit:
git commit -m "Initial commit: Legal document automation"

# Push to GitHub:
git push -u origin main

# Enter GitHub credentials if prompted
```

#### **Step 3: Deploy on Render**

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: lexsy-backend
   - **Region**: Choose closest to you
   - **Branch**: main
   - **Root Directory**: backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free

6. **Environment Variables** (click "Advanced"):
   ```
   GROQ_API_KEY = gsk_your_actual_key
   SECRET_KEY = random-string-12345
   FLASK_ENV = production
   CORS_ORIGIN = https://lexsy-doc-automation.vercel.app
   ```
   (Use your actual frontend URL for CORS_ORIGIN)

7. Click "Create Web Service"

8. Wait 10-15 minutes for deployment

9. You'll get a URL like:
   ```
   https://lexsy-backend.onrender.com
   ```

#### **Step 4: Update Frontend with Backend URL**

1. Go back to Vercel
2. Go to your project
3. Click "Settings" → "Environment Variables"
4. Update `NEXT_PUBLIC_API_URL`:
   ```
   NEXT_PUBLIC_API_URL = https://lexsy-backend.onrender.com
   ```
5. Redeploy frontend:
   ```bash
   vercel --prod
   ```

---

## **Final Testing**

### **Test Deployed App**

1. Go to your frontend URL: `https://lexsy-doc-automation.vercel.app`
2. Upload a test document
3. Complete the conversation flow
4. Download the completed document

**If everything works: Congratulations! You're done!** 🎉

---

## **Troubleshooting**

### **Problem: "Port 5000 already in use"**

**On Mac, AirPlay uses port 5000. Solutions:**

**Option 1:** Disable AirPlay Receiver
1. System Preferences → Sharing
2. Uncheck "AirPlay Receiver"

**Option 2:** Use different port
```bash
export PORT=8000
python app.py
```

### **Problem: "Module not found"**

**Solution:**
```bash
# Make sure virtual environment is activated:
source venv/bin/activate

# Reinstall packages:
pip install -r requirements.txt
```

### **Problem: "CORS error in browser"**

**Solution:**
Check backend .env has correct CORS_ORIGIN:
```bash
CORS_ORIGIN=http://localhost:3000
# or for production:
CORS_ORIGIN=https://your-frontend.vercel.app
```

### **Problem: "Vercel build fails"**

**Solution:**
1. Check `package.json` has all dependencies
2. Run `npm run build` locally first
3. Fix any TypeScript errors
4. Push changes and redeploy

### **Problem: "Render deployment fails"**

**Solution:**
1. Check Render logs (Dashboard → Logs tab)
2. Verify `requirements.txt` is correct
3. Check environment variables are set
4. Verify start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### **Problem: "API key not working"**

**Solution:**
1. Verify Groq API key is correct (starts with `gsk_`)
2. Check it's set in environment variables
3. Try generating a new key at console.groq.com

### **Problem: "Can't find python3"**

**Solution:**
```bash
# Create alias:
echo "alias python=python3" >> ~/.zshrc
echo "alias pip=pip3" >> ~/.zshrc
source ~/.zshrc
```

---

## **Checklist Before Submission**

### **Functionality**
- [ ] Can upload .docx files
- [ ] Placeholders are detected
- [ ] AI conversation works
- [ ] All field types validate correctly
- [ ] Preview shows filled/unfilled
- [ ] Download produces valid .docx
- [ ] Mobile responsive
- [ ] No console errors

### **Code Quality**
- [ ] Code is on GitHub
- [ ] README.md exists
- [ ] Environment variables not committed
- [ ] No TODO or console.log statements
- [ ] TypeScript types defined
- [ ] Comments added where needed

### **Deployment**
- [ ] Frontend deployed on Vercel
- [ ] Backend deployed on Render
- [ ] Both URLs working
- [ ] Environment variables set
- [ ] HTTPS working
- [ ] CORS configured correctly

### **Documentation**
- [ ] README has setup instructions
- [ ] README has deployed URLs
- [ ] Screenshots included (optional)
- [ ] Loom video recorded (2 min)

---

## **Timeline**

**Hour 1: Setup**
- Install prerequisites
- Create project structure
- Initialize frontend
- Initialize backend

**Hour 2-3: Development**
- Build upload component
- Create chat interface
- Implement backend logic
- Connect frontend to backend

**Hour 4: Polish**
- Improve UI/UX
- Add animations
- Test everything
- Fix bugs

**Hour 5: Deploy**
- Deploy frontend
- Deploy backend
- Test deployed version
- Update documentation

**Hour 6: Final**
- Record Loom video
- Write submission email
- Submit application

---

## **Getting Help**

If you get stuck:

1. **Read error messages carefully** - they usually tell you what's wrong
2. **Check the docs** in this repository
3. **Google the error** - someone has probably had the same issue
4. **Check Render/Vercel logs** - they show what went wrong during deployment

---

**You're ready to build! Good luck! 🚀**

*Remember: The goal is a working application that demonstrates your skills. Focus on functionality first, then make it look great!*