#!/usr/bin/env python3
"""
Rebuild the Class 6 and Class 7 route files from the Class 8 template.

The repository's git history has rolled back more than once, and each time it
takes app/class-7/ and app/class-6/computer-science/[unit]/ with it, while
content/ and public/figures/ (both untracked or modified) survive. This
script restores the missing pages.

It is idempotent: running it on a healthy tree changes nothing.

    python3 scripts/restore_class67_pages.py
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLURBS = {
    6: ("Essentials of Computer Science for Grade 6, 15 chapters. Each chapter carries notes "
        "with the textbook's figures and tables, plus the exercise question bank with solved "
        "answers."),
    7: ("Essentials of Computer Science for Grade 7, 21 chapters. Each chapter carries notes "
        "with the textbook's figures and tables, plus the exercise question bank with solved "
        "answers."),
}

NOTE_BLOCK = (
    "chapter ({[\n"
    "                        `${detailed.exercise.short.length} short`,\n"
    "                        `${detailed.exercise.long.length} long`,\n"
    "                        detailObjectiveCount > 0 ? `${detailObjectiveCount} objective` : '',\n"
    "                        detailProgrammingCount > 0 ? `${detailProgrammingCount} programming` : '',\n"
    "                        detailPracticalCount > 0 ? `${detailPracticalCount} practical` : '',\n"
    "                        detailed.exercise.mcq.length > 0 ? `${detailed.exercise.mcq.length} multiple-choice` : '',\n"
    "                      ].filter(Boolean).join(', ')} questions{detailed.exercise.mcq.length > 0 ? ' with answer key' : ''}) is given in full in\n"
    "                      the <a href=\"#exercise\" className=\"text-amber-deep font-semibold underline\">{detailed.exercise_heading ?? `Exercise ${unit.chapter.replace('Chapter ', '')}`}</a> section\n"
    "                      below, with a solved model answer for every question."
)

CLASS7_PAGE = '''import Link from 'next/link';
import { ArrowRight, Monitor } from 'lucide-react';
import { Breadcrumbs } from '@/components/Breadcrumbs';

export const metadata = { title: 'Class 7 — Computer Science | Study Platform', description: 'Class 7 Computer Science study materials verified against textbook.' };

export default function Class7Page() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials', href: '/browse' }, { label: 'Class 7' }]} />
      <section aria-label="Class 7" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24 pt-6">
        <div className="text-center mb-12">
          <h1 className="font-serif text-5xl sm:text-7xl font-bold text-ink tracking-tight mb-4">Class 7</h1>
          <p className="text-stone text-lg max-w-xl mx-auto">Essentials of Computer Science — 21 chapters with detailed teaching notes and solutions.</p>
        </div>
        <div className="max-w-md mx-auto">
          <Link href="/class-7/computer-science" className="group block rounded-3xl bg-white border border-slate-100 p-8 shadow-xl shadow-slate-200/20 hover:shadow-2xl hover:-translate-y-1 transition-all" aria-label="Computer Science">
            <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-ink to-slate text-white flex items-center justify-center text-2xl mb-5 shadow-lg shadow-ink/20 group-hover:scale-105 transition-transform">\U0001f4bb</div>
            <h2 className="text-2xl font-extrabold text-ink mb-2">Computer Science</h2>
            <p className="text-sm text-stone leading-relaxed mb-5">Essentials of Computer Science by Asmita Publication. 21 chapters covering fundamentals, history and generations, hardware and software, operating systems, MS Office, webpage design, ICT, ethics and cyber law, networking, number systems, graphics, multimedia and QBASIC programming.</p>
            <div className="flex items-center gap-2 text-sm font-bold text-ink group-hover:text-amber-deep transition"><Monitor size={18} /> View Materials <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" /></div>
          </Link>
        </div>
      </section>
    </>
  );
}
'''


def p(*parts):
    return os.path.join(ROOT, *parts)


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def apply_note_patch(src):
    """Make the question-count sentence list only the banks a chapter has."""
    if 'detailObjectiveCount' not in src:
        src = src.replace(
            "  const detailProgrammingCount = detailed?.exercise?.programming?.length ?? 0;",
            "  const detailProgrammingCount = detailed?.exercise?.programming?.length ?? 0;\n"
            "  const detailObjectiveCount = detailed?.exercise?.objective?.length ?? 0;")
    old = re.search(
        r"chapter \(\{detailed\.exercise\.short\.length\} short.*?solved model answer for every question\.",
        src, re.S)
    if old:
        src = src[:old.start()] + NOTE_BLOCK + src[old.end():]
    return src


def main():
    template = read(p('app', 'class-8', 'computer-science', '[unit]', 'page.tsx'))
    index_template = read(p('app', 'class-8', 'computer-science', 'page.tsx'))

    for c in (6, 7):
        # --- the dynamic unit route -------------------------------------
        static_dir = p('app', 'class-%d' % c, 'computer-science', 'unit-1')
        if os.path.isdir(static_dir):
            shutil.rmtree(static_dir)
            print('removed stale static route:', os.path.relpath(static_dir, ROOT))

        unit_page = p('app', 'class-%d' % c, 'computer-science', '[unit]', 'page.tsx')
        src = (template
               .replace('class-8-computer-science', 'class-%d-computer-science' % c)
               .replace('/class-8', '/class-%d' % c)
               .replace('Class 8', 'Class %d' % c))
        write(unit_page, apply_note_patch(src))
        print('wrote', os.path.relpath(unit_page, ROOT))

        # --- the chapter list -------------------------------------------
        list_page = p('app', 'class-%d' % c, 'computer-science', 'page.tsx')
        src = (index_template
               .replace('class-8-computer-science', 'class-%d-computer-science' % c)
               .replace('/class-8', '/class-%d' % c)
               .replace('Class 8', 'Class %d' % c))
        src = re.sub(r'(<p className="text-stone text-lg max-w-2xl mx-auto">\s*\n\s*).*?(\n\s*</p>)',
                     lambda m: m.group(1) + BLURBS[c] + m.group(2), src, flags=re.S)
        write(list_page, src)
        print('wrote', os.path.relpath(list_page, ROOT))

    # --- Class 7 landing page (absent from the original repo) ------------
    write(p('app', 'class-7', 'page.tsx'), CLASS7_PAGE)
    print('wrote app/class-7/page.tsx')

    # --- Class 8 unit page needs the same note patch ---------------------
    c8 = p('app', 'class-8', 'computer-science', '[unit]', 'page.tsx')
    patched = apply_note_patch(read(c8))
    if patched != read(c8):
        write(c8, patched)
        print('wrote app/class-8/computer-science/[unit]/page.tsx (note patch)')

    # --- browse + home copy ---------------------------------------------
    browse = p('app', 'browse', 'page.tsx')
    src = read(browse)
    src = src.replace(
        "{ c: 7, name: 'Class 7', desc: 'Essentials of Computer Science — chapters on hardware, software, OS.', subjects: ['Computer Science'], icon: '\U0001f4d8' },",
        "{ c: 7, name: 'Class 7', desc: 'Essentials of Computer Science — 21 chapters.', subjects: ['Computer Science'], icon: '\U0001f4d8' },")
    src = src.replace(
        "{ c: 8, name: 'Class 8', desc: 'Computer Science — revised edition.', subjects: ['Computer Science'], icon: '\U0001f4bb' },",
        "{ c: 8, name: 'Class 8', desc: 'Essentials of Computer Science — 11 chapters, complete course.', subjects: ['Computer Science'], icon: '\U0001f4bb' },")
    write(browse, src)
    print('wrote app/browse/page.tsx')

    print('\ndone. Now run:  npm install  &&  npm run build')


if __name__ == '__main__':
    main()
