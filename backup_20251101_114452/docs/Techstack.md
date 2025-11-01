# 🛠️ Technology Stack - Next.js + Flask

## **Overview**

Modern, production-ready stack using Next.js for frontend and Flask for backend, with FREE AI integration.

**Total Cost: $0/month** 💰

---

## **Frontend Stack**

### **Core Framework**
```json
{
  "framework": "Next.js 14",
  "language": "TypeScript 5.x",
  "runtime": "Node.js 20.x"
}
```

**Why Next.js?**
- ✅ Server-side rendering (SSR)
- ✅ Excellent performance
- ✅ Built-in optimization
- ✅ Great DX (Developer Experience)
- ✅ Free deployment on Vercel

### **UI Framework & Styling**

#### **Tailwind CSS 3.4**
```bash
npm install tailwindcss@latest postcss autoprefixer
```

**Features:**
- Utility-first CSS
- JIT compiler
- Responsive design
- Custom theme support
- Tiny production bundle

**Configuration:**
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#667eea',
        secondary: '#764ba2',
      },
    },
  },
  plugins: [],
}
```

#### **shadcn/ui**
```bash
npx shadcn-ui@latest init
```

**Components to Install:**
```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add scroll-area
```

**Why shadcn/ui?**
- ✅ Not an npm package (you own the code)
- ✅ Highly customizable
- ✅ Beautiful out of the box
- ✅ Accessible (Radix UI based)
- ✅ TypeScript support

### **Additional Libraries**

#### **Framer Motion**
```bash
npm install framer-motion
```
For smooth animations:
```typescript
const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3 }
};
```

#### **Lucide React**
```bash
npm install lucide-react
```
For beautiful icons:
```typescript
import { Upload, Download, Check } from 'lucide-react';
```

#### **React Hook Form**
```bash
npm install react-hook-form zod @hookform/resolvers
```
For form validation:
```typescript
const schema = z.object({
  companyName: z.string().min(1),
  date: z.string().regex(/^\d{2}\/\d{2}\/\d{4}$/),
});
```

### **Frontend Dependencies**
```json
{
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    "tailwindcss": "3.4.0",
    "framer-motion": "10.16.16",
    "lucide-react": "0.294.0",
    "react-hook-form": "7.49.2",
    "zod": "3.22.4",
    "@hookform/resolvers": "3.3.2",
    "class-variance-authority": "0.7.0",
    "clsx": "2.0.0",
    "tailwind-merge": "2.2.0"
  },
  "devDependencies": {
    "@types/node": "20.10.0",
    "@types/react": "18.2.42",
    "@types/react-dom": "18.2.17",
    "eslint": "8.55.0",
    "eslint-config-next": "14.0.4",
    "autoprefixer": "10.4.16",
    "postcss": "8.4.32"
  }
}
```

---

## **Backend Stack**

### **Core Framework**
```python
framework = "Flask 3.0.0"
language = "Python 3.11"
server = "Gunicorn 21.2.0"
```

**Why Flask?**
- ✅ Lightweight and flexible
- ✅ Easy to learn
- ✅ Great for APIs
- ✅ Huge ecosystem
- ✅ Fast development

### **Core Dependencies**

#### **Document Processing**
```bash
pip install python-docx==1.1.0
```
For reading and writing .docx files:
```python
from docx import Document
doc = Document('template.docx')
```

#### **AI Integration - Groq (FREE)**
```bash
pip install groq==0.4.1
```
For AI conversations:
```python
from groq import Groq
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7
)
```

**Why Groq?**
- ✅ Completely FREE
- ✅ Fast inference (< 1s)
- ✅ llama-3.1-70b model
- ✅ 30 requests/minute (enough for this project)
- ✅ No credit card required

**Alternative: Google Gemini (Also FREE)**
```bash
pip install google-generativeai==0.3.2
```

#### **Flask Extensions**
```bash
pip install Flask-CORS==4.0.0
```
For handling cross-origin requests:
```python
from flask_cors import CORS
CORS(app, origins=["http://localhost:3000"])
```

#### **Utilities**
```bash
pip install python-dotenv==1.0.0
pip install python-dateutil==2.8.2
pip install defusedxml==0.7.1
```

### **Backend Dependencies**
```text
# requirements.txt

# Core Framework
Flask==3.0.0
Flask-CORS==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0

# Document Processing
python-docx==1.1.0
python-dateutil==2.8.2
defusedxml==0.7.1

# AI Provider (Choose ONE or BOTH for fallback)
groq==0.4.1
google-generativeai==0.3.2

# Utilities
python-dotenv==1.0.0
requests==2.31.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-flask==1.3.0

