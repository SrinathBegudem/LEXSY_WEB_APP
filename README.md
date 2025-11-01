# Lexsy - Legal Document Automation Platform

An AI-powered full-stack application that helps users fill legal documents through an intelligent conversational interface.

## 🚀 Features

- **Document Upload** - Drag & drop .docx file upload with validation
- **AI-Powered Conversations** - Intelligent chat interface powered by Groq AI (llama-3.1-70b)
- **Placeholder Detection** - Automatically identifies placeholders in documents ({{}}, [], __ formats)
- **Real-time Preview** - Live document preview with filled values highlighted
- **Progress Tracking** - Visual progress indicator showing completion status
- **Document Generation** - Generate completed documents with all filled values
- **Modern UI** - Beautiful glassmorphism design with smooth animations

## 🏗️ Architecture

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

## 🛠️ Technology Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components
- **Framer Motion** animations
- **Lucide Icons**

### Backend
- **Flask 3.0** (Python)
- **python-docx** (document processing)
- **Groq API** (FREE AI - llama-3.1-70b)
- **Flask-CORS** (API access)

### Deployment
- **Frontend**: Vercel (FREE)
- **Backend**: Render.com (FREE)

## 📁 Project Structure

```
lexsy-assignment/
├── frontend/                 # Next.js application
│   ├── app/
│   │   ├── page.tsx         # Main page (single page app)
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   ├── ui/              # shadcn components
│   │   ├── upload-zone.tsx   # Drag & drop upload
│   │   ├── chat-interface.tsx
│   │   ├── document-preview.tsx
│   │   └── progress-tracker.tsx
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   ├── types.ts          # TypeScript types
│   │   └── utils.ts          # Utility functions
│   └── package.json
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
│   ├── Prompt.md
│   ├── Techstack.md
│   ├── Styling_guide.md
│   └── Manual.md
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Groq API key (free from https://console.groq.com)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
CORS_ORIGIN=http://localhost:3000
MAX_FILE_SIZE=10485760
PORT=5000
```

4. Run the backend:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📡 API Endpoints

### Backend (Flask)

- `POST /api/upload` - Upload document
- `POST /api/chat` - Send message to AI
- `GET /api/preview` - Get document preview
- `POST /api/complete` - Generate final document
- `GET /api/download/:filename` - Download completed document
- `POST /api/reset` - Reset session
- `GET /api/health` - Health check

## 🎨 Design Features

- **Glassmorphism UI** - Modern frosted glass effects
- **Smooth Animations** - Framer Motion powered transitions
- **Responsive Design** - Mobile-first approach
- **Accessibility** - WCAG 2.1 AA compliant
- **Color Palette** - Purple gradient theme (#667eea, #764ba2)

## 📝 Usage Flow

1. **Upload Document** - User uploads a .docx file with placeholders like `{{COMPANY_NAME}}`
2. **Detect Placeholders** - System automatically identifies all placeholders
3. **AI Conversation** - AI asks questions one by one to fill each placeholder
4. **Real-time Preview** - Document preview updates as fields are filled
5. **Complete & Download** - Generate final document with all filled values

## 🔒 Security Considerations

- File type validation (.docx only)
- File size limits (10MB max)
- Input sanitization
- CORS configuration
- Session management

## 🧪 Development

### Frontend
```bash
npm run dev      # Development server
npm run build    # Production build
npm run lint     # Run ESLint
npm run type-check  # TypeScript check
```

### Backend
```bash
python app.py    # Development server
pytest           # Run tests
black .          # Format code
flake8 .         # Lint code
```

## 📦 Deployment

### Frontend (Vercel)
1. Connect GitHub repository
2. Set `NEXT_PUBLIC_API_URL` environment variable
3. Deploy automatically on push

### Backend (Render)
1. Connect GitHub repository
2. Set environment variables (GROQ_API_KEY, SECRET_KEY, etc.)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`

## 📄 License

This project is built for Lexsy assignment.

## 👨‍💻 Author

Legal Tech Solutions - October 2025

## 🙏 Acknowledgments

- Groq for free AI API access
- shadcn/ui for beautiful components
- Next.js and Flask communities

