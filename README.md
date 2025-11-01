# Lexsy - Legal Document Automation Platform

An intelligent, AI-powered full-stack application designed to streamline legal document processing through natural language conversations. Built with modern web technologies and deployed on scalable cloud infrastructure.

---

## 📖 How to Use

Follow these simple steps to automate your legal document filling process:

### Step 1: Sign In with Gmail
Click the **"Sign in with Google"** button to authenticate using your Gmail account. This authentication system demonstrates enterprise-grade security practices and user management capabilities. The platform uses Firebase Authentication to ensure secure user sessions and protect your document data.

### Step 2: Upload Your Document
Drag and drop your `.docx` file or click to browse and select your legal document. The system supports documents with various placeholder formats including `{{field}}`, `[field]`, and `__field__` notation. The upload is validated for file type and size (maximum 10MB).

### Step 3: Fill Fields with AI Assistant
Once your document is processed, the AI assistant will guide you through filling each placeholder field conversationally. Simply respond to the AI's questions naturally, and it will extract and validate the information automatically.

**To Edit Previously Filled Values:**
- Look for the **green highlighted text** in the document preview
- Click on any completed field (shown in green) to edit it
- The AI assistant will update the value and automatically sync it across all occurrences in the document

### Step 4: AI Documentation Assistant
Located beside the document assistant, you'll find an **AI-powered chat interface** capable of:
- Providing detailed explanations about legal terms in your document
- Answering general legal questions
- Offering insights about document structure and requirements
- Engaging in contextual conversations about your specific document

This feature is powered by Groq's free API. With a paid Groq subscription, response quality and speed would improve significantly.

**Note:** In state/address fields, you can enter either the full state name or abbreviation (e.g., "CA" or "California"). The system intelligently detects and converts abbreviations to the complete state name.

### Step 5: Complete and Download
After filling all required fields:
1. Scroll to the bottom of the page
2. Click the **"Complete"** button to generate your final document
3. The system will process and replace all placeholders with your entered values
4. Click **"Download"** to save the completed document to your device
5. The session will be automatically cleared after download for privacy

---

## 🚀 Features

- **Enterprise Authentication** - Secure Google OAuth integration with Firebase
- **Intelligent Document Processing** - Advanced placeholder detection across multiple formats
- **AI-Powered Conversations** - Natural language interface powered by Groq AI (Llama 3.1 70B)
- **Real-time Document Preview** - Live preview with field highlighting and progress tracking
- **Smart Field Editing** - Click-to-edit completed fields with automatic synchronization
- **Document Generation** - Production-ready document output with all values properly formatted
- **Modern UI/UX** - Beautiful glassmorphism design with smooth animations and responsive layout
- **Session Management** - Redis-backed persistent sessions ensuring data reliability

---

## 🏗️ System Architecture

The platform follows a modern microservices architecture pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  Next.js 14 (App Router) │ TypeScript │ Tailwind CSS        │
│  Firebase Auth │ Vercel Deployment                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS/REST API
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    Backend Services Layer                    │
│  Flask 3.0 API │ Python 3.11 │ Gunicorn (Production)       │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Document Processor  │  AI Service  │  Placeholder │    │
│  │  Detector │ Session Manager │ Firebase Admin       │    │
│  └────────────────────────────────────────────────────┘    │
│  Render.com Deployment │ Redis (Session Storage)             │
└──────────────────────────┬──────────────────────────────────┘
                           │ API Integration
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  Groq AI API │ Firebase Authentication                     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Authentication Flow:** User authenticates via Firebase Auth → Token sent to backend → Backend validates token using Firebase Admin SDK
2. **Document Processing:** Upload → Document parsed → Placeholders detected → Session created in Redis
3. **AI Interaction:** User message → AI processes context → Validates input → Updates session → Returns response
4. **Document Generation:** All fields filled → Document template loaded → Values replaced → Final document generated → Ready for download

---

## 🛠️ Technology Stack

### Frontend Technologies

**Framework & Core:**
- **Next.js 14** with App Router - React framework with server-side rendering and static generation
- **TypeScript** - Type-safe development with enhanced IDE support
- **React 18** - Modern React with concurrent features and hooks

