# -*- coding: utf-8 -*-
"""신규 대목 레이아웃 L24~L36 — 한국수자원공사 경영실적보고서 20~24쪽에서 새로 확인한 모양.
치수는 참조 지면 px(1240px = 210mm)를 실측한 뒤 1.113배(= 1380px 격자)로 옮긴 값이고, 폭은 본문 폭 W에 비례한다.
기존 블록(Ladder·LabelRows·TwinPanel…)으로 담기는 모양은 새로 만들지 않고 변형 옵션만 추가했다."""
from blocks import *

R_ = 1.113          # 참조 px → 1380 격자 px


def _chip(d, s, x0, y0, text, h=30, fill=None, color=None):
    """작은 직각 태그(신설·강화·유지·한계·극복 …)"""
    w = text_w(text, SZ_D, True) / K + 20
    d.shp(s, x0, y0, x0 + w, y0 + h, text, fill or C['white'], color=color or C['navy'], line=TONE['g4'], lw=1.0, name='태그', mg=(0.2, 0, 0.2, 0))
    return w


# ---------------------------------------------------------------- L24 라벨 · 헤드라인 박스
class Headline(Block):
    """라벨 + 큰 제목 박스(제목 한 줄 + 보조 한 줄). 추진 방향·전략 목표처럼 한 문장을 크게 못 박는다."""
    kind = '헤드라인 박스'
    gap = 12

    def __init__(self, label, title, sub=None, tag=None):
        self.label, self.title, self.sub, self.tag = label, title, sub, tag

    def height(self, W):
        tl = est_lines(self.title, ((W - 130) * K) * 0.93, SZ_SHAPE)
        return round(30 + 36 * tl + (30 if self.sub else 0))

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('헤드라인 박스', x0, y, x0 + W, y + h)
        d.rail(s, x0, y, x0 + 110, y + h, self.label, 'blue', tag=self.tag)
        d.r(s, x0 + 114, y, x0 + W, y + h, fill=C['white'], line=TONE['line'], lw=1.25, name='헤드라인 박스')
        paras = [dict(t=self.title, sz=SZ_SHAPE, b=True, color=C['navy'], align='c')]
        if self.sub:
            paras.append(dict(t=self.sub, sz=SZ_D, color=C['slate_700'], align='c'))
        d.t(s, x0 + 124, y + 4, x0 + W - 10, y + h - 4, paras, name='헤드라인 글', tag='헤드라인')


# ---------------------------------------------------------------- L25 회색 배너
class GreyBanner(Block):
    """전폭 회색(블루 틴트) 그라데이션 배너 1~2줄. 둘째 줄 앞에 태그를 달 수 있다."""
    kind = '배너'
    gap = 10

    def __init__(self, lines):
        self.lines = [(None, l) if isinstance(l, str) else tuple(l) for l in lines]

    def height(self, W):
        return 22 + 38 * len(self.lines)

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('배너', x0, y, x0 + W, y + h)
        sp = d.r(s, x0, y, x0 + W, y + h, fill=TONE['g1'], name='배너')
        d.grad(sp, TONE['g1'], C['white'], 0)
        d.hl(s, x0, y, x0 + W, y, color=TONE['g2'], lw=1.0)
        for i, (chip, text) in enumerate(self.lines):
            yy = y + 10 + 38 * i
            tw = text_w(text, SZ_C, True) / K
            cx = x0 + (W - tw) / 2
            if chip:
                cw = text_w(chip, SZ_D, True) / K + 20
                _chip(d, s, cx - cw - 10, yy + 3, chip, h=30)
            d.t(s, x0, yy, x0 + W, yy + 36, [dict(t=text, sz=SZ_C, b=True, color=C['navy'], align='c')], name='배너 글', tag='배너')


