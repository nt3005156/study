/** Build-time search index for the static export.
 *
 * The site ships as `output: export` (no server), so global search runs
 * client-side against this JSON file, generated fresh on every build and
 * served from /search-index.json. Run via `npm run build`.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

const strip = (s) =>
  String(s ?? '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();

const entries = [];
for (const n of [6, 7, 8, 9, 10, 11, 12]) {
  const book = JSON.parse(readFileSync(join(root, `content/class-${n}-computer-science.json`), 'utf8'));
  for (const u of book.units ?? []) {
    const base = `/class-${n}/computer-science/${u.unit_id}`;
    const chapterLabel = strip(u.chapter || '');
    const chapterTitle = strip(u.detailed?.chapter_title || u.title || '');
    const ctx = `class ${n} ${chapterLabel} ${chapterTitle}`.toLowerCase();
    entries.push({
      k: 'chapter',
      t: chapterTitle || chapterLabel,
      s: `Class ${n}${chapterLabel ? ` · ${chapterLabel}` : ''}`,
      h: base,
      x: `${ctx} chapter unit`,
    });
    for (const s of u.detailed?.sections ?? []) {
      const t = strip(s.title || '');
      if (t) entries.push({ k: 'section', t, s: `Class ${n} · ${chapterTitle || chapterLabel}`, h: `${base}#sec-${s.id}`, x: `${ctx} ${t}`.toLowerCase() });
    }
    for (const k of u.detailed?.key_terms ?? []) {
      const t = strip(k.term);
      if (t) entries.push({ k: 'term', t, s: `Class ${n} · ${chapterTitle || chapterLabel}`, h: `${base}#key-terms`, x: `${ctx} ${t}`.toLowerCase() });
    }
    const ex = u.detailed?.exercise;
    if (ex) {
      for (const bank of [ex.short, ex.long, ex.objective, ex.programming, ex.practical, ex.full_forms, ex.mcq]) {
        for (const item of bank ?? []) {
          const t = strip(item.q);
          if (!t) continue;
          entries.push({
            k: 'question',
            t: t.length > 90 ? `${t.slice(0, 90)}…` : t,
            s: `Class ${n} · ${chapterTitle || chapterLabel}`,
            h: `${base}#exercise`,
            x: `${ctx} ${t}`.toLowerCase(),
          });
        }
      }
    }
  }
}

const out = join(root, 'public', 'search-index.json');
mkdirSync(join(root, 'public'), { recursive: true });
writeFileSync(out, JSON.stringify(entries));
console.log(`search-index: ${entries.length} entries, ${(JSON.stringify(entries).length / 1024).toFixed(0)} KB -> public/search-index.json`);
