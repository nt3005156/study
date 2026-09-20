'use client';

import { useState, type ReactNode } from 'react';
import { Columns2, BookOpen, PenTool, Printer } from 'lucide-react';

type Mode = 'split' | 'notes' | 'qa';

const MODES: { id: Mode; label: string; icon: typeof Columns2; hint: string }[] = [
  { id: 'split', label: 'Notes + Q&A', icon: Columns2, hint: 'Detailed notes on the left, questions and answers on the right' },
  { id: 'notes', label: 'Detailed notes', icon: BookOpen, hint: 'Full-width teaching notes with every figure and table' },
  { id: 'qa', label: 'Q&A only', icon: PenTool, hint: 'Only the questions and answers' },
];

export function UnitSplitView({
  notes,
  qa,
  hasDetailed,
}: {
  notes: ReactNode;
  qa: ReactNode;
  hasDetailed: boolean;
}) {
  const [mode, setMode] = useState<Mode>(hasDetailed ? 'split' : 'qa');

  const showNotes = hasDetailed && (mode === 'split' || mode === 'notes');
  const showQa = mode === 'split' || mode === 'qa';

  return (
    <div>
      {/* View switcher */}
      <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm no-print">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-stone mr-1">View</span>
          {MODES.filter((m) => hasDetailed || m.id === 'qa').map((m) => {
            const active = mode === m.id;
            return (
              <button
                key={m.id}
                type="button"
                onClick={() => setMode(m.id)}
                aria-pressed={active}
                title={m.hint}
                className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition ${
                  active
                    ? 'bg-ink text-white shadow-lg shadow-ink/20'
                    : 'bg-slate-50 text-slate-600 hover:bg-slate-100 hover:text-ink'
                }`}
              >
                <m.icon size={16} />
                {m.label}
              </button>
            );
          })}
          <button
            type="button"
            onClick={() => typeof window !== 'undefined' && window.print()}
            className="ml-auto inline-flex items-center gap-2 rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 hover:border-amber hover:text-amber-deep transition"
            aria-label="Print this page"
          >
            <Printer size={16} /> Print
          </button>
        </div>
        <p className="mt-2 px-1 text-xs text-stone">
          {MODES.find((m) => m.id === mode)?.hint}
        </p>
      </div>

      <div
        className={
          showNotes && showQa
            ? 'grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_400px] gap-8 items-start'
            : 'grid grid-cols-1 gap-8 items-start'
        }
      >
        {showNotes ? (
          <div className="min-w-0">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-amber/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-amber-deep no-print">
              <BookOpen size={13} /> Detailed notes
            </div>
            {notes}
          </div>
        ) : null}

        {showQa ? (
          <div className="min-w-0">
            {showNotes ? (
              <div className="xl:sticky xl:top-20 xl:max-h-[calc(100vh-7rem)] xl:overflow-y-auto xl:pr-2">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-emeraldLight px-3 py-1 text-xs font-bold uppercase tracking-wider text-emerald no-print">
                  <PenTool size={13} /> Questions &amp; answers
                </div>
                {qa}
              </div>
            ) : (
              <div>
                <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-emeraldLight px-3 py-1 text-xs font-bold uppercase tracking-wider text-emerald no-print">
                  <PenTool size={13} /> Questions &amp; answers
                </div>
                {qa}
              </div>
            )}
          </div>
        ) : null}
      </div>
    </div>
  );
}
