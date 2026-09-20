'use client';
import Link from 'next/link';
import { BookOpen, Github } from 'lucide-react';

export function Footer() {
  return (
    <footer className="mt-auto bg-ink text-slate-200 border-t border-white/10 no-print">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-12 grid md:grid-cols-3 gap-10">
        <div>
          <Link href="/" className="flex items-center gap-2.5 mb-3" aria-label="Study Platform">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-amber to-amber-deep text-white flex items-center justify-center shadow-lg shadow-amber/20"><BookOpen size={18} strokeWidth={2.5} /></div>
            <span className="text-lg font-extrabold tracking-tight text-white">Study Platform</span>
          </Link>
          <p className="text-sm text-slate-400 leading-relaxed">Digital textbook summaries, important concepts, Q&A solutions, and diagrams for Class 6–12 Computer Science.</p>
        </div>
        <div>
          <h3 className="text-white font-semibold mb-3">Quick Links</h3>
          <ul className="space-y-2 text-sm">
            <li><Link href="/" className="hover:text-amber transition">Home</Link></li>
            <li><Link href="/browse" className="hover:text-amber transition">Browse Materials</Link></li>
            <li><Link href="/class-6" className="hover:text-amber transition">Class 6</Link></li>
            <li><Link href="/class-7" className="hover:text-amber transition">Class 7</Link></li>
          </ul>
        </div>
        <div>
          <h3 className="text-white font-semibold mb-3">Content Source</h3>
          <p className="text-sm text-slate-400 mb-3">Based on verified Nepal Computer Science textbooks (Asmita/NCERT-style) for Classes 6–12.</p>
          <a href="https://github.com/nt3005156/computer-study-platform" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 text-sm font-medium text-amber hover:text-amber-deep transition"><Github size={16}/> View Source Repo</a>
        </div>
      </div>
      <div className="border-t border-white/10 mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-5 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
        <span>© {new Date().getFullYear()} Study Platform. Educational use only.</span>
        <span>Built for students, verified against textbooks.</span>
      </div>
    </footer>
  );
}
