#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class 6 round-2 fixes (content layer only; components are edited by hand).

  1. Regenerate the 15 diagram SVGs with working connector arrows (the old
     `_arrow` helper stripped every space from its <line>/<polygon> tags, so
     no arrow rendered). Updates both the `diagram` blocks and the legacy
     top-level `diagrams` entries. Every SVG is XML-validated.
  2. Restructure objective-bank answers into lists/tables:
       - (a),(b),... answers  -> <ol><li> (lettering supplied by CSS)
       - Term -> match answers -> <table> (like unit-1's matching answer)
     plus two typo fixes and real corrections for unit-6 items (f)-(j),
     which were bare statements with no answer.
  3. Restructure objective-bank questions for readability: one sub-part per
     line, lettered (a),(b),... to match the answers.

Usage: python3 scripts/fix_class6_round2.py
"""
import copy
import json
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, "scripts")
import class6_enrichment as E

PATH = "content/class-6-computer-science.json"

TYPO_SUBS = [
    # (old, new, minimum_expected_count)
    ("True. SsD is a non-volatile memory with high storage capacity.",
     "True. SSD is a non-volatile memory with high storage capacity.", 1),
    ("/ SsD is a non-volatile memory with high storage capacity.",
     "/ SSD is a non-volatile memory with high storage capacity.", 1),
    ("in a variety of file formats such as JPEG, PNG, BMP and GIF "
     "formats such as PNG, JPEG, BMP and GIF.",
     "in a variety of file formats such as JPEG, PNG, BMP and GIF.", 1),
]

# Unit-6 rewrite items (f)-(j) were bare statements with no correction.
# Corrections below are grounded in the chapter's own notes.
U6_CORRECTIONS = [
    ("<strong>(f)</strong> ICT is not used in the entertainment sector.",
     "<strong>(f)</strong> False. ICT <strong>is</strong> used in the entertainment "
     "sector — for video editing, special effects, animations, cartoon movies "
     "and booking cinema tickets online."),
    ("<strong>(g)</strong> The full form of ICT is International Computing Technology.",
     "<strong>(g)</strong> False. The full form of ICT is "
     "<strong>Information and Communication Technology</strong>."),
    ("<strong>(h)</strong> ICT is used in the banking sector to replace the manual system.",
     "<strong>(h)</strong> True. In the banking sector manual records are replaced "
     "by <strong>core banking software</strong>."),
    ("<strong>(i)</strong> The cyber law in Nepal is called Electronic Transaction Act 2063.",
     "<strong>(i)</strong> True. The Electronic Transaction Act, 2063 (2008 A.D.) "
     "is the cyber law of Nepal."),
    ("<strong>(j)</strong> Cyber law doesn't address the legal issues related "
     "to intellectual property.",
     "<strong>(j)</strong> False. Cyber law <strong>does</strong> address intellectual "
     "property — Intellectual Property Law is one of its five areas."),
]


def convert_answer(uid, a):
    """Return restructured answer HTML. Raises on unexpected shapes."""
    if "<table>" in a:
        return a, "kept-table"
    paras = re.findall(r"<p>(.*?)</p>", a, re.DOTALL)
    assert paras, f"{uid}: no <p> blocks in objective answer"
    pieces = []
    for p in paras:
        for chunk in re.split(r"<br\s*/?>", p):
            chunk = chunk.strip()
            if chunk:
                pieces.append(chunk)
    lettered = [bool(re.match(r"^<strong>\([a-z]\)", pc)) for pc in pieces]
    if all(lettered):
        items = []
        for i, pc in enumerate(pieces):
            m = re.match(r"^<strong>\(([a-z])\)\s*([^<]*)</strong>\s*(.*)$",
                         pc, re.DOTALL)
            assert m, f"{uid}: bad lettered piece: {pc[:80]!r}"
            assert m.group(1) == chr(ord("a") + i), \
                f"{uid}: letter order broken at item {i}: {pc[:60]!r}"
            verdict, rest = m.group(2).strip(), m.group(3).strip()
            # Unit-1 true/false keeps its verdict ("True."/"False."); the
            # (a),(b),... lettering is supplied by the <ol> styling instead.
            items.append(f"<li>{('<strong>' + verdict + '</strong> ') if verdict else ''}{rest}</li>")
        return "<ol>" + "".join(items) + "</ol>", f"ol-{len(items)}"
    if all("→" in pc for pc in pieces):
        rows = []
        for pc in pieces:
            m = re.match(r"^<strong>(.*?)</strong>\s*→\s*(.*)$", pc, re.DOTALL)
            assert m, f"{uid}: bad matching piece: {pc[:80]!r}"
            rows.append(f"<tr><td><strong>{m.group(1)}</strong></td>"
                        f"<td>{m.group(2)}</td></tr>")
        return ("<table><tr><th>Item</th><th>Matches</th></tr>"
                + "".join(rows) + "</table>", f"table-{len(rows)}")
    raise AssertionError(f"{uid}: mixed/unexpected objective answer shape: {a[:120]!r}")


def convert_question(uid, q, n_answers):
    """One sub-part per line; lettered to match the answers."""
    if re.search(r"\([b-h]\)", q):
        # Already lettered inline (unit-1 style): break lines before (b)..(h).
        out = re.sub(r"\s+(?=\([b-h]\))", "<br>", q).strip()
        assert out.count("<br>") == n_answers - 1, \
            f"{uid}: question break count {out.count('<br>')} != answers {n_answers}"
        return out
    if " / " in q:
        head, rest = q.split(":", 1) if ":" in q else ("", q)
        parts = [p.strip().rstrip(".") for p in rest.split(" / ")]
        parts = [p for p in parts if p]
        if len(parts) == n_answers:
            lines = [f"({chr(ord('a') + i)}) {p}" for i, p in enumerate(parts)]
        else:
            lines = parts  # keep unlettered rather than risk a mismatch
        return head.strip() + ":<br>" + "<br>".join(lines)
    return q  # single-part question; nothing to split


def main():
    with open(PATH, encoding="utf-8") as f:
        raw = f.read()

    for old, new, minimum in TYPO_SUBS:
        n = raw.count(old)
        assert n >= minimum, f"typo pattern missing: {old[:60]!r}"
        raw = raw.replace(old, new)
    for old, new in U6_CORRECTIONS:
        n = raw.count(old)
        assert n == 1, f"unit-6 correction anchor found {n}x: {old[:60]!r}"
        raw = raw.replace(old, new)
    print("typos + unit-6 corrections applied")

    data = json.loads(raw)
    units = {u["unit_id"]: u for u in data["units"]}

    # ---- 1. regenerate diagrams --------------------------------------
    for uid, (title, svg) in E.DIAGRAMS.items():
        ET.fromstring(svg)  # XML must parse
        assert "<line x1=" in svg or "<line x1" not in svg.replace(" ", ""), uid
        assert "<linex1" not in svg and "<polygonpoints" not in svg, uid
        u = units[uid]
        u["diagrams"][0]["svg"] = svg
        u["diagrams"][0]["title"] = title
        hits = [b for s in u["detailed"]["sections"] for b in s["blocks"]
                if b.get("type") == "diagram"]
        assert len(hits) == 1, f"{uid}: {len(hits)} diagram blocks"
        hits[0]["svg"] = svg
        hits[0]["title"] = title
    u1svg = units["unit-1"]["detailed"]["sections"][0]["blocks"][-1]["svg"]
    assert "<polygon points='142,74 133,69 133,79' fill='#0f172a'/>" in u1svg
    print("diagrams regenerated + XML-validated: 15")

    # ---- 2+3. objective answers + questions ---------------------------
    stats = {}
    for u in data["units"]:
        for it in u["detailed"]["exercise"].get("objective", []):
            new_a, kind = convert_answer(u["unit_id"], it["a"])
            n_items = len(re.findall(r"<li>|<tr><td>", new_a))
            it["q"] = convert_question(u["unit_id"], it["q"], n_items)
            it["a"] = new_a
            stats[kind] = stats.get(kind, 0) + 1
    print("objective answers converted:", stats)

    # ---- validation ---------------------------------------------------
    errors = []
    for u in data["units"]:
        for it in u["detailed"]["exercise"].get("objective", []):
            a = it["a"]
            if not (a.startswith("<ol>") or a.startswith("<table>")):
                errors.append(f"{u['unit_id']}: answer not restructured: {a[:60]!r}")
            if re.search(r"<br\s*/?>", a):
                errors.append(f"{u['unit_id']}: leftover <br> in answer")
            if "<strong>(a)</strong>" in a:
                errors.append(f"{u['unit_id']}: leftover letter prefix in answer")
            if " / " in it["q"]:
                errors.append(f"{u['unit_id']}: unconverted / in question: {it['q'][:70]!r}")
    blob = json.dumps(data)
    for bad in ["<linex1", "<polygonpoints", "SsD is a non-volatile",
                "BMP and GIF formats such as"]:
        if bad in blob:
            errors.append(f"leftover {bad!r}")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors[:20]:
            print("  -", e)
        sys.exit(1)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("OK — wrote", PATH)


if __name__ == "__main__":
    main()
