'use client';

/**
 * A code block with:
 *   - readable syntax highlighting on a dark editor background
 *   - a Copy button
 *   - "Run it" — an embedded OneCompiler editor, pre-filled with this exact code
 *     and auto-run, so the student sees the output without leaving the page.
 *
 * OneCompiler embed API (https://onecompiler.com/apis/embed-editor):
 *   <iframe src="https://onecompiler.com/embed/{lang}?listenToEvents=true">
 *   iframe.contentWindow.postMessage({ eventType: 'populateCode', language, files })
 *   iframe.contentWindow.postMessage({ eventType: 'triggerRun' })
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { Check, Copy, ExternalLink, Play, X } from 'lucide-react';

export type Lang = 'c' | 'php' | 'javascript' | 'html' | 'sql' | 'python' | 'text';

type Runner = { slug: string; label: string; file: string };

/** OneCompiler language slugs, per detected language. */
const RUNNERS: Record<Lang, Runner[]> = {
  c: [{ slug: 'c', label: 'C (gcc)', file: 'program.c' }],
  php: [{ slug: 'php', label: 'PHP', file: 'program.php' }],
  javascript: [
    { slug: 'javascript', label: 'JavaScript', file: 'program.js' },
    { slug: 'nodejs', label: 'Node.js', file: 'program.js' },
  ],
  html: [{ slug: 'html', label: 'HTML + JS', file: 'index.html' }],
  sql: [
    { slug: 'mysql', label: 'MySQL', file: 'query.sql' },
    { slug: 'sqlite', label: 'SQLite', file: 'query.sql' },
    { slug: 'postgresql', label: 'PostgreSQL', file: 'query.sql' },
  ],
  python: [{ slug: 'python', label: 'Python 3', file: 'main.py' }],
  text: [{ slug: 'javascript', label: 'JavaScript', file: 'program.js' }],
};

const LANG_LABEL: Record<Lang, string> = {
  c: 'C', php: 'PHP', javascript: 'JavaScript',
  html: 'HTML + JavaScript', sql: 'SQL', python: 'Python', text: 'Code',
};

