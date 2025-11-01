# 📋 Product Requirements Document (PRD)

## **Project Title**
Legal Document Automation Platform - Lexsy Assignment

**Version**: 1.0  
**Date**: October 2025  
**Author**: Full-Stack Engineer Candidate  
**Status**: In Development  

---

## **1. Executive Summary**

### **1.1 Purpose**
Build a web application that automates the process of filling legal documents using AI-powered conversational interface. This is a test assignment for Lexsy, an AI law firm for startups.

### **1.2 Problem Statement**
Legal documents contain many placeholders ({{COMPANY_NAME}}, {{DATE}}, etc.) that need to be filled manually. This process is:
- Time-consuming
- Error-prone
- Not user-friendly
- Lacks guidance for non-legal professionals

### **1.3 Solution**
An AI-powered single-page application that:
- Automatically detects placeholders in legal documents
- Guides users through filling each field conversationally
- Validates inputs based on field type
- Generates completed, downloadable documents

### **1.4 Success Metrics**
- **Functionality**: 100% of features working
- **Performance**: Page load < 2s
- **UX**: User completes process in < 5 minutes
- **Quality**: Zero critical bugs
- **Design**: Modern, professional appearance

---

## **2. Target Audience**

### **2.1 Primary Users**
- **Startup founders** filling incorporation documents
- **Small business owners** handling contracts
- **Legal professionals** automating routine docs

### **2.2 User Personas**

**Persona 1: Tech Founder**
- Age: 25-35
- Tech-savvy
- Needs: Fast, efficient process
- Pain point: Doesn't understand legal jargon

**Persona 2: Small Business Owner**
- Age: 35-50
- Moderate tech skills
- Needs: Guidance through process
- Pain point: Intimidated by legal documents

---

## **3. Core Features**

### **3.1 Feature 1: Document Upload**

**Priority**: P0 (Must Have)

**User Story**:
```
As a user
I want to upload my legal document template
So that I can fill it with my information
```

**Acceptance Criteria**:
- ✅ Supports .docx file format
- ✅ Drag-and-drop functionality
- ✅ File browse option
- ✅ File size validation (max 10MB)
- ✅ File type validation
- ✅ Visual feedback during upload
- ✅ Error handling for invalid files

**Technical Requirements**:
- File upload via FormData API
- Client-side validation
- Server-side validation
- Secure file storage
- Unique session ID generation

**UI Requirements**:
- Large, prominent upload zone
- Clear instructions
- File preview after selection
- Progress indicator during upload
- Success/error notifications

---

### **3.2 Feature 2: Placeholder Detection**

**Priority**: P0 (Must Have)

**User Story**:
```
As the system
I want to automatically identify placeholders
So that I know which fields need to be filled
```

**Acceptance Criteria**:
- ✅ Detects {{PLACEHOLDER}} format
- ✅ Detects [PLACEHOLDER] format
- ✅ Detects __PLACEHOLDER__ format
- ✅ Identifies placeholder type (name, date, amount, etc.)
- ✅ Maintains document structure
- ✅ Groups related placeholders

**Technical Requirements**:
- Regex pattern matching
- NLP-based context detection
- Type inference algorithm
- Document parsing (python-docx)

**Detection Patterns**:
```python
patterns = {
    'double_curly': r'\{\{([^}]+)\}\}',
    'square_bracket': r'\[([A-Z_\s]+)\]',
    'underscore': r'__([A-Z_\s]+)__',
    'angle_bracket': r'<([A-Z_\s]+)>',
}
```

---

### **3.3 Feature 3: AI Conversational Interface**

**Priority**: P0 (Must Have)

**User Story**:
```
As a user
I want AI to ask me questions about each field
So that I can fill the document conversationally
```

**Acceptance Criteria**:
- ✅ AI asks one question at a time
- ✅ Questions are context-aware
- ✅ Provides examples when helpful
- ✅ Validates user inputs
- ✅ Handles corrections gracefully
- ✅ Shows progress through fields
- ✅ Natural, friendly tone

**Conversation Flow**:
```
1. AI: "Welcome! I'll help you fill this document."
2. AI: "Let's start. What's the company name?"
3. User: "Acme Corporation"
4. AI: "Great! Now, when was the company incorporated?"
5. User: "January 15, 2024"
6. AI: "Perfect! That's 01/15/2024. Next..."
```

**Technical Requirements**:
- Groq API integration (llama-3.1-70b)
- Conversation state management
- Context preservation
- Error recovery
- Input validation by type

