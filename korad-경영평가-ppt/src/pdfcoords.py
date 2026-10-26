# -*- coding: utf-8 -*-
"""참조 PDF에서 도형·글자 좌표를 그대로 뽑는다(눈대중·경계선 검출 없이 벡터 값 사용).
  python3 pdfcoords.py 참조.pdf 쪽번호(1부터) [out.json]
출력(mm, 용지 왼쪽 위 기준): rects(채움색·선색·선굵기·bbox), texts(글·글꼴·크기pt·색·bbox), images(bbox)
이 값으로 레이아웃 대장의 블록과 대조하고, 새 블록의 칸 폭·높이·간격·글자 크기를 정한다."""
import sys, json
import pymupdf

MM = 25.4 / 72.0


def hexcol(c):
    if c is None: return None
    return '%02X%02X%02X' % tuple(int(round(v * 255)) for v in c[:3])


def page_coords(path, pno):
    doc = pymupdf.open(path); pg = doc[pno - 1]
    out = dict(page=pno, w_mm=round(pg.rect.width * MM, 2), h_mm=round(pg.rect.height * MM, 2), rects=[], texts=[], images=[])
    for d in pg.get_drawings():
        r = d['rect']
        if r.width < 0.5 and r.height < 0.5: continue
        out['rects'].append(dict(x=round(r.x0 * MM, 2), y=round(r.y0 * MM, 2), w=round(r.width * MM, 2), h=round(r.height * MM, 2),
                                 fill=hexcol(d.get('fill')), line=hexcol(d.get('color')), lw=round((d.get('width') or 0) * MM, 2)))
    for b in pg.get_text('dict')['blocks']:
        if b['type'] == 1:
            r = b['bbox']; out['images'].append(dict(x=round(r[0] * MM, 2), y=round(r[1] * MM, 2), w=round((r[2] - r[0]) * MM, 2), h=round((r[3] - r[1]) * MM, 2))); continue
        for l in b.get('lines', []):
            for s in l['spans']:
                if not s['text'].strip(): continue
                r = s['bbox']
                out['texts'].append(dict(t=s['text'], font=s['font'], pt=round(s['size'], 1), color='%06X' % s['color'], x=round(r[0] * MM, 2), y=round(r[1] * MM, 2), w=round((r[2] - r[0]) * MM, 2), h=round((r[3] - r[1]) * MM, 2)))
    return out


if __name__ == '__main__':
    res = page_coords(sys.argv[1], int(sys.argv[2]))
    if len(sys.argv) > 3:
        json.dump(res, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    print('rects', len(res['rects']), 'texts', len(res['texts']), 'images', len(res['images']))
    sizes = {}
    for t in res['texts']:
        sizes[t['pt']] = sizes.get(t['pt'], 0) + len(t['t'])
    print('글자 크기(pt)별 글자 수:', dict(sorted(sizes.items())))
