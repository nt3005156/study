'use client';
import { useState } from 'react';
import Link from 'next/link';
import { BookOpen, Menu, X, Sparkles } from 'lucide-react';

export function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-xl border-b border-slate-100 no-print">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group" aria-label="Study Platform Home">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-amber to-amber-deep text-white flex items-center justify-center shadow-lg shadow-amber/20 group-hover:shadow-amber/40 transition">
            <BookOpen size={18} strokeWidth={2.5} />
          </div>
          <div className="leading-none">
            <span className="block text-base font-extrabold tracking-tight text-ink">Study Platform</span>
            <span className="block text-[10px] font-medium text-stone tracking-wide uppercase">Class 6–12</span>
          </div>
        </Link>

        <nav aria-label="Primary" className="hidden md:flex items-center gap-1">
          {[
            { label: 'Home', href: '/' },
            { label: 'Browse Materials', href: '/browse' },
            { label: 'Classes', href: '/class-6' },
            { label: 'About', href: '/about' },
          ].map((item) => (
            <Link key={item.href} href={item.href} className="px-3 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-ink hover:bg-slate-50 transition">
              {item.label}
            </Link>
          ))}
          <Link href="/search" className="ml-2 px-3.5 py-2 rounded-full text-sm font-semibold bg-ink text-white shadow-lg shadow-ink/20 hover:bg-slate-800 transition flex items-center gap-2">
            <Sparkles size={15} /> Search
          </Link>
        </nav>

        <button onClick={() => setOpen(!open)} className="md:hidden p-2 rounded-xl hover:bg-slate-50 text-ink" aria-label={open ? 'Close menu' : 'Open menu'} aria-expanded={open}>
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-slate-100 bg-white/95 backdrop-blur-xl px-4 py-4 space-y-2 shadow-2xl shadow-black/5">
          {[
            { label: 'Home', href: '/' },
            { label: 'Browse Materials', href: '/browse' },
            { label: 'Classes', href: '/class-6' },
            { label: 'About', href: '/about' },
            { label: 'Search', href: '/search' },
          ].map((item) => (
            <Link key={item.href} href={item.href} onClick={() => setOpen(false)} className="block px-3 py-2.5 rounded-xl text-sm font-medium text-slate-700 hover:bg-amber/10 hover:text-amber-deep transition">
              {item.label}
            </Link>
          ))}
        </div>
      )}
    </header>
  );
}
