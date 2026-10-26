# -*- coding: utf-8 -*-
"""KORAD 경영평가 지면 — 서사 단락 블록 라이브러리.

쪽 단위가 아니라 '서사가 끊기는 단락' 단위로 레이아웃을 만든다.
블록은 내용(글·줄 수)으로 높이를 스스로 계산하고, Flow가 A4 한 쪽(본문 높이)에 맞춰 위에서부터 쌓는다.
남는 높이가 모자라면 행 단위로 쪼개 다음 쪽(홀수·짝수 마스터 교대)에 이어 놓는다.
좌표 단위는 px(참조 이미지 1380px = 210mm). 칸 폭·간격·높이는 참조 5쪽 실측값.
"""
import copy
from road import *

W = 1150            # 본문 폭(px)
RAIL = 106          # 레일 폭
HEAD = 42           # 머리칸 높이
LP = 4.30 / K       # 10pt 한 줄 높이(px)
BODY_TOP, BODY_BOT = 188, 1895
X0 = dict(odd=98, even=132)


# --------------------------------------------------------------- 높이 계산
def nl(text, w_px, hang=3.3):
    return est_lines(text, max((w_px * K - hang - 2.4) * 0.93, 8), SZ_D)


SUB_LW = 96


def sub_rows_h(sub, w_px):
    return sum(max(items_h(lines, w_px - SUB_LW - 14), 60) for _, lines in sub)


def items_h(items, w_px):
    h = 0.0
    for it in items:
        if isinstance(it, dict) and 'sub' in it:
            h += sub_rows_h(it['sub'], w_px) - 8
        elif isinstance(it, dict) and 'table' in it:
            h += len(it['table']) * 38 + 6
        else:
            h += nl(it if isinstance(it, str) else it['t'], w_px) * LP + 1
    return h + 4


def edges_of(xa, xb, n, ratios=None):
    ratios = ratios or [1] * n
    t = float(sum(ratios)); e = [xa]
    for r in ratios:
        e.append(e[-1] + (xb - xa) * r / t)
    return e


def lines_of(label):
    return len(str(label).split('\n'))


# --------------------------------------------------------------- 블록 기반
class Block:
    kind = '블록'
    gap = 14                    # 위 블록과의 기본 간격(px)
    splittable = False

    def height(self, W):
        raise NotImplementedError

    def draw(self, d, s, x0, y, W):
        raise NotImplementedError


# ---- 제목류 ----------------------------------------------------------
class ChapterBand(Block):
    kind = '장 제목 띠'

    def __init__(self, title):
        self.title = title

    def height(self, W):
        return 77

    def draw(self, d, s, x0, y, W):
        d.chapter_band(s, x0, y, x0 + W, y + 77, self.title)


class EvalBand(Block):
    kind = '평가내용 띠'
    gap = 28

    def __init__(self, n, title):
        self.n, self.title = n, title

    def height(self, W):
        lines = est_lines(self.title, ((W - 178 - 36) * K) * 0.93, SZ_SHAPE)
        return 63 + 46 * (lines - 1)

    def draw(self, d, s, x0, y, W):
        d.eval_band(s, y, self.n, self.title, self.height(W), x0=x0, x1=x0 + W)


class NumBar(Block):
    kind = '번호 띠'
    gap = 26

    def __init__(self, n, title):
        self.n, self.title = n, title

    def height(self, W):
        return 56

    def draw(self, d, s, x0, y, W):
        d.sec_bar(s, x0, y, self.n, self.title, h=56, w=W)


class SubHead(Block):
    kind = '소제목'
    gap = 22

    def __init__(self, text, chips=()):
        self.text, self.chips = text, chips

    def height(self, W):
        return 44

    def draw(self, d, s, x0, y, W):
        d.sub_head(s, x0, y, self.text, self.chips, w=W)


class Connector(Block):
    kind = '연결 화살표'
    gap = 3

    def height(self, W):
        return 36

    def draw(self, d, s, x0, y, W):
        d.bracket(s, x0 + 212, y, x0 + W - 98, 36)


