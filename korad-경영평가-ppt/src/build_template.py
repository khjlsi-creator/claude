# -*- coding: utf-8 -*-
"""레이아웃 템플릿 만들기: RL 24종(영역 단위 쪽 레이아웃) + PL 9종(서사 유형별 쪽 조합)을
진짜 PowerPoint 슬라이드 레이아웃(자리표시자)으로 만든다.
  python3 build_template.py 템플릿.pptx [적용예시.pptx]"""
import sys
from compose import compose
from layouts import LAYOUTS, PAGES, K, PL_NODES
from recipes import NOTE
from layoutize import layoutize_slide, drop_slides

tmpl = sys.argv[1]
sample = sys.argv[2] if len(sys.argv) > 2 else None
nodes = []; groups = []          # (이름, 노드 수)
for pid, letter, name, flow, src in PAGES:
    if nodes: nodes.append(dict(t='newpage'))
    nodes += PL_NODES[pid]; groups.append((f'{pid} {name}', len(PL_NODES[pid])))
d, f = compose(dict(start_no=1, first='odd', note=NOTE, nodes=nodes), '/tmp/_tpl.pptx')
for pid, letter, *_ in PAGES:
    dd, ff = compose(dict(start_no=1, first='odd', nodes=PL_NODES[pid]), '/tmp/_chk.pptx')
    assert ff.pages() == 1, f'{pid}는 한 쪽을 넘습니다({ff.pages()}쪽)'
    print(pid, '채움', round((max(p['y'] + p['h'] for p in ff.placed) - 188) / 17.07), '%')
# 그룹별 쪽 범위
pages_of = []; bi = 0
for name, n in groups:
    blocks = f.placed[bi:bi + n]; bi += n
    pages_of.append((name, sorted({b['page'] for b in blocks})))
names = {}
for name, pgs in pages_of:
    for j, p in enumerate(pgs):
        names[p] = name if len(pgs) == 1 else f'{name} ({j + 1}/{len(pgs)})'
prs = d.prs
for i, sl in enumerate(list(prs.slides), 1):
    layoutize_slide(prs, sl, names[i])
prs.save(tmpl)          # 샘플 글자가 채워진 쪽을 함께 둔다(복제해서 글만 바꾼다)
if sample:
    drop_slides(prs)
    prs.save(sample)
print('레이아웃', len(prs.slide_layouts), '쪽 예시', len(names))
