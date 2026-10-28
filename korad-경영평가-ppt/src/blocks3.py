# -*- coding: utf-8 -*-
"""서사 단위 레이아웃 L37~L41 — 한국수자원공사 경영실적보고서 15~18쪽에서 새로 확인한 모양.
(14쪽은 요청에 따라 제외.) 치수는 참조 px(1240px = 210mm)를 실측해 1.113배(1380 격자)로 옮겼고 폭은 본문 폭 W에 비례한다."""
from blocks import *
from blocks2 import _chip


def _icon(d, s, x, y, w, h, cap=''):
    """아이콘 자리(직각 칸). 실제 아이콘은 이 칸 위에 얹는다."""
    d.shp(s, x, y, x + w, y + h, cap, TONE['g1'], color=C['navy'], line=TONE['g2'], lw=0.75, name='아이콘 칸', sz=9, mg=(0.1, 0, 0.1, 0))


def _title_bar(d, s, x0, y0, x1, y1, text, left=True):
    bar = d.r(s, x0, y0, x1, y1, fill=TONE['g1'], name='소제목 띠')
    d.grad(bar, TONE['g1'], C['white'], 0 if left else 180)
    d.t(s, x0 + (50 if left else 6), y0, x1 - (6 if left else 50), y1, [dict(t=text, sz=SZ_C, b=True, color=C['navy'], align='l' if left else 'r')], name='띠 제목', tag=text[:10])
    _icon(d, s, x0 + 4 if left else x1 - 40, y0 + 4, 36, y1 - y0 - 8)


# ------------------------------------------------------------ L37 환경진단 4분면
class QuadPanel(Block):
    """왼쪽 레일 + 2행 × (왼쪽 칸 | 가운데 사진 두 칸 | 오른쪽 칸). 칸마다 제목 띠(아이콘) + 불릿과 * 보충. 행 사이 삼각 화살표."""
    kind = '4분면 진단 패널'
    gap = 12
    ROW = 236

    def __init__(self, label, rows):
        self.label, self.rows = label, rows

    def height(self, W):
        return len(self.rows) * self.ROW + 10

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('4분면 진단 패널', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['line'], lw=0.75, name='패널 외곽')
        d.rail(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, 'blue')
        ax = x0 + 118; aw = W - 124; mid = 250; cw = (aw - mid) / 2
        for i, r in enumerate(self.rows):
            yy = y + 6 + i * self.ROW
            _title_bar(d, s, ax, yy, ax + cw - 4, yy + 48, r['left']['title'], True)
            _title_bar(d, s, ax + cw + mid + 4, yy, ax + aw, yy + 48, r['right']['title'], False)
            for xs, side in ((ax, 'left'), (ax + cw + mid + 4, 'right')):
                d.t(s, xs, yy + 52, xs + cw - 4, yy + self.ROW - 14, [B(t) if not t.startswith('*') else dict(t=t, sz=9, color=C['slate_700']) for t in r[side]['lines']], anchor='t', mg=(1.4, 0.2, 0.6, 0.2), name='칸 본문', tag=f'{i}{side}')
            for k, (chip, cap) in enumerate(r['photos']):
                px = ax + cw + k * (mid / 2) + 2
                d.photo(s, px, yy + 30, px + mid / 2 - 4, yy + self.ROW - 16, cap)
                _chip(d, s, px + 12, yy + 6, chip, h=30)
            if i < len(self.rows) - 1:
                ly = yy + self.ROW - 8
                d.hl(s, ax, ly, ax + aw, ly, color=TONE['g2'], lw=0.75)
                d.tri_arrow(s, ax + cw / 2, ly, 24, 12, down=True)
                d.tri_arrow(s, ax + cw + mid + cw / 2, ly, 24, 12, down=True)


# ------------------------------------------------------------ L37 해석 매트릭스
class TierMatrix(Block):
    """회색 틀 + 왼쪽 단계 레일 여러 개 × 3열. 맨 위 '＋' 두 칸, 단계마다 (제목 칸 | 카드 | 설명 글), 맨 아래 요약 바."""
    kind = '단계 × 3열 매트릭스'
    gap = 12

    def __init__(self, top, rows, foot):
        self.top, self.rows, self.foot = top, rows, foot

    def _rh(self, r):
        return (42 if r.get('heads') else 0) + (112 if r.get('cards') else 0) + (84 if r.get('texts') else 0) + 8

    def height(self, W):
        return 50 + sum(self._rh(r) for r in self.rows) + 52

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('단계 × 3열 매트릭스', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=TONE['g0'], line=TONE['line'], lw=0.75, name='틀')
        ax = x0 + 118; aw = W - 124; cw = (aw - 8) / 3
        half = (aw - 40) / 2
        d.shp(s, ax, y + 6, ax + half, y + 44, self.top[0], TONE['g1'], color=C['navy'], name='상단 칸', mg=(0.4, 0, 0.4, 0))
        d.shp(s, ax + aw - half, y + 6, ax + aw, y + 44, self.top[1], TONE['g1'], color=C['navy'], name='상단 칸', mg=(0.4, 0, 0.4, 0))
        d.shp(s, ax + aw / 2 - 18, y + 8, ax + aw / 2 + 18, y + 42, '+', TONE['g4'], name='더하기', sz=SZ_C, mg=(0, 0, 0, 0))
        yy = y + 50; tones = ['blue', 'teal', 'deep']
        for ri, r in enumerate(self.rows):
            rh = self._rh(r)
            d.rail(s, x0 + 2, yy, x0 + 108, yy + rh - 4, r['label'], tones[ri % 3])
            cy = yy
            if r.get('heads'):
                for i, t_ in enumerate(r['heads']):
                    d.shp(s, ax + i * (cw + 4), cy, ax + i * (cw + 4) + cw, cy + 38, t_, TONE['g1'], color=C['navy'], name='열 머리', mg=(0.4, 0, 0.4, 0))
                cy += 42
            if r.get('cards'):
                for i, t_ in enumerate(r['cards']):
                    cx = ax + i * (cw + 4)
                    d.r(s, cx, cy, cx + cw, cy + 108, fill=TONE['g1'], name='카드')
                    _icon(d, s, cx + 6, cy + 10, 76, 88)
                    d.t(s, cx + 88, cy, cx + cw - 4, cy + 108, [dict(t=t_, sz=SZ_C, b=True, color=C['navy'])], name='카드 글', tag='카드')
                cy += 112
            if r.get('texts'):
                for i, t_ in enumerate(r['texts']):
                    cx = ax + i * (cw + 4)
                    d.t(s, cx, cy, cx + cw, cy + 80, [dict(t=t_, sz=SZ_C, color=C['navy'], align='c')], name='설명 글', tag='설명')
                    if i: d.hl(s, cx - 2, cy + 6, cx - 2, cy + 74, color=TONE['g2'], lw=0.75)
            yy += rh
        d.shp(s, ax, y + h - 48, ax + aw, y + h - 6, self.foot, TONE['g2'], color=C['navy'], name='요약 바', mg=(0.6, 0, 0.6, 0))


