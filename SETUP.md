# study.companion — setup guide

A Next.js site that turns the *Essentials of Computer Science* textbooks
(Classes 6–12, Asmita Publication) into teachable web pages: detailed
unit-by-unit notes with the textbook's own figures, plus the full exercise
question bank with a solved answer for every question.

This zip contains everything needed to run it. No database, no API keys, no
environment variables.

---

## 1. What you need

- **Node.js 18.17 or newer** (Next.js 14 requires it). Check with `node -v`.
- **npm** (comes with Node).

That is all. The content is plain JSON already committed here, and the
figures are ordinary JPEG/PNG files.

---

## 2. Run it locally

```bash
cd study-platform
npm install
npm run dev
```

Then open <http://localhost:3000>.

`npm install` takes roughly 10–20 seconds and pulls about 390 packages.

---

## 3. Build a static site

The project is configured as a static export (`output: 'export'`), so it
produces plain HTML that can be served by anything — no Node server needed
at runtime.

```bash
npm run build
```

This writes the whole site to **`dist/`**, including `public/figures/`, which
Next.js copies across automatically as part of the export — there is nothing
to copy by hand. You can confirm afterwards:

```bash
find dist/figures -type f | wc -l    # -> 720
```

Then serve `dist/` with any static server:

```bash
cd dist && python3 -m http.server 3000
```

or `npx serve dist`, or upload the folder to Netlify, Vercel, GitHub Pages,
an S3 bucket or a school web server.

**Open the pages with a trailing slash** (`/class-8/computer-science/unit-1/`).
`trailingSlash: true` is set, so directory-style URLs are what the export
produces.

---

## 4. Project layout

```
app/
  page.tsx                  home
  browse/page.tsx           pick a class
  class-<N>/page.tsx        class landing page
  class-<N>/computer-science/
      page.tsx              chapter list
      [unit]/page.tsx       the chapter itself  (one route for every unit)
  globals.css               Tailwind + fonts (Plus Jakarta Sans, Literata)
  layout.tsx                shell, header, footer

components/
  DetailedNotes.tsx         renders the notes (sections → blocks)
  ExerciseBank.tsx          the question banks and interactive MCQ
  AnswerBody.tsx            lifts <pre data-lang> blocks out of answers
  CodeBlock.tsx             Copy + "Run it" (OneCompiler iframe)
  Rich.tsx                  safe HTML renderer
  UnitSplitView.tsx         notes beside Q&A on wide screens
  Breadcrumbs.tsx  Header.tsx  Footer.tsx  PrintButton.tsx

content/
  class-6-computer-science.json   15 chapters
  class-7-computer-science.json   21 chapters
  class-8-computer-science.json   11 chapters
  class-9-computer-science.json    7 chapters
  class-10-computer-science.json   5 chapters
  class-11-computer-science.json   8 chapters
  class-12-computer-science.json   7 chapters

public/figures/             figures extracted from the PDFs (541 files)
```

### Config files

| File | Purpose |
|---|---|
| `next.config.js` | static export, `dist` output dir, trailing slashes, unoptimised images |
| `tailwind.config.ts` | theme colours and fonts |
| `tsconfig.json` | TypeScript settings, `@/*` path alias |
| `postcss.config.js` | Tailwind/Autoprefixer |

---

## 5. How the content JSON is shaped

Each file is `{ class, subject, book, units: [...] }`. A unit looks like:

```jsonc
{
  "unit_id": "unit-1",
  "chapter": "Chapter 1",
  "title": "Introduction to Computers",
  "pages": "1–12",
  "overview": "...", "summary": "...", "concepts": [], "questions": {...},
  "detailed": {
    "heading": "Chapter 1 — Introduction to Computers",
    "book_pages": "1–12",
    "chapter_number": "1",
    "chapter_title": "Introduction to Computers",
    "note": "...",
    "learning_objectives": ["..."],
    "sections": [
      { "id": "definition", "number": "1.2", "title": "Definition of Computer",
        "page": 2,
        "blocks": [
          { "type": "p",    "text": "<p>…</p>" },
          { "type": "definition", "term": "Computer", "text": "…" },
          { "type": "table", "head": ["Term","Meaning"], "rows": [["Data","…"]] },
          { "type": "figure", "src": "figures/class6/working-process.jpg", "caption": "…" },
          { "type": "code",  "lang": "python", "text": "…" }
        ] }
    ],
    "figures_index": [ { "file": "figures/…", "caption": "…", "section": "definition" } ],
    "exercise": {
      "full_forms": [ { "q": "AI", "a": "Artificial Intelligence" } ],
      "objective":  [ { "q": "…", "a": "…" } ],
      "short":      [ { "q": "…", "a": "…" } ],
      "long":       [ { "q": "…", "a": "…" } ],
      "programming":[ { "q": "…", "a": "…" } ],
      "practical":  [ { "q": "…", "a": "…" } ],
      "mcq": [ { "q": "…", "options": ["…"], "answer": 2, "teacher_note": "…" } ]
    },
    "exercise_heading": "Exercise 1",
    "key_terms": [ { "term": "…", "meaning": "…" } ],
    "quick_revision": [ { "title": "…", "points": ["…"] } ],
    "teaching_plan": [ { "period": "…", "topic": "…", "activity": "…" } ]
  }
}
```

### Block types

`p`, `h3`, `ul`, `ol`, `definition`, `note`, `table`, `figure`, `code`.

### Two things worth knowing

- **Question bank names.** `full_forms` renders as "Write the full form of";
  `objective` covers the rewrite-the-statement, true/false, fill-in and
  matching drills used by the Class 6 and 7 books; `mcq` is the only
  interactive bank. Every bank is optional and hidden when empty.
- **Code blocks.** Write code in an answer as
  `<pre data-lang="python"><code>…</code></pre>` and `AnswerBody` lifts it
  into a runnable `CodeBlock` with Copy and "Run it". Never pass code through
  the rich-text renderer — it contains real `<stdio.h>`, `a[i]`, `i < j`.

---

## 6. Adding or editing content

Edit the JSON, then rebuild. Unit pages are generated from the JSON at build
time, so a new chapter needs no new page file — add a unit and its route
appears.

If you add figures, put them in `public/figures/` and reference them as
`figures/<your-folder>/<name>.jpg` (no leading slash).

---

## 7. Notes and gotchas

- **Figures are gitignored.** `.gitignore` excludes `public/figures/`
  because they are large binaries, so a `git clone` will **not** have them.
  This zip includes all 541 so the site works out of the box. If you pull a
  fresh clone, copy the figures back from this zip.
- **The static export needs `dist/figures`.** See the build step above.
- **Empty arrays in the JSON break Next's type check.** Unit pages read
  `detailed` through an explicit cast for this reason. Keep that cast if you
  edit the page.
- **Node 18.17+.** Next.js 14 refuses to build on older versions.
- **Not included here** (generated outputs, not needed to run the site):
  `handouts/` (printable HTML), `docs/` (markdown exports), `scripts/`
  (the handout generator).

---

## 8. Current content status

| Class | Chapters | Notes |
|---|---|---|
| 6 | 15 | Chapter 1 done; 2–15 pending |
| 7 | 21 | structure rebuilt; notes pending |
| 8 | 11 | **complete** |
| 9 | 7 | **complete** |
| 10 | 5 | **complete** |
| 11 | 8 | **complete** |
| 12 | 7 | **complete** |

Exercises are answered in our own words rather than copied from the
textbook, and every MCQ carries a short teacher note explaining why the
right answer is right.
