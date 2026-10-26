# -*- coding: utf-8 -*-
"""재현 렌더와 참조의 경계선 위치 오차(px) 측정: python3 prec.py 렌더PNG접두사"""
import sys, numpy as np
from PIL import Image
import edges

def err(a, b, win=8):
    """a의 각 값에 대해 b에서 가장 가까운 값과의 거리(win 이내만)"""
    b = np.array(b); out = []
    for v in a:
        d = np.abs(b - v).min() if len(b) else 99
        if d <= win: out.append(d)
    return out

if __name__ == '__main__':
    pre = sys.argv[1]
    tot = []
    for n in range(1, 6):
        im = Image.open(f'{pre}-{n}.png').convert('RGB')
        canvas = Image.new('RGB', (1380, 2000), (255, 255, 255)); canvas.paste(im, (0, 48))
        ry, rx = edges.detect(canvas)
        sy, sx = edges.edges_of(n)
        sy = [y for y in sy if 90 < y < 1960]
        ey, ex = err(sy, ry), err(sx, rx)
        cov = (len(ey) / len(sy), len(ex) / len(sx))
        print(n, f'가로 평균 {np.mean(ey):.2f}px 중앙 {np.median(ey):.2f} ≤2px {np.mean(np.array(ey)<=2):.0%} | 세로 평균 {np.mean(ex):.2f}px ≤2px {np.mean(np.array(ex)<=2):.0%} | 대응 {cov[0]:.0%}/{cov[1]:.0%}')
        tot += ey + ex
    print('전체 평균', round(float(np.mean(tot)), 2), '≤2px', f'{np.mean(np.array(tot)<=2):.0%}', '≤4px', f'{np.mean(np.array(tot)<=4):.0%}')
