import Link from 'next/link';
import { ArrowRight, BookOpen, Lightbulb, PenTool, Zap } from 'lucide-react';

export default function HomePage() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-amberLight via-paper to-paper" aria-label="Hero">
        {/* Decorative background shapes */}
        <div aria-hidden="true" className="absolute top-[-12%] right-[-8%] w-[520px] h-[520px] rounded-full bg-amber/10 blur-3xl" />
        <div aria-hidden="true" className="absolute bottom-[-8%] left-[-6%] w-[420px] h-[420px] rounded-full bg-sky/10 blur-3xl" />

        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-16 pb-20 lg:pt-24 lg:pb-28 relative">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-amber/20 text-amber-deep text-xs font-semibold shadow-sm mb-6 tracking-tight shadow-amber/10">
              <Zap size={13} /> Digital Study Materials • Class 6 to 12
            </div>

            <h1 className="font-serif text-5xl sm:text-6xl lg:text-8xl font-bold tracking-tight text-ink leading-[0.95] mb-6">
              Hey Student <span className="inline-block" aria-label="wave">👋</span>
            </h1>

            <p className="text-xl sm:text-2xl text-slate-600 font-light leading-snug mb-4 max-w-2xl mx-auto">
              Learn every lesson, understand every concept, and practice every question.
            </p>
            <p className="text-lg text-stone mb-10 max-w-xl mx-auto">Learn smarter. Understand better. Prepare with confidence.</p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/browse" className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-ink text-white text-lg font-bold shadow-2xl shadow-ink/25 hover:bg-slate-800 hover:-translate-y-0.5 transition-all focus:outline-none focus:ring-4 focus:ring-ink/20" aria-label="Browse Materials">
                <BookOpen size={22} /> Browse Materials
                <ArrowRight size={18} />
              </Link>
              <Link href="/class-6" className="inline-flex items-center gap-2 px-6 py-4 rounded-2xl bg-white text-ink text-base font-semibold border border-slate-200 shadow-lg shadow-slate-200/40 hover:border-amber/40 hover:-translate-y-0.5 transition-all" aria-label="Start Class 6">
                Start with Class 6
              </Link>
            </div>
          </div>

          {/* Feature rows */}
          <div className="mt-20 grid sm:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {[
              { icon: BookOpen, title: 'Textbook Summaries', desc: 'Clear explanations of every chapter based on your actual books.' },
              { icon: Lightbulb, title: 'Key Concepts', desc: 'Quick cards for definitions, examples, and remember points.' },
              { icon: PenTool, title: 'Q&A & Solutions', desc: 'Very short, short, long, and exercise answers ready for exams.' },
            ].map((f) => (
              <div key={f.title} className="rounded-3xl bg-white/80 backdrop-blur border border-slate-100 p-7 shadow-xl shadow-slate-200/20 hover:-translate-y-1 transition-all">
                <div className="h-12 w-12 rounded-2xl bg-amber/10 text-amber-deep flex items-center justify-center mb-5"><f.icon size={24} /></div>
                <h3 className="text-lg font-bold text-ink mb-2">{f.title}</h3>
                <p className="text-sm text-stone leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats / trust bar */}
      <section aria-label="Coverage" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 -mt-8 relative z-10">
        <div className="rounded-3xl bg-ink text-white px-6 py-8 sm:px-10 sm:py-10 shadow-2xl shadow-ink/25 flex flex-wrap items-center justify-between gap-6">
          <div>
            <h2 className="text-2xl sm:text-3xl font-serif font-bold tracking-tight mb-1">Built for real textbooks</h2>
            <p className="text-slate-300 text-sm sm:text-base">Content verified against Class 6–12 Computer Science PDF sources.</p>
          </div>
          <div className="flex gap-8 sm:gap-14 text-center">
            <div><div className="text-2xl sm:text-3xl font-extrabold">7</div><div className="text-xs sm:text-sm text-slate-400">Books verified</div></div>
            <div><div className="text-2xl sm:text-3xl font-extrabold">6</div><div className="text-xs sm:text-sm text-slate-400">Classes covered</div></div>
            <div><div className="text-2xl sm:text-3xl font-extrabold">79</div><div className="text-xs sm:text-sm text-slate-400">Chapters across Classes 6–12</div></div>
          </div>
        </div>
      </section>

      {/* Browse teaser */}
      <section aria-label="Browse" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-14">
          <h2 className="font-serif text-4xl sm:text-5xl font-bold text-ink tracking-tight mb-4">Choose Your Class</h2>
          <p className="text-stone text-lg max-w-xl mx-auto">Select your grade to explore summaries, key concepts, and exercise solutions.</p>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { c: 6, desc: 'Essentials of CS', subjects: 1 },
            { c: 7, desc: 'Essentials of CS', subjects: 1 },
            { c: 8, desc: 'Computer Science', subjects: 1 },
            { c: 9, desc: 'Computer Science', subjects: 1 },
            { c: 10, desc: 'Computer Science', subjects: 1 },
            { c: 11, desc: 'Computer Science', subjects: 1 },
            { c: 12, desc: 'Computer Science', subjects: 1 },
          ].map(({ c, desc }) => (
            <Link key={c} href={`/class-${c}`} className="group rounded-3xl bg-white border border-slate-100 p-7 shadow-lg shadow-slate-200/20 hover:shadow-2xl hover:-translate-y-1 transition-all text-center" aria-label={`Class ${c}`}>
              <div className="h-16 w-16 mx-auto rounded-2xl bg-gradient-to-br from-amber/90 to-amber-deep text-white flex items-center justify-center text-2xl font-extrabold shadow-lg shadow-amber/20 mb-4 group-hover:scale-110 transition-transform">{c}</div>
              <h3 className="font-bold text-ink text-lg mb-1">Class {c}</h3>
              <p className="text-xs text-stone">{desc}</p>
              <span className="mt-4 inline-block text-sm font-semibold text-amber-deep group-hover:underline">View Materials →</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Study mode teaser */}
      <section aria-label="Study Mode" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24">
        <div className="rounded-[2.5rem] bg-gradient-to-br from-ink to-slate p-10 sm:p-14 text-white shadow-2xl shadow-ink/20 relative overflow-hidden">
          <div aria-hidden="true" className="absolute -top-20 -right-20 w-80 h-80 rounded-full bg-amber/20 blur-3xl" />
          <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center gap-8 lg:gap-14">
            <div className="flex-1">
              <h2 className="font-serif text-3xl sm:text-4xl font-bold tracking-tight mb-4">Quick Revision & Study Mode</h2>
              <p className="text-slate-200 text-lg leading-relaxed mb-6">Every unit includes a condensed quick-revision view, important definitions, key points, and practice questions — so you can revise right before the exam.</p>
              <ul className="space-y-2 text-slate-200">
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-amber" /> Quick Revision notes</li>
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-amber" /> Key Definitions & Remember points</li>
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-amber" /> Practice questions by type</li>
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-amber" /> Printable study notes</li>
              </ul>
            </div>
            <div className="w-full lg:w-80 shrink-0 bg-white/10 backdrop-blur rounded-3xl p-6 border border-white/10">
              <h3 className="font-bold mb-4">Class 6 — Chapter 1: Introduction to Computers</h3>
              <div className="space-y-3 text-sm">
                <div className="bg-white/10 rounded-xl px-3 py-2">Summary: 12 key points</div>
                <div className="bg-white/10 rounded-xl px-3 py-2">Very Short Q&A: 5 questions</div>
                <div className="bg-white/10 rounded-xl px-3 py-2">Exercise Solutions: 10 answers</div>
                <div className="bg-white/10 rounded-xl px-3 py-2">Diagrams: Input–Process–Output</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
