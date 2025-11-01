'use client';

import { useEffect, useState } from 'react';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  // Avoid SSR/CSR markup mismatch by deferring theme detection until mounted
  const [mounted, setMounted] = useState(false);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    setMounted(true);
    // Determine initial theme on client only
    const saved = (localStorage.getItem('theme') as 'light' | 'dark' | null);
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initial = saved ?? (prefersDark ? 'dark' : 'light');
    setTheme(initial);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    const root = document.documentElement;
    if (theme === 'dark') root.classList.add('dark');
    else root.classList.remove('dark');
    localStorage.setItem('theme', theme);
  }, [theme, mounted]);

  const toggle = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'));

  // Render a stable placeholder on server to prevent hydration mismatch
  if (!mounted) {
    return (
      <button
        aria-label="Toggle theme"
        className="h-9 px-3 rounded-xl border border-border text-foreground bg-card/80 hover:shadow-sm transition"
        suppressHydrationWarning
      >
        <div className="flex items-center gap-2 text-xs">Theme</div>
      </button>
    );
  }

  return (
    <button
      aria-label="Toggle theme"
      onClick={toggle}
      className="h-9 px-3 rounded-xl border border-border text-foreground bg-card/80 hover:shadow-sm transition"
    >
      {theme === 'dark' ? (
        <div className="flex items-center gap-2 text-xs"><Sun className="h-3.5 w-3.5" /> Light</div>
      ) : (
        <div className="flex items-center gap-2 text-xs"><Moon className="h-3.5 w-3.5" /> Dark</div>
      )}
    </button>
  );
}


