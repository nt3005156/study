#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot repair of content/class-6-computer-science.json.

Fixes (Class 6 only):
  1. Exercise banks use {question,answer}/{term,answer} but <ExerciseBank>
     reads {q,a} -> Q&A rendered blank. Rename keys.
  2. Blocks use {type: ul/ol} which <DetailedNotes> does not render (null).
     Convert to {type: list, ordered: bool} like Classes 11/12.
  3. Figure paths are relative ("figures/...") which 404 under
     trailingSlash:true. Make them absolute ("/figures/...") like 11/12.
  4. 80 figures sit only in figures_index (bottom gallery); notes carry ZERO
     inline figures. Insert each as a `figure` block into its anchored section.
  5. 15 orphaned `diagrams` SVGs are never rendered (and have misplaced
     labels). Replace with clean SVGs and inject as `diagram` blocks.
  6. OCR garbage (watermark fragments, screenshot-label soup, truncated
     headings) + flattened tables -> surgical patches from class6_enrichment.
  7. Scaffolding (notes, key terms, objectives, revision, teaching plan)
     rebuilt to the Class 11/12 standard.

Idempotency: the script refuses to run twice (it asserts the preconditions).
Usage: python3 scripts/fix_class6.py
"""
import copy
import json
import re
import sys
from collections import Counter

sys.path.insert(0, "scripts")
import class6_enrichment as E

PATH = "content/class-6-computer-science.json"
SUPPORTED_BLOCKS = {"p", "h3", "h4", "definition", "note", "example", "teacher",
                    "code", "list", "steps", "figure", "table", "diagram"}
QA_BANKS = ("short", "long", "objective", "practical", "programming",
            "full_forms", "mcq")


def walk_strings(node, fn):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                node[k] = fn(v)
            else:
                walk_strings(v, fn)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                node[i] = fn(v)
            else:
                walk_strings(v, fn)


def main():
    with open(PATH, encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)

    # ---- precondition: not already fixed --------------------------------
    probe = data["units"][0]["detailed"]["exercise"]["short"][0]
    assert "question" in probe, "already fixed? (no {question,answer} keys found)"
    types = Counter(b.get("type") for u in data["units"]
                    for s in u["detailed"]["sections"] for b in s["blocks"])
    assert types.get("ul", 0) > 0 and types.get("ol", 0) > 0, \
        "already fixed? (no ul/ol blocks found)"

    # ---- 1. global literal substitutions ---------------------------------
    counts = {}
    for old, new, minimum in E.GLOBAL_SUBS:
        n = raw.count(old)
        assert n >= minimum, f"GLOBAL_SUB missing: {old!r} found {n}, need >={minimum}"
        counts[old[:40]] = n
        raw = raw.replace(old, new)

    # ---- 2. global regex cleanups ----------------------------------------
    for pat, rep, minimum in E.GLOBAL_RES:
        n = len(re.findall(pat, raw))
        assert n >= minimum, f"GLOBAL_RE missing: {pat!r} found {n}, need >={minimum}"
        if "mita" in pat or "mila" in pat or (pat.startswith("(?<![A-Za-z])mil")
                                              and "mild" not in pat):
            print(f"  regex {pat!r}: {n} hits")
        raw = re.sub(pat, rep, raw)
    data = json.loads(raw)

    units = {u["unit_id"]: u for u in data["units"]}

    def section(uid, sid):
        for s in units[uid]["detailed"]["sections"]:
            if s["id"] == sid:
                return s
        raise KeyError(f"section {uid}/{sid} not found")

    # ---- 3. exercise key renames ------------------------------------------
    renamed = Counter()
    for u in data["units"]:
        ex = u["detailed"]["exercise"]
        for bank in QA_BANKS:
            items = ex.get(bank)
            if not isinstance(items, list):
                continue
            for it in items:
                if "question" in it:
                    it["q"] = it.pop("question")
                    renamed["question->q"] += 1
                if "term" in it:
                    it["q"] = it.pop("term")
                    renamed["term->q"] += 1
                if "answer" in it:
                    it["a"] = it.pop("answer")
                    renamed["answer->a"] += 1
    print("exercise keys renamed:", dict(renamed))

    # ---- 4. ul/ol -> list --------------------------------------------------
    converted = Counter()
    for u in data["units"]:
        for s in u["detailed"]["sections"]:
            for b in s["blocks"]:
                if b["type"] in ("ul", "ol"):
                    b["ordered"] = (b["type"] == "ol")
                    converted[b["type"]] += 1
                    b["type"] = "list"
    print("blocks converted:", dict(converted))

    # ---- 5. figure paths absolute ------------------------------------------
    prefixed = 0
    for u in data["units"]:
        for f in u["detailed"].get("figures_index", []):
            if f.get("file") and not f["file"].startswith("/"):
                f["file"] = "/" + f["file"]
                prefixed += 1
    print("figures_index paths fixed:", prefixed)

    # ---- 6. inline figure blocks from figures_index ------------------------
    section_ids = {u["unit_id"]: {s["id"] for s in u["detailed"]["sections"]}
                  for u in data["units"]}
    inserted = 0
    for u in data["units"]:
        for f in u["detailed"].get("figures_index", []):
            assert f["section"] in section_ids[u["unit_id"]], \
                f"bad anchor {u['unit_id']}/{f['section']}"
            sec = section(u["unit_id"], f["section"])
            sec["blocks"].append({
                "type": "figure",
                "src": f["file"],
                "caption": f["caption"],
                "page": f.get("page"),
            })
            inserted += 1
    print("inline figure blocks inserted:", inserted)

    # ---- 7. diagrams: replace SVG + inject diagram blocks ------------------
    for uid, (title, svg) in E.DIAGRAMS.items():
        u = units[uid]
        assert u.get("diagrams"), f"{uid} has no legacy diagrams entry"
        u["diagrams"][0]["svg"] = svg
        u["diagrams"][0]["title"] = title
        first = u["detailed"]["sections"][0]
        first["blocks"].append({"type": "diagram", "title": title, "svg": svg})
    print("diagram blocks injected:", len(E.DIAGRAMS))

    # ---- 8. new sections (before moves) ------------------------------------
    for uid, pos, sec in E.NEW_SECTIONS:
        secs = units[uid]["detailed"]["sections"]
        assert sec["id"] not in {s["id"] for s in secs}, f"dup section {uid}/{sec['id']}"
        secs.insert(min(pos, len(secs)), copy.deepcopy(sec))
    print("new sections:", len(E.NEW_SECTIONS))

    # ---- 9. moves (original indices) ---------------------------------------
    for uid, src, idxs, dst in E.MOVE_BLOCKS:
        s = section(uid, src)
        moved = [s["blocks"][i] for i in idxs]
        for i in sorted(idxs, reverse=True):
            del s["blocks"][i]
        section(uid, dst)["blocks"].extend(moved)
    print("moves:", len(E.MOVE_BLOCKS))

    # ---- 10. index-based ops, per section, descending ----------------------
    ops = {}  # (uid, sid) -> list of (index, rank, callable, label)

    def add(uid, sid, idx, rank, fn, label):
        ops.setdefault((uid, sid), []).append((idx, rank, fn, label))

    for uid, sid, idx, field, expect, new in E.PATCH_TEXT:
        def fn(s, i=idx, f=field, e=expect, n=new):
            old = s["blocks"][i].get(f, "")
            assert e in old, f"PATCH_TEXT mismatch {uid}/{sid}/{i}: {e!r} not in {old[:100]!r}"
            s["blocks"][i][f] = n
        add(uid, sid, idx, 2, fn, f"patch-text {uid}/{sid}/{idx}")

    for uid, sid, idx, j, expect, new in E.PATCH_ITEM:
        def fn(s, i=idx, k=j, e=expect, n=new):
            old = s["blocks"][i]["items"][k]
            assert e in old, f"PATCH_ITEM mismatch {uid}/{sid}/{i}/{k}: {e!r} not in {old[:100]!r}"
            s["blocks"][i]["items"][k] = n
        add(uid, sid, idx, 2, fn, f"patch-item {uid}/{sid}/{idx}/{j}")

    for uid, sid, idx in E.DELETE_BLOCKS:
        def fn(s, i=idx):
            del s["blocks"][i]
        add(uid, sid, idx, 0, fn, f"delete {uid}/{sid}/{idx}")

    for uid, sid, start, end, expect, blocks in E.REPLACE_SLICES:
        def fn(s, a=start, b=end, e=expect, nb=blocks):
            first = s["blocks"][a]
            hay = first.get("text") or (first.get("items") or [""])[0] or ""
            assert hay.startswith(e[:60]) or e[:60] in hay[:80], \
                f"SLICE mismatch {uid}/{sid}/{a}: {hay[:100]!r}"
            s["blocks"][a:b] = copy.deepcopy(nb)
        add(uid, sid, start, 1, fn, f"slice {uid}/{sid}/{start}:{end}")

    for uid, sid, pos, blocks in E.INSERT_BLOCKS:
        def fn(s, p=pos, nb=blocks):
            for k, b in enumerate(copy.deepcopy(nb)):
                s["blocks"].insert(p + k, b)
        add(uid, sid, pos, 3, fn, f"insert {uid}/{sid}@{pos}")

    applied = 0
    for (uid, sid), lst in sorted(ops.items()):
        sec = section(uid, sid)
        for idx, rank, fn, label in sorted(lst, key=lambda o: (-o[0], o[1])):
            fn(sec)
            applied += 1
    print("index ops applied:", applied)

    # ---- 11. retitles -------------------------------------------------------
    for (uid, sid), title in E.RETITLES.items():
        section(uid, sid)["title"] = title
    print("retitles:", len(E.RETITLES))

    # ---- 12. scaffolding ----------------------------------------------------
    for uid, sc in E.SCAFFOLD.items():
        det = units[uid]["detailed"]
        if "note" in sc:
            det["note"] = sc["note"]
        det["key_terms"] = copy.deepcopy(sc["key_terms"])
        det["learning_objectives"] = copy.deepcopy(sc["learning_objectives"])
    for uid, cards in E.QUICK_REVISION.items():
        units[uid]["detailed"]["quick_revision"] = copy.deepcopy(cards)
    for uid, plan in E.TEACHING_PLAN.items():
        units[uid]["detailed"]["teaching_plan"] = copy.deepcopy(plan)
    print("scaffolding replaced for units:", len(E.SCAFFOLD))

    # ---- 13. validation -----------------------------------------------------
    errors = []
    for u in data["units"]:
        det = u["detailed"]
        sids = {s["id"] for s in det["sections"]}
        if len(sids) != len(det["sections"]):
            errors.append(f"{u['unit_id']}: duplicate section ids")
        for s in det["sections"]:
            for b in s["blocks"]:
                if b["type"] not in SUPPORTED_BLOCKS:
                    errors.append(f"{u['unit_id']}/{s['id']}: bad block {b['type']}")
                if b["type"] == "figure" and not (b.get("src") or "").startswith("/"):
                    errors.append(f"{u['unit_id']}/{s['id']}: relative figure src")
                if b["type"] == "code" and not b.get("text"):
                    errors.append(f"{u['unit_id']}/{s['id']}: empty code block")
        ex = det["exercise"]
        for bank in QA_BANKS:
            items = ex.get(bank)
            if items is None or isinstance(items, str):
                continue
            for it in items:
                if bank == "mcq":
                    if not {"q", "options", "answer"} <= set(it):
                        errors.append(f"{u['unit_id']}: bad mcq keys {sorted(it)}")
                elif not {"q", "a"} <= set(it):
                    errors.append(f"{u['unit_id']}/{bank}: bad keys {sorted(it)}")
        for f in det.get("figures_index", []):
            if not (f.get("file") or "").startswith("/"):
                errors.append(f"{u['unit_id']}: relative index path")
            if f.get("section") not in sids:
                errors.append(f"{u['unit_id']}: broken anchor {f.get('section')}")
        for req in ("learning_objectives", "key_terms", "quick_revision",
                    "teaching_plan", "sections"):
            if not det.get(req):
                errors.append(f"{u['unit_id']}: empty {req}")
    # leftover garbage scan
    blob = json.dumps(data)
    for pat in [r"(?<![A-Za-z])A?mita(?=[\s\".,;:!?])",
                r"(?<![A-Za-z])A?mila(?=[\s\".,;:!?])",
                r"(?<![A-Za-z])mild(?=[\s\".,])",
                "\uf038", "Secureyour", "Iforgot", "viber", "BUILDINGS"]:
        hits = re.findall(pat, blob)
        if hits:
            errors.append(f"leftover {pat!r}: {len(hits)}")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors[:30]:
            print("  -", e)
        sys.exit(1)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("OK — wrote", PATH)

    # ---- summary ------------------------------------------------------------
    types = Counter(b.get("type") for u in data["units"]
                    for s in u["detailed"]["sections"] for b in s["blocks"])
    print("block types now:", dict(types))
    for u in data["units"]:
        det = u["detailed"]
        ex = det["exercise"]
        nb = sum(len(s["blocks"]) for s in det["sections"])
        print(f"  {u['unit_id']}: {len(det['sections'])} sections, {nb} blocks, "
              f"figs={sum(1 for s in det['sections'] for b in s['blocks'] if b['type']=='figure')}, "
              f"Q: short={len(ex.get('short', []))} long={len(ex.get('long', []))} "
              f"obj={len(ex.get('objective', []))} prac={len(ex.get('practical', []))} "
              f"ff={len(ex.get('full_forms', []))}, KT={len(det['key_terms'])} "
              f"LO={len(det['learning_objectives'])} QR={len(det['quick_revision'])} "
              f"TP={len(det['teaching_plan'])}")


if __name__ == "__main__":
    main()
