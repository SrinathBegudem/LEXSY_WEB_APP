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
    <html lang="en" className="h-full w-full light">
      <body className={`${inter.className} h-full w-full bg-slate-50`}>
        <div className="min-h-screen h-full w-full bg-slate-50">
          {children}
        </div>
      </body>
    </html>
  );
}