class Note(Block):
    kind = '주석'
    gap = 6

    def __init__(self, text):
        self.text = text

    def height(self, W):
        return 32

    def draw(self, d, s, x0, y, W):
        d.t(s, x0 + 300, y, x0 + W, y + 32, [dict(t=self.text, sz=SZ_D, color=C['slate_700'], align='r')], name='주석', tag='주석')


# ---- 사다리 표 ---------------------------------------------------------
def band_h(b, wc):
    k = b['k']
    if k == 'text':
        return items_h(b['items'], wc)
    if k == 'cols':
        n = len(b['items']); e = edges_of(0, wc, n, b.get('w'))
        body = max(items_h(it, e[i + 1] - e[i] - 4) for i, it in enumerate(b['items']))
        return (HEAD + 2 if b.get('heads') else 0) + max(body, b.get('min', 56))
    if k == 'steps':
        n = len(b['labels']); e = edges_of(0, wc, n, b.get('w'))
        body = max(items_h(it, e[i + 1] - e[i] - 4) for i, it in enumerate(b['items']))
        return HEAD + 4 + max(body, b.get('min', 56))
    if k == 'tags':
        return 36 * len(b['rows']) + 4
    if k == 'banner':
        return 40
    if k == 'photo':
        pw = b.get('photo_w', 197)
        body = items_h(b['items'][0], wc - pw - 10)
        return (HEAD + 2 if b.get('heads') else 0) + max(body, b.get('min', 100))
    raise ValueError(k)


def draw_band(d, s, xc, xr, y, b):
    wc = xr - xc
    k = b['k']; h = band_h(b, wc)
    if k == 'text':
        d.t(s, xc, y, xr, y + h, [B(t) if isinstance(t, str) else t for t in b['items']], anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='본문', tag='text')
    elif k == 'cols':
        n = len(b['items']); e = [xc + v for v in edges_of(0, wc, n, b.get('w'))]
        yy = y
        if b.get('heads'):
            d.head_row(s, y, y + HEAD, [(e[i], e[i + 1], t) for i, t in enumerate(b['heads'])]); yy = y + HEAD + 2
        _cols(d, s, yy, y + h, e, b['items'], b.get('bullet', True))
    elif k == 'steps':
        n = len(b['labels']); e = [xc + v for v in edges_of(0, wc, n, b.get('w'))]
        d.step_strip(s, y, y + HEAD, e, b['labels'])
        _cols(d, s, y + HEAD + 4, y + h, e, b['items'], True)
    elif k == 'tags':
        tw = max(text_w(t, SZ_D, True) for t, _ in b['rows']) / K + 26
        for i, (t, tx) in enumerate(b['rows']):
            d.tag_row(s, y + 2 + i * 36, y + 2 + (i + 1) * 36, t, tx, xc, tw, xr, tone=b.get('tone', 'g2'))
    elif k == 'banner':
        d.shp(s, xc, y, xr, y + 38, b['text'], TONE['g2'], name='배너')
    elif k == 'photo':
        pw = b.get('photo_w', 197)
        e = [xc, xr - pw - 6]
        yy = y
        if b.get('heads'):
            d.head_row(s, y, y + HEAD, [(e[0], e[1], b['heads'][0])]); yy = y + HEAD + 2
        _cols(d, s, yy, y + h, e, b['items'], True)
        d.photo(s, xr - pw, y + 1, xr, y + h - 1, b.get('photo', '사진'))
    return h