# Optional: Code Quality
black==23.12.0
flake8==6.1.0
mypy==1.7.1
```

---

## **Development Tools**

### **Version Control**
```bash
Git 2.40+
GitHub
```

### **Package Managers**
```bash
npm 10.x      # Frontend
pip 23.x      # Backend
```

### **Code Editors**
```bash
# Recommended: Cursor (AI-powered VS Code fork)
# Alternative: VS Code with extensions:
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Python
- Pylance
- GitLens
```

### **Linting & Formatting**

**Frontend:**
```json
{
  "scripts": {
    "lint": "next lint",
    "format": "prettier --write ."
  }
}
```

**Backend:**
```bash
black .        # Format code
flake8 .       # Lint code
mypy .         # Type check
```

---

## **Deployment**

### **Frontend - Vercel (FREE)**

**Features:**
- ✅ Automatic deployments from Git
- ✅ Global CDN
- ✅ Zero config
- ✅ Analytics
- ✅ Free custom domains
- ✅ 100GB bandwidth/month

**Deploy Command:**
```bash
vercel --prod
```

**Build Settings:**
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install"
}
```

### **Backend - Render.com (FREE)**

**Features:**
- ✅ 750 hours/month free
- ✅ Automatic HTTPS
- ✅ Continuous deployment
- ✅ Environment variables
- ✅ Health checks

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
```

**render.yaml:**
```yaml
services:
  - type: web
    name: lexsy-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

---

## **Architecture Diagram**

```
┌─────────────────────────────────────────────────────┐
│                   User's Browser                    │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTPS
                     ↓
┌─────────────────────────────────────────────────────┐
│              Vercel CDN (Frontend)                  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │         Next.js 14 Application               │  │
│  │                                              │  │
│  │  • React Components                          │  │
│  │  • TypeScript                                │  │
│  │  • Tailwind CSS + shadcn/ui                  │  │
│  │  • Framer Motion                             │  │
│  │  • State Management (Context)                │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
                     │ REST API (HTTPS)
                     ↓
┌─────────────────────────────────────────────────────┐
│            Render.com (Backend)                     │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │           Flask 3.0 API Server               │  │
│  │                                              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │    Document Processor                │   │  │
│  │  │    • python-docx                     │   │  │
│  │  │    • Parse & generate DOCX           │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │    Placeholder Detector              │   │  │
│  │  │    • Regex patterns                  │   │  │
│  │  │    • Type inference                  │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │    AI Service                        │   │  │
│  │  │    • Conversation management         │   │  │
│  │  │    • Input validation                │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                                              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │    Session Store                     │   │  │
│  │  │    • In-memory (Redis optional)      │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTPS API Calls
                     ↓
┌─────────────────────────────────────────────────────┐
│               Groq API (External)                   │
│                                                     │
│  • Model: llama-3.1-70b-versatile                   │
│  • FREE Tier: 30 requests/minute                    │
│  • Response Time: ~1 second                         │
└─────────────────────────────────────────────────────┘
```

---

## **Data Flow**

### **1. Upload Flow**
```typescript
User → Next.js → Flask → python-docx → Response
1. User drops .docx file
2. Next.js validates file client-side
3. FormData sent to Flask /api/upload
4. python-docx parses document
5. Placeholder detector runs
6. Session created
7. Response with placeholders
8. Next.js displays chat interface
```

### **2. Chat Flow**
```typescript
User → Next.js → Flask → Groq API → Response
1. User types answer
2. Next.js sends to /api/chat
3. Flask validates input
4. Groq API generates next question
5. Response with next placeholder
6. Next.js updates UI
7. Repeat until all filled
```

### **3. Download Flow**
```typescript
User → Next.js → Flask → python-docx → File
1. User clicks download
2. Next.js calls /api/complete
3. Flask generates final document
4. python-docx replaces placeholders
5. File saved to /processed
6. Download URL returned
7. Next.js triggers download
```

---

## **Environment Variables**

### **Frontend (.env.local)**
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000
# or production:
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com

# App Configuration
NEXT_PUBLIC_APP_NAME=Lexsy Doc Automation
NEXT_PUBLIC_MAX_FILE_SIZE=10485760

# Optional: Analytics
# NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### **Backend (.env)**
```bash
# AI Provider (Get FREE key at console.groq.com)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_ENV=development

# CORS Configuration
CORS_ORIGIN=http://localhost:3000
# or production:
CORS_ORIGIN=https://your-frontend.vercel.app

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
PROCESSED_FOLDER=processed

# Optional: Backup AI Provider
# GOOGLE_API_KEY=AIza...

# Production
# PORT=5000
```

---

## **Performance Benchmarks**

### **Frontend**
```
First Load JS: ~200KB
Lighthouse Score: 95+
Time to Interactive: <2s
Largest Contentful Paint: <1.5s
```

