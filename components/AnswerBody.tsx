'use client';

/**
 * Renders a solved answer that was authored as one HTML string, but lifts every
 * <pre data-lang="..."> block out of it and hands it to <CodeBlock> — so solved
 * programs get the copy button, syntax highlighting and online runner too.
 */

import { useMemo } from 'react';
import { RichBlock } from '@/components/Rich';
import { CodeBlock, type Lang } from '@/components/CodeBlock';

const PRE_RE = /<pre data-lang="([a-z]+)"><code>([\s\S]*?)<\/code><\/pre>/g;

function unescapeCode(s: string): string {
  return s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, '&'); // must come last
}

type Segment = { kind: 'html'; html: string } | { kind: 'code'; code: string; lang: Lang };

function split(html: string): Segment[] {
  const out: Segment[] = [];
  let last = 0;
  PRE_RE.lastIndex = 0;
  let m: RegExpExecArray | null;

  while ((m = PRE_RE.exec(html)) !== null) {
    if (m.index > last) out.push({ kind: 'html', html: html.slice(last, m.index) });
    out.push({ kind: 'code', code: unescapeCode(m[2]), lang: m[1] as Lang });
    last = m.index + m[0].length;
  }
  if (last < html.length) out.push({ kind: 'html', html: html.slice(last) });
  return out;
}

export function AnswerBody({ html, className }: { html: string; className?: string }) {
  const segments = useMemo(() => split(html || ''), [html]);

  return (
    <div className={className}>
      {segments.map((seg, i) =>
        seg.kind === 'code'
          ? <CodeBlock key={i} code={seg.code} lang={seg.lang} />
          : <RichBlock key={i} as="div" html={seg.html} />,
      )}
    </div>
  );
}

export default AnswerBody;
