import Link from 'next/link';
import { notFound } from 'next/navigation';
import {
  ArrowLeft, ArrowRight, BookOpen, Lightbulb, PenTool, Layers,
  KeyRound, Zap, CalendarClock, Target, Image as ImageIcon,
} from 'lucide-react';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { DetailedNotes, DetailedNotesToc, type Section } from '@/components/DetailedNotes';
import type { Lang } from '@/components/CodeBlock';
import { UnitSplitView } from '@/components/UnitSplitView';
import { ExerciseBank, type Exercise } from '@/components/ExerciseBank';
import { Rich, RichBlock } from '@/components/Rich';
import data from '@/content/class-12-computer-science.json';

type QA = { q: string; a: string };
type Detailed = {
  heading: string;
  book: string;
  book_pages: string;
  chapter_number: string;
  chapter_title: string;
  note: string;
  learning_objectives: string[];
  sections: Section[];
  figures_index: { file: string; caption: string; page?: number; section: string; section_title: string }[];
  exercise: Exercise;
  exercise_heading?: string;
  key_terms: { term: string; meaning: string }[];
  quick_revision: { title: string; points: string[] }[];
  teaching_plan: { period: string; topic: string; activity: string; figures: string[] }[];
};

const units = data.units as unknown as (typeof data.units)[number][];

export function generateStaticParams() {
  return units.map((u) => ({ unit: u.unit_id }));
}

/** Snippets too short to detect (syntax templates, sample output) fall back to
 *  the language this chapter is predominantly written in. */
const UNIT_DEFAULT_LANG: Record<string, Lang> = {
  'unit-1': 'sql',   // Database Management System
  'unit-3': 'html',  // Web Technology II (JavaScript in pages)
  'unit-4': 'c',     // Programming in C
};

