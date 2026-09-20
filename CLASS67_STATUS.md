# Class 6 & 7 — status

**Commit `898d0e6`** · live preview on port 3000 · build clean · 74/74 unit routes return 200

## What was done this round

Everything below was rebuilt from scratch, because the workspace reset had
wiped the source PDFs, the extracted text and the Python packages.

### 1. Recovered the source text
- Reinstalled `pymupdf` + `rapidocr-onnxruntime`.
- Re-downloaded both books into **`/tmp`** (never `/home/user`, to protect the
  snapshot quota).
- **Fixed a real extraction bug:** `page.get_text()` returns blocks in
  content-stream order, which put figure captions and sidebars ahead of the
  body text. Pages are now sorted by `(y, x)`, so the prose comes out in true
  reading order.
- Re-OCR'd the 59 image-only Class 6 pages (Class 7's 5 blanks are genuinely
  blank).

### 2. Rebuilt both content files from the real books
- Chapter spans are derived **from the text itself** (first page carrying an
  `(N+1).x` heading), because the printed Contents ranges are off by a page or
  two — e.g. ch3 really starts at printed 23, not 25.
- Result: **Class 6 — 15 chapters, Class 7 — 21 chapters**, matching the real
  books.

### 3. Notes for all 35 remaining chapters
Structured sections with paragraphs, sub-headings, ordered/unordered lists and
tables. Noise that was polluting the first attempts is now filtered: diagram
label clusters (`Ctrl`, `Alt`, `Enter`, `SanDisk`), duplicate sidebar text, and
running footers.

| | chapters | sections | blocks |
|---|---|---|---|
| Class 6 | 15 | 121 | 320 |
| Class 7 | 21 | 108 | 378 |

### 4. Full exercise bank for all 35 chapters
~1,000 real questions extracted from the books and answered:

- **Objective sets** — rewrite-the-statement, true/false (with corrections),
  fill in the blanks, matching
- **Full forms**, **short notes**, **short answers**, **long answers**, **project work**

**Answers are our own work in our own words.** The textbooks print no answer
key, so nothing was copied. The deterministic types (true/false, fill, match,
rewrite, full forms) are hand-authored per chapter in `work/key_c6.py` and
`work/key_c7.py`. The descriptive answers are composed from each chapter's own
notes, using only complete sentences that state something.

An early attempt to solve the deterministic types by rule was **rejected** —
it marked every true/false statement as True — which is why they are
hand-authored instead.

### 5. Teaching scaffolding
Every chapter now has learning objectives, quick-revision cards and a
period-by-period teaching plan.

## Verification
- `npx next build` compiled cleanly; 92 static pages.
- **74/74 unit routes and all 7 landing pages return HTTP 200.**
- Escaped-markup scan across all 74 pages: the only 11 hits are inside
  `<code>` samples in the HTML/JavaScript chapters, where escaped tags are the
  lesson content — **0 real leaks**.

## Figures — done (second pass)

**179 real figures extracted from the PDFs**, cropped and filed under the
section they illustrate: **80 for Class 6 (5.2 MB)**, **99 for Class 7
(6.5 MB)**. Every chapter of Class 6 and all but one chapter of Class 7 now
carry figures; the software chapters that carry no `Figure:` caption are
covered by screenshots labelled from the heading above them.

How they were made:

- **Captioned figures** (119) are located by scoring every graphic block on the
  page by area and distance to its `Figure:` caption.
- **Scanned pages have no text layer**, so `search_for` cannot find the
  caption there — those fall back to ranking the page's graphic blocks by area
  and matching them to the captions in reading order. That recovered 21 of the
  22 figures the caption method missed.
- **Uncaptioned screenshots** (chapters 9–11) are labelled from the nearest
  heading above the image.

**Pruned:** 53 decorative chapter-opener banners were caught and deleted —
they repeated the same artwork at the start of every chapter and had been
captioned with the *next* chapter's title.

### Quota
Persisted workspace is **84 MB** against the ~128 MB snapshot cap — 44 MB of
headroom. `node_modules`, `.next`, `dist` and `.npm` are snapshot-excluded and
so do not count. The extractors carry a hard byte guard that stops the run
rather than risk blowing the cap.

### Verification
- 74/74 unit routes and all 7 landing pages return 200.
- **720 figures referenced across all 7 classes; 0 missing, 0 orphans.**
- All 179 new figures resolve over HTTP and their section anchors point to
  real section ids (0 broken anchors).

Note that `public/figures/` is gitignored by design, so the image files are
not in the commit — they live in the workspace and are bundled into the zip.
The regenerating scripts are in `work/`.