# ------------------------------------------------------------ 공통: 사다리꼴 캡션 띠
class FunnelBand(Block):
    """위 칸에서 아래 칸으로 이어 주는 캡션 띠(양끝이 안쪽으로 접힌 사다리꼴). 【 … 】 문구."""
    kind = '캡션 연결 띠'
    gap = 4

    def __init__(self, text, chip=None):
        self.text, self.chip = text, chip

    def height(self, W):
        return 48

    def draw(self, d, s, x0, y, W):
        d.use('캡션 연결 띠', x0, y, x0 + W, y + 48)
        p = d.poly(s, [(x0, y), (x0 + W, y), (x0 + W - 34, y + 46), (x0 + 34, y + 46)], TONE['g1'], name='캡션 띠')
        d.grad(p, TONE['g2'], C['white'], 90)
        if self.chip:
            tx = x0 + 60 + _chip(d, s, x0 + 60, y + 8, self.chip, h=30) + 10
            d.t(s, tx, y, x0 + W - 40, y + 46, [dict(t=self.text, sz=SZ_C, b=True, color=C['navy'])], name='캡션', tag='캡션')
        else:
            d.t(s, x0 + 40, y, x0 + W - 40, y + 46, [dict(t='【 ' + self.text + ' 】', sz=SZ_C, b=True, color=C['navy'], align='c')], name='캡션', tag='캡션')


class ChipBanner(Block):
    """칩(프로세스·정책 제안·방향 설정) + 문장을 담은 전폭 그라데이션 띠."""
    kind = '칩 배너'
    gap = 8

    def __init__(self, chip, text):
        self.chip, self.text = chip, text

    def height(self, W):
        return 50

    def draw(self, d, s, x0, y, W):
        d.use('칩 배너', x0, y, x0 + W, y + 50)
        p = d.poly(s, [(x0, y), (x0 + W, y), (x0 + W - 12, y + 50), (x0 + 12, y + 50)], TONE['g1'], name='배너')
        d.grad(p, TONE['g2'], C['white'], 90)
        cw = _chip(d, s, x0 + 40, y + 10, self.chip, h=30)
        d.t(s, x0 + 50 + cw, y, x0 + W - 30, y + 50, [dict(t=self.text, sz=SZ_SHAPE, b=True, color=C['navy'])], name='배너 글', tag='배너')


