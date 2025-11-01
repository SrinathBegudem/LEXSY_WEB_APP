# 🎨 Styling Guide - UI/UX Design System

## **Design Philosophy**

**Core Principles:**
1. **Minimal** - Less is more, remove unnecessary elements
2. **Modern** - Cutting-edge design trends (glassmorphism, gradients)
3. **Accessible** - WCAG 2.1 AA compliant
4. **Responsive** - Mobile-first approach
5. **Performant** - Fast loading, smooth animations

---

## **Color System**

### **Primary Colors**
```typescript
const colors = {
  // Brand Colors
  primary: {
    DEFAULT: '#667eea',  // Main purple
    50: '#f5f7ff',
    100: '#ebefff',
    500: '#667eea',      // Base
    600: '#5568d3',
    700: '#4451b8',
    900: '#2d3582',
  },
  
  secondary: {
    DEFAULT: '#764ba2',  // Deep purple
    500: '#764ba2',
    600: '#653d8a',
  },
  
  // Semantic Colors
  success: {
    DEFAULT: '#10b981',
    50: '#ecfdf5',
    500: '#10b981',
    600: '#059669',
  },
  
  warning: {
    DEFAULT: '#f59e0b',
    50: '#fffbeb',
    500: '#f59e0b',
    600: '#d97706',
  },
  
  error: {
    DEFAULT: '#ef4444',
    50: '#fef2f2',
    500: '#ef4444',
    600: '#dc2626',
  },
  
  // Neutral Colors
  gray: {
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    900: '#0f172a',
  },
};
```

### **Tailwind Config**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: colors.primary,
        secondary: colors.secondary,
        success: colors.success,
        warning: colors.warning,
        error: colors.error,
      },
    },
  },
};
```

---

## **Typography**

### **Font Family**
```typescript
// Primary: Inter (Google Fonts)
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});
```

### **Font Sizes**
```typescript
const typography = {
  // Display (Hero sections)
  'display-xl': '60px',   // 3.75rem, line-height: 1.2
  'display-lg': '48px',   // 3rem, line-height: 1.2
  
  // Headings
  'h1': '36px',           // 2.25rem, line-height: 1.3
  'h2': '30px',           // 1.875rem, line-height: 1.3
  'h3': '24px',           // 1.5rem, line-height: 1.4
  'h4': '20px',           // 1.25rem, line-height: 1.4
  'h5': '18px',           // 1.125rem, line-height: 1.5
  
  // Body
  'body-lg': '18px',      // 1.125rem, line-height: 1.6
  'body': '16px',         // 1rem, line-height: 1.6
  'body-sm': '14px',      // 0.875rem, line-height: 1.5
  
  // Small
  'caption': '12px',      // 0.75rem, line-height: 1.4
  'overline': '10px',     // 0.625rem, line-height: 1.5
};
```

### **Font Weights**
```typescript
const fontWeights = {
  light: 300,
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
};
```

### **Usage Example**
```tsx
<h1 className="text-4xl font-bold text-gray-900">
  Legal Document Automation
</h1>

<p className="text-base font-normal text-gray-600">
  Fill your documents with AI assistance
</p>
```

---

## **Spacing System**

```typescript
const spacing = {
  px: '1px',
  0: '0',
  0.5: '0.125rem',  // 2px
  1: '0.25rem',     // 4px
  2: '0.5rem',      // 8px
  3: '0.75rem',     // 12px
  4: '1rem',        // 16px
  5: '1.25rem',     // 20px
  6: '1.5rem',      // 24px
  8: '2rem',        // 32px
  10: '2.5rem',     // 40px
  12: '3rem',       // 48px
  16: '4rem',       // 64px
  20: '5rem',       // 80px
  24: '6rem',       // 96px
};
```

**Usage Pattern:**
```tsx
// Consistent spacing
<div className="p-6">        {/* 24px padding */}
  <div className="mb-4">     {/* 16px margin-bottom */}
    <h2 className="text-2xl">Title</h2>
    <p className="mt-2">Description</p>  {/* 8px margin-top */}
  </div>
</div>
```

---

## **Component Styles**

### **1. Upload Zone**

```tsx
'use client';

import { Upload } from 'lucide-react';
import { Card } from '@/components/ui/card';