def _cols(d, s, y0, y1, e, items, bullet):
    for i, its in enumerate(items):
        a, b_ = e[i], e[i + 1]
        if its and isinstance(its[0], dict) and 'sub' in its[0]:
            sub = its[0]['sub']; yy = y0 + 2
            for k, (lab, lines) in enumerate(sub):
                rh = max(items_h(lines, b_ - a - 4 - SUB_LW - 14), 60)
                d.rail(s, a + 4, yy, a + 4 + SUB_LW, yy + rh - 3, lab, 'blue')
                d.t(s, a + SUB_LW + 8, yy, b_ - 2, yy + rh - 3, [B(t) for t in lines], anchor='m', mg=(1.2, 0.2, 0.6, 0.2), name='소행 본문', tag='소행')
                if k < len(sub) - 1:
                    d.hl(s, a + 4, yy + rh - 1, b_ - 4, yy + rh - 1, color=TONE['g2'], lw=0.75)
                yy += rh
            if i > 0:
                d.hl(s, a, y0 + 6, a, y1 - 6, color=TONE['hair'], lw=0.75)
            continue
        paras = []
        tables = [it for it in its if isinstance(it, dict) and 'table' in it]
        texts = [it for it in its if not (isinstance(it, dict) and 'table' in it)]
        for it in its:
            if isinstance(it, dict) and 'table' in it:
                continue
            paras.append(B(it) if (bullet and isinstance(it, str)) else (dict(t=it, sz=SZ_D, color=C['navy'], after=0.6) if isinstance(it, str) else it))
        ty = y0
        if tables:
            # 표가 있으면 글 → 표 → 글 순서로 세로 배치(표는 가운데)
            th = sum(len(t['table']) * 38 + 6 for t in tables)
            first = texts[:1]; rest = texts[1:]
            hh = nl(first[0], b_ - a - 4) * LP + 6 if first else 0
            if first:
                d.t(s, a + 2, y0, b_ - 2, y0 + hh, [B(first[0])], anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='칸 본문', tag='표앞')
            yy = y0 + hh
            for t in tables:
                n = len(t['table'][0]); cw = t.get('w') or [(b_ - a - 12) / n] * n
                d.grid_table(s, a + 8, yy + 2, cw, [38] * len(t['table']), t['table'], align=['c'] * n, bold_cols=(0,), name='인라인 표')
                d.use('인라인 수치표', a + 8, yy + 2, a + 8 + sum(cw), yy + 2 + 38 * len(t['table']))
                yy += len(t['table']) * 38 + 6
            if rest:
                d.t(s, a + 2, yy, b_ - 2, y1, [B(r) for r in rest], anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='칸 본문', tag='표뒤')
        else:
            d.t(s, a + 2, ty, b_ - 2, y1, paras, anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='칸 본문', tag='칸')
        if i > 0:
            d.hl(s, a, y0 + 6, a, y1 - 6, color=TONE['hair'], lw=0.75)