**Styling & UI:**
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **shadcn/ui** - High-quality, accessible component library
- **Framer Motion** - Production-ready motion library for animations
- **Lucide Icons** - Beautiful, consistent icon library

**Authentication & State:**
- **Firebase SDK v9+** - Google authentication and user management
- **React Hooks** - Built-in state management with custom hooks

**Deployment:**
- **Vercel** - Serverless deployment with automatic CI/CD
- **Edge Network** - Global CDN for optimal performance

### Backend Technologies

**Core Framework:**
- **Flask 3.0** - Lightweight Python web framework
- **Python 3.11** - Modern Python with enhanced performance
- **Gunicorn** - Production WSGI HTTP server with multi-worker support

**Document Processing:**
- **python-docx** - Microsoft Word document manipulation
- **Custom Parser** - Advanced placeholder detection engine supporting multiple formats

**AI Integration:**
- **Groq API** - High-performance AI inference (Llama 3.1 70B model)
- **Custom Prompt Engineering** - Context-aware prompt generation for legal documents
- **Streaming Support** - Real-time AI response streaming

**Database & Session Management:**
- **Redis 5.0** - In-memory data store for session persistence
- **Automatic Failover** - In-memory session backup when Redis unavailable

**Authentication:**
- **Firebase Admin SDK** - Backend token verification and user management
- **Secure Token Validation** - JWT verification for API security

**API & Security:**
- **Flask-CORS** - Cross-origin resource sharing configuration
- **Werkzeug** - WSGI utilities and security middleware
- **Input Validation** - Comprehensive data sanitization and validation

**Deployment:**
- **Render.com** - Cloud platform with automatic scaling
- **Docker-ready** - Containerized deployment support
- **Health Checks** - Automated service monitoring

### DevOps & Infrastructure

- **Git** - Version control with GitHub integration
- **Environment Variables** - Secure configuration management
- **CI/CD** - Automated deployment pipelines
- **Monitoring** - Application logging and error tracking
- **Backup Systems** - Redis persistence and session recovery

---

## 📊 Performance & Scalability

- **Frontend Load Time:** Optimized with Next.js static generation
- **API Response Time:** Average 200-500ms for AI responses
- **Session Management:** Redis-backed with 7-day TTL
- **Concurrent Users:** Supports multiple simultaneous document processing sessions
- **File Processing:** Handles documents up to 10MB efficiently
- **AI Latency:** Real-time streaming responses via Groq API

---

## 🔒 Security Features

- **Authentication:** Firebase OAuth 2.0 with secure token validation
- **Authorization:** Backend token verification for all protected endpoints
- **Input Validation:** Comprehensive sanitization of user inputs
- **File Security:** Type and size validation, secure filename handling
- **CORS Protection:** Whitelist-based origin validation
- **Session Security:** Encrypted session tokens with Redis storage
- **Environment Variables:** Secrets managed securely on deployment platforms

---

## 📡 API Endpoints

### Document Management
- `POST /api/upload` - Upload and process document
- `GET /api/preview` - Retrieve document preview with current values
- `POST /api/complete` - Generate final completed document
- `GET /api/download/<filename>` - Download generated document
- `POST /api/reset` - Clear current session

### AI & Interaction
- `POST /api/chat` - Send message to document assistant
- `POST /api/fill` - Directly fill a specific field
- `POST /api/groq/stream` - Streaming AI responses
- `POST /api/groq/document-stream` - Document-aware AI streaming
- `POST /api/groq` - Non-streaming AI completion

