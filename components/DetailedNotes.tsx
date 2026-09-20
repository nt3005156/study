import { Lightbulb, BookMarked, GraduationCap, FlaskConical, Info, ListChecks } from 'lucide-react';
import { Rich, RichBlock } from '@/components/Rich';
import { CodeBlock, type Lang } from '@/components/CodeBlock';
import { FigureImage } from '@/components/FigureImage';

export type Block = {
  type: string;
  text?: string;
  term?: string;
  title?: string;
  items?: string[];
  ordered?: boolean;
  caption?: string;
  head?: string[];
  rows?: string[][];
  src?: string;
  page?: number;
  width?: number;
  lang?: Lang;
  /** Inline SVG for `diagram` blocks (trusted build-time content). */
  svg?: string;
  /** `code` blocks for languages with no online runner (e.g. QBASIC). */
  runnable?: boolean;
};

export type Section = {
  id: string;
  number: string;
  title: string;
  /** Physical textbook page; omitted where the site hides print artifacts. */
  page?: number;
  blocks: Block[];
};

function BlockView({ block, defaultLang, compact = false }: { block: Block; defaultLang?: Lang; compact?: boolean }) {
  switch (block.type) {
    case 'p':
      return <RichBlock as="p" html={block.text} className="text-[15px] leading-[1.75] text-slate-700" />;

    case 'h3':
      return (
        <RichBlock as="h3" html={block.text} className="font-serif text-xl font-bold text-ink pt-2" />
      );

    case 'h4':
      return (
        <RichBlock as="h4" html={block.text} className="font-semibold text-base text-ink pt-1" />
      );

    case 'definition':
      return (
        <div className="rounded-2xl bg-cream border border-amber/25 p-5">
          <div className="flex items-start gap-2.5">
            <BookMarked size={17} className="text-amber-deep mt-0.5 shrink-0" />
            <p className="text-[15px] leading-relaxed text-slate-700">
              <strong className="font-bold text-ink"><Rich html={block.term} />:</strong>{' '}
              <Rich html={block.text} />
            </p>
          </div>
        </div>
      );

    case 'note':
      return (
        <div className="rounded-2xl bg-skyLight border border-sky/25 p-5">
          <div className="flex items-start gap-2.5">
            <Info size={17} className="text-sky mt-0.5 shrink-0" />
            <div>
              <p className="font-bold text-ink text-sm mb-1">{block.title}</p>
              <RichBlock as="p" html={block.text} className="text-[15px] leading-relaxed text-slate-700" />
            </div>
          </div>
        </div>
      );

    case 'example':
      return (
        <div className="rounded-2xl bg-emeraldLight border border-emerald/25 p-5">
          <div className="flex items-start gap-2.5">
            <Lightbulb size={17} className="text-emerald mt-0.5 shrink-0" />
            <p className="text-[15px] leading-relaxed text-slate-700">
              <strong className="font-bold text-ink">Example.</strong> <Rich html={block.text} />
            </p>
          </div>
        </div>
      );

    case 'teacher':
      return (
        <div className="rounded-2xl bg-violet/5 border border-violet/25 p-5">
          <div className="flex items-start gap-2.5">
            <GraduationCap size={17} className="text-violet mt-0.5 shrink-0" />
            <div>
              <p className="font-bold text-violet text-xs uppercase tracking-wider mb-1">Exam note</p>
              <RichBlock as="p" html={block.text} className="text-[15px] leading-relaxed text-slate-700" />
            </div>
          </div>
        </div>
      );

    case 'code':
      return <CodeBlock code={block.text ?? ''} lang={block.lang} title={block.title} defaultLang={defaultLang} runnable={block.runnable} />;

    case 'list':
      return (
        <div>
          {block.title ? <p className="font-semibold text-ink mb-2"><Rich html={block.title} /></p> : null}
          {block.ordered ? (
            <ol className="list-decimal pl-5 space-y-2 text-[15px] leading-relaxed text-slate-700">
              {(block.items || []).map((it, i) => <li key={i}><Rich html={it} /></li>)}
            </ol>
          ) : (
            <ul className="list-disc pl-5 space-y-2 text-[15px] leading-relaxed text-slate-700">
              {(block.items || []).map((it, i) => <li key={i}><Rich html={it} /></li>)}
            </ul>
          )}
        </div>
      );

    case 'steps':
      return (
        <ol className="rounded-2xl bg-paper border border-slate-200 p-5 space-y-2.5">
          {block.title ? <li className="list-none font-semibold text-ink mb-1"><Rich html={block.title} /></li> : null}
          {(block.items || []).map((it, i) => (
            <li key={i} className="flex gap-3 text-[15px] leading-relaxed text-slate-700">
              <span className="shrink-0 h-6 w-6 rounded-full bg-ink text-white text-xs font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
              <span><Rich html={it} /></span>
            </li>
          ))}
        </ol>
      );

    case 'figure':
      if (!compact) {
        return (
          <figure className="rounded-2xl bg-white border border-slate-200 shadow-sm overflow-hidden">
            <div className="bg-slate-50 flex items-center justify-center p-4">
              <FigureImage src={block.src} alt={block.caption || 'Textbook figure'} width={block.width} />
            </div>
            <figcaption className="px-5 py-3 border-t border-slate-100 text-sm text-stone">
              <span className="font-semibold text-ink">Figure</span> — <Rich html={block.caption} />
            </figcaption>
          </figure>
        );
      }
      return (
        <figure className="mx-auto w-full max-w-2xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_10px_36px_-16px_rgba(15,23,42,0.35)] ring-1 ring-slate-900/5">
          <div className="flex items-center justify-center bg-gradient-to-b from-slate-50 to-white p-3">
            <FigureImage src={block.src} alt={block.caption || 'Textbook figure'} width={block.width} compact />
          </div>
          <figcaption className="flex items-start gap-2 border-t border-slate-100 bg-white px-4 py-2.5 text-[13px] leading-snug text-stone">
            <span className="mt-px shrink-0 rounded-md bg-amber/15 px-1.5 py-0.5 text-[10px] font-extrabold uppercase tracking-wider text-amber-deep">Figure</span>
            <span className="min-w-0 flex-1"><Rich html={block.caption} /></span>
          </figcaption>
        </figure>
      );

    case 'diagram': {
      // Inline SVG overview diagrams (Class 6). The SVG is trusted build-time
      // content from our own JSON; strip any script element defensively.
      const svg = (block.svg || '').replace(/<script[\s\S]*?<\/script>/gi, '');
      if (!compact) {
        return (
          <figure className="rounded-2xl bg-white border border-slate-200 shadow-sm overflow-hidden">
            <div className="bg-slate-50 flex items-center justify-center p-4">
              <div
                role="img"
                aria-label={block.title || 'Chapter diagram'}
                className="w-full max-w-full rounded-lg border border-slate-200 bg-white p-2 [&>svg]:h-auto [&>svg]:w-full"
                dangerouslySetInnerHTML={{ __html: svg }}
              />
            </div>
            <figcaption className="px-5 py-3 border-t border-slate-100 text-sm text-stone">
              <span className="font-semibold text-ink">Diagram</span> — <Rich html={block.title} />
            </figcaption>
          </figure>
        );
      }
      return (
        <figure className="mx-auto w-full max-w-2xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_10px_36px_-16px_rgba(15,23,42,0.35)] ring-1 ring-slate-900/5">
          <div className="flex items-center justify-center bg-gradient-to-b from-slate-50 to-white p-3">
            <div
              role="img"
              aria-label={block.title || 'Chapter diagram'}
              className="w-full max-w-full rounded-lg border border-slate-200 bg-white p-2 [&>svg]:h-auto [&>svg]:w-full"
              dangerouslySetInnerHTML={{ __html: svg }}
            />
          </div>
          <figcaption className="flex items-start gap-2 border-t border-slate-100 bg-white px-4 py-2.5 text-[13px] leading-snug text-stone">
            <span className="mt-px shrink-0 rounded-md bg-sky/15 px-1.5 py-0.5 text-[10px] font-extrabold uppercase tracking-wider text-sky">Diagram</span>
            <span className="min-w-0 flex-1"><Rich html={block.title} /></span>
          </figcaption>
        </figure>
      );
    }

    case 'table':
      return (
        <div className="rounded-2xl border border-slate-200 overflow-hidden">
          {block.caption ? (
            <div className="bg-slate-50 px-5 py-2.5 border-b border-slate-200 text-sm font-semibold text-ink">
              {block.caption}
            </div>
          ) : null}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-white">
                <tr>
                  {(block.head || []).map((h, i) => (
                    <RichBlock as="th" key={i} html={h} className="text-left font-bold text-ink px-4 py-3 border-b border-slate-200 whitespace-nowrap" />
                  ))}
                </tr>
              </thead>
              <tbody>
                {(block.rows || []).map((row, ri) => (
                  <tr key={ri} className={ri % 2 ? 'bg-slate-50/60' : 'bg-white'}>
                    {row.map((cell, ci) => (
                      <RichBlock as="td" key={ci} html={cell} className="px-4 py-3 text-slate-700 leading-relaxed align-top border-b border-slate-100" />
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );

    default:
      return null;
  }
}

/** Print-textbook layout: a figure/diagram is set beside the paragraph, table or
 *  list that introduces it, instead of stacking full-width below it. Runs of
 *  consecutive figures become a 2-up gallery. Only used with `sideBySide`. */
const PAIRABLE = new Set(['p', 'list', 'table', 'steps', 'code', 'definition', 'note', 'example', 'teacher']);
const VISUAL = new Set(['figure', 'diagram']);

type Node =
  | { kind: 'single'; block: Block }
  | { kind: 'pair'; text: Block; visual: Block; flip?: boolean; extra?: Block }
  | { kind: 'gallery'; blocks: Block[] };

function pairBlocks(blocks: Block[]): Node[] {
  const nodes: Node[] = [];
  const lastSingle = (): Block | null => {
    const prev = nodes[nodes.length - 1];
    return prev && prev.kind === 'single' ? prev.block : null;
  };
  let i = 0;
  while (i < blocks.length) {
    const b = blocks[i];
    if (b.type === 'figure') {
      let j = i;
      while (j < blocks.length && blocks[j].type === 'figure') j++;
      const run = blocks.slice(i, j);
      const prev = lastSingle();
      let rest = run;
      if (prev && PAIRABLE.has(prev.type)) {
        nodes[nodes.length - 1] = { kind: 'pair', text: prev, visual: run[0] };
        rest = run.slice(1);
      }
      if (rest.length >= 2) nodes.push({ kind: 'gallery', blocks: rest });
      else if (rest.length === 1) nodes.push({ kind: 'single', block: rest[0] });
      i = j;
      continue;
    }
    if (b && VISUAL.has(b.type)) {
      const prev = lastSingle();
      if (prev && PAIRABLE.has(prev.type)) {
        nodes[nodes.length - 1] = { kind: 'pair', text: prev, visual: b };
      } else {
        nodes.push({ kind: 'single', block: b });
      }
      i++;
      continue;
    }
    // Figure-first ordering: a lone visual directly above a text block pairs
    // with it, keeping DOM order (visual left, text right on desktop).
    const prev = lastSingle();
    if (b && prev && PAIRABLE.has(b.type) && VISUAL.has(prev.type)) {
      nodes[nodes.length - 1] = { kind: 'pair', text: b, visual: prev, flip: true };
    } else {
      nodes.push({ kind: 'single', block: b });
    }
    i++;
  }
  // A list directly below a pair continues the same breath of text (an intro
  // paragraph followed by its key points): fold it into the pair's text
  // column so the figure sits beside the full content, not a lone sentence.
  for (let k = 0; k + 1 < nodes.length; k++) {
    const cur = nodes[k];
    const nxt = nodes[k + 1];
    if (cur.kind === 'pair' && !cur.extra && nxt.kind === 'single' && nxt.block.type === 'list') {
      cur.extra = nxt.block;
      nodes.splice(k + 1, 1);
    }
  }
  return nodes;
}

export function DetailedNotes({ sections, defaultLang, sideBySide = false }: { sections: Section[]; defaultLang?: Lang; sideBySide?: boolean }) {
  return (
    <div className="space-y-14">
      {sections.map((section) => {
        const nodes: Node[] = sideBySide
          ? pairBlocks(section.blocks)
          : section.blocks.map((block) => ({ kind: 'single', block }) as Node);
        return (
        <section key={section.id} id={`sec-${section.id}`} className="scroll-mt-32">
          <header className="mb-5 pb-3 border-b-2 border-amber/30">
            <div className="flex items-baseline gap-3 flex-wrap">
              <h2 className="font-serif text-2xl sm:text-3xl font-bold text-ink tracking-tight"><Rich html={section.title} /></h2>
            </div>
          </header>
          <div className="space-y-5">
            {nodes.map((node, i) =>
              node.kind === 'single' ? (
                <BlockView key={i} block={node.block} defaultLang={defaultLang} compact={sideBySide} />
              ) : node.kind === 'gallery' ? (
                <div key={i} className="grid items-start gap-5 sm:grid-cols-2">
                  {node.blocks.map((gb, j) => (
                    <BlockView key={j} block={gb} defaultLang={defaultLang} compact={sideBySide} />
                  ))}
                </div>
              ) : node.flip ? (
                <div key={i} className="grid items-start gap-6 lg:grid-cols-[300px_minmax(0,1fr)]">
                  <aside className="min-w-0">
                    <BlockView block={node.visual} defaultLang={defaultLang} compact={sideBySide} />
                  </aside>
                  <div className="min-w-0 space-y-4">
                    <BlockView block={node.text} defaultLang={defaultLang} compact={sideBySide} />
                    {node.extra ? <BlockView block={node.extra} defaultLang={defaultLang} compact={sideBySide} /> : null}
                  </div>
                </div>
              ) : (
                <div key={i} className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_300px]">
                  <div className="min-w-0 space-y-4">
                    <BlockView block={node.text} defaultLang={defaultLang} compact={sideBySide} />
                    {node.extra ? <BlockView block={node.extra} defaultLang={defaultLang} compact={sideBySide} /> : null}
                  </div>
                  <aside className="min-w-0">
                    <BlockView block={node.visual} defaultLang={defaultLang} compact={sideBySide} />
                  </aside>
                </div>
              ),
            )}
          </div>
        </section>
        );
      })}
    </div>
  );
}

export function DetailedNotesToc({ sections }: { sections: Section[] }) {
  return (
    <nav aria-label="Chapter contents" className="sticky top-16 z-30 -mx-4 sm:mx-0 mb-8 bg-paper/90 backdrop-blur border-y border-slate-200 no-print">
      <div className="px-4 py-3 overflow-x-auto">
        <ul className="flex items-center gap-2 min-w-max">
          {sections.map((s) => (
            <li key={s.id}>
              <a
                href={`#sec-${s.id}`}
                className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:border-amber hover:text-amber-deep transition"
              >
                <ListChecks size={13} />
                <Rich html={s.title} />
              </a>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}

export function LabWorkBadge() {
  return (
    <span className="inline-flex items-center gap-1.5 bg-emeraldLight text-emerald text-xs font-bold px-2.5 py-1 rounded-md">
      <FlaskConical size={13} /> Lab work
    </span>
  );
}
