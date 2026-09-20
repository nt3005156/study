'use client';

import { useState } from 'react';
import { CheckCircle2, XCircle, Eye, EyeOff, FileQuestion, ListOrdered, HelpCircle, AlertTriangle, FlaskConical, Code2, CaseSensitive, PenLine } from 'lucide-react';
import { Rich, RichBlock } from '@/components/Rich';
import { AnswerBody } from '@/components/AnswerBody';

export type Mcq = {
  q: string;
  options: string[];
  answer: number;
  page?: number;
  teacher_note?: string;
};

export type Qa = {
  q: string;
  a: string;
};

export type Exercise = {
  source?: string;
  short: Qa[];
  long: Qa[];
  /** Chapter 4 of the Class 10 book has a separate "Programming Questions"
   *  section (Section D) distinct from the Practical Activities. */
  programming?: Qa[];
  practical?: Qa[];
  /** Several Class 8 chapters open with a "Write the full form of" drill. */
  full_forms?: Qa[];
  practical_heading?: string;
  /** The Class 6 and 7 books set objective work — rewrite the false
   *  statement, true/false, fill in the blanks, matching — that is not
   *  multiple choice and so will not fit the MCQ bank. One bank covers all
   *  of it; each item's question carries its own instruction. */
  objective?: Qa[];
  objective_heading?: string;
  mcq: Mcq[];
};

const LETTERS = ['a', 'b', 'c', 'd', 'e', 'f'];

