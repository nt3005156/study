import Link from 'next/link';
import { ArrowRight, Monitor } from 'lucide-react';
import { Breadcrumbs } from '@/components/Breadcrumbs';

export const metadata = { title: 'Class 6 — Computer Science | Study Platform', description: 'Class 6 Computer Science study materials verified against textbook.' };

export default function Class6Page() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials', href: '/browse' }, { label: 'Class 6' }]} />
      <section aria-label="Class 6" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24 pt-6">
        <div className="text-center mb-12">
          <h1 className="font-serif text-5xl sm:text-7xl font-bold text-ink tracking-tight mb-4">Class 6</h1>
          <p className="text-stone text-lg max-w-xl mx-auto">Essentials of Computer Science — 15 chapters with verified summaries and solutions.</p>
        </div>
        <div className="max-w-md mx-auto">
          <Link href="/class-6/computer-science" className="group block rounded-3xl bg-white border border-slate-100 p-8 shadow-xl shadow-slate-200/20 hover:shadow-2xl hover:-translate-y-1 transition-all" aria-label="Computer Science">
            <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-ink to-slate text-white flex items-center justify-center text-2xl mb-5 shadow-lg shadow-ink/20 group-hover:scale-105 transition-transform">💻</div>
            <h2 className="text-2xl font-extrabold text-ink mb-2">Computer Science</h2>
            <p className="text-sm text-stone leading-relaxed mb-5">Essentials of Computer Science by Asmita Publication. 15 chapters covering hardware, software, OS, ICT, internet, malware, MS Office, programming.</p>
            <div className="flex items-center gap-2 text-sm font-bold text-ink group-hover:text-amber-deep transition"><Monitor size={18} /> View Materials <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" /></div>
          </Link>
        </div>
      </section>
    </>
  );
}