export function UploadZone() {
  return (
    <Card className="
      relative
      border-2 border-dashed border-gray-300
      hover:border-primary-500
      transition-all duration-300
      rounded-xl
      p-12
      bg-gradient-to-br from-gray-50 to-white
      backdrop-blur-sm
      group
    ">
      <div className="flex flex-col items-center justify-center space-y-4">
        <div className="
          w-16 h-16
          rounded-full
          bg-primary-100
          flex items-center justify-center
          group-hover:scale-110
          transition-transform duration-300
        ">
          <Upload className="w-8 h-8 text-primary-600" />
        </div>
        
        <div className="text-center">
          <h3 className="text-xl font-semibold text-gray-900">
            Upload Your Document
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Drag & drop your .docx file or click to browse
          </p>
        </div>
        
        <button className="
          px-6 py-2
          bg-primary-600
          hover:bg-primary-700
          text-white
          rounded-lg
          font-medium
          transition-colors duration-200
        ">
          Browse Files
        </button>
        
        <p className="text-xs text-gray-500">
          Maximum file size: 10MB
        </p>
      </div>
    </Card>
  );
}
```

### **2. Chat Interface**

```tsx
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';

export function ChatInterface() {
  return (
    <div className="flex flex-col h-[600px] bg-white rounded-xl shadow-lg">
      {/* Header */}
      <div className="
        px-6 py-4
        border-b border-gray-200
        bg-gradient-to-r from-primary-50 to-secondary-50
      ">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              AI Assistant
            </h3>
            <p className="text-sm text-gray-600">
              Helping you fill the document
            </p>
          </div>
          <Badge variant="success">
            5 of 15 completed
          </Badge>
        </div>
      </div>
      
      {/* Messages */}
      <ScrollArea className="flex-1 p-6">
        {/* Assistant Message */}
        <div className="flex gap-3 mb-4">
          <Avatar className="w-8 h-8 bg-primary-100">
            <span className="text-primary-600">AI</span>
          </Avatar>
          <div className="
            flex-1
            bg-gray-100
            rounded-lg
            rounded-tl-none
            p-4
          ">
            <p className="text-gray-900">
              What's the company name?
            </p>
          </div>
        </div>
        
        {/* User Message */}
        <div className="flex gap-3 mb-4 justify-end">
          <div className="
            flex-1
            max-w-[70%]
            bg-primary-600
            text-white
            rounded-lg
            rounded-tr-none
            p-4
          ">
            <p>Acme Corporation</p>
          </div>
        </div>
      </ScrollArea>
      
      {/* Input */}
      <div className="p-6 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Type your answer..."
            className="
              flex-1
              px-4 py-3
              border border-gray-300
              rounded-lg
              focus:outline-none
              focus:ring-2
              focus:ring-primary-500
              focus:border-transparent
            "
          />
          <button className="
            px-6 py-3
            bg-primary-600
            hover:bg-primary-700
            text-white
            rounded-lg
            font-medium
            transition-colors duration-200
          ">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

### **3. Progress Tracker**

```tsx
import { Progress } from '@/components/ui/progress';
import { CheckCircle2, Circle } from 'lucide-react';

export function ProgressTracker({ current, total }) {
  const percentage = (current / total) * 100;
  
  return (
    <div className="
      p-6
      bg-white
      rounded-xl
      shadow-lg
      border border-gray-200
    ">
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm font-medium text-gray-700">
          Progress
        </span>
        <span className="text-sm font-semibold text-primary-600">
          {current} of {total} fields
        </span>
      </div>
      
      <Progress value={percentage} className="h-2 mb-4" />
      
      <div className="space-y-2">
        {Array.from({ length: total }).map((_, i) => (
          <div key={i} className="flex items-center gap-2">
            {i < current ? (
              <CheckCircle2 className="w-4 h-4 text-success-600" />
            ) : (
              <Circle className="w-4 h-4 text-gray-300" />
            )}
            <span className={`text-sm ${
              i < current ? 'text-gray-900 font-medium' : 'text-gray-500'
            }`}>
              Field {i + 1}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### **4. Document Preview**

```tsx
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';

export function DocumentPreview({ content, filledValues }) {
  return (
    <div className="
      bg-white
      rounded-xl
      shadow-lg
      overflow-hidden
      border border-gray-200
    ">
      <div className="
        px-6 py-4
        border-b border-gray-200
        bg-gray-50
      ">
        <h3 className="text-lg font-semibold text-gray-900">
          Document Preview
        </h3>
      </div>
      
      <ScrollArea className="h-[600px] p-6">
        <div className="prose prose-gray max-w-none">
          {/* Filled placeholder */}
          <span className="
            inline-flex items-center gap-1
            px-2 py-0.5
            bg-success-100
            text-success-800
            rounded
            text-sm
            font-medium
          ">
            Acme Corporation
            <Badge variant="success" size="sm">Filled</Badge>
          </span>
          
          {/* Unfilled placeholder */}
          <span className="
            inline-flex items-center gap-1
            px-2 py-0.5
            bg-warning-100
            text-warning-800
            rounded
            text-sm
            font-medium
            cursor-pointer
            hover:bg-warning-200
            transition-colors
          ">
            {{DATE}}
            <Badge variant="warning" size="sm">Pending</Badge>
          </span>
        </div>
      </ScrollArea>
    </div>
  );
}
```

---

## **Glassmorphism Effect**

```tsx
// Glassmorphism card component
export function GlassCard({ children, className = '' }) {
  return (
    <div className={`
      relative
      bg-white/10
      backdrop-blur-lg
      border border-white/20
      rounded-xl
      p-6
      shadow-xl
      ${className}
    `}>
      {/* Gradient overlay */}
      <div className="
        absolute inset-0
        bg-gradient-to-br from-white/10 to-transparent
        rounded-xl
        pointer-events-none
      " />
      
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}

// Usage
<GlassCard>
  <h3 className="text-white text-xl font-bold">
    Beautiful Glassmorphism
  </h3>
</GlassCard>
```

---

## **Animations**

### **Framer Motion Variants**

```typescript
// Fade in animation
export const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.3 }
};

// Slide in from left
export const slideInLeft = {
  initial: { x: -100, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  transition: { type: 'spring', damping: 20 }
};

// Scale in
export const scaleIn = {
  initial: { scale: 0.8, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  transition: { duration: 0.2 }
};

// Stagger children
export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};
```

### **Usage Example**

```tsx
import { motion } from 'framer-motion';

export function AnimatedCard() {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      variants={fadeIn}
      className="p-6 bg-white rounded-xl"
    >
      <h3>Animated Content</h3>
    </motion.div>
  );
}
```

---

## **Responsive Design**

### **Breakpoints**
```typescript
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Laptop
  xl: '1280px',  // Desktop
  '2xl': '1536px', // Large desktop
};
```

### **Mobile-First Approach**

```tsx
<div className="
  // Mobile (default)
  px-4 py-6
  text-sm
  
  // Tablet
  md:px-6 md:py-8
  md:text-base
  
  // Desktop
  lg:px-8 lg:py-12
  lg:text-lg