function QuestionList({
  title,
  icon,
  tone,
  items,
  polished = false,
}: {
  title: string;
  icon: typeof ListOrdered;
  tone: 'amber' | 'sky' | 'emerald' | 'violet';
  items: Qa[];
  polished?: boolean;
}) {
  const [open, setOpen] = useState<Set<number>>(new Set());
  const Icon = icon;

  const toggle = (i: number) =>
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });

  const allOpen = open.size === items.length;
  const toggleAll = () => setOpen(allOpen ? new Set() : new Set(items.map((_, i) => i)));

  const toneCls =
    tone === 'amber'
      ? 'bg-amber/10 text-amber-deep border-amber/25'
      : tone === 'emerald'
      ? 'bg-emeraldLight text-emerald border-emerald/25'
      : tone === 'violet'
      ? 'bg-violet/10 text-violet border-violet/25'
      : 'bg-skyLight text-sky border-sky/25';

  const answerCls =
    tone === 'amber'
      ? 'bg-amber/5 border-amber/20'
      : tone === 'emerald'
      ? 'bg-emeraldLight/60 border-emerald/20'
      : tone === 'violet'
      ? 'bg-violet/5 border-violet/20'
      : 'bg-skyLight/50 border-sky/20';

  // Welcoming answer cards (polished classes): soft gradient wash, coloured
  // spine, airier student-friendly typography. Lettered <ol> markers come
  // from `.answer-polished` in globals.css.
  const polishedAnswerCls =
    tone === 'amber'
      ? 'border-amber-200 border-l-4 border-l-amber bg-gradient-to-br from-amber-50 via-white to-white'
      : tone === 'emerald'
      ? 'border-emerald-200 border-l-4 border-l-emerald bg-gradient-to-br from-emerald-50 via-white to-white'
      : tone === 'violet'
      ? 'border-violet-200 border-l-4 border-l-violet bg-gradient-to-br from-violet-50 via-white to-white'
      : 'border-sky-200 border-l-4 border-l-sky bg-gradient-to-br from-sky-50 via-white to-white';

  const polishedType =
    'answer-polished text-[15px] leading-[1.8] text-slate-700 ' +
    '[&_p]:mb-2.5 [&_ol]:pl-6 [&_ol]:space-y-2.5 [&_ul]:list-disc [&_ul]:pl-6 [&_ul]:space-y-2 ' +
    '[&_li]:leading-[1.8] ' +
    '[&_table]:w-full [&_table]:text-sm [&_table]:border-collapse ' +
    '[&_th]:border [&_th]:border-slate-300 [&_th]:bg-white/70 [&_th]:px-2.5 [&_th]:py-2 [&_th]:text-left [&_th]:font-bold [&_th]:text-ink ' +
    '[&_td]:border [&_td]:border-slate-300 [&_td]:px-2.5 [&_td]:py-2 [&_td]:align-top ' +
    '[&_code]:rounded [&_code]:bg-ink/5 [&_code]:px-1 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-[0.85em] [&_code]:text-ink ' +
    '[&_strong]:font-bold [&_strong]:text-ink [&_em]:text-slate-600';

  const legacyType =
    'text-[15px] leading-relaxed text-slate-700 ' +
    '[&_p]:mb-2 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 ' +
    '[&_li]:mb-1 [&_li]:leading-relaxed ' +
    '[&_table]:w-full [&_table]:text-sm [&_table]:border-collapse ' +
    '[&_th]:border [&_th]:border-slate-300 [&_th]:bg-white/70 [&_th]:px-2 [&_th]:py-1.5 [&_th]:text-left [&_th]:font-bold [&_th]:text-ink ' +
    '[&_td]:border [&_td]:border-slate-300 [&_td]:px-2 [&_td]:py-1.5 [&_td]:align-top ' +
    '[&_code]:rounded [&_code]:bg-ink/5 [&_code]:px-1 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-[0.85em] [&_code]:text-ink';

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <h3 className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider border ${toneCls}`}>
          <Icon size={14} /> {title}
        </h3>
        <span className="text-xs font-semibold text-stone">{items.length} questions</span>
        <button
          type="button"
          onClick={toggleAll}
          className="ml-auto inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-semibold text-stone hover:border-amber/50 hover:text-amber-deep transition no-print"
        >
          {allOpen ? <EyeOff size={13} /> : <Eye size={13} />}
          {allOpen ? 'Hide answers' : 'Show all answers'}
        </button>
      </div>

      <ol className="space-y-2">
        {items.map((item, i) => {
          const isOpen = open.has(i);
          return (
            <li key={i}>
              <button
                type="button"
                onClick={() => toggle(i)}
                aria-expanded={isOpen}
                className={
                  polished
                    ? 'w-full text-left rounded-2xl border border-slate-200 bg-white px-5 py-3.5 shadow-sm hover:border-amber/60 hover:shadow-md transition'
                    : 'w-full text-left rounded-xl border border-slate-200 bg-paper px-4 py-3 hover:border-amber/50 transition'
                }
              >
                <span className={polished ? 'text-[17px] font-extrabold tracking-tight text-ink' : 'font-semibold text-ink'}>Q{i + 1}.</span>{' '}
                <Rich html={item.q} className={polished ? 'question-polished text-[15px] font-semibold leading-relaxed text-slate-800' : 'text-slate-700 leading-relaxed'} />
                {polished ? (
                  <span
                    aria-hidden
                    className="float-right ml-3 inline-flex h-6 w-6 items-center justify-center rounded-full bg-amber/10 text-sm font-bold text-amber-deep"
                  >
                    {isOpen ? '−' : '+'}
                  </span>
                ) : (
                  <span className="float-right ml-2 text-stone" aria-hidden>
                    {isOpen ? '−' : '+'}
                  </span>
                )}
              </button>

              {isOpen ? (
                <div className={polished ? `mt-2 rounded-2xl border px-5 py-4 shadow-sm ${polishedAnswerCls}` : `mt-2 rounded-xl border px-4 py-3 ${answerCls}`}>
                  {polished ? null : (
                    <p className="mb-2 text-[11px] font-bold uppercase tracking-wider text-stone">
                      Model answer
                    </p>
                  )}
                  <div className={polished ? polishedType : legacyType}>
                    <AnswerBody html={item.a} />
                  </div>
                </div>
              ) : null}
            </li>
          );
        })}
      </ol>
    </div>
  );
}

export function ExerciseBank({ exercise, polished = false }: { exercise: Exercise; polished?: boolean }) {
  const [reveal, setReveal] = useState(false);
  const [picked, setPicked] = useState<Record<number, number>>({});

  const score = exercise.mcq.reduce(
    (acc, m, i) => acc + (picked[i] === m.answer ? 1 : 0),
    0
  );
  const answered = Object.keys(picked).length;

  return (
    <div className="space-y-6">
      {exercise.full_forms && exercise.full_forms.length > 0 ? (
        <QuestionList
          title="Write the full form of"
          icon={CaseSensitive}
          tone="emerald"
          items={exercise.full_forms}
          polished={polished}
        />
      ) : null}

      {exercise.short.length > 0 || exercise.long.length > 0 ? (
        <div className="grid lg:grid-cols-2 gap-6">
          {exercise.short.length > 0 ? (
  <QuestionList title="Short answer questions" icon={FileQuestion} tone="amber" items={exercise.short} polished={polished} />
          ) : null}
          {exercise.long.length > 0 ? (
  <QuestionList title="Long answer questions" icon={ListOrdered} tone="sky" items={exercise.long} polished={polished} />
          ) : null}
        </div>
      ) : null}

      {exercise.programming && exercise.programming.length > 0 ? (
        <QuestionList
          title="Programming questions"
          icon={Code2}
          tone="violet"
          items={exercise.programming}
          polished={polished}
        />
      ) : null}

      {exercise.objective && exercise.objective.length > 0 ? (
        <QuestionList
          title={exercise.objective_heading || 'Objective questions'}
          icon={PenLine}
          tone="emerald"
          items={exercise.objective}
          polished={polished}
        />
      ) : null}

      {exercise.practical && exercise.practical.length > 0 ? (
        <QuestionList
          title={exercise.practical_heading || 'Database practical exercise'}
          icon={FlaskConical}
          tone="emerald"
          items={exercise.practical}
          polished={polished}
        />
      ) : null}

      {exercise.mcq.length > 0 ? (
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-center gap-3 mb-5">
            <h3 className="inline-flex items-center gap-2 rounded-full bg-violet/10 text-violet border border-violet/25 px-3 py-1 text-xs font-bold uppercase tracking-wider">
              <HelpCircle size={14} /> Multiple choice questions
            </h3>
            <div className="ml-auto flex flex-wrap items-center gap-2">
              {answered > 0 ? (
                <span className="text-sm font-bold text-ink">
                  Score: {score}/{answered}
                </span>
              ) : null}
              <button
                type="button"
                onClick={() => setReveal((r) => !r)}
                className="inline-flex items-center gap-2 rounded-xl bg-ink px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 transition no-print"
              >
                {reveal ? <EyeOff size={15} /> : <Eye size={15} />}
                {reveal ? 'Hide answer key' : 'Show answer key'}
              </button>
            </div>
          </div>

          <ol className="space-y-4">
            {exercise.mcq.map((m, i) => {
              const chosen = picked[i];
              return (
                <li key={i} className="rounded-2xl border border-slate-200 bg-paper p-4">
                  <p className="font-semibold text-ink mb-3">
                    <span className="text-stone">Q{i + 1}.</span> <Rich html={m.q} />
                  </p>
                  <div className="grid sm:grid-cols-2 gap-2">
                    {m.options.map((opt, oi) => {
                      const isAnswer = oi === m.answer;
                      const isChosen = chosen === oi;
                      let cls = 'border-slate-200 bg-white text-slate-700 hover:border-amber/60';
                      if (reveal && isAnswer) cls = 'border-emerald bg-emeraldLight text-emerald font-semibold';
                      else if (reveal && isChosen && !isAnswer) cls = 'border-rose bg-rose/5 text-rose font-semibold';
                      else if (!reveal && isChosen) cls = 'border-ink bg-ink/5 text-ink font-semibold';
                      return (
                        <button
                          key={oi}
                          type="button"
                          onClick={() => setPicked((p) => ({ ...p, [i]: oi }))}
                          className={`flex items-start gap-2 text-left rounded-xl border px-3 py-2 text-sm transition ${cls}`}
                        >
                          <span className="font-bold uppercase">{LETTERS[oi]}.</span>
                          <Rich html={opt} className="flex-1" />
                          {reveal && isAnswer ? <CheckCircle2 size={16} className="shrink-0 mt-0.5" /> : null}
                          {reveal && isChosen && !isAnswer ? <XCircle size={16} className="shrink-0 mt-0.5" /> : null}
                        </button>
                      );
                    })}
                  </div>
                  {reveal && m.teacher_note ? (
                    <p className="mt-3 flex items-start gap-2 rounded-xl bg-violet/5 border border-violet/20 px-3 py-2 text-sm text-slate-700">
                      <AlertTriangle size={15} className="text-violet shrink-0 mt-0.5" />
                      <span><strong>Teacher note:</strong> <Rich html={m.teacher_note} /></span>
                    </p>
                  ) : null}
                </li>
              );
            })}
          </ol>
        </div>
      ) : null}
    </div>
  );
}
