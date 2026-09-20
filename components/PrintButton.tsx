'use client';
import { Printer } from 'lucide-react';
export function PrintButton() {
  return (
    <button onClick={() => typeof window !== 'undefined' && window.print()} className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-ink text-white font-bold shadow-xl shadow-ink/25 hover:bg-slate-800 transition no-print" aria-label="Print this page">
      <Printer size={20} /> Print Study Note
    </button>
  );
}
