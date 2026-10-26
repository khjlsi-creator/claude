# -*- coding: utf-8 -*-
"""디자인 시스템 미리보기용 HTML 조각을 만든다(그림 없음): 블록 견본 · RL 레이아웃 · PL 쪽 조합 · 레시피 카탈로그 쪽."""
import json, sys
from pptx import Presentation
import slots
from compose import compose
from layouts import LAYOUTS, PAGES, K
from recipes import NOTE, catalog_spec
from pptx2html import slide_html, CSS

K2 = 960 / 1380.0
PAGE_H = 960 * 297 / 210


def region(slide, y_img, h_img, x0_img, w_img=1150, pad=6):
    y0 = (y_img - 48) * K2 - pad; y1 = (y_img - 48 + h_img) * K2 + pad; x0 = x0_img * K2 - pad
    w = w_img * K2 + 2 * pad
    return slide_html(slide, y0, y1, x0), round(w), round(y1 - y0)


def full(slide):
    return slide_html(slide), 960, round(PAGE_H)


def build(tmp):
    out = {'blocks': {}, 'rl': {}, 'pl': {}, 'recipe': [], 'css': CSS}
    # RL
    nodes = []
    for i, L in enumerate(LAYOUTS):
        if i: nodes.append(dict(t='newpage'))
        nodes += L['nodes']
    d, f = compose(dict(start_no=93, first='odd', note=NOTE, nodes=nodes), tmp + '/rl.pptx')
    prs = Presentation(tmp + '/rl.pptx')
    by_page = {}
    for pl, blk in zip(f.placed, f.placed_blocks):
        by_page.setdefault(pl['page'], []).append((pl, blk))
    rl = {}
    for i, L in enumerate(LAYOUTS):
        items = by_page[i + 1]; sl = prs.slides[i]
        y0 = items[0][0]['y']; ymax = max(p['y'] + p['h'] for p, _ in items); x0 = items[0][0]['x0']
        html, w, h = region(sl, y0, ymax - y0, x0)
        sls = []
        for pl, blk in items:
            for name, x, y, ww, hh in blk.slots(1150):
                sls.append(dict(name=name, x=round((x * K2) + 6), y=round((pl['y'] - y0 + y) * K2 + 6), w=round(ww * K2), h=round(hh * K2), block=pl['cls']))
        out['rl'][L['id']] = dict(id=L['id'], name=L['name'], when=L['when'], src=L['src'], html=html, w=w, h=h, slots=sls,
                                  blocks=[dict(cls=p['cls'], h=round(p['h'])) for p, _ in items])
        rl[L['id']] = [(sl, p) for p, _ in items]
    def blk(rid, idx, cls=None):
        sl, p = rl[rid][idx]
        assert cls is None or p['cls'] == cls, (rid, idx, p['cls'])
        return region(sl, p['y'], p['h'], p['x0'])
    B = out['blocks']
    B['chapter-band'] = blk('RL01', 0); B['eval-band-2line'] = blk('RL02', 0); B['num-bar'] = blk('RL02', 1); B['sub-head'] = blk('RL03', 0)
    B['ladder-env'] = blk('RL04', 1, 'Ladder') if rl['RL04'][0][1]['cls'] != 'Ladder' else blk('RL04', 0)
    B['ladder-side'] = blk('RL05', 0, 'Ladder'); B['ladder-steps'] = blk('RL06', 0, 'Ladder'); B['ladder-banner-photo'] = blk('RL08', 0, 'Ladder')
    B['ladder-result'] = blk('RL09', 0, 'Ladder'); B['ladder-photos'] = blk('RL12', 0, 'Ladder'); B['ladder-cause'] = blk('RL13', 0, 'Ladder')
    B['label-rows-strategy'] = blk('RL14', 0, 'LabelRows'); B['label-rows-check'] = blk('RL16', 0, 'LabelRows'); B['label-rows-vision'] = blk('RL17', 0, 'LabelRows')
    B['label-rows-nested'] = blk('RL18', 0, 'LabelRows'); B['twin-panel'] = blk('RL19', 0, 'TwinPanel'); B['three-panel'] = blk('RL20', 0, 'ThreePanel')
    B['data-table'] = blk('RL21', 0, 'DataTable'); B['result-1'] = blk('RL22', 0, 'Result'); B['result-2'] = blk('RL23', 0, 'Result'); B['result-prog'] = blk('RL24', 0, 'Result')
    # 사다리 + 연결 + 점검
    # PL
    for pid, letter, name, flow, src in PAGES:
        d2, f2 = compose(dict(start_no=93, first='odd', note=NOTE, nodes=K[letter]), f'{tmp}/{pid.lower()}.pptx')
        pr = Presentation(f'{tmp}/{pid.lower()}.pptx')
        assert len(pr.slides) == 1, f'{pid}는 한 쪽이어야 합니다({len(pr.slides)}쪽): 서사를 대목별로 쪼개세요'
        out['pl'][pid] = dict(id=pid, name=name, flow=flow, src=src, pages=[full(s) for s in pr.slides],
                              blocks=[dict(page=p['page'], cls=p['cls']) for p in f2.placed])
        for sl, p in zip([pr.slides[q['page'] - 1] for q in f2.placed], f2.placed):
            if letter == 'A' and p['cls'] == 'Connector': B['connector'] = region(sl, p['y'], p['h'], p['x0'])
            if letter == 'E' and p['cls'] == 'Note': B['note'] = region(sl, p['y'], p['h'], p['x0'])
            if letter == 'H' and p['cls'] == 'EvalBand': B['eval-band-1line'] = region(sl, p['y'], p['h'], p['x0'])
    # 쪽 마스터: 머리·하단
    sl = prs.slides[0]
    odd = slide_html(sl, 0, 200, 0); even_prs = Presentation(tmp + '/pl02.pptx') if False else None
    B['master-odd'] = (slide_html(sl, 0, 110, 0) , 960, 110)
    B['master-odd-foot'] = (slide_html(sl, PAGE_H - 70, PAGE_H, 0), 960, 70)
    # 카탈로그
    d3, f3 = compose(catalog_spec(), tmp + '/cat.pptx')
    pr = Presentation(tmp + '/cat.pptx')
    out['recipe'] = [full(s) for s in pr.slides]
    even = [s for i, s in enumerate(pr.slides) if i % 2 == 1][0]
    B['master-even'] = (slide_html(even, 0, 110, 0), 960, 110); B['master-even-foot'] = (slide_html(even, PAGE_H - 70, PAGE_H, 0), 960, 70)
    return out


if __name__ == '__main__':
    import os
    tmp = sys.argv[1]; os.makedirs(tmp, exist_ok=True)
    o = build(tmp)
    json.dump(o, open(tmp + '/snips.json', 'w'), ensure_ascii=False)
    print(len(o['rl']), 'RL', len(o['pl']), 'PL', len(o['blocks']), 'blocks', len(o['recipe']), 'recipe pages')