**Validation Rules**:
```typescript
validators = {
  date: /^\d{2}\/\d{2}\/\d{4}$/,
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  amount: /^\$[\d,]+(\.\d{2})?$/,
  phone: /^\+?[\d\s\-\(\)]+$/,
}
```

---

### **3.4 Feature 4: Real-Time Preview**

**Priority**: P0 (Must Have)

**User Story**:
```
As a user
I want to see my document update in real-time
So that I can verify my entries are correct
```

**Acceptance Criteria**:
- ✅ Preview updates after each field
- ✅ Filled fields highlighted in green
- ✅ Unfilled fields highlighted in yellow
- ✅ Click placeholder to edit value
- ✅ Side-by-side or modal view
- ✅ Maintains document formatting

**UI Requirements**:
- Scrollable preview pane
- Syntax highlighting
- Hover tooltips
- Click-to-edit functionality
- Zoom controls (optional)

---

### **3.5 Feature 5: Document Download**

**Priority**: P0 (Must Have)

**User Story**:
```
As a user
I want to download my completed document
So that I can use it for my legal needs
```

**Acceptance Criteria**:
- ✅ All fields must be filled
- ✅ Generates valid .docx file
- ✅ Preserves original formatting
- ✅ Highlights filled values (optional)
- ✅ Downloads immediately
- ✅ Proper filename

**Technical Requirements**:
- Document generation (python-docx)
- File streaming
- Proper MIME types
- Download endpoint

**Filename Format**:
```
completed_[original-name]_[timestamp].docx
Example: completed_safe_agreement_20241031_143022.docx
```

---

## **4. Non-Functional Requirements**

### **4.1 Performance**
- **Page Load**: < 2 seconds
- **API Response**: < 200ms (average)
- **Document Upload**: < 5 seconds for 10MB
- **AI Response**: 1-3 seconds
- **Download Generation**: < 3 seconds

### **4.2 Security**
- ✅ HTTPS only
- ✅ File type validation
- ✅ File size limits
- ✅ Input sanitization
- ✅ No sensitive data in logs
- ✅ Environment variables for secrets
- ✅ CORS configuration

### **4.3 Scalability**
- Support 100 concurrent users
- Handle documents up to 100 pages
- Process 50+ placeholders
- Session cleanup after 24 hours

### **4.4 Reliability**
- 99% uptime target
- Graceful error handling
- Data persistence during session
- Auto-save progress (optional)

### **4.5 Usability**
- Mobile responsive (< 768px)
- Keyboard navigation
- Screen reader compatible
- No more than 3 clicks to any feature
- Clear error messages

### **4.6 Compatibility**
- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Devices**: Desktop, tablet, mobile
- **OS**: Windows, macOS, Linux, iOS, Android

---

## **5. User Interface Requirements**

### **5.1 Design Principles**
- **Minimal**: Clean, uncluttered interface
- **Modern**: Glassmorphism, gradients, smooth animations
- **Intuitive**: Self-explanatory, no training needed
- **Accessible**: WCAG 2.1 AA compliant
- **Responsive**: Works on all screen sizes

### **5.2 Color Scheme**
```
Primary:     #667eea (Purple)
Secondary:   #764ba2 (Deep Purple)
Success:     #10b981 (Green)
Warning:     #f59e0b (Amber)
Error:       #ef4444 (Red)
Background:  #f8fafc (Light Gray)
Text:        #1e293b (Dark Gray)
Glass:       rgba(255,255,255,0.1) + backdrop-blur
```

### **5.3 Typography**
- **Font Family**: Inter (Google Fonts)
- **Headings**: 24px-48px, weight 600-700
- **Body**: 16px, weight 400
- **Small**: 14px, weight 400
- **Line Height**: 1.6

### **5.4 Spacing**
```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
2xl: 48px
```

### **5.5 Layout Structure**