class Ladder(Block):
    """사다리 표: 왼쪽 레일(서사 단계 이름) + 오른쪽 띠 묶음. 단계마다 높이는 내용으로 정해진다."""
    kind = '사다리 표'
    splittable = True
    gap = 8

    PHOTO_W = 175

    def __init__(self, rows, frame='g2', side=None, rail=RAIL, photos=None):
        self.rows, self.frame, self.side, self.rail, self.photos = rows, frame, side, rail, photos

    def _wc(self, W):
        return W - (self.side['w'] + 40 if self.side else 0) - (self.PHOTO_W + 8 if self.photos else 0)

    def row_h(self, r, W):
        wc = self._wc(W) - self.rail - 14
        hb = sum(band_h(b, wc) for b in r['bands']) + 3 * (len(r['bands']) - 1) + 5
        lab = lines_of(r['label']) * LP + 18 + (44 if r.get('tag') else 0) + (24 if r.get('notch') else 0)
        return max(hb, lab, r.get('min', 0))

    def height(self, W):
        return sum(self.row_h(r, W) for r in self.rows) + 3 * (len(self.rows) - 1) + 6

    def split(self, W, avail):
        acc = 6; k = 0
        for r in self.rows:
            h = self.row_h(r, W) + 3
            if acc + h > avail:
                break
            acc += h; k += 1
        if k == 0 or k == len(self.rows):
            return None
        if self.photos:
            return None
        a = Ladder(self.rows[:k], self.frame, None, self.rail); b = Ladder(self.rows[k:], self.frame, self.side, self.rail)
        return a, b

    def draw(self, d, s, x0, y, W):
        H = self.height(W); wl = self._wc(W)
        d.use('사다리 표', x0, y, x0 + wl, y + H, f'{len(self.rows)}단계')
        d.r(s, x0, y, x0 + wl, y + H, fill=C['white'], line=C['green_400'] if self.frame == 'g4' else TONE['line'], lw=0.75, name='표 외곽')
        yy = y + 3; prev = None; ys = []
        for r in self.rows:
            ys.append((yy, self.row_h(r, W)))
            rh = self.row_h(r, W)
            tone = r.get('tone', 'blue')
            d.rail(s, x0 + 2, yy, x0 + 2 + self.rail, yy + rh, r['label'], tone, tag=r.get('tag'), notch=r.get('notch', False))
            if r.get('notch') and prev:
                d.rail_notch(s, x0 + 2, yy, x0 + 2 + self.rail, prev)
            xc, xr = x0 + self.rail + 8, x0 + wl - 5
            by = yy + 4
            for b in r['bands']:
                bh = draw_band(d, s, xc, xr, by, b)
                by += bh + 3
            prev = tone
            yy += rh + 3
        if self.photos:
            px0 = x0 + wl + 8
            for ph in self.photos:
                i0, i1 = ph['rows']
                ya, yb = ys[i0][0], ys[i1][0] + ys[i1][1]
                d.photo(s, px0, ya, x0 + W, yb, ph.get('caption', '사진'))
        if self.side:
            sd = self.side
            ax = x0 + wl + 4
            d.tri_arrow(s, ax + 14, y + H / 2, 52, 26, down=False, name='성과 화살표')
            px0 = x0 + wl + 36
            d.shp(s, px0, y, x0 + W, y + 44, sd['title'], '008C6B', color=C['white'], sz=SZ_C, name='성과 패널 머리')
            d.r(s, px0, y + 46, x0 + W, y + H, fill=C['tint_mint'], line=C['green_400'], lw=1.5, name='성과 패널')
            d.t(s, px0 + 4, y + 50, x0 + W - 4, y + H - 4, [B(t) if isinstance(t, str) else t for t in sd['items']], anchor='m', mg=(1.5, 0.5, 1.0, 0.5), name='성과 패널 본문', tag='성과패널')
            d.use('성과 사이드 패널', px0, y, x0 + W, y + H)