# ------------------------------------------------------------ L38 이해관계자 재분류
class StakeGrid(Block):
    """레일 + 위 배너 + 단계 띠 4칸 + 2×2 카드(아이콘 칸 / 기존·확장 칩 줄 / 아래 한 줄 요약)."""
    kind = '이해관계자 2×2 카드'
    gap = 12
    CARD = 172

    def __init__(self, label, banner, steps, cards):
        self.label, self.banner, self.steps, self.cards = label, banner, steps, cards

    def height(self, W):
        return 6 + 44 + 52 + 2 * self.CARD + 10

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('이해관계자 2×2 카드', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['line'], lw=0.75, name='패널 외곽')
        d.rail(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, 'blue')
        ax = x0 + 118; aw = W - 124
        d.shp(s, ax, y + 6, ax + aw, y + 46, self.banner, TONE['g2'], color=C['navy'], name='배너', mg=(0.4, 0, 0.4, 0))
        e = [ax + aw * i / len(self.steps) for i in range(len(self.steps) + 1)]
        d.step_strip(s, y + 52, y + 94, e, self.steps)
        cw = (aw - 8) / 2
        for i, c in enumerate(self.cards):
            cx = ax + (i % 2) * (cw + 8); cy = y + 102 + (i // 2) * self.CARD
            d.r(s, cx, cy, cx + cw, cy + self.CARD - 6, fill=C['white'], line=TONE['g2'], lw=0.75, name='카드')
            _icon(d, s, cx + 6, cy + 8, 78, 78, c['icon'])
            for k, (chip, text) in enumerate(c['rows']):
                ry = cy + 8 + k * 40
                d.shp(s, cx + 92, ry, cx + 144, ry + 34, chip, TONE['g1'], color=C['navy'], line=TONE['g2'], lw=0.75, name='구분 칩', mg=(0.2, 0, 0.2, 0))
                d.t(s, cx + 150, ry, cx + cw - 4, ry + 34, [dict(t=text, sz=SZ_D, color=C['navy'])], name='칩 줄 글', tag=f'{i}{k}')
            d.shp(s, cx + 4, cy + 96, cx + cw - 4, cy + self.CARD - 10, c['foot'], TONE['g0'], color=C['navy'], bold=False, name='카드 요약', mg=(0.6, 0, 0.6, 0))


# ------------------------------------------------------------ L38 가치전략 진단
class SurveyPanel(Block):
    """레일 + 위 불릿 + 3열 머리/불릿 + 강조 띠 + (가치체계·전략체계) × 3 지표(내/외 수치) + 오른쪽 ☑ 판단."""
    kind = '진단 결과 패널'
    gap = 12

    def __init__(self, label, intro, heads, subs, strip, grid, notes):
        self.label, self.intro, self.heads, self.subs, self.strip, self.grid, self.notes = label, intro, heads, subs, strip, grid, notes

    def height(self, W):
        return 6 + 70 + 38 + 84 + 50 + len(self.grid) * 76 + 10

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('진단 결과 패널', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['line'], lw=0.75, name='패널 외곽')
        d.rail(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, 'blue')
        ax = x0 + 118; aw = W - 124; cw = (aw - 8) / 3
        d.t(s, ax, y + 4, ax + aw, y + 74, [B(self.intro[0]), dict(t=self.intro[1], sz=9, color=C['slate_700'])], name='도입 글', tag='도입')
        for i, t_ in enumerate(self.heads):
            d.shp(s, ax + i * (cw + 4), y + 76, ax + i * (cw + 4) + cw, y + 112, t_, TONE['g1'], color=C['navy'], name='열 머리', mg=(0.4, 0, 0.4, 0))
            d.t(s, ax + i * (cw + 4), y + 114, ax + i * (cw + 4) + cw, y + 198, [B(self.subs[i][0]), dict(t=self.subs[i][1], sz=9, color=C['slate_700'])], name='열 본문', tag=f'열{i}')
        d.shp(s, ax, y + 202, ax + aw, y + 242, self.strip, TONE['g2'], color=C['navy'], name='강조 띠', mg=(0.6, 0, 0.6, 0))
        gw = aw * 0.70; nx = ax + gw + 8
        for ri, (lab, cells) in enumerate(self.grid):
            ry = y + 248 + ri * 76
            d.shp(s, ax, ry, ax + 64, ry + 70, lab, TONE['g4'], name='행 라벨', mg=(0.2, 0, 0.2, 0))
            for ci, (t_, nums) in enumerate(cells):
                cx = ax + 70 + ci * ((gw - 70) / 3)
                d.t(s, cx, ry, cx + (gw - 70) / 3 - 4, ry + 34, [dict(t=t_, sz=SZ_D, b=True, color=C['navy'], align='c')], name='지표', tag='지표')
                d.t(s, cx, ry + 36, cx + (gw - 70) / 3 - 4, ry + 70, [dict(t=nums, sz=SZ_D, color=C['navy'], align='c')], name='수치', tag='수치')
            d.hl(s, ax + 70, ry + 35, ax + gw, ry + 35, color=TONE['g2'], lw=0.75)
        for ri, t_ in enumerate(self.notes):
            ry = y + 248 + ri * 76
            d.t(s, nx, ry, ax + aw, ry + 70, [dict(t='☑ ' + t_, sz=SZ_D, b=True, color=C['navy'])], name='판단 글', tag='판단')


# ------------------------------------------------------------ L38 가치전략 롤링
class RollingCols(Block):
    """단계 머리(칩) 3칸 + 칸마다 (아이콘 + 큰 문구 / 요약 줄 / 불릿)."""
    kind = '롤링 3열'
    gap = 12

    def __init__(self, heads, cols):
        self.heads, self.cols = heads, cols

    def height(self, W):
        return 46 + 118 + 38 + 76 + 8

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('롤링 3열', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['g2'], lw=0.75, name='틀')
        e = [x0 + W * i / 3 for i in range(4)]
        d.step_strip(s, y, y + 46, e, self.heads)
        for i, c in enumerate(self.cols):
            a, b = e[i], e[i + 1]
            _icon(d, s, a + 10, y + 56, 76, 80)
            d.t(s, a + 92, y + 50, b - 8, y + 164, [dict(t=c['big'], sz=SZ_C, b=True, color=C['navy'])], name='큰 문구', tag=f'큰{i}')
            d.shp(s, a + 4, y + 166, b - 4, y + 202, c['sum'], TONE['g1'], color=C['navy'], bold=False, name='요약 줄', mg=(0.4, 0, 0.4, 0))
            d.t(s, a + 4, y + 206, b - 4, y + h - 4, [B(c['bullet'])], name='불릿', tag=f'불릿{i}')
            if i: d.hl(s, a, y + 56, a, y + h - 8, color=TONE['g2'], lw=0.75)


# ------------------------------------------------------------ L39 영향력·관심도 + 맞춤 소통
class InfluencePanel(Block):
    """왼쪽 영향력×관심도 4분면, 오른쪽 '유형별 맞춤형 소통' 번호 행 4개 + '전방위 확산' 사진 행 3개."""
    kind = '유형 분류 + 맞춤 소통'
    gap = 12

    def __init__(self, quad, caption, left_title, rows, right_title, spread):
        self.quad, self.caption, self.left_title, self.rows, self.right_title, self.spread = quad, caption, left_title, rows, right_title, spread

    def height(self, W):
        return 410

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('유형 분류 + 맞춤 소통', x0, y, x0 + W, y + h)
        lw_ = W * 0.34
        d.r(s, x0, y, x0 + lw_, y + h, fill=TONE['g1'], line=TONE['g2'], lw=0.75, name='분류 패널')
        qx = x0 + 30; qy = y + 10; qw = lw_ - 40; qh = h - 92
        d.r(s, qx, qy, qx + qw, qy + qh, fill=C['white'], line=TONE['g3'], lw=0.75, name='4분면')
        d.hl(s, qx + qw / 2, qy, qx + qw / 2, qy + qh, color=TONE['g3'], lw=0.75); d.hl(s, qx, qy + qh / 2, qx + qw, qy + qh / 2, color=TONE['g3'], lw=0.75)
        for i, (name, items) in enumerate(self.quad):
            cx = qx + (i % 2) * qw / 2; cy = qy + (i // 2) * qh / 2
            d.shp(s, cx + 4, cy + 4 if i < 2 else cy + qh / 2 - 34, cx + qw / 2 - 4, (cy + 34) if i < 2 else cy + qh / 2 - 4, name, TONE['g4'], sz=SZ_D, name='분면 이름', mg=(0.2, 0, 0.2, 0))
            d.t(s, cx + 4, cy + 36 if i < 2 else cy + 4, cx + qw / 2 - 4, cy + qh / 2 - 36 if i >= 2 else cy + qh / 2 - 4, [dict(t=t_, sz=9, color=C['navy'], align='c') for t_ in items], name='분면 글', tag=f'분면{i}', mg=(0.2, 0, 0.2, 0))
        d.t(s, x0 + 2, y + 10, x0 + 28, y + qh, [dict(t='영향력', sz=9, color=C['slate_700'], align='c')], name='세로축', tag='세로축', mg=(0, 0, 0, 0))
        d.t(s, qx, qy + qh + 2, qx + qw, qy + qh + 34, [dict(t='관심도 ▶', sz=9, color=C['slate_700'], align='c')], name='가로축', tag='가로축', mg=(0, 0, 0, 0))
        d.shp(s, x0 + 6, y + h - 52, x0 + lw_ - 6, y + h - 6, self.caption, TONE['g1'], color=C['navy'], name='분류 설명', mg=(0.4, 0, 0.4, 0))
        rx = x0 + lw_ + 8; rw = W - lw_ - 8; mw = rw * 0.60
        d.r(s, rx, y, x0 + W, y + h, fill=C['white'], line=TONE['g2'], lw=0.75, name='소통 패널')
        d.shp(s, rx, y, rx + mw, y + 44, self.left_title, TONE['g4'], name='패널 머리', sz=SZ_C, mg=(0.4, 0, 0.4, 0))
        d.shp(s, rx + mw + 6, y, x0 + W, y + 44, self.right_title, TONE['g5'], name='패널 머리', sz=SZ_C, mg=(0.4, 0, 0.4, 0))
        rh = (h - 52) / len(self.rows)
        for i, (a, b) in enumerate(self.rows):
            ry = y + 50 + i * rh
            d.t(s, rx + 2, ry, rx + 34, ry + rh, [dict(t=str(i + 1), sz=22, b=True, color=TONE['g2'], align='c')], name='번호', tag='번호', mg=(0, 0, 0, 0))
            for k, (t_, tag_) in enumerate((a, b)):
                bx = rx + 38 + k * (mw - 40) / 2; bw = (mw - 40) / 2 - 4
                d.t(s, bx, ry, bx + bw, ry + rh * 0.45, [dict(t=t_, sz=SZ_D, color=C['navy'], align='c')], name='소통 이름', tag=f'소통{i}{k}', mg=(0.2, 0, 0.2, 0))
                d.shp(s, bx, ry + rh * 0.48, bx + bw, ry + rh - 6, tag_, C['white'], color=C['navy'], line=TONE['g4'], lw=1.0, name='소통 칩', mg=(0.2, 0, 0.2, 0))
        sx = rx + mw + 6; sw = x0 + W - sx; sh = (h - 52) / len(self.spread)
        for i, (chip, text) in enumerate(self.spread):
            sy = y + 50 + i * sh
            d.photo(s, sx + 2, sy, sx + sw * 0.40, sy + sh - 6, '사진')
            _chip(d, s, sx + sw * 0.42, sy + 4, chip, h=26)
            d.t(s, sx + sw * 0.42, sy + 30, x0 + W - 4, sy + sh - 6, [dict(t=text, sz=SZ_D, b=True, color=C['navy'])], name='확산 글', tag=f'확산{i}', mg=(0.2, 0, 0.2, 0))


# ------------------------------------------------------------ L41 프로세스 로드맵
class Timeline(Block):
    """왼쪽 주체 박스 + 오른쪽 START 선 위·아래로 마디(상자 + 날짜)를 엇갈려 놓은 로드맵."""
    kind = '로드맵 타임라인'
    gap = 8

    def __init__(self, who, top, bottom):
        self.who, self.top, self.bottom = who, top, bottom

    def height(self, W):
        return 236

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('로드맵 타임라인', x0, y, x0 + W, y + h)
        ww = W * 0.19
        d.shp(s, x0, y + 2, x0 + ww, y + h - 2, '\n'.join(self.who), TONE['g1'], color=C['navy'], name='주체 박스', mg=(0.6, 0, 0.6, 0))
        lx = x0 + ww + 90; lr = x0 + W - 6; ly = y + h / 2
        d.t(s, x0 + ww + 4, ly - 14, lx - 4, ly + 14, [dict(t='START', sz=SZ_D, b=True, color=C['navy'])], name='시작', tag='시작', mg=(0, 0, 0, 0))
        d.r(s, lx, ly - 3, lr, ly + 3, fill=TONE['g4'], name='로드맵 선')
        n = len(self.top); cw = (lr - lx) / n
        for i, (box, date) in enumerate(self.top):
            cx = lx + i * cw
            d.shp(s, cx + 2, y + 2, cx + cw - 4, y + 66, box, C['white'], color=C['navy'], line=TONE['g3'], lw=0.75, bold=False, name='위 마디', mg=(0.3, 0, 0.3, 0))
            d.tri_arrow(s, cx + cw / 2 - 1, y + 74, 16, 9, down=True)
            d.t(s, cx, y + 78, cx + cw - 2, y + 112, [dict(t=date, sz=SZ_C, b=True, color=C['navy'], align='c')], name='날짜', tag='날짜', mg=(0, 0, 0, 0))
            d.r(s, cx + cw / 2 - 7, ly - 7, cx + cw / 2 + 5, ly + 7, fill=C['white'], line=TONE['g4'], lw=1.5, name='마디 점')
        m = len(self.bottom); cw2 = (lr - lx) / m
        for i, (box, date) in enumerate(self.bottom):
            cx = lx + i * cw2
            d.r(s, cx + cw2 / 2 - 7, ly - 7, cx + cw2 / 2 + 5, ly + 7, fill=C['white'], line=TONE['g4'], lw=1.5, name='마디 점')
            d.t(s, cx, ly + 10, cx + cw2 - 2, ly + 46, [dict(t=date, sz=SZ_C, b=True, color=C['navy'], align='c')], name='날짜', tag='날짜', mg=(0, 0, 0, 0))
            d.shp(s, cx + 2, ly + 50, cx + cw2 - 4, y + h - 2, box, C['white'], color=C['navy'], line=TONE['g3'], lw=0.75, bold=False, name='아래 마디', mg=(0.3, 0, 0.3, 0))


class DateCols(Block):
    """월 칩 + 제목 머리 3칸, 칸마다 불릿 + * 보충."""
    kind = '월별 3열'
    gap = 8

    def __init__(self, cols):
        self.cols = cols

    def height(self, W):
        return 46 + 76

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('월별 3열', x0, y, x0 + W, y + h)
        n = len(self.cols); e = [x0 + W * i / n for i in range(n + 1)]
        for i, c in enumerate(self.cols):
            a, b = e[i], e[i + 1]
            d.r(s, a, y, b - 4, y + 44, fill=TONE['g1'], name='머리')
            cw = _chip(d, s, a + 10, y + 7, c['chip'], h=30)
            d.t(s, a + 16 + cw, y, b - 8, y + 44, [dict(t=c['head'], sz=SZ_SHAPE, b=True, color=C['navy'])], name='머리 글', tag=f'머리{i}')
            d.t(s, a, y + 48, b - 4, y + h, [B(c['bullet']), dict(t=c['note'], sz=9, color=C['slate_700'])], name='본문', tag=f'본문{i}')
            if i: d.hl(s, a - 2, y + 52, a - 2, y + h - 4, color=TONE['g2'], lw=0.75)


# ------------------------------------------------------------ L41 과제 지도
class TaskMap(Block):
    """두 머리(직접 반영 | 확장 반영) 아래 분야 라벨 × 번호 칩 + 과제명 목록."""
    kind = '번호 과제 지도'
    gap = 8
    LINE = 31

    def __init__(self, heads, rows):
        self.heads, self.rows = heads, rows

    def _rh(self, r):
        return max(len(r['left']), len(r['right'])) * self.LINE + 12

    def height(self, W):
        return 46 + sum(self._rh(r) for r in self.rows)

    def draw(self, d, s, x0, y, W):
        d.use('번호 과제 지도', x0, y, x0 + W, y + self.height(W))
        lw_ = 92; cw = (W - lw_ - 8) / 2 ; ax = x0 + lw_ + 4
        d.step_strip(s, y, y + 42, [ax, ax + cw, ax + 2 * cw + 4], self.heads)
        yy = y + 46
        for ri, r in enumerate(self.rows):
            rh = self._rh(r)
            d.r(s, x0, yy, x0 + W, yy + rh, fill=C['white'] if ri % 2 == 0 else TONE['g0'], line=TONE['g2'], lw=0.75, name='행 틀')
            d.rail(s, x0 + 2, yy + 2, x0 + lw_, yy + rh - 2, r['label'], 'blue')
            for ci, key in enumerate(('left', 'right')):
                bx = ax + ci * cw
                for k, (no, text) in enumerate(r[key]):
                    iy = yy + 6 + k * self.LINE
                    nw = text_w(no, 9, True) / K + 14
                    d.shp(s, bx + 4, iy + 3, bx + 4 + nw, iy + self.LINE - 3, no, C['white'], color=C['navy'], line=TONE['g4'], lw=0.75, name='번호 칩', sz=9, mg=(0, 0, 0, 0))
                    d.t(s, bx + 10 + nw, iy, bx + cw - 4, iy + self.LINE, [dict(t=text, sz=SZ_D, color=C['navy'])], name='과제명', tag=f'과제{ri}{ci}{k}', mg=(0.2, 0, 0.2, 0))
            d.hl(s, ax + cw - 2, yy + 4, ax + cw - 2, yy + rh - 4, color=TONE['g3'], lw=0.75)
            yy += rh


# ------------------------------------------------------------ L41 방향 설정 짝
class PairLinks(Block):
    """두 갈래 머리(칩 + 제목) 아래, 왼쪽 알약 칸 — 연결선 — 오른쪽 상자를 한 쌍씩 쌓는다."""
    kind = '짝 연결 패널'
    gap = 8
    ROW = 62

    def __init__(self, left, right):
        self.left, self.right = left, right

    def height(self, W):
        return 50 + max(len(self.left['pairs']), len(self.right['pairs'])) * self.ROW + 6

    def draw(self, d, s, x0, y, W):
        d.use('짝 연결 패널', x0, y, x0 + W, y + self.height(W))
        pw = (W - 12) / 2
        for k, side in enumerate((self.left, self.right)):
            px = x0 + k * (pw + 12)
            bar = d.r(s, px, y, px + pw, y + 44, fill=TONE['g1'], name='머리')
            d.grad(bar, TONE['g2'], C['white'], 0)
            cw = _chip(d, s, px + 8, y + 7, side['chip'], h=30)
            d.t(s, px + 14 + cw, y, px + pw - 20, y + 44, [dict(t=side['title'], sz=SZ_SHAPE, b=True, color=C['navy'])], name='머리 글', tag=f'머리{k}')
            d.tri_arrow(s, px + pw - 10, y + 22, 24, 14, down=False)
            for i, (a, b) in enumerate(side['pairs']):
                ry = y + 50 + i * self.ROW
                d.shp(s, px, ry + 4, px + pw * 0.45, ry + self.ROW - 4, a, TONE['g1'], color=C['navy'], bold=False, name='알약 칸', mg=(0.6, 0, 0.6, 0))
                d.hl(s, px + pw * 0.45, ry + self.ROW / 2, px + pw * 0.55, ry + self.ROW / 2, color=TONE['g4'], lw=1.25)
                d.r(s, px + pw * 0.45 - 4, ry + self.ROW / 2 - 4, px + pw * 0.45 + 4, ry + self.ROW / 2 + 4, fill=TONE['g4'], name='연결 점')
                d.shp(s, px + pw * 0.55, ry + 4, px + pw, ry + self.ROW - 4, b, C['white'], color=C['navy'], line=TONE['g4'], lw=1.25, name='상자', mg=(0.4, 0, 0.4, 0))


# ------------------------------------------------------------ L30·L33 괄호 머리 3열
class BracketCols(Block):
    """칸 제목 아래에 삼각 화살표(▼)가 달린 머리 N칸 + 칸마다 불릿(사진 칸 선택). 환경분석·구성/제도화처럼 위에서 아래로 내려가는 서술."""
    kind = '괄호 머리 칸'
    gap = 10
    BODY = 150

    def __init__(self, heads, cols, label=None):
        self.heads, self.cols, self.label = heads, cols, label

    def height(self, W):
        return 54 + self.BODY + 6

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('괄호 머리 칸', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['line'], lw=0.75, name='틀')
        ax = x0
        if self.label:
            d.rail(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, 'blue'); ax = x0 + 116
        n = len(self.heads); cw = (x0 + W - 6 - ax) / n
        for i, (hd, c) in enumerate(zip(self.heads, self.cols)):
            a = ax + i * cw
            bar = d.r(s, a + 4, y + 6, a + cw - 4, y + 40, fill=TONE['g1'], name='칸 제목 띠')
            d.t(s, a + 4, y + 6, a + cw - 4, y + 40, [dict(t=hd, sz=SZ_C, b=True, color=C['navy'], align='c')], name='칸 제목', tag=f'제목{i}')
            d.tri_arrow(s, a + cw / 2, y + 47, 22, 10, down=True)
            tx0 = a + 6
            if c.get('photo'):
                d.photo(s, a + cw * 0.52, y + 56, a + cw - 6, y + 54 + self.BODY - 8, c['photo'])
                tx1 = a + cw * 0.50
            else:
                tx1 = a + cw - 6
            d.t(s, tx0, y + 54, tx1, y + 54 + self.BODY - 4, [B(t) if not t.startswith('*') else dict(t=t, sz=9, color=C['slate_700']) for t in c['lines']], anchor='m', mg=(1.2, 0.2, 0.6, 0.2), name='칸 본문', tag=f'본문{i}')
            if i: d.hl(s, a, y + 52, a, y + h - 8, color=TONE['g2'], lw=0.75)


# ------------------------------------------------------------ L31·L32 종합성과 · 추진성과 막대 카드
class ResultCharts(Block):
    """회색 라벨 + 위 요약 띠 + 카드 N장(왼쪽 문구 상자 | 오른쪽 연도별 막대). 종합성과·추진성과를 수치로 못 박는다."""
    kind = '성과 막대 카드'
    gap = 12

    def __init__(self, label, banner, cards):
        self.label, self.banner, self.cards = label, banner, cards

    def height(self, W):
        return 52 + 128 + 12

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('성과 막대 카드', x0, y, x0 + W, y + h)
        d.r(s, x0, y, x0 + W, y + h, fill=C['white'], line=TONE['g3'], lw=1.0, name='틀')
        d.shp(s, x0 + 2, y + 2, x0 + 108, y + h - 2, self.label, TONE['g2'], color=C['navy'], name='성과 라벨', sz=SZ_C, mg=(0.4, 0, 0.4, 0))
        ax = x0 + 116; aw = W - 122
        d.shp(s, ax, y + 6, ax + aw, y + 44, self.banner, TONE['g1'], color=C['navy'], name='성과 띠', mg=(0.6, 0, 0.6, 0))
        n = len(self.cards); cw = (aw - 8 * (n - 1)) / n
        for i, c in enumerate(self.cards):
            cx = ax + i * (cw + 8)
            d.r(s, cx, y + 50, cx + cw, y + h - 6, fill=C['white'], line=TONE['g3'], lw=0.75, name='카드')
            tw = cw * 0.46 if c.get('bars') and not c.get('compact') else cw
            if c.get('compact'):
                d.t(s, cx + 4, y + 52, cx + cw - 4, y + 80, [dict(t=t_, sz=SZ_D, b=True, color=C['navy'], align='c') for t_ in c['lines']], name='카드 문구', tag=f'문구{i}', mg=(0.3, 0, 0.3, 0))
            else:
                d.t(s, cx + 4, y + 52, cx + tw, y + h - 8, [dict(t=t_, sz=SZ_D, b=True, color=C['navy'], align='c') for t_ in c['lines']], name='카드 문구', tag=f'문구{i}', mg=(0.3, 0, 0.3, 0))
            bars = c.get('bars')
            if bars:
                mx = max(v for _, v, _ in bars); bw = 30
                bx0 = cx + 14 if c.get('compact') else cx + tw + 10
                step = (cw - 28) / len(bars) if c.get('compact') else (cw - tw - 20) / len(bars)
                for k, (yr, v, lab) in enumerate(bars):
                    bx = bx0 + k * step; hh = max(14, (30 if c.get('compact') else 40) * v / mx)
                    d.r(s, bx, y + h - 34 - hh, bx + bw, y + h - 34, fill=TONE['g3'] if k < len(bars) - 1 else TONE['g4'], name='막대')
                    d.t(s, bx - 16, y + h - 34 - hh - 32, bx + bw + 16, y + h - 34 - hh - 2, [dict(t=lab, sz=9, b=True, color=C['navy'], align='c')], name='값', tag='값', mg=(0, 0, 0, 0))
                    d.t(s, bx - 16, y + h - 32, bx + bw + 16, y + h - 8, [dict(t=yr, sz=9, color=C['slate_700'], align='c')], name='연도', tag='연도', mg=(0, 0, 0, 0))


# ------------------------------------------------------------ L35 그룹 소제목 + 카드 격자
class CardGrid(Block):
    """그룹마다 [아이콘 + 분류 칩 + 굵은 제목] 소제목 줄 아래 카드 격자(2열). 카드 = 칩 + 제목 머리 / 불릿 / 오른쪽 작은 막대 도표 또는 요약 칸."""
    kind = '그룹 카드 격자'
    gap = 14
    ROW = 200

    def __init__(self, groups):
        self.groups = groups

    def _gh(self, g):
        rows = (len(g['cards']) + 1) // 2
        return 48 + rows * self.ROW + 10

    def height(self, W):
        return sum(self._gh(g) + 12 for g in self.groups) - 12

    def draw(self, d, s, x0, y, W):
        d.use('그룹 카드 격자', x0, y, x0 + W, y + self.height(W))
        yy = y
        for g in self.groups:
            gh = self._gh(g)
            _icon(d, s, x0, yy + 4, 32, 32)
            cw_ = _chip(d, s, x0 + 40, yy + 4, g['chip'], h=32)
            d.t(s, x0 + 48 + cw_, yy, x0 + W - 4, yy + 40, [dict(t=g['title'], sz=SZ_SUB, b=True, color=C['navy'])], name='그룹 제목', tag=g['chip'][:6], mg=(0, 0, 0, 0))
            d.r(s, x0, yy + 44, x0 + W, yy + gh, fill=C['white'], line=TONE['line'], lw=1.25, name='그룹 틀')
            n = len(g['cards']); half = (W - 12) / 2
            for i, c in enumerate(g['cards']):
                cx = x0 + 6 + (i % 2) * half; cy = yy + 48 + (i // 2) * self.ROW
                bar = d.r(s, cx, cy, cx + half - 4, cy + 38, fill=TONE['g1'], name='카드 머리')
                d.grad(bar, TONE['g1'], C['white'], 0)
                kw = _chip(d, s, cx + 8, cy + 4, c['chip'], h=30)
                d.t(s, cx + 14 + kw, cy, cx + half - 8, cy + 38, [dict(t=c['title'], sz=SZ_C, b=True, color=C['navy'])], name='카드 제목', tag=c['chip'][:6])
                tw = (half - 8) * (0.62 if c.get('bars') or c.get('side') else 1.0)
                d.t(s, cx, cy + 40, cx + tw, cy + self.ROW - 6, [B(t) if not t.startswith('*') else dict(t=t, sz=9, color=C['slate_700']) for t in c['lines']], anchor='m', mg=(1.2, 0.2, 0.6, 0.2), name='카드 본문', tag=f'{g["chip"][:3]}{i}')
                if c.get('bars'):
                    bars = c['bars']; mx = max(v for _, v, _ in bars); bx0 = cx + tw + 14; stp = (half - 8 - tw - 20) / len(bars)
                    d.t(s, cx + tw, cy + 40, cx + half - 8, cy + 70, [dict(t=c.get('cap', ''), sz=9, b=True, color=C['navy'], align='c')], name='도표 제목', tag='도표', mg=(0, 0, 0, 0))
                    for k, (yr, v, lab) in enumerate(bars):
                        bx = bx0 + k * stp; hh = max(12, 24 * v / mx); base = cy + self.ROW - 34
                        d.r(s, bx, base - hh, bx + 26, base, fill=TONE['g3'] if k < len(bars) - 1 else TONE['g4'], name='막대')
                        d.t(s, bx - 26, base - hh - 32, bx + 52, base - hh - 2, [dict(t=lab, sz=9, b=True, color=C['navy'], align='c')], name='값', tag='값', mg=(0, 0, 0, 0))
                        d.t(s, bx - 26, base + 2, bx + 52, base + 30, [dict(t=yr, sz=9, color=C['slate_700'], align='c')], name='연도', tag='연도', mg=(0, 0, 0, 0))
                elif c.get('side'):
                    d.shp(s, cx + tw + 8, cy + 46, cx + half - 12, cy + self.ROW - 12, c['side'], TONE['g1'], color=C['navy'], line=TONE['g2'], lw=0.75, name='요약 칸', mg=(0.4, 0, 0.4, 0))
                if i % 2 == 0 and i + 1 < n:
                    d.hl(s, cx + half - 2, cy + 6, cx + half - 2, cy + self.ROW - 8, color=TONE['g2'], lw=0.75)
            yy += gh + 12


# ------------------------------------------------------------ L42 십자 패널
class CrossPanel(Block):
    """위 머리 두 칸(칩 + 제목) → 위쪽 불릿 두 칸 → 가운데 아이콘 → 아래쪽 불릿 두 칸 → 아래 머리 두 칸. 네 방향 지원을 한 판에 모은다."""
    kind = '십자 패널'
    gap = 12

    def __init__(self, top, upper, lower, bottom, side_label=None):
        self.top, self.upper, self.lower, self.bottom = top, upper, lower, bottom

    def height(self, W):
        return 54 + 150 + 30 + 150 + 54

    def draw(self, d, s, x0, y, W):
        h = self.height(W)
        d.use('십자 패널', x0, y, x0 + W, y + h)
        half = (W - 40) / 2; xr = x0 + W - half
        for k, (chip, text) in enumerate(self.top):
            xa = x0 if k == 0 else xr
            d.r(s, xa, y, xa + half, y + 48, fill=TONE['g5'], name='위 머리')
            cw = _chip(d, s, xa + 12, y + 8, chip, h=32)
            d.t(s, xa + 18 + cw, y, xa + half - 10, y + 48, [dict(t=text, sz=SZ_C, b=True, color=C['white'])], name='위 머리 글', tag=chip[:6])
        for blk_, yy0 in ((self.upper, y + 54), (self.lower, y + 54 + 150 + 30)):
            for k, lines in enumerate(blk_):
                xa = x0 if k == 0 else xr
                d.t(s, xa, yy0, xa + half, yy0 + 150, [B(t) if not t.startswith('*') else dict(t=t, sz=9, color=C['slate_700']) for t in lines], anchor='m', mg=(1.2, 0.2, 0.6, 0.2), name='본문', tag=f'본문{k}')
        d.r(s, x0, y + 54 + 150 + 12, x0 + W, y + 54 + 150 + 20, fill=TONE['g2'], name='가운데 띠')
        _icon(d, s, x0 + W / 2 - 34, y + 54 + 150 - 8, 68, 56, '아이콘')
        for k, (chip, text) in enumerate(self.bottom):
            xa = x0 if k == 0 else xr
            yb = y + h - 48
            d.r(s, xa, yb, xa + half, yb + 48, fill=TONE['g5'], name='아래 머리')
            cw = _chip(d, s, xa + 12, yb + 8, chip, h=32)
            d.t(s, xa + 18 + cw, yb, xa + half - 10, yb + 48, [dict(t=text, sz=SZ_C, b=True, color=C['white'])], name='아래 머리 글', tag=chip[:6])


# ------------------------------------------------------------ L47 탭 카드(그룹 소제목 + 2열 카드)
class TabCards(Block):
    """그룹 소제목([아이콘 + 칩 + 한 문장]) 아래 2열 카드. 카드 = 모서리 탭(단계명) + 가운데 제목 / 불릿 / 아래 요약 띠."""
    kind = '탭 카드 격자'
    gap = 14
    ROW = 196

    def __init__(self, chip, title, cards):
        self.chip, self.title, self.cards = chip, title, cards

    def height(self, W):
        return 48 + ((len(self.cards) + 1) // 2) * self.ROW + 4

    def draw(self, d, s, x0, y, W):
        d.use('탭 카드 격자', x0, y, x0 + W, y + self.height(W))
        _icon(d, s, x0, y + 4, 32, 32)
        cw_ = _chip(d, s, x0 + 40, y + 4, self.chip, h=32)
        d.t(s, x0 + 48 + cw_, y, x0 + W - 4, y + 40, [dict(t=self.title, sz=SZ_SUB, b=True, color=C['navy'])], name='그룹 제목', tag=self.chip[:6], mg=(0, 0, 0, 0))
        half = (W - 8) / 2
        for i, c in enumerate(self.cards):
            cx = x0 + (i % 2) * (half + 8); cy = y + 46 + (i // 2) * self.ROW
            d.r(s, cx, cy, cx + half, cy + self.ROW - 6, fill=C['white'], line=TONE['g3'], lw=1.0, name='카드 틀')
            d.shp(s, cx, cy, cx + 76, cy + 38, c['tab'], TONE['g5'], name='탭', mg=(0.2, 0, 0.2, 0))
            d.t(s, cx + 82, cy, cx + half - 6, cy + 38, [dict(t=c['title'], sz=SZ_C, b=True, color=C['navy'], align='c')], name='카드 제목', tag=c['tab'])
            d.t(s, cx + 4, cy + 42, cx + half - 4, cy + self.ROW - 58, [B(t) for t in c['lines']], anchor='m', mg=(1.2, 0.2, 0.6, 0.2), name='카드 본문', tag=f'본문{i}')
            d.shp(s, cx, cy + self.ROW - 52, cx + half, cy + self.ROW - 6, c['foot'], TONE['g2'], color=C['navy'], name='카드 요약', mg=(0.6, 0, 0.6, 0))


# ------------------------------------------------------------ L49 니즈 → 실적 → 성과 행렬
class NeedsMatrix(Block):
    """머리(3칸 단계 띠) 아래 행마다 [레일 라벨 | 니즈 문구 | 추진실적(불릿 + 칩 줄) | 성과(머리 + 문구)]."""
    kind = '니즈·실적·성과 행렬'
    gap = 12
    ROW = 134

    def __init__(self, heads, rows):
        self.heads, self.rows = heads, rows

    def height(self, W):
        return 48 + len(self.rows) * self.ROW

    def draw(self, d, s, x0, y, W):
        d.use('니즈·실적·성과 행렬', x0, y, x0 + W, y + self.height(W))
        ax = x0 + 116; aw = W - 122
        w1, w2 = aw * 0.28, aw * 0.43
        ed = [ax, ax + w1, ax + w1 + w2, ax + aw]
        d.step_strip(s, y, y + 44, ed, self.heads)
        for i, r in enumerate(self.rows):
            ry = y + 48 + i * self.ROW
            d.r(s, x0, ry, x0 + W, ry + self.ROW - 4, fill=C['white'], line=TONE['g2'], lw=0.75, name='행 틀')
            d.rail(s, x0 + 2, ry + 2, x0 + 108, ry + self.ROW - 6, r['label'], 'blue')
            d.t(s, ed[0], ry, ed[1] - 4, ry + self.ROW - 4, [dict(t=t_, sz=SZ_D, color=C['navy'], align='c') for t_ in r['need']], name='니즈', tag=f'니즈{i}')
            d.t(s, ed[1], ry + 2, ed[2] - 4, ry + 40, [B(r['act'][0])], name='실적 머리', tag=f'실적{i}', mg=(1.2, 0.2, 0.6, 0.2))
            for k, (chip, text) in enumerate(r['act'][1:]):
                ky = ry + 44 + k * 42
                kw = _chip(d, s, ed[1] + 8, ky + 4, chip, h=30)
                d.t(s, ed[1] + 14 + kw, ky, ed[2] - 4, ky + 38, [dict(t=text, sz=SZ_D, b=True, color=C['navy'])], name='칩 줄 글', tag=f'{chip}{i}')
            d.shp(s, ed[2] + 4, ry + 6, ed[3] - 4, ry + 48, r['res'][0], TONE['g1'], color=C['navy'], name='성과 머리', mg=(0.4, 0, 0.4, 0))
            d.t(s, ed[2] + 4, ry + 50, ed[3] - 4, ry + self.ROW - 8, [dict(t=t_, sz=SZ_D, color=C['navy'], align='c') for t_ in r['res'][1]], name='성과 글', tag=f'성과{i}')
            d.hl(s, ed[1] - 2, ry + 6, ed[1] - 2, ry + self.ROW - 10, color=TONE['g2'], lw=0.75)
            d.hl(s, ed[2] - 2, ry + 6, ed[2] - 2, ry + self.ROW - 10, color=TONE['g2'], lw=0.75)
