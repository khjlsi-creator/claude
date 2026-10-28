# -*- coding: utf-8 -*-
"""KORAD 경영평가 보고서 레이아웃 레지스트리 (누적형).

한 쪽의 스펙(layouts/specs/pNN.json: 블록 종류·좌표)을 읽어
  1) 블록 단위 지문(fingerprint)으로 기존 블록 레이아웃(BL-)과 비교
  2) 쪽 단위 구성(블록 지문의 순서 + 프레임 변형)으로 기존 쪽 레이아웃(PG-)과 비교
같으면 '재사용(SKIP)', 다르면 새 레이아웃으로 '쌓는다(NEW)'.

사용:
  python3 src/layout_registry.py check  layouts/specs/p10.json   # 비교만 (저장 안 함)
  python3 src/layout_registry.py add    layouts/specs/p10.json   # 비교 후 새것만 레지스트리에 누적
  python3 src/layout_registry.py rebuild                          # specs/ 전체를 쪽 번호 순으로 다시 쌓기
  python3 src/layout_registry.py list                             # 누적 현황
  python3 src/layout_registry.py render                           # 와이어프레임 PNG + PPTX 갱신
좌표: 원본 쪽 이미지(1240px 폭) 픽셀. 1px = 210/1240 mm. y는 page_origin_y를 빼서 쪽 기준으로 바꾼다.
"""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LAY = os.path.join(ROOT, 'layouts')
REG = os.path.join(LAY, 'registry.json')
SPECS = os.path.join(LAY, 'specs')
PX_W = 1240.0
MM_PER_PX = 210.0 / PX_W


# ------------------------------------------------------------------ 지문
def block_fp(b):
    """같은 형태인지 판단하는 키. 글자·칩 문구·세부 좌표는 보지 않고 구조만 본다."""
    kind = b['kind']
    if kind == 'section_bar':
        return 'section_bar|num+chip'
    lw = int(round(b.get('label_w', 0) / 10.0)) * 10 if b.get('label') else 0
    # 라벨 폭 117·125는 같은 형태로 본다(10px 양자화 후 120)
    return '|'.join([kind, b.get('body', '-'), 'L%d' % lw, 'c%s' % b.get('cols', '-'), 'r%s' % b.get('rows', '-')])


def frame_fp(spec):
    ch = spec.get('chrome', {})
    tab = 'tab' if ch.get('side_tab') else 'notab'
    side = (ch.get('footer') or {}).get('side', '-')
    return 'frame|%s|footer-%s' % (tab, side)


def lcs_ratio(a, b):
    if not a or not b:
        return 0.0
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    return 2.0 * dp[-1][-1] / (len(a) + len(b))


# ------------------------------------------------------------------ 입출력
def load_reg():
    if os.path.exists(REG):
        return json.load(open(REG, encoding='utf-8'))
    return {'blocks': {}, 'pages': {}, 'frames': {}, 'log': []}


