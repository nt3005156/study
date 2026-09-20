/**
 * Rich text renderer for the detailed teaching notes.
 *
 * The note content is authored by us from the textbook and lives in
 * content/class-12-computer-science.json — it is trusted, static, build-time
 * data (there is no user input anywhere in it), so inline markup such as
 * <strong>, <em>, <code>, <br /> and HTML entities must be rendered as markup
 * rather than shown as literal text.
 *
 * Anything that is not a known inline tag is escaped, so stray angle brackets
 * in prose (i<j, a[i], n<0, `#include <stdio.h>`) can never break the markup.
 *
 * Do NOT use this for `code` blocks: those contain real source code and are
 * rendered as escaped text by design.
 */

// Inline tags keep prose safe; the block tags (p/ul/ol/li/table/…) are needed
// because model answers are authored as small HTML documents and must render as
// real paragraphs, bullets and tables — not as visible "<p>" / "<li>" text.
// NOTE: keep this list in sync with _ALLOWED in scripts/make_handout.py and with
// the PRE_RE language list in components/AnswerBody.tsx.
const ALLOWED =
  /^<\/?(strong|b|em|i|u|s|code|pre|br|span|sub|sup|mark|p|ul|ol|li|div|blockquote|dl|dt|dd|h4|h5|hr|table|thead|tbody|tr|td|th)(\s[^<>]*)?\/?>/i;

/** Escape every `<` that does not begin (or end) a permitted inline tag. */
export function safeRich(html: string | undefined | null): string {
  if (!html) return '';
  return String(html)
    .split('<')
    .map((chunk, i) => (i === 0 ? chunk : ALLOWED.test('<' + chunk.slice(0, 60)) ? '<' + chunk : '&lt;' + chunk))
    .join('');
}

export function Rich({ html, className }: { html?: string | null; className?: string }) {
  return <span className={className} dangerouslySetInnerHTML={{ __html: safeRich(html) }} />;
}

export function RichBlock({
  html,
  as: Tag = 'p',
  className,
}: {
  html?: string | null;
  as?: 'p' | 'h3' | 'h4' | 'div' | 'li' | 'td' | 'th';
  className?: string;
}) {
  return <Tag className={className} dangerouslySetInnerHTML={{ __html: safeRich(html) }} />;
}
