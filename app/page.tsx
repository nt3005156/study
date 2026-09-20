import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

export default function HomePage() {
  return (
    <section aria-label="Welcome" className="relative overflow-hidden bg-gradient-to-b from-amberLight via-paper to-paper">
      <div aria-hidden="true" className="absolute top-[-12%] right-[-8%] w-[520px] h-[520px] rounded-full bg-amber/10 blur-3xl" />
      <div aria-hidden="true" className="absolute bottom-[-8%] left-[-6%] w-[420px] h-[420px] rounded-full bg-sky/10 blur-3xl" />
      <div className="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-20 pb-24 text-center">
        <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-amber-deep">
          Class 6–12 · Computer Science
        </p>
        <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-ink mb-4">
          What do you want to learn today?
        </h1>
        <p className="text-stone text-lg mb-10 max-w-xl mx-auto">
          Search any chapter, concept or question from the bar above — or explore
          every class in the interactive map.
        </p>
        <Link
          href="/browse"
          className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-ink text-white text-lg font-bold shadow-2xl shadow-ink/25 hover:bg-slate-800 hover:-translate-y-0.5 transition-all focus:outline-none focus:ring-4 focus:ring-ink/20"
          aria-label="Browse Materials"
        >
          Browse Materials
          <ArrowRight size={18} />
        </Link>
      </div>
    </section>
  );
}