# ---- 라벨 박스 행 ------------------------------------------------------
class LabelRows(Block):
    """라벨 박스 행들: 추진 목표·방향·과제·채널·지표, 추진배경·점검방법·점검결과처럼 이름 붙은 한 줄~여러 줄 칸"""
    kind = '라벨 박스 행'
    splittable = True
    gap = 10

    def __init__(self, rows, label_w=110, gap=10):
        self.rows, self.label_w, self.rgap = rows, label_w, gap

    def row_h(self, r, W):
        wc = W - self.label_w - 14
        k = r['k']
        if k in ('bar', 'center'):
            return max(53, nl(r['text'], wc) * LP + 24)
        if k == 'center3':
            n = len(r['items']); e = edges_of(0, wc, n)
            return max(53, max(nl(t, e[1] - 6) for t in r['items']) * LP + 22)
        if k == 'cols':
            n = len(r['items']); e = edges_of(0, wc, n, r.get('w'))
            return max(max(items_h(it, e[i + 1] - e[i] - 4) for i, it in enumerate(r['items'])) + 8, r.get('min', 60))
        if k == 'heads':
            n = len(r['items']); e = edges_of(0, wc, n, r.get('w'))
            return HEAD + 6 + max(max(items_h(it, e[i + 1] - e[i] - 4) for i, it in enumerate(r['items'])), 56) + 8
        if k == 'text':
            return max(53, items_h(r['items'], wc) + 12)
        raise ValueError(k)

    def height(self, W):
        return sum(self.row_h(r, W) for r in self.rows) + self.rgap * (len(self.rows) - 1)

    def split(self, W, avail):
        acc = 0; k = 0
        for r in self.rows:
            h = self.row_h(r, W) + self.rgap
            if acc + h - self.rgap > avail:
                break
            acc += h; k += 1
        if k == 0 or k == len(self.rows):
            return None
        return LabelRows(self.rows[:k], self.label_w, self.rgap), LabelRows(self.rows[k:], self.label_w, self.rgap)

    def draw(self, d, s, x0, y, W):
        yy = y
        for r in self.rows:
            h = self.row_h(r, W)
            xi = d.label_box(s, yy, yy + h, r['label'], self.label_w, x0, x0 + W, r.get('tone', 'g2'))
            xr = x0 + W - 6; wc = xr - xi
            k = r['k']
            if k == 'bar':
                d.r(s, xi, yy + 6, xr, yy + h - 6, fill=TONE['g2'], name='강조 바')
                d.t(s, xi, yy + 6, xr, yy + h - 6, [LB(r['text'])], name='강조 바 글')
            elif k == 'center':
                d.t(s, xi, yy + 3, xr, yy + h - 3, [dict(t=r['text'], sz=SZ_D, color=C['navy'], align='c')], name='가운데 글')
            elif k == 'center3':
                e = [xi + v for v in edges_of(0, wc, len(r['items']))]
                for i, t in enumerate(r['items']):
                    d.t(s, e[i], yy + 3, e[i + 1], yy + h - 3, [LB(t)], name='가운데 글')
                    if i:
                        d.hl(s, e[i], yy + 10, e[i], yy + h - 10)
            elif k == 'cols':
                e = [xi + v for v in edges_of(0, wc, len(r['items']), r.get('w'))]
                _cols(d, s, yy + 3, yy + h - 3, e, r['items'], True)
            elif k == 'heads':
                e = [xi + v for v in edges_of(0, wc, len(r['items']), r.get('w'))]
                d.head_row(s, yy + 5, yy + 5 + HEAD, [(e[i], e[i + 1], t) for i, t in enumerate(r['heads'])])
                _cols(d, s, yy + 5 + HEAD + 2, yy + h - 3, e, r['items'], True)
            elif k == 'text':
                d.t(s, xi, yy + 3, xr, yy + h - 3, [B(t) for t in r['items']], name='본문')
            yy += h + self.rgap
        d.use('라벨 박스 행', x0, y, x0 + W, y + self.height(W))


# ---- 2분할 패널 --------------------------------------------------------
class TwinPanel(Block):
    kind = '2분할 패널'
    splittable = True
    gap = 10

    def __init__(self, left, right, label_w=(135, 148)):
        """left/right = (제목, [(태그|None, 라벨, [줄...]), ...]) — 두 쪽 행 수는 같아야 한다"""
        self.left, self.right, self.lw = left, right, label_w

    def _rows(self, W):
        pw = (W - 9) / 2; out = []
        for i in range(len(self.left[1])):
            h = 0
            for (t, rows), lw in ((self.left, self.lw[0]), (self.right, self.lw[1])):
                tag, lab, its = rows[i]
                h = max(h, items_h(its, pw - lw - 30) + 4, lines_of(lab) * LP + 16 + (40 if tag else 0))
            out.append(max(h, 64))
        return out

    def height(self, W):
        return 44 + 8 + sum(self._rows(W))

    def split(self, W, avail):
        rows = self._rows(W); acc = 52; k = 0
        for h in rows:
            if acc + h > avail:
                break
            acc += h; k += 1
        if k == 0 or k == len(rows):
            return None
        return (TwinPanel((self.left[0], self.left[1][:k]), (self.right[0], self.right[1][:k]), self.lw),
                TwinPanel((self.left[0], self.left[1][k:]), (self.right[0], self.right[1][k:]), self.lw))

    def draw(self, d, s, x0, y, W):
        pw = (W - 9) / 2; rows = self._rows(W)
        ys = [y + 48]
        for h in rows:
            ys.append(ys[-1] + h)
        H = ys[-1] + 4 - y
        d.twin_panel(s, y, y + H, dict(title=self.left[0], x0=x0, x1=x0 + pw, rows=self.left[1]),
                     dict(title=self.right[0], x0=x0 + pw + 9, x1=x0 + W, rows=self.right[1]), head_h=44, label_w=self.lw, rows_y=ys)