def save_reg(reg):
    json.dump(reg, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def norm_block(spec, b):
    """레지스트리에 저장할 블록 레이아웃 정의(쪽 기준 좌표, px와 mm)."""
    oy = spec.get('page_origin_y', 0)

    def conv(bb):
        x0, y0, x1, y1 = bb
        return dict(px=[x0, y0 - oy, x1, y1 - oy],
                    mm=[round(x0 * MM_PER_PX, 1), round((y0 - oy) * MM_PER_PX, 1),
                        round(x1 * MM_PER_PX, 1), round((y1 - oy) * MM_PER_PX, 1)])
    out = dict(kind=b['kind'], body=b.get('body'), label_w=b.get('label_w', 0),
               cols=b.get('cols'), rows=b.get('rows'),
               w_mm=round((b['bbox'][2] - b['bbox'][0]) * MM_PER_PX, 1),
               h_mm=round((b['bbox'][3] - b['bbox'][1]) * MM_PER_PX, 1))
    out['regions'] = [dict(name=r['name'], note=r.get('note', ''),
                           rel_mm=[round((r['bbox'][0] - b['bbox'][0]) * MM_PER_PX, 1),
                                   round((r['bbox'][1] - b['bbox'][1]) * MM_PER_PX, 1),
                                   round((r['bbox'][2] - r['bbox'][0]) * MM_PER_PX, 1),
                                   round((r['bbox'][3] - r['bbox'][1]) * MM_PER_PX, 1)])
                      for r in b.get('regions', [])]
    return out


def analyze(spec, reg, commit):
    """스펙 한 쪽을 레지스트리와 비교. commit이면 새것을 누적."""
    src = spec['source']
    tag = 'p%02d' % src['print_page']
    res = {'page': tag, 'blocks': [], 'frame': None, 'page_layout': None}
    # 프레임
    ff = frame_fp(spec)
    fid = next((k for k, v in reg['frames'].items() if v['fp'] == ff), None)
    if fid:
        res['frame'] = ('REUSE', fid)
    else:
        fid = 'PF-%d' % (len(reg['frames']) + 1)
        res['frame'] = ('NEW', fid)
        if commit:
            ch = spec['chrome']
            reg['frames'][fid] = dict(fp=ff, side_tab=ch.get('side_tab'), footer=ch.get('footer'), first_seen=tag)
    # 블록
    seq = []
    for b in spec['blocks']:
        fp = block_fp(b)
        bid = next((k for k, v in reg['blocks'].items() if v['fp'] == fp), None)
        if bid:
            res['blocks'].append((b['id'], b['kind'], 'REUSE', bid))
            if commit and tag not in reg['blocks'][bid]['used_in']:
                reg['blocks'][bid]['used_in'].append(tag)
        else:
            bid = 'BL-%03d' % (len(reg['blocks']) + 1)
            res['blocks'].append((b['id'], b['kind'], 'NEW', bid))
            if commit:
                d = norm_block(spec, b)
                d.update(fp=fp, first_seen=tag, used_in=[tag], label_example=b.get('label'))
                reg['blocks'][bid] = d
        seq.append(bid)
    # 쪽 구성
    comp = [fid] + seq
    pid = next((k for k, v in reg['pages'].items() if v['composition'] == comp), None)
    if pid:
        res['page_layout'] = ('SKIP(동일)', pid, 1.0)
        if commit and tag not in reg['pages'][pid]['instances']:
            reg['pages'][pid]['instances'].append(tag)
    else:
        near = max(((lcs_ratio(comp, v['composition']), k) for k, v in reg['pages'].items()), default=(0.0, None))
        pid = 'PG-%02d' % (len(reg['pages']) + 1)
        res['page_layout'] = ('NEW', pid, round(near[0], 2), near[1])
        if commit:
            oy = spec.get('page_origin_y', 0)
            reg['pages'][pid] = dict(
                composition=comp, instances=[tag], source=src,
                title=src.get('section'),
                blocks=[dict(spec_id=b['id'], layout=bid, label=b.get('label'),
                             y_mm=[round((b['bbox'][1] - oy) * MM_PER_PX, 1), round((b['bbox'][3] - oy) * MM_PER_PX, 1)],
                             x_mm=[round(b['bbox'][0] * MM_PER_PX, 1), round(b['bbox'][2] * MM_PER_PX, 1)])
                        for b, bid in zip(spec['blocks'], seq)])
    if commit:
        reg['log'].append(dict(page=tag, frame=res['frame'][1], page_layout=res['page_layout'][1],
                               new_blocks=[x[3] for x in res['blocks'] if x[2] == 'NEW']))
    return res


def report(res):
    print('== %s ==' % res['page'])
    print('  프레임  :', res['frame'][0], res['frame'][1])
    for bid, kind, st, lid in res['blocks']:
        print('  %-4s %-22s %-6s %s' % (bid, kind, st, lid))
    pl = res['page_layout']
    print('  쪽 레이아웃:', pl[0], pl[1], ('(가장 가까운 기존 %s, 유사도 %s)' % (pl[3], pl[2])) if pl[0] == 'NEW' and pl[3] else '')


def cmd_list(reg):
    print('프레임 %d · 블록 레이아웃 %d · 쪽 레이아웃 %d' % (len(reg['frames']), len(reg['blocks']), len(reg['pages'])))
    for k, v in reg['frames'].items():
        print(' ', k, v['fp'], '첫 등장', v['first_seen'])
    for k, v in reg['blocks'].items():
        print(' ', k, '%-48s' % v['fp'], '사용:', ','.join(v['used_in']))
    for k, v in reg['pages'].items():
        print(' ', k, v['title'], '인스턴스:', ','.join(v['instances']), '|', ' '.join(v['composition']))


def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd = sys.argv[1]
    reg = load_reg()
    if cmd == 'list':
        cmd_list(reg)
    elif cmd in ('check', 'add'):
        spec = json.load(open(sys.argv[2], encoding='utf-8'))
        res = analyze(spec, reg, commit=(cmd == 'add'))
        report(res)
        if cmd == 'add':
            save_reg(reg); print('→ registry.json 저장')
    elif cmd == 'rebuild':
        reg = {'blocks': {}, 'pages': {}, 'frames': {}, 'log': []}
        for f in sorted(glob.glob(os.path.join(SPECS, 'p*.json'))):
            report(analyze(json.load(open(f, encoding='utf-8')), reg, commit=True))
        save_reg(reg); print('→ registry.json 저장'); cmd_list(reg)
    elif cmd == 'render':
        import layout_render
        layout_render.render_all(reg)
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
