import Link from 'next/link';
import { ArrowRight, BookOpen, CheckCircle2, Sparkles } from 'lucide-react';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import data from '@/content/class-10-computer-science.json';

export const metadata = {
  title: 'Class 10 Computer Science — Chapters | study.companion',
  description: 'Class 10 Computer Science chapters with summaries, key concepts, Q&A, exercise solutions and detailed teaching notes with figures.',
};

export default function SubjectPage() {
  const units = data.units as unknown as {
    unit_id: string; chapter: string; title: string; pages: string; overview: string;
    detailed?: { chapter_title: string; book_pages: string; sections: unknown[]; figures_index: unknown[] };
  }[];

  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials', href: '/browse' }, { label: 'Class 10', href: '/class-10' }, { label: 'Computer Science' }]} />
      <section aria-label="Class 10 Computer Science" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24 pt-6">
        <div className="text-center mb-12">
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-ink tracking-tight mb-3">
            Class 10 Computer Science
          </h1>
          <p className="text-stone text-lg max-w-2xl mx-auto">
            Essentials of Computer Science for Grade 10, 5 chapters. Each chapter carries detailed teaching
            notes with the textbook&apos;s own figures and tables, plus the full exercise question bank with
            solved answers.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {units.map((unit) => {
            const detailed = unit.detailed;
            return (
              <Link
                key={unit.unit_id}
                href={`/class-10/computer-science/${unit.unit_id}`}
                className={`group relative rounded-3xl bg-white border p-6 shadow-lg shadow-slate-200/20 hover:shadow-2xl hover:-translate-y-1 transition-all ${
                  detailed ? 'border-amber/40 ring-1 ring-amber/20' : 'border-slate-100'
                }`}
                aria-label={`${unit.chapter}: ${detailed ? detailed.chapter_title : unit.title}`}
              >
                <div className="flex items-start gap-3 mb-3">
                  <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-amber to-amber-deep text-white flex items-center justify-center text-xs font-extrabold shadow-md shadow-amber/20 shrink-0">
                    {unit.chapter.replace('Chapter ', '')}
                  </div>
                  <h3 className="font-bold text-ink text-lg leading-snug group-hover:text-amber-deep transition">
                    {detailed ? detailed.chapter_title : unit.title.replace(/^Chapter \d+ — /, '')}
                  </h3>
                </div>

                {detailed ? (
                  <>
                    <p className="text-sm text-stone leading-relaxed mb-4">
                      {detailed.chapter_title} — full notes with every figure from the textbook (pages {detailed.book_pages}).
                    </p>
                    <div className="flex flex-wrap items-center gap-2 text-xs font-semibold mb-4">
                      <span className="inline-flex items-center gap-1 bg-amber/10 text-amber-deep px-2 py-0.5 rounded-full">
                        <Sparkles size={12} /> Detailed notes
                      </span>
                      <span className="inline-flex items-center gap-1 bg-emeraldLight text-emerald px-2 py-0.5 rounded-full">
                        <BookOpen size={12} /> {detailed.sections.length} sections
                      </span>
                      <span className="inline-flex items-center gap-1 bg-skyLight text-sky px-2 py-0.5 rounded-full">
                        <CheckCircle2 size={12} /> {detailed.figures_index.length} figures
                      </span>
                    </div>
                  </>
                ) : (
                  <>
                    <p className="text-sm text-stone leading-relaxed mb-4">{unit.overview}</p>
                    <div className="flex items-center gap-2 text-xs font-semibold text-stone mb-4">
                      <span className="inline-flex items-center gap-1 bg-amber/10 text-amber-deep px-2 py-0.5 rounded-full"><BookOpen size={12} /> Summary</span>
                      <span className="inline-flex items-center gap-1 bg-emeraldLight text-emerald px-2 py-0.5 rounded-full"><CheckCircle2 size={12} /> Q&amp;A</span>
                    </div>
                  </>
                )}

                <div className="mt-4 flex items-center gap-2 text-sm font-bold text-ink group-hover:text-amber-deep transition">
                  Open Chapter <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </>
  );
}
