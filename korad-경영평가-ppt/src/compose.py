# -*- coding: utf-8 -*-
"""서사 → 레이아웃 조합기.

서사를 단락별 노드(JSON)로 적으면 노드마다 맞는 블록을 골라 A4 쪽에 쌓는다.
  python3 compose.py 서사.json 출력.pptx        # 서사 한 편을 PPT로
  python3 compose.py --catalog 출력.pptx        # 레이아웃 카탈로그(서사 유형별 쪽 예시)
  --layouts 를 붙이면 쪽마다 진짜 슬라이드 레이아웃(자리표시자)으로 만들어 PowerPoint에서 칸을 눌러 고친다

노드 종류(t): chapter · eval · topic · sub · ladder · strategy · twin · panel3 · table · result · connector · note · newpage
블록 선택표는 narratives.md 참고. 문구는 구조 확인용 예시이며 KORAD 실적이 아니다.
"""
import sys, json
from blocks import *

PALETTE = {1: ['blue'], 2: ['blue', 'deep'], 3: ['blue', 'teal', 'deep'], 4: ['blue', 'teal', 'teal', 'deep'], 5: ['blue', 'teal', 'teal', 'deep', 'deep']}
RESULT_LABELS = ('추진성과', '성과', '핵심성과')


def auto_rows(rows):
    """레일 색을 서사 순서(블루 → 틸 → 딥블루)로, 성과 레일은 그린으로 자동 배정하고 색이 바뀌는 곳에 쐐기를 단다."""
    n = len(rows); pal = PALETTE.get(n, ['blue'] + ['teal'] * (n - 2) + ['deep']) if n > 1 else PALETTE[1]
    out = []; prev = None
    for i, r in enumerate(rows):
        r = dict(r)
        label = r['label'].replace('\n', '')
        r.setdefault('tone', 'res' if label in RESULT_LABELS else pal[i])
        r.setdefault('notch', prev is not None and r['tone'] != prev and r['tone'] != 'res' and not r.get('tag') is False)
        prev = r['tone']
        out.append(r)
    return out


def make(node):
    t = node['t']
    if t == 'chapter': return ChapterBand(node['title'])
    if t == 'eval': return EvalBand(node['n'], node['title'])
    if t == 'topic': return NumBar(node['n'], node['title'])
    if t == 'sub': return SubHead(node['text'], node.get('chips', []))
    if t == 'ladder':
        frame = 'g4' if all(r['label'].replace('\n', '') in RESULT_LABELS for r in node['rows']) else node.get('frame', 'g2')
        lad = Ladder(auto_rows(node['rows']), frame=frame, side=node.get('side'), photos=node.get('photos'))
        lad.tag = 'photos' if node.get('photos') else ('side' if node.get('side') else None)
        return lad
    if t == 'strategy':
        lr = LabelRows(node['rows'], node.get('label_w', 110))
        lr.tag = 'nested' if any(isinstance(it, dict) and 'sub' in it for r in node['rows'] for col in r.get('items', []) if isinstance(col, list) for it in col) else None
        return lr
    if t == 'twin':
        mk = lambda side: (side['title'], [(r[0], r[1], r[2]) for r in side['rows']])
        return TwinPanel(mk(node['left']), mk(node['right']), tuple(node.get('label_w', (135, 148))))
    if t == 'panel3': return ThreePanel(node['panels'])
    if t == 'table': return DataTable(node['header'], node['rows'])
    if t == 'result': return Result(node.get('items') or node['text'], node.get('label', '핵심성과'))
    if t == 'connector': return Connector()
    if t == 'note': return Note(node['text'])
    raise ValueError('알 수 없는 노드 ' + t)


def compose(spec, out, layouts=False):
    d = RD()
    f = Flow(d, spec.get('start_no', 1), spec.get('first', 'odd'), foot=spec.get('foot', '2025년도 경영실적보고서'), indicator=spec.get('indicator', '노사관계'),
             number=spec.get('number', '4'), cat=spec.get('cat', 'Ⅰ. 경영관리 범주'), name=spec.get('name', '조직 운영 및 관리'), note=spec.get('note'))
    pending = []
    for node in spec['nodes']:
        if node['t'] == 'newpage':
            f.add_all(pending); pending = []
            f.break_page(); continue
        pending.append(make(node))
    f.add_all(pending)
    if layouts:
        from layoutize import layoutize_slide
        for i, sl in enumerate(list(d.prs.slides), 1):
            layoutize_slide(d.prs, sl, f'{spec.get("layout_prefix", "P")}{i:02d} 쪽 레이아웃')
    d.save(out)
    return d, f


if __name__ == '__main__':
    lay = '--layouts' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--layouts']
    if args[0] == '--catalog':
        from layouts import catalog_spec
        d, f = compose(catalog_spec(), args[1], layouts=lay)
    else:
        d, f = compose(json.load(open(args[0], encoding='utf-8')), args[1], layouts=lay)
    print('saved', args[-1], f.pages(), '쪽')
    for w in d.warn:
        print('WARN', w)