export default function UnitPage({ params }: { params: { unit: string } }) {
  const index = units.findIndex((u) => u.unit_id === params.unit);
  if (index === -1) notFound();

  const unit = units[index] as (typeof units)[number] & { detailed?: Detailed };
  const detailed = unit.detailed;
  const detailPracticalCount = detailed?.exercise?.practical?.length ?? 0;
  const q = unit.questions as { very_short: QA[]; short: QA[]; long: QA[]; exercise: QA[] };
  const prev = index > 0 ? units[index - 1] : null;
  const next = index < units.length - 1 ? units[index + 1] : null;

  const heading = detailed ? `${unit.chapter} — ${detailed.chapter_title}` : unit.title;
  const pageRange = detailed ? detailed.book_pages : unit.pages;

  return (
    <>
      <Breadcrumbs
        items={[
          { label: 'Browse Materials', href: '/browse' },
          { label: 'Class 12', href: '/class-12' },
          { label: 'Computer Science', href: '/class-12/computer-science' },
          { label: heading },
        ]}
      />

      <article className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pb-24 pt-4" aria-label={heading}>
        {/* ---------------- header ---------------- */}
        <header className="mb-8">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span className="text-xs font-bold text-amber-deep bg-amber/10 px-2.5 py-1 rounded-full">
              {unit.chapter} {pageRange ? `• Textbook pages ${pageRange}` : ''}
            </span>
            {detailed ? (
              <span className="text-xs font-bold text-emerald bg-emeraldLight px-2.5 py-1 rounded-full">
                Detailed notes + figures
              </span>
            ) : null}
          </div>
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-ink tracking-tight leading-[1.1] mb-4">
            <Rich html={heading} />
          </h1>
          <p className="text-lg text-stone leading-relaxed max-w-4xl">
            {detailed
              ? detailed.note
              : `${unit.title}. Summary, key concepts and exercise answers from the Class 12 Computer Science textbook.`}
          </p>
        </header>

        {/* ---------------- learning objectives ---------------- */}
        {detailed ? (
          <section aria-labelledby="lo-heading" className="mb-10">
            <div className="rounded-3xl bg-white border border-slate-200 p-7 shadow-sm">
              <h2 id="lo-heading" className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-4">
                <Target className="text-amber" size={24} /> Learning Objectives
              </h2>
              <p className="text-sm text-stone mb-3">After reading this chapter you will be able to:</p>
              <ul className="grid sm:grid-cols-2 gap-2">
                {detailed.learning_objectives.map((o, i) => (
                  <li key={i} className="flex items-start gap-2 text-[15px] text-slate-700 leading-relaxed">
                    <span className="mt-2 h-1.5 w-1.5 rounded-full bg-amber shrink-0" />
                    <Rich html={o} />
                  </li>
                ))}
              </ul>
            </div>
          </section>
        ) : null}

        {/* ---------------- overview / summary (existing content) ---------------- */}
        {!detailed ? (
          <>
            <section className="mb-10 rounded-3xl bg-white border border-slate-200 p-7 shadow-sm">
              <h2 className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-4">
                <BookOpen className="text-amber" size={24} /> Unit Overview
              </h2>
              <p className="text-stone leading-relaxed mb-2"><strong>Introduction:</strong> {unit.overview}</p>
              <p className="text-stone leading-relaxed"><strong>Summary:</strong> {unit.summary}</p>
            </section>
            <section className="mb-10">
              <h2 className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-5">
                <Lightbulb className="text-amber" size={24} /> Important Concepts
              </h2>
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {unit.concepts.map((c, i) => (
                  <div key={i} className="rounded-2xl bg-white border border-slate-200 p-6 shadow-sm">
                    <span className="inline-block text-[10px] font-extrabold tracking-wider uppercase px-2 py-0.5 rounded-md mb-3 bg-amber/10 text-amber-deep">
                      {c.type}
                    </span>
                    <h3 className="font-bold text-ink mb-2">{c.term}</h3>
                    <p className="text-sm text-stone leading-relaxed">{c.text}</p>
                  </div>
                ))}
              </div>
            </section>
          </>
        ) : null}

        {/* ---------------- the split view: notes beside the Q&A ---------------- */}
        <section aria-label="Notes and questions" className="mb-14">
          {detailed ? <DetailedNotesToc sections={detailed.sections} /> : null}

          <UnitSplitView
            hasDetailed={Boolean(detailed)}
            notes={detailed ? <DetailedNotes sections={detailed.sections} defaultLang={UNIT_DEFAULT_LANG[unit.unit_id]} /> : null}
            qa={
              <div className="space-y-5 rounded-3xl bg-white border border-slate-200 p-6 shadow-sm">
                {([
                  ['Very Short Questions', q.very_short],
                  ['Short Questions', q.short],
                  ['Long Questions', q.long],
                  ['Exercise Solutions', q.exercise],
                ] as [string, QA[]][])
                  .filter(([, list]) => list && list.length > 0)
                  .map(([label, list]) => (
                    <div key={label}>
                      <h3 className="font-bold text-ink mb-3 text-sm uppercase tracking-wide text-stone">{label}</h3>
                      <div className="space-y-3">
                        {list.map((item, i) => (
                          <div key={i} className="rounded-xl bg-paper border border-slate-200 p-4">
                            <p className="font-semibold text-ink mb-1 text-sm">Q{i + 1}. {item.q}</p>
                            <p className="text-sm text-stone leading-relaxed">
                              <strong className="text-ink">Answer:</strong> {item.a}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}

                {detailed ? (
                  <div className="rounded-xl bg-amber/5 border border-amber/25 p-4">
                    <p className="text-xs text-stone leading-relaxed">
                      <strong className="text-ink">Note.</strong> The question bank printed in the textbook for this
                      chapter ({detailed.exercise.short.length} short, {detailed.exercise.long.length} long{detailPracticalCount > 0 ? `, ${detailPracticalCount} practical` : ''} and {detailed.exercise.mcq.length} multiple-choice questions with answer key) is given in full in
                      the <a href="#exercise" className="text-amber-deep font-semibold underline">{detailed.exercise_heading ?? `Exercise ${unit.chapter.replace('Chapter ', '')}`}</a> section
                      below, with a solved model answer for every question.
                    </p>
                  </div>
                ) : null}
              </div>
            }
          />
        </section>

        {/* ---------------- exercise bank ---------------- */}
        {detailed ? (
          <>
            <section id="exercise" aria-labelledby="ex-heading" className="mb-14 scroll-mt-24">
              <h2 id="ex-heading" className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-5">
                <PenTool className="text-amber" size={24} /> {detailed.exercise_heading ?? `Exercise ${unit.chapter.replace('Chapter ', '')}`} — Question Bank with Solved Answers
              </h2>
              <ExerciseBank exercise={detailed.exercise} />
            </section>

            {/* key terms */}
            <section id="key-terms" aria-labelledby="kt-heading" className="mb-14 scroll-mt-24">
              <h2 id="kt-heading" className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-5">
                <KeyRound className="text-amber" size={24} /> Glossary — {detailed.key_terms.length} Key Terms
              </h2>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {detailed.key_terms.map((k, i) => (
                  <div key={i} className="rounded-2xl bg-white border border-slate-200 p-5 shadow-sm">
                    <RichBlock as="h3" html={k.term} className="font-bold text-ink mb-1" />
                    <RichBlock as="p" html={k.meaning} className="text-sm text-stone leading-relaxed" />
                  </div>
                ))}
              </div>
            </section>

            {/* quick revision */}
            <section id="quick-revision" aria-labelledby="qr-heading" className="mb-14 scroll-mt-24">
              <h2 id="qr-heading" className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-5">
                <Zap className="text-amber" size={24} /> Quick Revision
              </h2>
              <div className="grid sm:grid-cols-2 gap-5">
                {detailed.quick_revision.map((r, i) => (
                  <div key={i} className="rounded-3xl bg-cream border border-amber/25 p-6">
                    <RichBlock as="h3" html={r.title} className="font-bold text-ink mb-3" />
                    <ul className="space-y-1.5">
                      {r.points.map((p, j) => (
                        <li key={j} className="flex items-start gap-2 text-sm text-slate-700 leading-relaxed">
                          <span className="mt-2 h-1.5 w-1.5 rounded-full bg-amber shrink-0" />
                          <Rich html={p} />
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </section>

            {/* teaching plan */}
            <section id="teaching-plan" aria-labelledby="tp-heading" className="mb-14 scroll-mt-24">
              <h2 id="tp-heading" className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-5">
                <CalendarClock className="text-amber" size={24} /> Suggested Teaching Plan
              </h2>
              <div className="rounded-3xl border border-slate-200 overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-white">
                    <tr>
                      <th className="text-left font-bold text-ink px-5 py-3 border-b border-slate-200">Period</th>
                      <th className="text-left font-bold text-ink px-5 py-3 border-b border-slate-200">Sections</th>
                      <th className="text-left font-bold text-ink px-5 py-3 border-b border-slate-200">Classroom activity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detailed.teaching_plan.map((t, i) => (
                      <tr key={i} className={i % 2 ? 'bg-slate-50/60' : 'bg-white'}>
                        <td className="px-5 py-4 font-semibold text-ink whitespace-nowrap align-top border-b border-slate-100">{t.period}</td>
                        <RichBlock as="td" html={t.topic} className="px-5 py-4 text-slate-700 whitespace-nowrap align-top border-b border-slate-100" />
                        <RichBlock as="td" html={t.activity} className="px-5 py-4 text-slate-700 leading-relaxed align-top border-b border-slate-100" />
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            {/* figure index */}
            <section id="figures" aria-labelledby="fig-heading" className="mb-14 scroll-mt-24">
              <h2 id="fig-heading" className="flex items-center gap-3 font-serif text-2xl font-bold text-ink mb-5">
                <ImageIcon className="text-amber" size={24} /> Figure Index ({detailed.figures_index.length} figures)
              </h2>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {detailed.figures_index.map((f, i) => (
                  <a
                    key={i}
                    href={`#sec-${f.section}`}
                    className="group rounded-2xl bg-white border border-slate-200 overflow-hidden shadow-sm hover:shadow-lg hover:-translate-y-0.5 transition"
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={f.file} alt={f.caption} className="h-32 w-full object-contain bg-slate-50 p-2" loading="lazy" />
                    <div className="p-4">
                      <p className="text-xs font-bold text-amber-deep mb-1">
                        {f.section_title}
                      </p>
                      <p className="text-sm text-slate-700 leading-snug group-hover:text-ink"><Rich html={f.caption} /></p>
                    </div>
                  </a>
                ))}
              </div>
            </section>
          </>
        ) : (
          <section className="mb-14">
            <div className="rounded-3xl bg-gradient-to-br from-ink to-slate p-8 sm:p-10 text-white shadow-2xl shadow-ink/25">
              <h2 className="font-serif text-3xl font-bold tracking-tight mb-4 flex items-center gap-3">
                <Layers className="text-amber" /> Quick Revision
              </h2>
              <p className="text-slate-200 leading-relaxed">{unit.study_note}</p>
            </div>
          </section>
        )}

        {/* ---------------- prev / next ---------------- */}
        <nav aria-label="Unit navigation" className="flex items-center justify-between gap-4 pt-10 border-t border-slate-200">
          {prev ? (
            <Link href={`/class-12/computer-science/${prev.unit_id}`} className="inline-flex items-center gap-2 px-5 py-3 rounded-2xl bg-white border border-slate-200 text-ink font-semibold shadow-sm hover:border-amber transition" aria-label={`Previous: ${prev.title}`}>
              <ArrowLeft size={18} /> {prev.chapter}
            </Link>
          ) : <span />}
          <Link href="/class-12/computer-science" className="text-sm font-semibold text-stone hover:text-ink">All chapters</Link>
          {next ? (
            <Link href={`/class-12/computer-science/${next.unit_id}`} className="inline-flex items-center gap-2 px-5 py-3 rounded-2xl bg-white border border-slate-200 text-ink font-semibold shadow-sm hover:border-amber transition" aria-label={`Next: ${next.title}`}>
              {next.chapter} <ArrowRight size={18} />
            </Link>
          ) : <span />}
        </nav>
      </article>
    </>
  );
}
