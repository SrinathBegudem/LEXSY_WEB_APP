# 🤖 CURSOR AI - PROJECT CONTEXT

## **Project Overview**
You are building a **Legal Document Automation Platform** for Lexsy - an AI law firm for startups. This is a full-stack application that helps users fill legal documents through an AI-powered conversational interface.

## **Core Functionality**
1. **Upload** - User uploads legal document (.docx)
2. **Detect** - System identifies placeholders like {{COMPANY_NAME}}
3. **Converse** - AI asks questions to fill each placeholder
4. **Preview** - Real-time document preview with filled values
5. **Download** - Export completed document

## **Technology Stack**

### **Frontend**
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components
- **Lucide Icons**

### **Backend**
- **Flask 3.0** (Python)
- **python-docx** (document processing)
- **Groq API** (FREE AI - llama-3.1-70b)
- **Flask-CORS** (API access)

### **Deployment**
- **Frontend**: Vercel (FREE)
- **Backend**: Render.com (FREE)
- **Total Cost**: $0/month

## **Architecture**

```
┌─────────────────┐         ┌─────────────────┐
│   Next.js App   │ ←────→  │   Flask API     │
│   (Frontend)    │  REST   │   (Backend)     │
│                 │         │                 │
│  - UI/UX        │         │  - Doc Process  │
│  - State Mgmt   │         │  - AI Service   │
│  - File Upload  │         │  - Placeholder  │
└─────────────────┘         └─────────────────┘
         │                           │
         │                           ↓
         │                  ┌────────────────┐
         │                  │   Groq API     │
         │                  │   (FREE AI)    │
         └─────────────────→└────────────────┘
```

## **Key Files Structure**

```
lexsy-assignment/
├── frontend/                 # Next.js application
│   ├── app/
│   │   ├── page.tsx         # Main page (single page app)
│   │   ├── layout.tsx       # Root layout
│   │   └── api/             # API routes (optional)
│   ├── components/
│   │   ├── ui/              # shadcn components
│   │   ├── upload-zone.tsx  # Drag & drop upload
│   │   ├── chat-interface.tsx
│   │   ├── document-preview.tsx
│   │   └── progress-tracker.tsx
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   └── types.ts         # TypeScript types
│   └── public/
│
├── backend/                  # Flask application
│   ├── app.py               # Main Flask app
│   ├── services/
│   │   ├── document_processor.py
│   │   ├── ai_service.py
│   │   └── placeholder_detector.py
│   ├── requirements.txt
│   └── .env
│
├── docs/                     # Documentation
│   ├── PRD.md
│   ├── TECHSTACK.md
│   ├── STYLING_GUIDE.md
│   └── MANUAL.md
│
└── README.md
```

## **Design Principles**

### **UI/UX**
- **Modern glassmorphism** with frosted glass effects
- **Smooth animations** using Framer Motion
- **Responsive design** - mobile-first approach
- **Accessibility** - WCAG 2.1 AA compliant
- **Dark mode** support (optional)

### **Color Palette**
```typescript
const colors = {
  primary: '#667eea',      // Purple
  secondary: '#764ba2',    // Deep purple
  success: '#10b981',      // Green
  warning: '#f59e0b',      // Amber
  error: '#ef4444',        // Red
  background: '#f8fafc',   // Light gray
  glass: 'rgba(255, 255, 255, 0.1)', // Glassmorphism
}
```

### **Typography**
- **Font**: Inter (Google Fonts)
- **Headings**: 600-700 weight
- **Body**: 400-500 weight
- **Code**: Fira Code

## **API Endpoints**

### **Backend (Flask)**
```typescript
POST   /api/upload          // Upload document
POST   /api/chat            // Send message to AI
GET    /api/preview         // Get document preview
POST   /api/complete        // Generate final document
GET    /api/download/:id    // Download completed doc
POST   /api/reset           // Reset session
GET    /api/health          // Health check
```

## **State Management**

Use React hooks and Context API:
```typescript
// Global state
interface AppState {
  document: Document | null;
  placeholders: Placeholder[];
  filledValues: Record<string, string>;
  currentIndex: number;
  progress: number;
  isLoading: boolean;
  error: string | null;
}
```

## **Key Components (shadcn/ui)**

```typescript
// Use these shadcn components
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
import { toast } from "@/components/ui/use-toast"
import { Dialog } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
```

## **Code Style Guidelines**

### **TypeScript**
- Use strict mode
- Define interfaces for all data structures
- Use type guards
- Avoid `any` type

### **React/Next.js**
- Use functional components
- Use hooks (useState, useEffect, useCallback, useMemo)
- Implement proper error boundaries
- Use Suspense for loading states

### **Python/Flask**
- Follow PEP 8 style guide
- Use type hints
- Implement proper error handling
- Use environment variables for config

## **Security Considerations**

1. **File Upload**
   - Validate file type (.docx only)
   - Limit file size (10MB max)
   - Sanitize filenames
   - Scan for malicious content

2. **API Security**
   - CORS configuration
   - Rate limiting
   - Input validation
   - API key encryption