### **Backend**
```
API Response Time: <200ms avg
Document Processing: <2s
AI Response: 1-3s
Download Generation: <3s
```

### **Total User Flow**
```
Upload → Process → Chat → Download
< 2s     < 2s      varies   < 3s

Total: ~10 minutes for complete flow
```

---

## **Security**

### **Frontend**
- ✅ CSP Headers
- ✅ HTTPS only
- ✅ Input sanitization
- ✅ XSS protection
- ✅ File type validation

### **Backend**
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ File validation
- ✅ Input sanitization
- ✅ Environment variables
- ✅ No secrets in code

### **API Security**
```python
# Rate limiting example
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour"]
)

@app.route('/api/upload')
@limiter.limit("10 per minute")
def upload():
    # Implementation
    pass
```

---

## **Testing Stack**

### **Frontend Tests**
```bash
# Jest + React Testing Library
npm install -D @testing-library/react
npm install -D @testing-library/jest-dom
npm install -D jest jest-environment-jsdom
```

**Example Test:**
```typescript
import { render, screen } from '@testing-library/react';
import UploadZone from './upload-zone';

describe('UploadZone', () => {
  it('renders upload zone', () => {
    render(<UploadZone />);
    expect(screen.getByText(/drag & drop/i)).toBeInTheDocument();
  });
});
```

### **Backend Tests**
```bash
# pytest
pip install pytest pytest-cov pytest-flask
```

**Example Test:**
```python
def test_upload_endpoint(client):
    """Test document upload"""
    with open('test.docx', 'rb') as f:
        response = client.post('/api/upload', data={'document': f})
    assert response.status_code == 200
    assert 'session_id' in response.json
```

---

## **Monitoring & Analytics**

### **Frontend**
```typescript
// Vercel Analytics (FREE)
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

### **Backend**
```python
# Basic logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

---

## **Cost Breakdown (Monthly)**

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| **Vercel** | Hobby | FREE | 100GB bandwidth |
| **Render** | Free | FREE | 750 hours |
| **Groq API** | Free | FREE | 30 req/min |
| **GitHub** | Free | FREE | Unlimited public repos |
| **Domain** | Optional | ~$12/year | - |
| **Total** | - | **$0** | - |

**Note:** All free tiers are sufficient for this assignment and beyond!

---

## **Browser Support**

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| Mobile Safari | iOS 14+ | ✅ Full |
| Chrome Mobile | Android 90+ | ✅ Full |

---

## **Development Commands**

### **Frontend**
```bash
# Install dependencies
npm install

# Development server
npm run dev          # http://localhost:3000

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Type check
npm run type-check

# Run tests
npm test
```

### **Backend**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py             # http://localhost:5000

# Run with auto-reload
FLASK_ENV=development flask run

# Run tests
pytest
pytest --cov

# Format code
black .

# Lint code
flake8 .

# Type check
mypy .
```

---

## **Quick Setup**

### **Frontend**
```bash
# Create Next.js app with TypeScript
npx create-next-app@latest frontend --typescript --tailwind --app

cd frontend

# Install shadcn/ui
npx shadcn-ui@latest init

# Install dependencies
npm install framer-motion lucide-react

# Run dev server
npm run dev
```

### **Backend**
```bash
# Create backend directory
mkdir backend && cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Flask
pip install Flask Flask-CORS python-docx groq python-dotenv

# Create requirements.txt
pip freeze > requirements.txt

# Create app.py
touch app.py

# Run server
python app.py
```

---

## **Why This Stack?**

### **Next.js + TypeScript**
- ✅ Type safety catches bugs early
- ✅ Great developer experience
- ✅ Excellent performance
- ✅ SEO-friendly
- ✅ Easy deployment

### **Flask + Python**
- ✅ Perfect for AI integration
- ✅ Excellent for document processing
- ✅ Fast development
- ✅ Great libraries ecosystem
- ✅ Easy to deploy

### **Tailwind + shadcn/ui**
- ✅ Rapid UI development
- ✅ Consistent design system
- ✅ Highly customizable
- ✅ Small bundle size
- ✅ Accessible components

### **Groq API**
- ✅ Completely FREE
- ✅ Fast inference
- ✅ No rate limit issues
- ✅ Great AI quality
- ✅ Simple API

---

## **Resources**

- **Next.js**: https://nextjs.org/docs
- **TypeScript**: https://www.typescriptlang.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **shadcn/ui**: https://ui.shadcn.com
- **Flask**: https://flask.palletsprojects.com
- **python-docx**: https://python-docx.readthedocs.io
- **Groq API**: https://console.groq.com/docs
- **Vercel**: https://vercel.com/docs
- **Render**: https://render.com/docs

---

**This stack is production-ready, cost-effective ($0!), and perfect for the assignment! 🚀**