### System & Health
- `GET /api/health` - Service health check
- `GET /api/session/health` - Session validation
- `GET /api/sessions` - Retrieve user sessions
- `GET /api/sessions/history` - Session activity history
- `GET /api/sessions/stats` - System statistics

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Groq API Key** (free from https://console.groq.com)
- **Firebase Project** (for authentication)

### Local Development Setup

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp env.txt .env
# Edit .env with your API keys

python app.py
```

Backend runs on `http://localhost:5001`

#### Frontend Setup

```bash
cd frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:5001" > .env.local

npm run dev
```

Frontend runs on `http://localhost:3000`

---

## 📦 Deployment

### Production Environment

**Frontend:**
- **Platform:** Vercel
- **URL:** https://lexsy-web-app.vercel.app
- **Features:** Automatic deployments, edge network, SSL

**Backend:**
- **Platform:** Render.com
- **URL:** https://lexsy-backend-s2dv.onrender.com
- **Features:** Auto-scaling, Redis integration, health monitoring

**Infrastructure:**
- **Session Store:** Render Redis (Key-Value service)
- **Authentication:** Firebase (Google Cloud)
- **AI Service:** Groq Cloud API

---

## 📈 Project Timeline

This project was conceptualized, designed, developed, and deployed in **10 hours**, demonstrating rapid development capabilities across:

- **Frontend Development:** Next.js application with complex state management
- **Backend Development:** Flask API with document processing and AI integration
- **AI Integration:** Groq API integration with custom prompt engineering
- **Authentication System:** Firebase OAuth implementation
- **Deployment:** Multi-platform deployment (Vercel + Render) with infrastructure setup

The rapid development timeline showcases proficiency in modern web technologies, AI integration, cloud deployment, and end-to-end full-stack development.

---

## 📁 Project Structure

```
lexsy/
├── frontend/                    # Next.js Frontend Application
│   ├── app/
│   │   ├── page.tsx           # Main application page
│   │   ├── layout.tsx          # Root layout with metadata
│   │   └── globals.css         # Global styles and themes
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── auth/               # Authentication components
│   │   ├── upload-zone.tsx     # Document upload interface
│   │   ├── chat-interface.tsx  # AI conversation UI
│   │   ├── document-preview.tsx # Live document preview
│   │   └── progress-tracker.tsx # Completion progress indicator
│   ├── lib/
│   │   ├── api.ts              # API client with error handling
│   │   ├── firebase.ts          # Firebase configuration
│   │   ├── types.ts            # TypeScript type definitions
│   │   └── utils.ts            # Utility functions
│   ├── hooks/
│   │   └── useAuth.ts          # Authentication hook
│   └── package.json
│
├── backend/                     # Flask Backend Application
│   ├── app.py                  # Main Flask application
│   ├── services/
│   │   ├── document_processor.py    # Document parsing and generation
│   │   ├── ai_service.py            # Groq AI integration
│   │   ├── placeholder_detector.py  # Placeholder detection engine
│   │   ├── session_manager.py       # Redis session management
│   │   └── firebase_auth.py         # Firebase Admin SDK
│   ├── requirements.txt        # Python dependencies
│   ├── build.sh                # Production build script
│   └── .env                    # Environment configuration
│
├── render.yaml                  # Render.com Blueprint configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 🎨 Design Philosophy

The platform follows modern design principles:

- **User-Centric Design:** Intuitive workflow reducing cognitive load
- **Visual Feedback:** Real-time preview and progress indicators
- **Accessibility:** WCAG 2.1 AA compliant components
- **Responsive:** Mobile-first approach with graceful degradation
- **Performance:** Optimized load times and smooth animations
- **Consistency:** Unified design language across all components

---

## 🔄 Development Workflow

### Frontend Development
```bash
npm run dev      # Development server with hot reload
npm run build    # Production build optimization
npm run lint     # Code quality checks
```

### Backend Development
```bash
python app.py           # Development server
pytest                  # Run test suite
black .                 # Code formatting
flake8 .                # Lint checking
```

---

## 📄 License

This project is developed for Lexsy as a demonstration of full-stack development capabilities, AI integration expertise, and modern web application architecture.

---

## 👨‍💻 Development

Built with modern development practices, comprehensive error handling, and production-ready deployment configurations. The codebase demonstrates clean architecture, separation of concerns, and maintainable code structure.

---

## 🙏 Acknowledgments

- **Groq** for providing free, high-performance AI API access
- **Firebase** for robust authentication infrastructure
- **shadcn/ui** for beautiful, accessible component library
- **Next.js & Flask communities** for excellent documentation and support
- **Vercel & Render** for seamless deployment platforms

---

## 📞 Support

For technical inquiries or feature requests, please refer to the project documentation or deployment logs for detailed error information.

---

*Last Updated: November 2025*
