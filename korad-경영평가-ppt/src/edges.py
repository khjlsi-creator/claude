# -*- coding: utf-8 -*-
"""참조 이미지에서 가로·세로 경계선(px)을 검출한다. 도형 좌표를 이 값에 맞춘다(스냅)."""
import numpy as np
from PIL import Image
SRC = '/tmp/claude-0/-home-user-claude/59deb4d2-f2ce-54b3-bb46-46930883f26e/images/%d.webp'


def _runs_axis(diff, minlen):
    """diff: 2D bool. 각 행에서 연속 True 길이 >= minlen 인 행 번호 목록"""
    out = []
    for i, row in enumerate(diff):
        d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
        s = np.where(d == 1)[0]; e = np.where(d == -1)[0]
        if len(s) and (e - s).max() >= minlen:
            out.append((i, int((e - s).max())))
    return out


def _merge(vals, tol=2):
    vals = sorted(vals); res = []
    for v in vals:
        if res and v - res[-1][-1] <= tol:
            res[-1].append(v)
        else:
            res.append([v])
    return [float(np.mean(g)) for g in res]


def detect(src, thr=18, hmin=36, vmin=22):
    """src: 파일 경로 또는 PIL 이미지 → (가로선 y 목록, 세로선 x 목록), 용지 좌표(px, 이미지 y 그대로)"""
    im = src if hasattr(src, 'convert') else Image.open(src)
    g = np.array(im.convert('L')).astype(int)
    dy = np.abs(np.diff(g, axis=0)) > thr          # 행 사이 경계
    dx = np.abs(np.diff(g, axis=1)) > thr
    ys = [i + 0.5 for i, _ in _runs_axis(dy, hmin)]
    xs = [i + 0.5 for i, _ in _runs_axis(dx.T, vmin)]
    return _merge(ys), _merge(xs)


_cache = {}


def edges_of(n):
    if n not in _cache:
        ys, xs = detect(SRC % n)
        _cache[n] = ([y for y in ys if y > 52], xs)
    return _cache[n]
