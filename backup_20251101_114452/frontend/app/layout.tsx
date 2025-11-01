import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Lexsy - Legal Document Automation Platform',
  description: 'AI-powered legal document automation for startups. Fill legal documents through an intuitive conversational interface.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className="h-full w-full">
      <head>
        {/* Prevent theme flash */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
(function(){
  try{
    var saved = localStorage.getItem('theme');
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if((saved && saved==='dark') || (!saved && prefersDark)){
      document.documentElement.classList.add('dark');
    }
  }catch(e){}
})();
`}}
        />
      </head>
      <body className={`${inter.className} h-full w-full`}>
        <div style={{ minHeight: '100vh', height: '100%', width: '100%', backgroundColor: 'hsl(248, 250, 252)', background: 'hsl(248, 250, 252)' }}>
          {children}
        </div>
      </body>
    </html>
  );
}