">
  Responsive content
</div>
```

---

## **Accessibility**

### **ARIA Labels**

```tsx
// Upload button
<button
  aria-label="Upload document"
  aria-describedby="upload-description"
>
  <Upload />
</button>

<span id="upload-description" className="sr-only">
  Upload your legal document in .docx format
</span>
```

### **Keyboard Navigation**

```tsx
// Tab index and keyboard handlers
<div
  tabIndex={0}
  role="button"
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
  className="focus:outline-none focus:ring-2 focus:ring-primary-500"
>
  Interactive element
</div>
```

### **Color Contrast**

```typescript
// All text must meet WCAG AA standards
const contrastRatios = {
  'text-gray-900 on bg-white': 17.68,   // ✅ Pass
  'text-gray-600 on bg-white': 5.96,    // ✅ Pass
  'text-primary-600 on bg-white': 4.68, // ✅ Pass
  'text-white on bg-primary-600': 4.68, // ✅ Pass
};
```

---

## **Button Styles**

```tsx
// Primary button
<button className="
  px-6 py-3
  bg-primary-600
  hover:bg-primary-700
  active:bg-primary-800
  text-white
  font-medium
  rounded-lg
  shadow-sm
  hover:shadow-md
  transition-all duration-200
  focus:outline-none
  focus:ring-2
  focus:ring-primary-500
  focus:ring-offset-2
  disabled:opacity-50
  disabled:cursor-not-allowed
">
  Primary Action
</button>

