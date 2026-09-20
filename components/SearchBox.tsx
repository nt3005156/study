'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, BookOpen, Hash, HelpCircle, FileText, Loader2 } from 'lucide-react';

type Hit = { k: 'chapter' | 'section' | 'term' | 'question'; t: string; s: string; h: string; x: string };

const KIND_ICON = { chapter: BookOpen, section: Hash, term: FileText, question: HelpCircle } as const;
const KIND_LABEL = { chapter: 'Chapter', section: 'Section', term: 'Key term', question: 'Question' } as const;
const KIND_RANK = { chapter: 0, section: 1, term: 2, question: 3 } as const;

/** Index loads once per page, shared by every SearchBox on screen. */
let indexPromise: Promise<Hit[]> | null = null;
function loadIndex(): Promise<Hit[]> {
  if (!indexPromise) {
    indexPromise = fetch('/search-index.json')
      .then((res) => (res.ok ? (res.json() as Promise<Hit[]>) : []))
      .catch(() => []);
  }
  return indexPromise;
}

export function SearchBox({ size = 'sm' }: { size?: 'sm' | 'lg' }) {
  const [q, setQ] = useState('');
  const [hits, setHits] = useState<Hit[]>([]);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  const boxRef = useRef<HTMLDivElement>(null);
  const big = size === 'lg';

  useEffect(() => {
    const needle = q.trim().toLowerCase();
    if (needle.length < 2) {
      setHits([]);
      setBusy(false);
      return;
    }
    setBusy(true);
    let cancelled = false;
    const t = setTimeout(async () => {
      const words = needle.split(/\s+/);
      const index = await loadIndex();
      if (cancelled) return;
      const found = index
        .filter((e) => words.every((w) => e.x.includes(w)))
        .sort((a, b) => KIND_RANK[a.k] - KIND_RANK[b.k] || a.t.length - b.t.length)
        .slice(0, 12);
      setHits(found);
      setBusy(false);
    }, 150);
    return () => {
      cancelled = true;
      clearTimeout(t);
    };
  }, [q]);

  useEffect(() => {
    const onDown = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', onDown);
    return () => document.removeEventListener('mousedown', onDown);
  }, []);

  const go = (href: string) => {
    setOpen(false);
    setQ('');
    router.push(href);
  };

  return (
    <div ref={boxRef} className="relative w-full">
      <div
        className={`flex items-center gap-2 rounded-full border border-slate-200 bg-white shadow-sm transition focus-within:border-amber/60 focus-within:ring-4 focus-within:ring-amber/10 ${
          big ? 'px-5 py-3.5' : 'px-4 py-2'
        }`}
      >
        {busy ? (
          <Loader2 size={big ? 20 : 16} className="shrink-0 animate-spin text-stone" />
        ) : (
          <Search size={big ? 20 : 16} className="shrink-0 text-stone" />
        )}
        <input
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setOpen(true);
          }}
          onFocus={() => {
            setOpen(true);
            loadIndex();
          }}
          onKeyDown={(e) => {
            if (e.key === 'Escape') setOpen(false);
            if (e.key === 'Enter' && hits.length > 0) go(hits[0].h);
          }}
          type="search"
          role="combobox"
          aria-expanded={open && hits.length > 0}
          aria-label="Search all study materials"
          placeholder="Search chapters, concepts, questions…"
          className={`w-full bg-transparent outline-none placeholder:text-slate-400 text-ink ${
            big ? 'text-base' : 'text-sm'
          }`}
        />
      </div>

      {open && q.trim().length >= 2 && (
        <div className="absolute left-0 right-0 top-full z-50 mt-2 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl shadow-slate-900/10">
          {hits.length === 0 && !busy ? (
            <p className="px-4 py-5 text-center text-sm text-stone">
              No matches for “{q.trim()}”. Try a chapter, concept or keyword.
            </p>
          ) : (
            <ul className="max-h-[22rem] overflow-y-auto py-2">
              {hits.map((hit, i) => {
                const Icon = KIND_ICON[hit.k];
                return (
                  <li key={`${hit.h}-${i}`}>
                    <button
                      type="button"
                      onClick={() => go(hit.h)}
                      className="flex w-full items-start gap-3 px-4 py-2.5 text-left hover:bg-amber/5 transition"
                    >
                      <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-amber/10 text-amber-deep">
                        <Icon size={14} />
                      </span>
                      <span className="min-w-0">
                        <span className="block truncate text-sm font-semibold text-ink">{hit.t}</span>
                        <span className="block truncate text-xs text-stone">
                          {KIND_LABEL[hit.k]} · {hit.s}
                        </span>
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
