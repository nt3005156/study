import Link from 'next/link';
import { ArrowRight, Monitor, Sparkles } from 'lucide-react';
import { Breadcrumbs } from '@/components/Breadcrumbs';

export const metadata = {
  title: 'Class 11 — Study Materials | Study Platform',
  description: 'Class 11 Computer Science study materials: summaries, key concepts, Q&A and detailed teaching notes.',
};

export default function Class10Page() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials', href: '/browse' }, { label: 'Class 11' }]} />
      <section aria-label="Class 11" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24 pt-6">
        <div className="text-center mb-12">
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-ink tracking-tight mb-3">Class 11</h1>
          <p className="text-stone text-lg max-w-2xl mx-auto">
            Select a subject to explore summaries, key concepts, question &amp; answer solutions and detailed teaching notes.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link
            href="/class-11/computer-science"
            className="group relative rounded-3xl bg-white border border-amber/40 ring-1 ring-amber/20 p-7 shadow-xl shadow-slate-200/20 hover:shadow-2xl hover:-translate-y-1 transition-all"
            aria-label="Class 11 Computer Science"
          >
            <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-amber/90 to-amber-deep text-white flex items-center justify-center shadow-lg shadow-amber/20 mb-5 group-hover:scale-110 transition-transform">
              <Monitor size={28} />
            </div>
            <h2 className="font-bold text-ink text-xl mb-1">Computer Science</h2>
            <p className="text-sm text-stone leading-relaxed mb-4">
              5 chapters from Essentials of Computer Science for Grade 11. Each chapter has detailed
              teaching notes with the textbook&apos;s own figures, tables and solved exercises.
            </p>
            <div className="flex flex-wrap gap-2 mb-5">
              <span className="inline-flex items-center gap-1 rounded-full bg-amber/10 px-2.5 py-1 text-xs font-bold text-amber-deep">
                <Sparkles size={12} /> Detailed notes
              </span>
              <span className="inline-flex items-center gap-1 rounded-full bg-emeraldLight px-2.5 py-1 text-xs font-bold text-emerald">
                Q&amp;A + MCQs
              </span>
            </div>
            <span className="inline-flex items-center gap-2 text-sm font-bold text-ink group-hover:text-amber-deep transition">
              View Materials <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>
        </div>
      </section>
    </>
  );
}
