# Lexsy Document Automation - Frontend

A modern Next.js 14 frontend for the Legal Document Automation Platform.

## Features

- **Drag & Drop Upload** - Easy document upload with validation
- **AI Chat Interface** - Conversational document filling
- **Real-time Preview** - See your document update as you fill fields
- **Progress Tracking** - Visual progress indicator
- **Modern UI** - Glassmorphism design with smooth animations

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components
- **Framer Motion** (for animations)
- **Lucide Icons**

## Getting Started

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Main page
│   └── globals.css      # Global styles
├── components/
│   ├── ui/             # shadcn/ui components
│   ├── upload-zone.tsx
│   ├── chat-interface.tsx
│   ├── document-preview.tsx
│   └── progress-tracker.tsx
└── lib/
    ├── api.ts         # API client
    ├── types.ts       # TypeScript types
    └── utils.ts       # Utility functions
```

## API Integration

The frontend communicates with the Flask backend through REST API:

- `POST /api/upload` - Upload document
- `POST /api/chat` - Send chat message
- `GET /api/preview` - Get document preview
- `POST /api/complete` - Complete document
- `GET /api/download/:filename` - Download document
- `POST /api/reset` - Reset session

## Deployment

The frontend can be deployed to Vercel:

1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically on push

For manual deployment:

```bash
npm run build
# Deploy the .next folder
```

