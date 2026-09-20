"""Round-3 Class-6 content migration.

1. Objective-question stems: lettered `<br>(a)...` sub-lines -> real <ol> so the
   (a)/(b)/... marker sits on the same line as its text with clean alignment.
2. "Match the following" stems -> side-by-side Column A / Column B tables
   (`table.match-cols`). Single-sided stems (units 2-6) get Column B rebuilt
   from the solved answer's Matches column, rotated so it is not trivially
   aligned with Column A.
3. Solved-answer matching tables get class="match-cols" for shared styling.
4. Student-only pass: delete teaching_plan blocks; strip numeric `page` keys
   (figure blocks, sections, figures_index) that rendered as "p. N" badges.

Class-6 JSON only. Writes atomically (tmp + rename).
"""
import copy
import json
import os
import re
import shutil

PATH = 'content/class-6-computer-science.json'
BACKUP = '/home/user/audit/class-6-BEFORE-R3.json'

LETTERED = re.compile(r'^\(?([a-z])[\)\.]\s+(.+)$')
MATCH_Q = re.compile(r'(?i)^match the following[\.\:]?\s*(.*)$', re.S)
WITH_SPLIT = re.compile(r'\s*[—–-]\s*with\s*:\s*', re.I)
ANSWER_ROW = re.compile(
    r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>', re.S | re.I)
MATCH_TH = re.compile(r'<th>[^<]*Match[^<]*</th>', re.I)
TAG = re.compile(r'<[^>]+>')

shutil.copy2(PATH, BACKUP)
data = json.load(open(PATH))
stats = {'q_to_ol': 0, 'q_match_2sided': 0, 'q_match_1sided': 0,
         'a_match_tagged': 0, 'q_unconverted_br': []}


def norm(s):
    return TAG.sub('', s).strip().lower().rstrip('.')


def match_table(col_a, col_b):
    assert len(col_a) == len(col_b), f'A({len(col_a)}) != B({len(col_b)})'
    rows = ['<table class="match-cols"><tr><th>Column A</th><th>Column B</th></tr>']
    for i, (a, b) in enumerate(zip(col_a, col_b)):
        letter = chr(ord('a') + i)
        rows.append(
            f'<tr><td><strong>({letter})</strong> {a}</td><td>{b}</td></tr>')
    rows.append('</table>')
    return ''.join(rows)


def convert_match_q(q, a):
    """Return new question html, or None if the shape is unexpected."""
    m = MATCH_Q.match(q.strip())
    if not m:
        return None
    rest = m.group(1).strip()
    if '<br>' in rest:  # two-sided: "(a) A1<br>(b) A2... — with: B1; B2..."
        chunks = [c.strip() for c in rest.split('<br>')]
        col_a, tail_b = [], None
        for c in chunks:
            lm = LETTERED.match(c)
            if lm and tail_b is None:
                item, extra = lm.group(2), None
                wm = WITH_SPLIT.search(item)
                if wm:  # last A chunk carries " — with: B1; B2..."
                    item, tail_b = item[:wm.start()].strip(), item[wm.end():]
                col_a.append(item)
            elif tail_b is not None:
                tail_b += ' ' + c
            else:
                return None
        if tail_b is None:
            return None
        col_b = [b.strip().rstrip('.') for b in tail_b.split(';') if b.strip()]
        if len(col_a) != len(col_b) or not col_a:
            return None
        stats['q_match_2sided'] += 1
        return 'Match the following:' + match_table(col_a, col_b)
    # one-sided: "Match the following: A1; A2; ..." — rebuild B from answer.
    col_a = [c.strip().rstrip('.') for c in rest.split(';') if c.strip()]
    rows = ANSWER_ROW.findall(a)
    if not col_a or len(rows) != len(col_a):
        return None
    for (cell_a, _), want in zip(rows, col_a):
        if norm(cell_a) != norm(want):
            return None  # answer rows must cover A in order; else don't invent
    col_b = [b.strip() for _, b in rows]
    col_b = col_b[2:] + col_b[:2]  # rotate: practice, not a giveaway
    stats['q_match_1sided'] += 1
    return 'Match the following:' + match_table(col_a, col_b)


def convert_lettered_q(q):
    chunks = [c.strip() for c in q.split('<br>')]
    if len(chunks) < 2:
        return None
    items = []
    for c in chunks[1:]:
        lm = LETTERED.match(c)
        if not lm:
            return None
        items.append(lm.group(2))
    stats['q_to_ol'] += 1
    return chunks[0] + '<ol>' + ''.join(f'<li>{t}</li>' for t in items) + '</ol>'


for u in data['units']:
    det = u.get('detailed') or {}
    # --- student-only: drop teaching plans + numeric page keys ---
    det.pop('teaching_plan', None)
    for f in det.get('figures_index', []):
        f.pop('page', None)
    for s in det.get('sections', []):
        s.pop('page', None)
        for b in s.get('blocks', []):
            if b.get('type') == 'figure':
                b.pop('page', None)
    # --- exercise banks ---
    for bank in ('short', 'long', 'programming', 'practical', 'full_forms',
                 'objective'):
        for i, it in enumerate(det.get('exercise', {}).get(bank) or []):
            q, a = it['q'], it['a']
            if MATCH_Q.match(q.strip()):
                new_q = convert_match_q(q, a)
                assert new_q, f'UNPARSED matching Q {u["unit_id"]}.{bank}#{i}: {q[:100]}'
                it['q'] = new_q
            elif '<br>' in q:
                new_q = convert_lettered_q(q)
                if new_q:
                    it['q'] = new_q
                else:
                    stats['q_unconverted_br'].append(
                        f'{u["unit_id"]}.{bank}#{i}: {q[:90]}')
            if '<table' in a and MATCH_TH.search(a) and 'match-cols' not in a:
                it['a'] = a.replace('<table>', '<table class="match-cols">', 1)
                stats['a_match_tagged'] += 1

blob = json.dumps(data, ensure_ascii=False)
assert '"teaching_plan"' not in blob, 'teaching_plan left!'
assert '"page":' not in blob, 'numeric page key left!'
assert stats['q_match_2sided'] + stats['q_match_1sided'] == 6, stats
assert stats['a_match_tagged'] == 6, stats
leftover = [f"{u['unit_id']}" for u in data['units']
            for it in ((u.get('detailed') or {}).get('exercise', {}).get('objective') or [])
            if re.search(r'<br>\(?[a-z][\.\)]', it['q'])]
assert not leftover, leftover

tmp = PATH + '.tmp'
with open(tmp, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
os.replace(tmp, PATH)
print('stats:', stats)
print('OK — wrote', PATH, f'({len(blob)} chars)')

# samples
d2 = json.load(open(PATH))
u1 = next(u for u in d2['units'] if u['unit_id'] == 'unit-1')
print('U1 match Q:', u1['detailed']['exercise']['objective'][3]['q'][:330])
u2 = next(u for u in d2['units'] if u['unit_id'] == 'unit-2')
print('U2 match Q:', u2['detailed']['exercise']['objective'][3]['q'][:330])
print('U2 match A head:', u2['detailed']['exercise']['objective'][3]['a'][:140])
u6 = next(u for u in d2['units'] if u['unit_id'] == 'unit-6')
print('U6 TF Q:', u6['detailed']['exercise']['objective'][0]['q'][:220])