```
┌─────────────────────────────────────────────┐
│              Header / Logo                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐  │
│  │                                     │  │
│  │         Upload Zone                 │  │
│  │    (or Chat Interface)              │  │
│  │                                     │  │
│  └─────────────────────────────────────┘  │
│                                             │
│  ┌────────────┐  ┌────────────────────┐   │
│  │  Preview   │  │    Download        │   │
│  │  Button    │  │    Button          │   │
│  └────────────┘  └────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## **6. Technical Specifications**

### **6.1 Frontend Stack**
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **State**: React Context + Hooks
- **API Client**: Fetch API

### **6.2 Backend Stack**
- **Framework**: Flask 3.0 (Python)
- **Language**: Python 3.11
- **Document**: python-docx 1.1.0
- **AI**: Groq API (llama-3.1-70b)
- **Server**: Gunicorn
- **CORS**: Flask-CORS

### **6.3 Development Tools**
- **Version Control**: Git + GitHub
- **Package Manager**: npm (frontend), pip (backend)
- **Linting**: ESLint, Flake8
- **Formatting**: Prettier, Black
- **Testing**: Jest, pytest

### **6.4 Deployment**
- **Frontend**: Vercel (FREE)
- **Backend**: Render.com (FREE)
- **Domain**: Custom or provided subdomain
- **SSL**: Auto-provided by platforms

---

## **7. API Specifications**

### **7.1 Upload Endpoint**
```typescript
POST /api/upload
Content-Type: multipart/form-data

Request:
  document: File (.docx)

Response: {
  success: boolean,
  session_id: string,
  filename: string,
  placeholders: Placeholder[],
  placeholders_count: number,
  message: string
}

Errors:
  400: Invalid file type
  400: File too large
  500: Processing error
```

### **7.2 Chat Endpoint**
```typescript
POST /api/chat
Content-Type: application/json

Request: {
  message: string,
  session_id: string
}

Response: {
  response: string,
  placeholder_filled: boolean,
  current_progress: number,
  total_placeholders: number,
  all_filled: boolean,
  filled_values: Record<string, string>
}

Errors:
  400: No session found
  500: AI service error
```

### **7.3 Preview Endpoint**
```typescript
GET /api/preview?session_id=xxx

Response: {
  preview: string (HTML),
  filled_count: number,
  total_count: number,
  placeholders: Placeholder[],
  filled_values: Record<string, string>
}

Errors:
  400: No session found
  500: Generation error
```

### **7.4 Complete Endpoint**
```typescript
POST /api/complete
Content-Type: application/json

Request: {
  session_id: string
}

Response: {
  success: boolean,
  download_url: string,
  filename: string
}

Errors:
  400: Not all placeholders filled
  500: Document generation error
```

---

## **8. Data Models**

### **8.1 Document**
```typescript
interface Document {
  id: string;
  filename: string;
  content: {
    paragraphs: Paragraph[];
    tables: Table[];
    raw_text: string;
    metadata: Metadata;
  };
  uploaded_at: Date;
}
```

### **8.2 Placeholder**
```typescript
interface Placeholder {
  key: string;              // unique identifier
  name: string;             // display name
  original: string;         // original text ({{NAME}})
  type: PlaceholderType;    // date, amount, text, etc.
  pattern_type: string;     // double_curly, etc.
  location: number | string;
  location_type: 'paragraph' | 'table';
  context: string;          // surrounding text
  required: boolean;
  validation?: ValidationRule;
}

type PlaceholderType = 
  | 'company' 
  | 'person' 
  | 'date' 
  | 'amount' 
  | 'percentage' 
  | 'address' 
  | 'contact' 
  | 'text';
```

### **8.3 Session**
```typescript
interface Session {
  id: string;
  document: Document;
  placeholders: Placeholder[];
  filled_values: Record<string, string>;
  current_index: number;
  started_at: Date;
  expires_at: Date;
}
```

### **8.4 ChatMessage**
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: {
    placeholder_key?: string;
    validation_result?: boolean;
  };
}
```

---

## **9. User Flows**

### **9.1 Happy Path Flow**
```
1. User lands on homepage
   ↓
2. User uploads .docx document
   ↓
3. System processes document
   ↓
4. System detects 15 placeholders
   ↓
5. AI: "Welcome! Found 15 fields. Let's start."
   ↓
6. AI: "What's the company name?"
   ↓
7. User: "Acme Corp"
   ↓
8. System validates → Success
   ↓
9. AI: "Great! When was it incorporated?"
   ↓
10. User: "Jan 15 2024"
   ↓
11. System validates → Reformats to 01/15/2024
   ↓
12. ... (repeat for all 15 fields)
   ↓
13. AI: "All done! Review your document."
   ↓
14. User clicks "Preview"
   ↓
15. User reviews document
   ↓
16. User clicks "Download"
   ↓
17. Document downloads
   ↓
18. ✅ Success!
```