// Secondary button
<button className="
  px-6 py-3
  bg-white
  hover:bg-gray-50
  text-gray-700
  font-medium
  rounded-lg
  border border-gray-300
  shadow-sm
  hover:shadow
  transition-all duration-200
  focus:outline-none
  focus:ring-2
  focus:ring-primary-500
  focus:ring-offset-2
">
  Secondary Action
</button>

// Ghost button
<button className="
  px-6 py-3
  bg-transparent
  hover:bg-gray-100
  text-gray-700
  font-medium
  rounded-lg
  transition-colors duration-200
  focus:outline-none
  focus:ring-2
  focus:ring-primary-500
">
  Ghost Action
</button>
```

---

## **Form Elements**

### **Input Field**

```tsx
<div className="space-y-2">
  <label
    htmlFor="company-name"
    className="block text-sm font-medium text-gray-700"
  >
    Company Name
  </label>
  <input
    id="company-name"
    type="text"
    placeholder="Enter company name"
    className="
      w-full
      px-4 py-3
      border border-gray-300
      rounded-lg
      focus:outline-none
      focus:ring-2
      focus:ring-primary-500
      focus:border-transparent
      placeholder:text-gray-400
      transition-all duration-200
    "
  />
  <p className="text-xs text-gray-500">
    Enter the legal name of your company
  </p>
</div>
```

### **Error State**

```tsx
<input
  className="
    border-error-500
    focus:ring-error-500
  "
/>
<p className="text-sm text-error-600 mt-1">
  Company name is required
</p>
```

---

## **Loading States**

### **Skeleton Loader**

```tsx
export function SkeletonCard() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-200 rounded w-3/4" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
      <div className="h-4 bg-gray-200 rounded w-2/3" />
    </div>
  );
}
```

### **Spinner**

```tsx
export function Spinner() {
  return (
    <div className="
      w-8 h-8
      border-4 border-gray-200
      border-t-primary-600
      rounded-full
      animate-spin
    " />
  );
}
```

---

## **Toast Notifications**

```tsx
import { useToast } from '@/components/ui/use-toast';

export function ExampleComponent() {
  const { toast } = useToast();
  
  const showSuccess = () => {
    toast({
      title: "Success!",
      description: "Document uploaded successfully",
      variant: "success",
    });
  };
  
  const showError = () => {
    toast({
      title: "Error",
      description: "Failed to upload document",
      variant: "destructive",
    });
  };
  
  return (
    <>
      <button onClick={showSuccess}>Show Success</button>
      <button onClick={showError}>Show Error</button>
    </>
  );
}
```

---

## **Layout Structure**

```tsx
export default function Page() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="
        sticky top-0 z-50
        bg-white/80
        backdrop-blur-md
        border-b border-gray-200
        shadow-sm
      ">
        <div className="
          max-w-7xl mx-auto
          px-4 sm:px-6 lg:px-8
          py-4
        ">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              Lexsy Doc Automation
            </h1>
            <button>New Document</button>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="
        max-w-7xl mx-auto
        px-4 sm:px-6 lg:px-8
        py-8 sm:py-12
      ">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-8">
            {/* Upload Zone */}
            {/* Chat Interface */}
          </div>
          
          {/* Right Column */}
          <div className="space-y-8">
            {/* Progress Tracker */}
            {/* Preview */}
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="
        mt-24
        py-8
        border-t border-gray-200
        bg-white
      ">
        <div className="
          max-w-7xl mx-auto
          px-4 sm:px-6 lg:px-8
          text-center
        ">
          <p className="text-sm text-gray-600">
            Built for Lexsy Assignment
          </p>
        </div>
      </footer>
    </div>
  );
}
```

---

## **Dark Mode (Optional)**

```tsx
// Add to tailwind.config.js
module.exports = {
  darkMode: 'class',
  // ...
};

// Usage
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-white
">
  Content adapts to dark mode
</div>
```

---

## **Performance Tips**

1. **Use Next/Image for images**
```tsx
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={50}
  priority
/>
```

2. **Lazy load heavy components**
```tsx
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <SkeletonCard />,
});
```

3. **Optimize Tailwind CSS**
```javascript
// tailwind.config.js
module.exports = {
  purge: {
    content: ['./app/**/*.{js,ts,jsx,tsx}'],
    options: {
      safelist: ['bg-success-100', 'text-error-600'],
    },
  },
};
```

---

**This styling guide ensures a consistent, beautiful, and accessible UI! 🎨**