/** No code block in the content carries a `lang`, so infer it from the source. */
export function detectLang(code: string): Lang {
  const c = code || '';

  // Python — checked FIRST. Class 10 chapter 4 is Python, and its markers
  // (def / import / self / elif / None-True-False) cannot occur in C, PHP, SQL
  // or HTML. Detecting it first also keeps `print(` from being read as C's
  // `printf(` or PHP's `echo`.
  if (
    /^\s*def\s+\w+\s*\(/m.test(c) ||            // def greet():
    /^\s*(?:import|from)\s+[\w.]+(?:\s+import)?/m.test(c) ||
    /\bif\s+__name__\s*==/.test(c) ||
    /\bself\b/.test(c) ||
    /\bclass\s+\w+\s*(?:\(|:)/.test(c) ||
    /\b(?:elif|None|True|False)\b/.test(c)
  ) return 'python';

  // Python, weaker form: a Python builtin call together with a block-introducing
  // line ending in a colon. Guarded against C/PHP, which end lines in ';' or '{'.
  if (
    !/[;{}]\s*$/m.test(c) && !/#include/.test(c) && !/->/.test(c) &&
    /\b(?:print|input|range|len|str|int|float|list|dict)\s*\(/.test(c) &&
    /^\s*(?:for|while|if|else|elif|def|try|with)\b[^\n]*:\s*$/m.test(c)
  ) return 'python';

  // PHP — checked first, because PHP files embed HTML and use $variables.
  if (
    /<\?php/.test(c) ||
    /\$\w+\s*->/.test(c) ||          // $conn->query(...)
    /\bmysqli_\w+/.test(c) ||
    /\bnew\s+mysqli\b/.test(c) ||
    /\becho\s+['"]/.test(c)
  ) return 'php';

  // C
  if (
    /#include\s*[<'"]/.test(c) ||
    /\b(int\s+main|printf\s*\(|scanf\s*\(|FILE\s*\*|fopen\s*\(|fclose\s*\()/.test(c) ||
    /\bstruct\s+\w+/.test(c) ||
    /\b(int|float|double|char|void|long|short|unsigned)\s+\w+\s*[;=(\[]/.test(c) ||
    /\b(fprintf|fscanf|fseek|ftell|fopen|fclose|fgets|fputs|fgetc|fputc|fread|fwrite|printf|scanf|puts|gets|malloc|calloc|realloc|sizeof|strcpy|strcat|strcmp|strlen|strrev|rename|remove|rewind|feof)\s*\(/.test(c) ||
    /->/.test(c) ||
    /%[dfs]\b/.test(c)
  ) return 'c';

  // A full HTML document — checked BEFORE SQL because the SQL test is
  // case-insensitive, so a page with <select name="fruit"> reads as a SELECT.
  if (/<!DOCTYPE|<html[\s>]|<head[\s>]|<body[\s>]|<script|<\/script>|<form[\s>]|<input[\s>]|<button[\s>]|<select[\s>]/i.test(c)) return 'html';

  // SQL
  if (/\b(SELECT|CREATE\s+(DATABASE|TABLE)|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|DROP\s+(DATABASE|TABLE)|ALTER\s+TABLE|USE\s+\w+)\b/i.test(c)) return 'sql';

  // HTML (also catches JS embedded in a full page)
  if (/<!DOCTYPE|<html[\s>]|<script|<\/script>|<form|document\.write|document\.getElementById|<[a-zA-Z][\w-]*(?:\s|>)/.test(c)) return 'html';

  // JavaScript — deliberately strict, so C syntax templates such as
  // "return_type function_name(parameter-list);" are not mistaken for JS.
  if (/\b(function\s*\(|function\s+\w+\s*\(|var\s+\w+\s*=|let\s+\w+\s*=|const\s+\w+\s*=|window\.|addEventListener)/.test(c)) return 'javascript';

  return 'text';
}

/* ------------------------------------------------------------------ tokens */

const TOKEN_RE: Record<Lang, RegExp> = {
  c: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|^[ \t]*#[^\n]*)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
  php: /(\/\/[^\n]*|#[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
  javascript: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
  html: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
  sql: /(--[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
  // Python: '#' comments, plus triple-quoted docstrings as well as normal strings.
  python: /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
  text: /()|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)/gm,
};

const KEYWORDS: Record<Lang, string[]> = {
  c: ['#include', '#define', 'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'FILE', 'float', 'for', 'fclose', 'feof', 'fgetc', 'fgets',
    'fopen', 'fprintf', 'fputc', 'fputs', 'fread', 'fscanf', 'fseek', 'ftell', 'fwrite', 'gets',
    'if', 'int', 'long', 'main', 'malloc', 'calloc', 'free', 'NULL', 'EOF', 'printf', 'puts',
    'return', 'rewind', 'remove', 'rename', 'scanf', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'while'],
  sql: ['SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE',
    'DATABASE', 'TABLE', 'DROP', 'ALTER', 'ADD', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'UNIQUE',
    'DEFAULT', 'NOT', 'NULL', 'ORDER', 'BY', 'GROUP', 'HAVING', 'JOIN', 'LEFT', 'RIGHT', 'INNER',
    'OUTER', 'ON', 'AS', 'DISTINCT', 'LIKE', 'BETWEEN', 'AND', 'OR', 'IN', 'EXISTS', 'COUNT', 'SUM',
    'AVG', 'MIN', 'MAX', 'ROUND', 'LIMIT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'USE', 'SHOW',
    'DESCRIBE', 'INT', 'VARCHAR', 'DECIMAL', 'DATE', 'FLOAT', 'CHAR', 'TEXT', 'AUTO_INCREMENT',
    'COMMIT', 'ROLLBACK', 'GRANT', 'REVOKE', 'ASC', 'DESC'],
  javascript: ['var', 'let', 'const', 'function', 'return', 'if', 'else', 'for', 'while', 'do',
    'switch', 'case', 'break', 'continue', 'new', 'typeof', 'instanceof', 'this', 'document',
    'window', 'alert', 'prompt', 'console', 'Math', 'Array', 'String', 'Number', 'parseInt',
    'parseFloat', 'isNaN', 'true', 'false', 'null', 'undefined', 'innerHTML', 'value', 'length'],
  php: ['echo', 'print', 'if', 'else', 'elseif', 'for', 'foreach', 'while', 'do', 'switch', 'case',
    'break', 'continue', 'function', 'return', 'new', 'class', 'public', 'private', 'protected',
    'array', 'isset', 'empty', 'count', 'sort', 'rsort', 'asort', 'ksort', 'implode', 'explode',
    'strlen', 'strrev', 'strtolower', 'strtoupper', 'str_replace', 'mysqli_connect',
    'mysqli_query', 'mysqli_select_db', 'mysqli_fetch_assoc', 'mysqli_num_rows', 'mysqli_close',
    'mysqli_error', 'mysqli_insert_id', 'mysqli_affected_rows', 'true', 'false', 'null'],
  html: ['function', 'var', 'let', 'const', 'return', 'if', 'else', 'for', 'while', 'document',
    'window', 'alert', 'prompt', 'console', 'innerHTML', 'value', 'true', 'false', 'null',
    'addEventListener', 'getElementById', 'parseFloat', 'parseInt'],
  python: ['def', 'class', 'return', 'if', 'elif', 'else', 'for', 'while', 'in', 'range',
    'print', 'input', 'len', 'int', 'str', 'float', 'bool', 'list', 'dict', 'tuple', 'set',
    'import', 'from', 'as', 'try', 'except', 'finally', 'raise', 'with', 'lambda', 'None',
    'True', 'False', 'and', 'or', 'not', 'is', 'pass', 'break', 'continue', 'global',
    'self', 'open', 'read', 'write', 'close', 'append', 'sum', 'min', 'max', 'sorted',
    'abs', 'round', 'type', 'isinstance', 'yield', 'del', 'assert', 'async', 'await',
    'turtle', 'pandas', 'matplotlib', 'plt', 'pd', 'np', 'main'],
  text: [],
};

/* Explicit hex colours — never rely on a Tailwind class for code contrast, so a
   palette problem can never again make code black-on-black. */
const C_BASE = '#e2e8f0';
const C_KEYWORD = '#fbbf24';
const C_STRING = '#6ee7b7';
const C_COMMENT = '#7c8ba1';
const C_NUMBER = '#7dd3fc';

type Piece = { text: string; color?: string };

function tokenise(code: string, lang: Lang): Piece[] {
  const kw = new Set(KEYWORDS[lang] || []);
  const re = TOKEN_RE[lang] || TOKEN_RE.text;
  re.lastIndex = 0;

  const out: Piece[] = [];
  let last = 0;
  let m: RegExpExecArray | null;

  while ((m = re.exec(code)) !== null) {
    if (m.index > last) out.push({ text: code.slice(last, m.index) });
    const [full, comment, str, num, word] = m;

    let color: string | undefined;
    if (comment) color = C_COMMENT;
    else if (str) color = C_STRING;
    else if (num) color = C_NUMBER;
    else if (word) {
      const probe = lang === 'sql' ? word.toUpperCase() : word;
      if (kw.has(probe)) color = C_KEYWORD;
    }
    out.push({ text: full, color });
    last = m.index + full.length;
    if (full.length === 0) re.lastIndex++; // guard against zero-width matches
  }
  if (last < code.length) out.push({ text: code.slice(last) });
  return out;
}

/* ------------------------------------------------------------------- copy */

async function copyText(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch { /* fall through to the legacy path */ }
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    return ok;
  } catch {
    return false;
  }
}

function CopyButton({ code, compact }: { code: string; compact?: boolean }) {
  const [done, setDone] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);

  const onClick = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const ok = await copyText(code);
    if (!ok) return;
    setDone(true);
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => setDone(false), 1800);
  };

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label="Copy code"
      className={`no-print inline-flex items-center gap-1.5 rounded-lg border border-white/20 bg-white/10 font-semibold text-slate-200 transition hover:bg-white/20 ${compact ? 'px-2 py-1 text-[11px]' : 'px-2.5 py-1 text-xs'}`}
    >
      {done ? <Check size={13} className="text-emerald-300" /> : <Copy size={13} />}
      {done ? 'Copied' : 'Copy'}
    </button>
  );
}

/* ----------------------------------------------------------------- runner */

export function RunnerPanel({ code, lang, onClose }: { code: string; lang: Lang; onClose: () => void }) {
  const options = RUNNERS[lang] || RUNNERS.text;
  const [slug, setSlug] = useState(options[0].slug);
  const frame = useRef<HTMLIFrameElement>(null);

  const runner = options.find((o) => o.slug === slug) || options[0];

  const src = `https://onecompiler.com/embed/${runner.slug}`
    + '?listenToEvents=true&theme=dark&fontSize=14&hideNew=true&hideTitle=true&hideLanguageSelection=true';

  const push = useCallback(() => {
    const win = frame.current?.contentWindow;
    if (!win) return;
    win.postMessage(
      { eventType: 'populateCode', language: runner.slug, files: [{ name: runner.file, content: code }] },
      '*',
    );
  }, [code, runner.slug, runner.file]);

  useEffect(() => {
    // The editor needs a moment to boot and start listening, so send the code a
    // few times and only then press Run.
    const timers = [
      setTimeout(push, 400),
      setTimeout(push, 1400),
      setTimeout(push, 2800),
      setTimeout(() => frame.current?.contentWindow?.postMessage({ eventType: 'triggerRun' }, '*'), 3600),
    ];
    return () => timers.forEach(clearTimeout);
  }, [push]);

  return (
    <div className="no-print border-t border-white/10 bg-ink">
      <div className="flex flex-wrap items-center gap-2 px-4 py-2.5">
        <span className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-emerald-300">
          <Play size={12} /> Runner
        </span>

        {options.length > 1 ? (
          <select
            value={slug}
            onChange={(e) => setSlug(e.target.value)}
            className="rounded-lg border border-white/20 bg-slate-800 px-2 py-1 text-[11px] font-semibold text-slate-200"
          >
            {options.map((o) => <option key={o.slug} value={o.slug}>{o.label}</option>)}
          </select>
        ) : (
          <span className="text-[11px] font-semibold text-slate-400">{runner.label}</span>
        )}

        <div className="ml-auto flex items-center gap-2">
          <CopyButton code={code} compact />
          <a
            href={`https://onecompiler.com/${runner.slug}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 rounded-lg border border-white/20 bg-white/10 px-2 py-1 text-[11px] font-semibold text-slate-200 transition hover:bg-white/20"
          >
            <ExternalLink size={12} /> Full screen
          </a>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close runner"
            className="inline-flex items-center gap-1 rounded-lg border border-white/20 bg-white/10 px-2 py-1 text-[11px] font-semibold text-slate-200 transition hover:bg-white/20"
          >
            <X size={12} />
          </button>
        </div>
      </div>

      <iframe
        ref={frame}
        key={runner.slug}
        src={src}
        title={`Run ${LANG_LABEL[lang]} online`}
        className="block h-[520px] w-full border-0 bg-white"
        allow="clipboard-write"
      />

      <p className="px-4 py-2.5 text-[11px] leading-relaxed text-slate-400">
        The code above is loaded into this editor automatically and run once — edit it and press Run again.
        The runner is an online compiler, so it needs an internet connection; if the panel stays blank,
        use <strong className="text-slate-300">Copy</strong> and paste into any compiler, or open
        {' '}<strong className="text-slate-300">Full screen</strong>.
      </p>
    </div>
  );
}

/* -------------------------------------------------------------- code block */

export function CodeBlock({
  code,
  lang,
  title,
  defaultLang,
  runnable = true,
}: {
  code: string;
  lang?: Lang;
  title?: string;
  /** Used when the snippet is too short to detect (syntax templates, output samples). */
  defaultLang?: Lang;
  /** False for languages with no online runner (e.g. QBASIC): hides "Run it". */
  runnable?: boolean;
}) {
  const body = (code || '').replace(/\s+$/, '');
  const guess = lang && lang !== 'text' ? lang : detectLang(body);
  const detected: Lang = guess === 'text' && defaultLang ? defaultLang : guess;
  const [open, setOpen] = useState(false);
  const pieces = tokenise(body, detected);

  return (
    <div className="my-5 overflow-hidden rounded-2xl border border-slate-700 bg-ink shadow-sm">
      <div className="flex flex-wrap items-center gap-2 bg-slate-800 px-4 py-2.5">
        <span className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-full bg-rose/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald/70" />
        </span>
        <span className="ml-1 text-[11px] font-bold uppercase tracking-wider text-slate-300">
          {LANG_LABEL[detected]}
        </span>
        {title ? <span className="text-[11px] text-slate-400">— {title}</span> : null}

        <div className="ml-auto flex items-center gap-2">
          <CopyButton code={body} />
          {runnable ? (
            <button
              type="button"
              onClick={() => setOpen((v) => !v)}
              aria-expanded={open}
              className="no-print inline-flex items-center gap-1.5 rounded-lg bg-emerald px-2.5 py-1 text-xs font-bold text-white transition hover:bg-emerald-600"
            >
              <Play size={13} /> {open ? 'Hide runner' : 'Run it'}
            </button>
          ) : (
            <span className="no-print inline-flex items-center gap-1.5 rounded-lg border border-white/20 bg-white/10 px-2.5 py-1 text-[11px] font-semibold text-slate-300">
              Try this in the QBASIC editor (F5 to run)
            </span>
          )}
        </div>
      </div>

      <pre
        className="overflow-x-auto px-5 py-4 text-[13px] leading-[1.7]"
        style={{ background: '#0f172a', color: C_BASE }}
      >
        <code className="whitespace-pre font-mono">
          {pieces.map((p, i) =>
            p.color ? <span key={i} style={{ color: p.color }}>{p.text}</span> : <span key={i}>{p.text}</span>,
          )}
        </code>
      </pre>

      {open ? <RunnerPanel code={body} lang={detected} onClose={() => setOpen(false)} /> : null}
    </div>
  );
}

export default CodeBlock;