# ---- 실적표 -----------------------------------------------------------
class DataTable(Block):
    """구분 / 내용 실적표(편집 가능한 실제 표). 앞 두 열의 빈 칸은 위 칸과 자동 병합."""
    kind = '실적 구분표'
    splittable = True
    gap = 16

    def __init__(self, header, rows, col_w=(121, 114, None)):
        self.header, self.rows, self.col_w = header, rows, col_w

    def _cw(self, W):
        a, b, c = self.col_w
        return [a, b, c or W - a - b]

    def _rh(self, W):
        cw = self._cw(W)
        return [max(45, max(nl(str(r[2]), cw[2] - 20) * LP + 14, 0)) for r in self.rows]

    def height(self, W):
        return 42 + sum(self._rh(W))

    def split(self, W, avail):
        acc = 42; k = 0
        for h in self._rh(W):
            if acc + h > avail:
                break
            acc += h; k += 1
        if k < 2 or k == len(self.rows):
            return None
        return DataTable(self.header, self.rows[:k], self.col_w), DataTable(self.header, self.rows[k:], self.col_w)

    def draw(self, d, s, x0, y, W):
        cw = self._cw(W); rh = self._rh(W)
        rows = [list(self.header)] + [list(r) for r in self.rows]
        merges = [(0, 0, 0, 1)]
        for c in (0, 1):
            start = None
            for i in range(1, len(rows)):
                if rows[i][c] == '' and start is not None:
                    continue
                if start is not None and i - 1 > start:
                    merges.append((start, c, i - 1, c))
                start = i if rows[i][c] != '' else None
            if start is not None and len(rows) - 1 > start:
                merges.append((start, c, len(rows) - 1, c))
        fills = {(0, c): TONE['g2'] for c in range(3)}
        for i in range(1, len(rows)):
            fills[(i, 0)] = TONE['g1']; fills[(i, 1)] = TONE['g1']
        d.grid_table(s, x0, y, cw, [42] + rh, rows, merge=merges, fills=fills, bold_cols=(0, 1), name='실적표')
        d.use('실적 구분표', x0, y, x0 + W, y + self.height(W))


# ---- 3분할 패널 -------------------------------------------------------
class ThreePanel(Block):
    """칸 2~4개 패널: 머리 + 불릿 + 하단 요약 바(수치 한 줄). 예) 복리후생 향상 | 가족친화경영 확대 | 안전일터 조성"""
    kind = '3분할 패널'
    gap = 10

    def __init__(self, panels):
        self.panels = panels

    def _pw(self, W):
        n = len(self.panels)
        return (W - 8 * (n - 1)) / n

    def height(self, W):
        pw = self._pw(W)
        body = max(items_h(p['items'], pw - 6) for p in self.panels)
        has_f = any(p.get('footer') for p in self.panels)
        return 42 + max(body, 90) + (44 if has_f else 4) + 4

    def draw(self, d, s, x0, y, W):
        pw = self._pw(W); H = self.height(W)
        d.use('3분할 패널', x0, y, x0 + W, y + H, f'{len(self.panels)}칸')
        for i, p in enumerate(self.panels):
            xa = x0 + i * (pw + 8); xb = xa + pw
            d.r(s, xa, y, xb, y + H, fill=C['white'], line=TONE['g2'], lw=1.0, name='패널 외곽')
            d.shp(s, xa, y, xb, y + 42, p['title'], TONE['g2'], color=C['navy'], name='패널 머리')
            fh = 44 if p.get('footer') else 0
            d.t(s, xa + 4, y + 44, xb - 4, y + H - fh - 4, [B(t) for t in p['items']], anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='패널 본문', tag=p['title'])
            if p.get('footer'):
                d.shp(s, xa + 4, y + H - 44, xb - 4, y + H - 4, p['footer'], TONE['g1'], color=C['navy'], bold=False, name='요약 바')


