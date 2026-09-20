"""Round-4 Class-6 content migration (unit-1 "Application Areas of Computer").

- Moves the 5 "Computer in X" figures out of the Definition section and places
  each one directly after its own sub-area intro paragraph, so the side-by-side
  pairing renders every image beside its own text on desktop.
- Converts each dense sub-area paragraph into: short intro <p> + bulleted
  <list> with a "Used ... for:" title. Wording stays faithful to the original
  paragraphs (Education bullets as specified).
- Keeps the summary table at the end; updates figures_index section pointers.

Class-6 JSON only. Writes atomically (tmp + rename).
"""
import json
import os
import shutil

PATH = 'content/class-6-computer-science.json'
BACKUP = '/home/user/audit/class-6-BEFORE-R4.json'

shutil.copy2(PATH, BACKUP)
data = json.load(open(PATH))
u1 = next(u for u in data['units'] if u['unit_id'] == 'unit-1')
det = u1['detailed']

AREAS = [
    dict(h3='1. Computer in education', slug='education',
         intro=('Computers support teaching and learning at every level, '
                'in classrooms as well as online.'),
         title='Used for learning:',
         items=['Online classes &amp; online examinations',
                'Online tutoring &amp; reading e-books',
                'Practical exercises and laboratory work',
                'Audio-visual learning materials']),
    dict(h3='2. Computer in business', slug='business',
         intro=('Computers are fully used across the business sector — in '
                'department stores, restaurants, hotels and other retail centres.'),
         title='Used in business for:',
         items=['Processing sales transactions — easy and accurate',
                'Analysing investments, sales, income and expenses',
                'Studying markets and other aspects of business']),
    dict(h3='3. Computer in office', slug='office',
         intro=('Office work runs on computers, from daily correspondence '
                'to worldwide presentations.'),
         title='Used in the office for:',
         items=['Writing letters, memos and notices',
                'Sending emails and scheduling meetings',
                'Presenting business around the world through multimedia presentations',
                ('Working on the move — reading and answering email, opening '
                 'business files and posting updates on mobile devices')]),
    dict(h3='4. Computer in communication', slug='communication',
         intro=('The computer is vital to communication — it is the centrepiece '
                'of Information and Communication Technology (ICT).'),
         title='Used for communication through:',
         items=['Email and internet fax',
                'Social media, websites and blogs',
                'Video chat and online conferencing']),
    dict(h3='5. Computer in bank', slug='bank',
         intro=('Banks depend on computers to serve customers quickly and '
                'keep records accurate.'),
         title='Used in banks for:',
         items=['Handling customer transactions, withdrawals and deposits',
                'Maintaining the ledger and issuing deposit receipts',
                'Online services such as balance enquiry',
                'Online payments']),
]

app = next(s for s in det['sections'] if s['id'] == 'application-areas')
old = app['blocks']
assert [b['type'] for b in old] == (
    ['p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'h3', 'p', 'table']), \
    [b['type'] for b in old]
for area, h3block in zip(AREAS, [old[1], old[3], old[5], old[7], old[9]]):
    assert h3block['text'] == area['h3'], h3block['text']

dfs = next(s for s in det['sections'] if s['id'] == 'definition')
moved = [b for b in dfs['blocks'] if b.get('type') == 'figure']
assert len(moved) == 5, len(moved)
fig_by_slug = {}
for b in moved:
    for area in AREAS:
        if area['slug'] in b['src']:
            fig_by_slug[area['slug']] = b
assert set(fig_by_slug) == {a['slug'] for a in AREAS}, set(fig_by_slug)
dfs['blocks'] = [b for b in dfs['blocks'] if b.get('type') != 'figure']

new_blocks = [old[0]]  # section intro paragraph, unchanged
for area in AREAS:
    new_blocks += [
        {'type': 'h3', 'text': area['h3']},
        {'type': 'p', 'text': area['intro']},
        fig_by_slug[area['slug']],
        {'type': 'list', 'title': area['title'], 'items': area['items']},
    ]
new_blocks.append(old[-1])  # summary table, unchanged
app['blocks'] = new_blocks

for f in det['figures_index']:
    if f['file'] in {b['src'] for b in moved}:
        f['section'] = 'application-areas'
        f['section_title'] = 'Application Areas of Computer'

# --- asserts: each figure directly follows its intro <p> (=> side-by-side) ---
types = [b['type'] for b in app['blocks']]
assert types == ['p'] + ['h3', 'p', 'figure', 'list'] * 5 + ['table'], types
for i, b in enumerate(app['blocks']):
    if b['type'] == 'figure':
        assert app['blocks'][i - 1]['type'] == 'p'
        assert app['blocks'][i + 1]['type'] == 'list'
assert not any(b.get('type') == 'figure' for b in dfs['blocks'])
assert sum(1 for f in det['figures_index']
           if f['section'] == 'application-areas') == 5

tmp = PATH + '.tmp'
with open(tmp, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
os.replace(tmp, PATH)
print('OK — restructured unit-1/application-areas:',
      len(new_blocks), 'blocks;',
      sum(len(a["items"]) for a in AREAS), 'bullets total')
