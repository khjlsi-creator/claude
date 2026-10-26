# -*- coding: utf-8 -*-
"""레이아웃 카탈로그 렌더링: RL24종 + PL9종의 견본 이미지와 영역 좌표(JSON)를 만든다."""
import json, os, subprocess, glob, sys
from PIL import Image
import slots
from compose import compose, make
from layouts import LAYOUTS, PAGES, K
from recipes import NOTE

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SC = 166.9
# --- RL: 레이아웃마다 새 쪽
nodes = []
for i, L in enumerate(LAYOUTS):
    if i: nodes.append(dict(t='newpage'))
    nodes += L['nodes']
d, f = compose(dict(start_no=1, first='odd', note=NOTE, nodes=nodes), OUT + '/rl.pptx')
subprocess.run(f'cd {OUT} && soffice --headless --convert-to pdf rl.pptx >/dev/null 2>&1 && rm -f rl-*.png && pdftoppm -r {SC} -png rl.pdf rl', shell=True)
pages = sorted(glob.glob(OUT + '/rl-*.png'))
# placed → 레이아웃별 묶기(쪽 번호로)
spec = {}
for L in LAYOUTS:
    spec[L['id']] = dict(id=L['id'], name=L['name'], when=L['when'], src=L['src'], blocks=[])
by_page = {}
for pl, blk in zip(f.placed, f.placed_blocks):
    by_page.setdefault(pl['page'], []).append((pl, blk))
for i, L in enumerate(LAYOUTS):
    items = by_page[i + 1]
    y0 = items[0][0]['y']; x0 = items[0][0]['x0']
    ymax = max(p['y'] + p['h'] for p, _ in items)
    im = Image.open(pages[i]).convert('RGB')
    cx0, cy0 = max(0, x0 - 8), max(0, int(y0 - 48 - 6))
    crop = im.crop((cx0, cy0, min(1380, x0 + 1158), min(im.height, int(ymax - 48 + 8))))
    fn = f"{L['id'].lower()}.png"
    crop.save(f'{OUT}/{fn}')
    sl = []
    for pl, blk in items:
        dy = pl['y'] - y0
        for name, x, y, w, h in blk.slots(1150):
            sl.append(dict(name=name, x=round(x), y=round(y + dy), w=round(w), h=round(h), block=pl['cls']))
    spec[L['id']].update(img=fn, iw=crop.width, ih=crop.height, ox=x0 - cx0, oy=y0 - 48 - cy0, slots=sl,
                        blocks=[dict(cls=p['cls'], kind=p['kind'], y=round(p['y'] - y0), h=round(p['h'])) for p, _ in items])
# --- PL: 레시피별 쪽 조합
pl_spec = {}
for pid, letter, name, flow, src in PAGES:
    nd = K[letter]
    d2, f2 = compose(dict(start_no=1, first='odd', note=NOTE, nodes=nd), f'{OUT}/{pid.lower()}.pptx')
    subprocess.run(f'cd {OUT} && soffice --headless --convert-to pdf {pid.lower()}.pptx >/dev/null 2>&1 && rm -f {pid.lower()}-*.png && pdftoppm -r {SC} -png {pid.lower()}.pdf {pid.lower()}', shell=True)
    pgs = sorted(glob.glob(f'{OUT}/{pid.lower()}-*.png'))
    ims = []
    for j, p in enumerate(pgs, 1):
        im = Image.open(p).convert('RGB'); im = im.resize((828, int(im.height * 828 / 1380))); fn = f'{pid.lower()}-p{j}.png'; im.save(f'{OUT}/{fn}'); ims.append(fn)
    blocks = [dict(page=p['page'], kind=p['kind'], cls=p['cls'], x0=p['x0'], y=round(p['y'] - 48), h=round(p['h'])) for p in f2.placed]
    pl_spec[pid] = dict(id=pid, name=name, flow=flow, src=src, letter=letter, imgs=ims, blocks=blocks)
json.dump(dict(rl=spec, pl=pl_spec), open(OUT + '/layouts.json', 'w'), ensure_ascii=False, indent=1)
print(len(spec), 'RL', len(pl_spec), 'PL', len(f.placed), '블록', 'warn', d.warn[:3])