# ---- 성과 띠 ----------------------------------------------------------
class Result(Block):
    """핵심성과·추진성과 띠. 항목 1개=한 줄 띠, 2개 이상=불릿 여러 줄 띠"""
    kind = '핵심성과 띠'
    gap = 16

    def __init__(self, items, label='핵심성과'):
        self.items = [items] if isinstance(items, str) else list(items)
        self.label = label

    def height(self, W):
        wc = W - 160
        lines = sum(est_lines(t, (wc * K - 8) * 0.93, SZ_C) for t in self.items)
        return max(55, lines * 5.0 / K + 24 + 6 * (len(self.items) - 1))

    def draw(self, d, s, x0, y, W):
        if len(self.items) == 1:
            d.core_band(s, y, self.items[0], x0=x0, x1=x0 + W, h=self.height(W), label=self.label)
        else:
            d.core_band2(s, y, self.items, x0=x0, x1=x0 + W, h=self.height(W), label=self.label)


# ---------------------------------------------------------------- 쪽 흐름
class Flow:
    """블록을 쪽 높이에 맞춰 쌓는다. 모자라면 행 단위로 쪼개 다음 쪽에 잇는다."""

    def __init__(self, d, start_no=93, first='odd', foot='2025년도 경영실적보고서', indicator='노사관계',
                 number='4', cat='Ⅰ. 경영관리 범주', name='조직 운영 및 관리', note=None):
        self.d, self.no, self.kind = d, start_no, first
        self.foot, self.ind, self.number, self.cat, self.name, self.note = foot, indicator, number, cat, name, note
        d.do_snap = False
        self.s = None; self.y = BODY_TOP; self.prev = None
        self.placed = []
        self.placed_blocks = []
        self._new_page()

    def _new_page(self):
        d = self.d
        self.s = d.page(self.kind, number=self.number, cat=self.cat, name=self.name, pg=str(self.no), foot=self.foot, indicator=self.ind, note=self.note)
        self.x0 = X0[self.kind]
        self.y = BODY_TOP if self.kind == 'odd' else BODY_TOP + 2
        self.prev = None
        self.kind = 'even' if self.kind == 'odd' else 'odd'
        self.no += 1

    def add(self, blk):
        gap = 0 if self.prev is None else blk.gap
        h = blk.height(W)
        avail = BODY_BOT - (self.y + gap)
        if h <= avail:
            return self._place(blk, gap)
        if blk.splittable and avail > 160:
            sp = blk.split(W, avail)
            if sp:
                a, b = sp
                self._place(a, gap)
                self._new_page()
                return self.add(b)
        if self.prev is not None:
            self._new_page()
            return self.add(blk)
        self._place(blk, gap)

    def _place(self, blk, gap):
        y = self.y + gap
        blk.draw(self.d, self.s, self.x0, y, W)
        self.placed.append(dict(page=len(self.d.prs.slides), kind=blk.kind, cls=type(blk).__name__, x0=self.x0, y=y, h=blk.height(W), tag=getattr(blk, 'tag', None)))
        self.placed_blocks.append(blk)
        self.y = y + blk.height(W)
        self.prev = blk.kind

    HEADS = ('장 제목 띠', '평가내용 띠', '번호 띠', '소제목')

    def add_all(self, blocks):
        """제목류(장·평가내용·번호 띠·소제목)는 뒤따르는 본문 블록과 같은 쪽에 둔다(홀로 쪽 끝에 남지 않게)."""
        i, n = 0, len(blocks)
        while i < n:
            j = i
            while j < n and blocks[j].kind in self.HEADS:
                j += 1
            if j > i:
                grp = blocks[i:j + 1] if j < n else blocks[i:j]
                need = 0.0
                for k, bl in enumerate(grp):
                    hh = bl.height(W)
                    if bl is blocks[j] if j < n else False:
                        hh = hh if not bl.splittable else min(hh, 200)
                    need += hh + (bl.gap if (k or self.prev is not None) else 0)
                if self.prev is not None and self.y + need > BODY_BOT:
                    self._new_page()
                for bl in grp:
                    self.add(bl)
                i = j + 1
            else:
                self.add(blocks[i]); i += 1

    def break_page(self):
        """새 서사(평가내용)는 새 쪽에서 시작"""
        if self.prev is not None:
            self._new_page()

    def pages(self):
        return len(self.d.prs.slides)