### **9.2 Error Flow - Invalid File**
```
1. User uploads .pdf file
   ↓
2. System validates file type
   ↓
3. Error: "Invalid file type"
   ↓
4. User sees error message
   ↓
5. User uploads .docx instead
   ↓
6. ✅ Continue happy path
```

### **9.3 Error Flow - Invalid Input**
```
1. AI: "What's the incorporation date?"
   ↓
2. User: "sometime in 2024"
   ↓
3. System validates → Fail
   ↓
4. AI: "Please use MM/DD/YYYY format"
   ↓
5. User: "01/15/2024"
   ↓
6. System validates → Success
   ↓
7. ✅ Continue
```

---

## **10. Testing Requirements**

### **10.1 Unit Tests**
- All utility functions
- Validation logic
- API client functions
- Component rendering

### **10.2 Integration Tests**
- File upload flow
- Chat conversation
- Document preview
- Download generation

### **10.3 E2E Tests**
- Complete user flow
- Mobile responsive
- Error scenarios
- Cross-browser

### **10.4 Manual Testing Checklist**
- [ ] Upload various document types
- [ ] Fill all field types correctly
- [ ] Test validation errors
- [ ] Preview updates correctly
- [ ] Download works
- [ ] Mobile responsive
- [ ] Keyboard navigation
- [ ] Screen reader compatibility

---

## **11. Deployment Requirements**

### **11.1 Frontend (Vercel)**
- [ ] Next.js build succeeds
- [ ] Environment variables configured
- [ ] API_URL points to backend
- [ ] Custom domain (optional)
- [ ] Analytics setup (optional)

### **11.2 Backend (Render)**
- [ ] Python 3.11 runtime
- [ ] requirements.txt updated
- [ ] Environment variables set
- [ ] Health check endpoint
- [ ] CORS configured
- [ ] File storage configured

### **11.3 Environment Variables**

**Frontend:**
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_NAME=Lexsy Doc Automation
```

**Backend:**
```bash
GROQ_API_KEY=gsk_xxxxx
SECRET_KEY=random-secret-key
FLASK_ENV=production
CORS_ORIGIN=https://yourdomain.com
MAX_FILE_SIZE=10485760
PORT=5000
```

---

## **12. Success Criteria**

### **12.1 Functionality** (40 points)
- ✅ Upload works (10 points)
- ✅ Placeholder detection accurate (10 points)
- ✅ AI conversation natural (10 points)
- ✅ Download produces valid document (10 points)

### **12.2 Design** (30 points)
- ✅ Modern, professional UI (15 points)
- ✅ Mobile responsive (10 points)
- ✅ Smooth animations (5 points)

### **12.3 Code Quality** (20 points)
- ✅ Clean, maintainable code (10 points)
- ✅ Proper error handling (5 points)
- ✅ Documentation (5 points)

### **12.4 Performance** (10 points)
- ✅ Fast load times (5 points)
- ✅ No console errors (5 points)

**Target Score: 95+/100** 🎯

---

## **13. Timeline**

### **Day 1 (6 hours)**
- Setup project structure (1h)
- Build upload component (1h)
- Integrate backend API (1h)
- Build chat interface (2h)
- Initial testing (1h)

### **Day 2 (6 hours)**
- Build preview component (2h)
- Polish UI/UX (2h)
- Deploy (1h)
- Final testing (1h)

**Total: 12 hours** (you have 48 hours)

---

## **14. Risks & Mitigation**

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Groq API down | High | Low | Use mock responses |
| Large file processing | Medium | Medium | Add file size limit |
| Complex placeholders | Medium | Medium | Use multiple patterns |
| Mobile performance | Low | Medium | Optimize bundle size |

---

## **15. Future Enhancements** (Out of Scope)

- [ ] Multiple document formats (PDF, ODT)
- [ ] Document templates library
- [ ] User accounts & history
- [ ] Collaborative editing
- [ ] E-signature integration
- [ ] OCR for scanned documents
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Analytics dashboard

---

## **16. Acceptance Criteria Summary**

The project is considered complete when:

✅ **All P0 features implemented and working**
✅ **Deployed and publicly accessible**
✅ **Works on mobile devices**
✅ **No critical bugs**
✅ **Professional UI/UX**
✅ **Documentation complete**
✅ **Performance targets met**

---

## **17. Sign-off**

**Prepared by**: [Your Name]  
**Date**: October 31, 2025  
**Version**: 1.0  
**Status**: Ready for Development  

---

**Let's build this! 🚀**