3. **Environment Variables**
   - Never commit .env files
   - Use different keys for dev/prod
   - Rotate keys regularly

## **Performance Optimization**

### **Frontend**
- Use Next.js Image component
- Implement code splitting
- Lazy load components
- Optimize bundle size
- Use React.memo for expensive components

### **Backend**
- Implement caching
- Use async operations
- Optimize database queries
- Compress responses

## **Testing Strategy**

### **Frontend**
```typescript
// Jest + React Testing Library
describe('UploadZone', () => {
  it('should accept .docx files', () => {
    // Test implementation
  });
});
```

### **Backend**
```python
# pytest
def test_document_upload():
    """Test document upload endpoint"""
    # Test implementation
    pass
```

## **Error Handling**

### **Frontend**
```typescript
try {
  await uploadDocument(file);
  toast({ title: "Success", description: "Document uploaded" });
} catch (error) {
  toast({ 
    title: "Error", 
    description: error.message,
    variant: "destructive" 
  });
}
```

### **Backend**
```python
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Error: {str(error)}")
    return jsonify({'error': str(error)}), 500
```

## **Accessibility (a11y)**

- Use semantic HTML
- Proper ARIA labels
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratio > 4.5:1
- Focus indicators

## **Mobile Responsiveness**

```typescript
// Tailwind breakpoints
sm: '640px',  // Small devices
md: '768px',  // Medium devices
lg: '1024px', // Large devices
xl: '1280px', // Extra large devices
```

## **Animation Guidelines**

```typescript
// Framer Motion animations
const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3 }
};

const slideIn = {
  initial: { x: -100, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  transition: { type: "spring", damping: 20 }
};
```

## **Environment Variables**

### **Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_NAME=Lexsy Doc Automation
```

### **Backend (.env)**
```bash
GROQ_API_KEY=gsk_xxxxx
SECRET_KEY=your-secret-key
FLASK_ENV=development
CORS_ORIGIN=http://localhost:3000
MAX_FILE_SIZE=10485760
```

## **Git Workflow**

```bash
# Feature branch workflow
git checkout -b feature/upload-component
git add .
git commit -m "feat: add drag-drop upload component"
git push origin feature/upload-component
# Create PR on GitHub
```

## **Commit Message Convention**

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

## **Development Commands**

### **Frontend**
```bash
npm run dev          # Development server
npm run build        # Production build
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript check
```

### **Backend**
```bash
python app.py        # Development server
pytest               # Run tests
pytest --cov         # Run tests with coverage
black .              # Format code
flake8 .             # Lint code
```

## **Deployment Checklist**

### **Frontend (Vercel)**
- [ ] Build succeeds locally
- [ ] Environment variables set
- [ ] API URL configured
- [ ] Custom domain (optional)

### **Backend (Render)**
- [ ] requirements.txt updated
- [ ] Environment variables set
- [ ] Health check endpoint working
- [ ] CORS configured for frontend

## **AI Instructions for Cursor**

When generating code:

1. **Always use TypeScript** for frontend
2. **Use shadcn/ui components** - don't create custom versions
3. **Implement proper error handling** in all functions
4. **Add loading states** for async operations
5. **Use proper TypeScript types** - no `any`
6. **Follow Next.js 14 App Router** conventions
7. **Make components responsive** - mobile-first
8. **Add accessibility** features (ARIA labels, keyboard nav)
9. **Optimize performance** - use React.memo, useMemo, useCallback
10. **Write clean, documented code** - add JSDoc comments

## **Example Code Patterns**

### **API Call Pattern**
```typescript
// lib/api.ts
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
```

### **Component Pattern**
```typescript
// components/upload-zone.tsx
'use client';

interface UploadZoneProps {
  onUpload: (file: File) => void;
  isLoading?: boolean;
}

export function UploadZone({ onUpload, isLoading = false }: UploadZoneProps) {
  // Component implementation
}
```

## **Success Criteria**

Your application is successful when:

- ✅ User can upload .docx documents
- ✅ AI detects all placeholders correctly
- ✅ Conversational flow is natural and intuitive
- ✅ Preview updates in real-time
- ✅ Download provides completed document
- ✅ Works perfectly on mobile
- ✅ Loads in < 2 seconds
- ✅ No console errors
- ✅ Accessible (keyboard navigation works)
- ✅ Deployed and publicly accessible

## **Resources**

- **Next.js Docs**: https://nextjs.org/docs
- **shadcn/ui**: https://ui.shadcn.com
- **Tailwind CSS**: https://tailwindcss.com
- **Flask Docs**: https://flask.palletsprojects.com
- **Groq API**: https://console.groq.com/docs
- **python-docx**: https://python-docx.readthedocs.io

## **Remember**

This is a test assignment for a job at Lexsy. Focus on:
1. **Functionality** - It must work perfectly
2. **Design** - Modern, professional UI
3. **Code Quality** - Clean, maintainable code
4. **Performance** - Fast and responsive
5. **Documentation** - Clear README

**You have 48 hours. Make it count! 🚀**