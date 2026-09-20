import { Lightbulb, BookMarked, GraduationCap, FlaskConical, Info, ListChecks } from 'lucide-react';
import { Rich, RichBlock } from '@/components/Rich';
import { CodeBlock, type Lang } from '@/components/CodeBlock';

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
};

export type Section = {
  id: string;
  number: string;
  title: string;
  page: number;
  blocks: Block[];
};

function BlockView({ block, defaultLang }: { block: Block; defaultLang?: Lang }) {
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
      return <CodeBlock code={block.text ?? ''} lang={block.lang} title={block.title} defaultLang={defaultLang} />;

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
      return (
        <figure className="rounded-2xl bg-white border border-slate-200 shadow-sm overflow-hidden">
          <div className="bg-slate-50 flex items-center justify-center p-4">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={block.src}
              alt={block.caption || 'Textbook figure'}
              width={block.width || 720}
              className="h-auto w-full max-w-full rounded-lg border border-slate-200 bg-white object-contain"
              loading="lazy"
            />
          </div>
          <figcaption className="px-5 py-3 border-t border-slate-100 text-sm text-stone">
            <span className="font-semibold text-ink">Figure</span> — <Rich html={block.caption} />
          </figcaption>
        </figure>
      );

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

export function DetailedNotes({ sections, defaultLang }: { sections: Section[]; defaultLang?: Lang }) {
  return (
    <div className="space-y-14">
      {sections.map((section) => (
        <section key={section.id} id={`sec-${section.id}`} className="scroll-mt-32">
          <header className="mb-5 pb-3 border-b-2 border-amber/30">
            <div className="flex items-baseline gap-3 flex-wrap">
              <h2 className="font-serif text-2xl sm:text-3xl font-bold text-ink tracking-tight"><Rich html={section.title} /></h2>
            </div>
          </header>
          <div className="space-y-5">
            {section.blocks.map((block, i) => <BlockView key={i} block={block} defaultLang={defaultLang} />)}
          </div>
        </section>
      ))}
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