# ---------------------------------------------------------------- L26 칩 셀 복합 박스
class ChipCells(Block):
    """라벨 + (칩 셀 2×2 | 전략 제목 + 타일 2×2 | 진한 요약 칸). 안전 전략처럼 한 박스 안에 세 묶음이 들어간다."""
    kind = '칩 셀 복합 박스'
    gap = 12

    def __init__(self, label, cells, mid_title, mid_tiles, right):
        self.label, self.cells, self.mid_title, self.mid_tiles, self.right = label, cells, mid_title, mid_tiles, right

    def height(self, W):
        return 164

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('칩 셀 복합 박스', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['line'], lw=0.75, name='박스 외곽')
        d.rail(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, 'blue')
        ax = x0 + 118; aw = (W - 126) * 0.40; bx = ax + aw + 8; bw = (W - 126) * 0.43; cx = bx + bw + 8; cw = x0 + W - 6 - cx
        for i, (chip, text) in enumerate(self.cells):
            cx0 = ax + (i % 2) * (aw / 2 + 2); cy0 = y + 10 + (i // 2) * 72
            d.shp(s, cx0, cy0, cx0 + 66, cy0 + 60, chip, TONE['g1'], color=C['navy'], line=TONE['g2'], lw=0.75, name='칩', mg=(0.2, 0, 0.2, 0))
            d.t(s, cx0 + 70, cy0, cx0 + aw / 2 - 2, cy0 + 60, [dict(t=text, sz=SZ_D, color=C['navy'])], name='칩 셀 글', tag='칩셀')
        d.hl(s, bx - 4, y + 10, bx - 4, y + h - 10, color=TONE['g2'], lw=0.75)
        d.t(s, bx, y + 6, bx + bw, y + 44, [dict(t=self.mid_title, sz=SZ_D, b=True, color=C['navy'], align='c')], name='전략 제목')
        for i, t_ in enumerate(self.mid_tiles):
            tx = bx + (i % 2) * (bw / 2 + 2); ty = y + 50 + (i // 2) * 52
            d.shp(s, tx, ty, tx + bw / 2 - 4, ty + 46, t_, TONE['g1'], color=C['navy'], bold=False, name='타일', mg=(0.4, 0, 0.4, 0))
        d.shp(s, cx, y + 10, cx + cw, y + h - 10, self.right, TONE['g4'], name='요약 칸', mg=(0.6, 0.2, 0.6, 0.2))


# ---------------------------------------------------------------- L27 CSF · PI · KPI · 로드맵 표
class RoadmapTable(Block):
    """분야(CSF) × 성과지표(PI) × 핵심성과지표(KPI) × 로드맵(꺾은선) 표. 행마다 칸 높이가 같다."""
    kind = 'CSF 로드맵 표'
    gap = 14
    splittable = True

    def __init__(self, head, rows):
        self.head, self.rows = head, rows

    def _cw(self, W):
        av = W - 110 - 18
        return [110, av * 0.33, av * 0.31, av * 0.36]

    def _rh(self, W):
        cw = self._cw(W)
        return [max(112, items_h(r['pi'], cw[1] - 6) + 14, 112) for r in self.rows]

    def height(self, W):
        return 40 + sum(self._rh(W)) + 6 * len(self.rows)

    def split(self, W, avail):
        acc = 44; k = 0
        for h in self._rh(W):
            if acc + h + 6 > avail:
                break
            acc += h + 6; k += 1
        if k == 0 or k == len(self.rows):
            return None
        return RoadmapTable(self.head, self.rows[:k]), RoadmapTable(self.head, self.rows[k:])

    def draw(self, d, s, x0, y, W):
        cw = self._cw(W); xs = [x0]
        for w_ in cw:
            xs.append(xs[-1] + w_ + 6)
        d.use('CSF 로드맵 표', x0, y, x0 + W, y + self.height(W))
        for i, hd in enumerate(self.head):
            d.shp(s, xs[i], y, xs[i] + cw[i], y + 38, hd, TONE['g4'] if i == 0 else TONE['g1'], color=C['white'] if i == 0 else C['navy'], name='머리칸')
        yy = y + 44
        for r, rh in zip(self.rows, self._rh(W)):
            d.rail(s, xs[0], yy, xs[0] + cw[0], yy + rh, r['label'], 'blue')
            d.t(s, xs[1], yy, xs[1] + cw[1], yy + rh, [B(t) for t in r['pi']], anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='PI 글', tag='PI')
            k = r['kpi']
            kx0, kx1 = xs[2], xs[2] + cw[2]
            d.r(s, kx0, yy, kx1, yy + rh, fill=C['white'], line=TONE['g2'], lw=0.75, name='KPI 칸')
            cwid = _chip(d, s, kx0 + 8, yy + 10, k['chip'], h=28)
            d.t(s, kx0 + 14 + cwid, yy + 6, kx1 - 6, yy + rh - 44, [dict(t=k['text'], sz=SZ_D, b=True, color=C['navy'])], name='KPI 글', tag='KPI')
            d.shp(s, kx0 + 2, yy + rh - 40, kx1 - 2, yy + rh - 2, k['result'], TONE['g1'], color=C['navy'], name='KPI 결과', mg=(0.4, 0, 0.4, 0))
            # 로드맵 꺾은선
            gx0, gx1 = xs[3] + 14, xs[3] + cw[3] - 14; gy0, gy1 = yy + 40, yy + rh - 44
            d.r(s, xs[3], yy, xs[3] + cw[3], yy + rh, fill=C['white'], line=TONE['g2'], lw=0.75, name='로드맵 칸')
            ch = r['chart']
            d.t(s, xs[3] + 4, yy + 2, xs[3] + 150, yy + 26, [dict(t='단위 : ' + ch['unit'], sz=9, color=C['slate_700'])], name='단위', tag='단위', mg=(0.4, 0, 0, 0))
            vals = ch['vals']; lo, hi = min(vals), max(vals); n = len(vals)
            pts = [(gx0 + (gx1 - gx0) * i / (n - 1), gy1 - (gy1 - gy0) * ((v - lo) / (hi - lo) if hi > lo else 0.5)) for i, v in enumerate(vals)]
            for (ax_, ay_), (bx_, by_) in zip(pts, pts[1:]):
                d.hl(s, ax_, ay_, bx_, by_, color=TONE['line'], lw=1.5)
            for i, ((px_, py_), v) in enumerate(zip(pts, vals)):
                d.r(s, px_ - 4, py_ - 4, px_ + 4, py_ + 4, fill=TONE['g4'], name='점')
                d.t(s, px_ - 30, py_ - 36, px_ + 30, py_ - 6, [dict(t=ch['labels'][i] if 'labels' in ch else str(v), sz=9, b=True, color=C['navy'], align='c')], name='값', tag='값', mg=(0, 0, 0, 0))
                d.t(s, px_ - 26, yy + rh - 36, px_ + 26, yy + rh - 4, [dict(t=ch['years'][i], sz=9, color=C['slate_700'], align='c')], name='연도', tag='연도', mg=(0, 0, 0, 0))
            d.hl(s, gx0 - 8, yy + rh - 38, gx1 + 8, yy + rh - 38, color=TONE['g2'], lw=1.0)
            yy += rh + 6


# ---------------------------------------------------------------- L28 지표 카드 매트릭스
class IndicatorMatrix(Block):
    """분야(라벨 + 신설·강화·유지 개수) × 지표 카드 N장. 카드 = 태그 + 제목 / 국정과제 한 줄 / 막대 또는 목표 변화."""
    kind = '지표 카드 매트릭스'
    gap = 12
    splittable = True
    ROW = 178

    def __init__(self, rows):
        self.rows = rows

    def height(self, W):
        return len(self.rows) * self.ROW + 4 * (len(self.rows) - 1)

    def split(self, W, avail):
        k = int((avail + 4) // (self.ROW + 4))
        if k < 1 or k >= len(self.rows):
            return None
        return IndicatorMatrix(self.rows[:k]), IndicatorMatrix(self.rows[k:])

    def draw(self, d, s, x0, y, W):
        d.use('지표 카드 매트릭스', x0, y, x0 + W, y + self.height(W))
        for ri, r in enumerate(self.rows):
            yy = y + ri * (self.ROW + 4)
            d.r(s, x0, yy, x0 + W, yy + self.ROW, fill=C['white'], line=TONE['g2'], lw=0.75, name='행 틀')
            d.shp(s, x0 + 4, yy + 4, x0 + 134, yy + 56, r['label'], TONE['g1'], color=C['navy'], name='분야 라벨', mg=(0.4, 0, 0.4, 0))
            d.t(s, x0 + 4, yy + 60, x0 + 134, yy + self.ROW - 4, [dict(t=f'{a} {b}개', sz=SZ_D, b=True, color=C['navy'], align='c') for a, b in r['counts']], name='개수', tag='개수', mg=(0.4, 0, 0.4, 0))
            n = len(r['cards']); cw = (W - 144 - 6 * (n - 1)) / n
            for ci, c in enumerate(r['cards']):
                cx = x0 + 140 + ci * (cw + 6)
                d.r(s, cx, yy + 4, cx + cw, yy + self.ROW - 4, fill=C['white'], line=TONE['g2'], lw=0.75, name='카드')
                d.r(s, cx, yy + 4, cx + cw, yy + 40, fill=TONE['g1'], name='카드 머리')
                tw = _chip(d, s, cx + 6, yy + 8, c['tag'], h=28)
                d.t(s, cx + 12 + tw, yy + 4, cx + cw - 4, yy + 40, [dict(t=c['title'], sz=SZ_D, b=True, color=C['navy'])], name='카드 제목', tag='카드제목')
                d.t(s, cx + 4, yy + 42, cx + cw - 4, yy + 72, [B(c['sub'])], anchor='m', mg=(1.2, 0, 0.4, 0), name='카드 부제', tag='카드부제')
                by0, by1 = yy + 76, yy + self.ROW - 8
                vals = c.get('bars')
                if vals:
                    mx = max(v for _, v, _ in vals); bw = 34
                    for bi, (yr, v, lab) in enumerate(vals):
                        bx = cx + 30 + bi * 90; hh = max(14, (by1 - by0 - 66) * v / mx)
                        d.r(s, bx, by1 - 30 - hh, bx + bw, by1 - 30, fill=TONE['g3'] if bi < len(vals) - 1 else TONE['g4'], name='막대')
                        d.t(s, bx - 20, by1 - 30 - hh - 32, bx + bw + 20, by1 - 30 - hh - 2, [dict(t=lab, sz=9, b=True, color=C['navy'], align='c')], name='값', tag='값', mg=(0, 0, 0, 0))
                        d.t(s, bx - 20, by1 - 30, bx + bw + 20, by1 + 2, [dict(t=yr, sz=9, color=C['slate_700'], align='c')], name='연도', tag='연도', mg=(0, 0, 0, 0))
                else:
                    a, b_ = c['change']
                    half = (cw - 60) / 2
                    d.shp(s, cx + 10, by0 + 10, cx + 10 + half, by1 - 10, a, TONE['g1'], color=C['navy'], name='현재', mg=(0.4, 0, 0.4, 0))
                    d.tri_arrow(s, cx + 10 + half + 20, (by0 + by1) / 2, 40, 24, down=False)
                    d.shp(s, cx + 50 + half, by0 + 10, cx + cw - 10, by1 - 10, b_, TONE['g4'], name='목표', mg=(0.4, 0, 0.4, 0))


# ---------------------------------------------------------------- L29 아이콘 라벨 · 요약 · 사진 행
class IconRows(Block):
    """행마다 분야 라벨 + 불릿 + 요약 박스 + 사진. 성과를 분야별로 나열하고 대표 사진을 붙인다."""
    kind = '라벨·요약·사진 행'
    gap = 12
    splittable = True

    def __init__(self, rows):
        self.rows = rows

    def _cw(self, W):
        av = W - 110 - 18
        return [110, av * 0.58, av * 0.16, av * 0.26]

    def _rh(self, W):
        cw = self._cw(W)
        return [max(108, items_h(r['lines'], cw[1] - 6) + 12, len(r['summary']) * LP + 24) for r in self.rows]

    def height(self, W):
        return sum(self._rh(W)) + 4 * (len(self.rows) - 1)

    def split(self, W, avail):
        acc = 0; k = 0
        for h in self._rh(W):
            if acc + h > avail:
                break
            acc += h + 4; k += 1
        if k == 0 or k == len(self.rows):
            return None
        return IconRows(self.rows[:k]), IconRows(self.rows[k:])

    def draw(self, d, s, x0, y, W):
        cw = self._cw(W); xs = [x0]
        for w_ in cw:
            xs.append(xs[-1] + w_ + 6)
        d.use('라벨·요약·사진 행', x0, y, x0 + W, y + self.height(W))
        yy = y
        for r, rh in zip(self.rows, self._rh(W)):
            d.r(s, x0, yy, x0 + W, yy + rh, fill=C['white'], line=TONE['g2'], lw=0.75, name='행 틀')
            d.rail(s, xs[0] + 2, yy + 2, xs[0] + cw[0], yy + rh - 2, r['label'], 'blue')
            d.t(s, xs[1], yy, xs[1] + cw[1], yy + rh, [B(t) for t in r['lines']], anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='행 글', tag='행글')
            d.shp(s, xs[2], yy + 6, xs[2] + cw[2], yy + rh - 6, '\n'.join(r['summary']), TONE['g1'], color=C['navy'], name='요약 박스', mg=(0.4, 0, 0.4, 0))
            d.photo(s, xs[3], yy + 4, xs[3] + cw[3] - 4, yy + rh - 4, r.get('photo', '사진'))
            yy += rh + 4


# ---------------------------------------------------------------- L30 Best Practice 박스
class BestPractice(Block):
    """진한 'Best Practice' 라벨 + 제목 띠 + 핵심 문장 불릿. 우수사례를 한 박스에 소개한다."""
    kind = 'Best Practice 박스'
    gap = 14

    def __init__(self, title, lines):
        self.title, self.lines = title, lines

    def height(self, W):
        return 62 + 38 * len(self.lines) + 14

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('Best Practice 박스', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['g5'], lw=2.25, name='박스 외곽')
        d.shp(s, x0, y, x0 + 130, y + h, 'Best\nPractice', TONE['g5'], sz=SZ_SHAPE, name='BP 라벨', mg=(0.4, 0, 0.4, 0))
        bar = d.r(s, x0 + 134, y + 4, x0 + W - 4, y + 60, fill=TONE['g1'], name='제목 띠')
        d.grad(bar, TONE['g2'], C['white'], 0)
        d.t(s, x0 + 150, y + 4, x0 + W - 12, y + 60, [dict(t=self.title, sz=SZ_SHAPE + 2, b=True, color=C['navy'])], name='BP 제목', tag='BP제목')
        d.t(s, x0 + 146, y + 66, x0 + W - 12, y + h - 8, [dict(t=t_, sz=SZ_C, b=True, color=C['navy'], bullet='•', hang=4.2, after=2.0) for t_ in self.lines], anchor='m', name='BP 문장', tag='BP문장')


# ---------------------------------------------------------------- L31 번호 과제 그룹
class NumberedGroups(Block):
    """회색 틀 안에 분야별 흰 박스 N개, 박스마다 머리 + (소분야 머리) + 번호 붙은 과제. 분야는 소분야로 나뉠 수 있다."""
    kind = '번호 과제 그룹'
    gap = 14

    def __init__(self, caption, groups):
        self.caption, self.groups = caption, groups

    def _rows(self):
        return max(max(len(items) for _, items in (g['subs'] if g.get('subs') else [(None, g['items'])])) for g in self.groups)

    def height(self, W):
        has_sub = any(g.get('subs') for g in self.groups)
        return 44 + 50 + (40 if has_sub else 0) + self._rows() * 68 + 24

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('번호 과제 그룹', x0, y, x0 + W, y + h)
        d.r(s, x0, y + 40, x0 + W, y + h, fill=TONE['g1'], name='그룹 틀')
        d.shp(s, x0 + W * 0.12, y, x0 + W * 0.88, y + 40, self.caption, C['white'], color=C['navy'], line=TONE['g2'], lw=1.0, name='캡션', mg=(0.4, 0, 0.4, 0))
        wts = [2.0 if g.get('subs') else 1.0 for g in self.groups]
        tot = sum(wts); av = W - 20 - 8 * (len(self.groups) - 1); xx = x0 + 10
        has_sub = any(g.get('subs') for g in self.groups)
        for g, wt in zip(self.groups, wts):
            gw = av * wt / tot
            d.r(s, xx, y + 52, xx + gw, y + h - 10, fill=C['white'], line=TONE['g2'], lw=0.75, name='분야 박스')
            d.t(s, xx, y + 54, xx + gw, y + 96, [dict(t=g['title'], sz=SZ_C, b=True, color=C['navy'], align='c')], name='분야 머리', tag='분야')
            subs = g.get('subs') or [(None, g['items'])]
            sw = (gw - 12) / len(subs)
            for si, (sub, items) in enumerate(subs):
                sx = xx + 6 + si * sw
                top = y + 98
                if has_sub:
                    if sub:
                        d.shp(s, sx, top, sx + sw - 4, top + 34, sub, TONE['g2'], color=C['navy'], name='소분야', mg=(0.3, 0, 0.3, 0))
                    top += 40
                for ii, (num, txt) in enumerate(items):
                    iy = top + ii * 68
                    d.shp(s, sx + 2, iy + 6, sx + 36, iy + 40, str(num), TONE['g4'], name='번호', mg=(0, 0, 0, 0))
                    d.t(s, sx + 42, iy, sx + sw - 6, iy + 64, [dict(t=txt, sz=SZ_D, color=C['navy'])], name='과제 글', tag='과제')
            xx += gw + 8


# ---------------------------------------------------------------- L32 조직 · 네트워크 패널
class OrgPanel(Block):
    """왼쪽 조직도(총괄 → 부서 3칸) + 오른쪽 네트워크 목록(분류 라벨 + 줄). 머리는 진한 띠."""
    kind = '조직·네트워크 패널'
    gap = 12

    def __init__(self, left, right):
        self.left, self.right = left, right

    def height(self, W):
        return 316

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        lw_ = W * 0.66; rx = x0 + lw_ + 8
        d.use('조직·네트워크 패널', x0, y, x0 + W, y + h)
        for xa, xb, tt in ((x0, x0 + lw_, self.left['title']), (rx, x0 + W, self.right['title'])):
            d.r(s, xa, y, xb, y + h, fill=C['white'], line=TONE['g5'], lw=1.25, name='패널 외곽')
            d.shp(s, xa, y, xb, y + 44, tt, TONE['g5'], sz=SZ_C, name='패널 머리', mg=(0.4, 0, 0.4, 0))
        L = self.left
        rootw = lw_ * 0.46; rx0 = x0 + (lw_ - rootw) / 2 - 40
        d.shp(s, rx0, y + 56, rx0 + rootw, y + 96, L['root'][0], TONE['g4'], name='총괄', mg=(0.4, 0, 0.4, 0))
        d.shp(s, rx0, y + 96, rx0 + rootw, y + 132, L['root'][1], TONE['g1'], color=C['navy'], bold=False, name='총괄 설명', mg=(0.4, 0, 0.4, 0))
        sx0 = x0 + lw_ - 150
        d.shp(s, sx0, y + 56, sx0 + 138, y + 92, L['side'][0], TONE['g2'], color=C['navy'], name='보조 조직', mg=(0.3, 0, 0.3, 0))
        d.t(s, sx0, y + 94, sx0 + 138, y + 160, [dict(t=t_, sz=SZ_D, color=C['navy'], align='c') for t_ in L['side'][1]], name='보조 글', tag='보조')
        n = len(L['children']); cw = (lw_ - 24 - 6 * (n - 1)) / n
        d.hl(s, x0 + 12 + cw / 2, y + 148, x0 + 12 + cw * (n - 0.5) + 6 * (n - 1), y + 148, color=TONE['g4'], lw=1.25)
        d.hl(s, rx0 + rootw / 2, y + 132, rx0 + rootw / 2, y + 148, color=TONE['g4'], lw=1.25)
        for i, (tt, lines) in enumerate(L['children']):
            cx = x0 + 12 + i * (cw + 6)
            d.hl(s, cx + cw / 2, y + 148, cx + cw / 2, y + 160, color=TONE['g4'], lw=1.25)
            d.shp(s, cx, y + 160, cx + cw, y + 192, tt, TONE['g1'], color=C['navy'], name='부서', mg=(0.3, 0, 0.3, 0))
            d.t(s, cx, y + 194, cx + cw, y + 264, [dict(t=t_, sz=SZ_D, color=C['navy'], align='c') for t_ in lines], name='부서 글', tag='부서')
        d.shp(s, x0 + 12, y + 270, x0 + lw_ - 12, y + h - 8, L['foot'], TONE['g1'], color=C['navy'], bold=False, name='실행조직', mg=(0.6, 0, 0.6, 0))
        R = self.right; ry = y + 52; rh = (h - 60) / len(R['rows'])
        for lab, lines in R['rows']:
            d.shp(s, rx + 6, ry + 2, rx + 96, ry + rh - 4, lab, TONE['g1'], color=C['navy'], name='분류', mg=(0.3, 0, 0.3, 0))
            d.t(s, rx + 102, ry, x0 + W - 6, ry + rh, [dict(t=t_, sz=SZ_D, color=C['navy']) for t_ in lines], anchor='m', name='분류 글', tag='분류')
            d.hl(s, rx + 6, ry + rh - 2, x0 + W - 6, ry + rh - 2, color=TONE['g2'], lw=0.75)
            ry += rh


# ---------------------------------------------------------------- L33 수상·성과 카드 행
class AwardRow(Block):
    """라벨 + 카드 N장(사진 + 제목 + 설명 + 일자). 인증·수상 실적을 나란히 보인다."""
    kind = '수상 카드 행'
    gap = 12

    def __init__(self, label, cards):
        self.label, self.cards = label, cards

    def height(self, W):
        return 196

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('수상 카드 행', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['g2'], lw=0.75, name='행 틀')
        d.rail(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, 'blue')
        n = len(self.cards); cw = (W - 124 - 6 * (n - 1)) / n
        for i, (title, sub, date) in enumerate(self.cards):
            cx = x0 + 116 + i * (cw + 6)
            d.photo(s, cx, y + 8, cx + cw, y + 82, '사진')
            d.t(s, cx, y + 86, cx + cw, y + 128, [dict(t=title, sz=SZ_D, b=True, color=C['navy'], align='c')], name='카드 제목', tag='카드제목', mg=(0.3, 0, 0.3, 0))
            d.t(s, cx, y + 126, cx + cw, y + h - 4, [dict(t=sub, sz=9, color=C['slate_700'], align='c'), dict(t=date, sz=9, color=C['slate_700'], align='c')], name='카드 설명', tag='카드설명', mg=(0.3, 0, 0.3, 0))


# ---------------------------------------------------------------- L34 주요성과 띠(회색 라벨)
class GreyResult(Block):
    """주요성과 띠. 핵심성과 띠(그린)와 달리 회색 틀 + 진한 라벨로 단락 중간 성과를 가볍게 모은다."""
    kind = '주요성과 띠'
    gap = 14

    def __init__(self, items, label='주요성과'):
        self.items = [items] if isinstance(items, str) else list(items)
        self.label = label

    def height(self, W):
        lines = sum(est_lines(t, ((W - 160) * K - 8) * 0.93, SZ_C) for t in self.items)
        return max(55, lines * 5.0 / K + 24 + 6 * (len(self.items) - 1))

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('주요성과 띠', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=TONE['g0'], line=TONE['g2'], lw=1.0, name='주요성과 박스')
        d.shp(s, x0 + 6, y + 6, x0 + 126, y + h - 6, self.label, TONE['g4'], sz=SZ_C, name='주요성과 라벨')
        d.t(s, x0 + 142, y + 3, x0 + W - 12, y + h - 3, [dict(t=t, sz=SZ_C, b=True, color=C['navy'], bullet='•', hang=4.2, after=1.0) for t in self.items], name='주요성과 문구', tag='주요성과')


# ---------------------------------------------------------------- L35 번호 띠 + 칩 · 소제목 + 박스 라벨
class NumChipBar(Block):
    """번호 띠 오른쪽 끝에 작은 칩(예: ✔ B.P)을 단다."""
    kind = '번호 띠 + 칩'
    gap = 26

    def __init__(self, n, title, chip):
        self.n, self.title, self.chip = n, title, chip

    def height(self, W):
        return 56

    def draw(self, d, s, x0, y, W):
        d.sec_bar(s, x0, y, self.n, self.title, h=56, w=W)
        xr = x0 + W - 12
        for c in reversed([self.chip] if isinstance(self.chip, str) else list(self.chip)):
            cw = text_w(c, SZ_D, True) / K + 28
            d.shp(s, xr - cw, y + 12, xr, y + 44, c, TONE['g4'], name='번호 띠 칩', mg=(0.3, 0, 0.3, 0))
            xr -= cw + 8


class BoxSubHead(Block):
    """소제목 앞에 분야 박스 라벨을 단다: 가. [적극행정·규제개선] 제목 + 칩."""
    kind = '소제목 + 박스 라벨'
    gap = 22

    def __init__(self, num, box, text, chips=()):
        self.num, self.box, self.text, self.chips = num, box, text, chips

    def height(self, W):
        return 44

    def draw(self, d, s, x0, y, W):
        d.use('소제목 + 박스 라벨', x0, y, x0 + W, y + 44)
        nw = text_w(self.num, SZ_SUB, True) / K + 10
        d.t(s, x0, y, x0 + nw, y + 44, [dict(t=self.num, sz=SZ_SUB, b=True, color=C['navy'])], name='번호', mg=(0, 0, 0, 0), tag=self.num)
        bw = text_w(self.box, SZ_D, True) / K + 28
        d.shp(s, x0 + nw, y + 6, x0 + nw + bw, y + 38, self.box, TONE['g1'], color=C['navy'], line=TONE['g2'], lw=0.75, name='분야 박스', mg=(0.3, 0, 0.3, 0))
        tx = x0 + nw + bw + 12
        tw = text_w(self.text, SZ_SUB, True)
        d.r(s, tx, y + 28, tx + tw / K + 4, y + 36, fill=C['mint_hl'], name='형광 밑줄')
        d.t(s, tx, y, x0 + W, y + 44, [dict(t=self.text, sz=SZ_SUB, b=True, color=C['navy'])], name='소제목', mg=(0, 0, 0, 0), tag=self.text[:12])
        cx = tx + tw / K + 22
        for c in self.chips:
            cw = text_w(c, SZ_D, True) / K + 24
            d.shp(s, cx, y + 6, cx + cw, y + 38, c, TONE['g4'], name='태그칩', mg=(0.3, 0, 0.3, 0))
            cx += cw + 8


# ---------------------------------------------------------------- L36 이행체계 · 화살 머리 칸
class ArrowSteps(Block):
    """머리 칸 끝이 삼각형 화살인 단계 띠(3~4칸) 아래에 칸별 불릿 글을 놓는다. 이행 체계·추진 절차용."""
    kind = '화살 머리 이행 체계'
    gap = 14

    def __init__(self, labels, cols, foot=None):
        self.labels, self.cols, self.foot = labels, cols, foot

    def height(self, W):
        cw = (W - 110) / len(self.labels)
        body = max(items_h(c, cw - 14) for c in self.cols) + 14
        return 46 + body + (46 if self.foot else 0)

    def draw(self, d, s, x0, y, W):
        h = self.height(W); n = len(self.labels)
        d.use('화살 머리 이행 체계', x0, y, x0 + W, y + h)
        d.rail(s, x0 + 2, y + 2, x0 + 108, y + 44, '이행체계', 'blue')
        ex = [x0 + 116 + (W - 116) * i / n for i in range(n + 1)]
        d.step_strip(s, y, y + 44, ex, self.labels)
        body_h = h - 46 - (46 if self.foot else 0)
        d.r(s, x0 + 116, y + 46, x0 + W, y + 46 + body_h, fill=C['white'], line=TONE['g2'], lw=0.75, name='본문 틀')
        d.cols(s, y + 46, y + 46 + body_h, ex, self.cols, tag='이행')
        if self.foot:
            d.shp(s, x0 + 116, y + h - 42, x0 + W, y + h, self.foot, TONE['g1'], color=C['navy'], name='이행 요약', mg=(0.6, 0, 0.6, 0))
