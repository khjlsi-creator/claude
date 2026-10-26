# -*- coding: utf-8 -*-
"""KORAD 경영평가 지면 디자인 시스템 — 경영실적보고서 지면(A4 세로) 모듈 라이브러리.

기준: 올려 주신 참조 지면 5쪽(1380×2000px 이미지)의 도형 좌표를 px로 실측하고,
      KORAD 색·Pretendard·12/14/15pt 표준으로 옮긴다.
좌표: 이미지 px 그대로 받는다.  x_mm = px × 210/1380,  y_mm = (px − 48) × 210/1380
      (이미지 위쪽 48px은 뷰어 막대라 용지 위끝은 y=48).
"""
import re, os
from PIL import ImageFont
from pptx.util import Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from lxml import etree
from kp import *          # C, mm, rgb, Deck, est_lines, _sp_xml, _ph_sp, _pic_xml, _add, NS, build_system ...
import kp
import edges as _edges
from kp import _add, _sp_xml, _ph_sp, _pic_xml

# 지면 밀도 글자 크기: 참조 지면이 약 9.5pt 밀도라 표·박스 안 글은 10pt(KORAD footnote 규격), 핵심성과는 12pt
SZ_D = 10
SZ_C = 11
SZ_SUB = 12      # 소제목(원본 본문의 약 1.2배)
SZ_CH = 18       # 장 제목 띠(원본 본문의 약 1.75배)
K = 210.0 / 1380.0        # mm per px
Y0 = 48                   # 용지 위끝 px


def X(px):
    return px * K


def Y(py):
    return (py - Y0) * K


def S(px):
    return px * K


_FB = ImageFont.truetype(os.path.expanduser('~/.fonts/Pretendard-Bold.ttf'), 1000)


def text_w(t, pt, bold=False):
    """글자 폭(mm) 추정"""
    f = _FB if bold else kp._F
    return f.getlength(t) / 1000.0 * pt * 0.3528


# ------------------------------------------------------------------ 색 대응(참조 지면 회색 → KORAD)
# 참조 지면의 회색 4단(바탕 F3 · 머리칸 E6 · 라벨 D0 · 진한 66)을 KORAD 블루 4단으로 옮긴다.
TONE = dict(
    g0=C['tint_panel'],      # F3F3F3 약한 바탕
    g1=C['tint_100'],        # E6E6E6 머리칸
    g2=C['tint_200'],        # D0D0D0 라벨·배너
    g3=C['blue_cyan'],       # B0B0B0 단계 3번째 · 레일 3단
    g4=C['blue_deep'],       # 66~55 진한 라벨·마지막 단계
    g5=C['navy_band'],       # 핵심성과 라벨
    line=C['blue_bright'],   # 외곽선
    hair=C['tint_200'],      # 칸 나누는 가는 선
)
# KORAD RowLabel 타일: trellis 패턴(전경/배경). 블루 → 틸 → 딥블루 순서로 쓰고, 성과는 그린 계열.
RAILS = dict(blue=(C['blue_panel_light'], C['blue_panel']), teal=('00BEC2', C['teal_panel']), deep=('0A6BE6', C['blue_deep']),
             res=(C['teal_500'], '008C6B'), navy=(C['navy_band'], C['navy_band']))
LEGACY = dict(g1='blue', g2='teal', g3='deep', g4='res')
DARK = (TONE['g4'], TONE['g5'])      # 흰 글자를 쓰는 바탕


def ink_on(fill):
    return C['white'] if fill in DARK else C['navy']


def B(t, **k):
    """불릿 1단계"""
    return {**dict(t=t, sz=SZ_D, bullet='•', hang=3.3, after=0.5), **k}


def B2(t, **k):
    return {**dict(t=t, sz=SZ_D, bullet='-', hang=3.0, indent=3.5, after=0.4), **k}


def LB(t, **k):
    """라벨·머리칸 글(가운데 굵게)"""
    return dict(t=t, sz=SZ_D, b=True, align='c', **k)


def lines_h(paras, w_mm):
    h = 0.0
    for p in paras:
        txt = p.get('t') or ''.join(r[0] for r in p['runs'])
        ind = (p.get('hang', 0) + p.get('indent', 0)) if p.get('bullet') else 0
        pt = p.get('sz', SZ_D)
        h += est_lines(txt, (w_mm - ind) * 0.93, pt) * pt * 0.3528 * 1.10 * 1.17 + p.get('after', 0) * 0.3528
    return h


class RD(Deck):
    """경영평가 지면 덱 — px 좌표로 모듈을 놓는다"""

    def __init__(self):
        self.prs = kp.Presentation()
        self.lay = build_road_system(self.prs)
        self.reg = []          # 모듈 사용 기록: dict(page, module, x0,y0,x1,y1)
        self.warn = []
        self.miss = []
        self.pageno = 0

    # ---------------------------------------------------------- 쪽
    def page(self, kind, number='4', cat='Ⅰ. 경영관리 범주', name='조직 운영 및 관리', pg='93',
             foot='2025년도 경영실적보고서', indicator='노사관계', note=None):
        lay = self.lay['지면-홀수' if kind == 'odd' else '지면-짝수']
        s = self.prs.slides.add_slide(lay)
        ph = {p.placeholder_format.idx: p for p in s.placeholders}
        if kind == 'odd':
            for i, t in ((13, number), (14, cat), (15, name), (16, pg), (17, foot)):
                ph[i].text_frame.text = t
        else:
            ph[13].text_frame.text = indicator
            ph[14].text_frame.text = pg
        if note:
            s.notes_slide.notes_text_frame.text = note
        self.pageno = len(self.prs.slides)
        self.kind = kind
        return s

    def use(self, module, x0, y0, x1, y1, note=''):
        self.reg.append(dict(page=self.pageno, module=module, x0=x0, y0=y0, x1=x1, y1=y1, note=note))

    def save(self, path):
        for sl in self.prs.slides:
            for st in list(sl.shapes._spTree.iter(qn('p:style'))):
                st.getparent().remove(st)
        self.prs.save(path)

    # ---------------------------------------------------------- px → 도형
    SNAP_TOL = 9.0

    def snap(self, v, axis):
        """참조 경계선(검출값)에 가장 가까운 좌표로 맞춘다. 9px 안에 없으면 그대로."""
        if not getattr(self, 'do_snap', True) or not 1 <= self.pageno <= 5:
            return v
        ys, xs = _edges.edges_of(self.pageno)
        arr = ys if axis == 'y' else xs
        best = min(arr, key=lambda e: abs(e - v)) if arr else None
        if best is not None and abs(best - v) <= self.SNAP_TOL:
            return best
        self.miss.append((self.pageno, axis, v, round(best - v, 1) if best is not None else None))
        return v

    def r(self, s, x0, y0, x1, y1, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE, rad=None, name=None):
        x0, x1, y0, y1 = self.snap(x0, 'x'), self.snap(x1, 'x'), self.snap(y0, 'y'), self.snap(y1, 'y')
        w, h = x1 - x0, y1 - y0
        adj = None
        # KORAD 기본은 직각: 둥근 모서리·원은 모두 사각형으로
        if shape in (MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.OVAL, MSO_SHAPE.ROUND_2_SAME_RECTANGLE):
            shape = MSO_SHAPE.RECTANGLE
        return self.rect(s, X(x0), Y(y0), S(w), S(h), fill=fill, line=line, line_w=lw, shape=shape, name=name, adj=adj)

    def t(self, s, x0, y0, x1, y1, paras, anchor='m', mg=(1.0, 0.3, 1.0, 0.3), name=None, tag=None):
        """글상자(px 박스). 넘치면 경고."""
        sp = s.shapes.add_textbox(mm(X(x0)), mm(Y(y0)), mm(S(x1 - x0)), mm(S(y1 - y0)))
        if name:
            sp.name = name
        self.fill_text(sp, paras, anchor=anchor, margins=mg)
        sp.text_frame.auto_size = MSO_AUTO_SIZE.NONE
        need = lines_h(paras, S(x1 - x0) - mg[0] - mg[2]) + mg[1] + mg[3]
        if need > S(y1 - y0) + 0.6 and tag != '번호':
            self.warn.append(f'p{self.pageno} 넘침 {tag or (paras[0].get("t") or "")[:14]!r}: 필요 {need:.1f}mm > {S(y1-y0):.1f}mm')
        return sp

    def shp(self, s, x0, y0, x1, y1, text, fill, shape=MSO_SHAPE.RECTANGLE, color=None, sz=SZ_D, bold=True, line=None,
            lw=0.75, rad=None, align='c', name=None, mg=(0.8, 0.2, 0.8, 0.2), anchor='m'):
        sp = self.r(s, x0, y0, x1, y1, fill=fill, line=line, lw=lw, shape=shape, rad=rad, name=name)
        if text is not None:
            col = color or ink_on(fill)
            paras = [dict(t=ln, sz=sz, b=bold, color=col, align=align) for ln in str(text).split('\n')]
            self.fill_text(sp, paras, anchor=anchor, margins=mg)
            w = S(x1 - x0) - mg[0] - mg[2]
            need = sum(est_lines(p['t'], w, sz) for p in paras) * sz * 0.3528 * 1.10 * 1.17 + mg[1] + mg[3]
            if need > S(y1 - y0) + 0.6 or any(text_w(p['t'], sz, bold) > w + 0.3 and '\n' in str(text) for p in paras):
                self.warn.append(f'p{self.pageno} 라벨 넘침 {str(text)[:10]!r}')
        return sp

    def hl(self, s, x0, y0, x1, y1, color=None, lw=0.5):
        return self.line(s, X(x0), Y(y0), X(x1), Y(y1), color=color or TONE['hair'], w=lw)

    def grad(self, sp, c1, c2, angle=0):
        sp.fill.gradient()
        sp.fill.gradient_angle = angle
        st = sp.fill.gradient_stops
        st[0].color.rgb = rgb(c1); st[0].position = 0.0
        st[1].color.rgb = rgb(c2); st[1].position = 1.0

    def poly(self, s, pts, fill, line=None, lw=0.5, name=None):
        """px 꼭짓점 다각형"""
        e = [(int(X(x) * 36000), int(Y(y) * 36000)) for x, y in pts]
        fb = s.shapes.build_freeform(e[0][0], e[0][1], scale=1.0)
        fb.add_line_segments(e[1:], close=True)
        sp = fb.convert_to_shape()
        if fill:
            sp.fill.solid(); sp.fill.fore_color.rgb = rgb(fill)
        else:
            sp.fill.background()
        if line:
            sp.line.color.rgb = rgb(line); sp.line.width = Pt(lw)
        else:
            sp.line.fill.background()
        sp.shadow.inherit = False
        if name:
            sp.name = name
        return sp

    # ======================================================= 공통 모듈
    def chapter_band(self, s, x0, y0, x1, y1, title, tile_w=262):
        """장 제목 띠 — 지면 첫 쪽 한 번. 오른쪽 칸에 KORAD CI."""
        self.use('장 제목 띠', x0, y0, x1, y1)
        self.r(s, x0, y0, x1, y1, fill=C['white'], line=TONE['g4'], lw=2.25, shape=MSO_SHAPE.ROUNDED_RECTANGLE, rad=14, name='장 제목 띠')
        tx0 = x1 - tile_w
        self.r(s, tx0, y0 + 1, x1 - 1, y1 - 1, fill=TONE['g1'], name='CI 칸')
        self.t(s, x0 + 50, y0 + 2, tx0, y1 - 2, [dict(t=title, sz=SZ_CH, b=True, color=C['navy'])], name='장 제목')
        ci_w = S(tile_w - 50)
        self.pic(s, CI, X(tx0 + 25), Y(y0) + (S(y1 - y0) - ci_w * 66 / 356) / 2, w=ci_w, name='KORAD CI')

    def eval_band(self, s, y0, n, title, h, x0=98, x1=1248, label_w=178):
        """평가내용 N 띠: 왼쪽 라벨 + 오른쪽 제목 박스"""
        y1 = y0 + h
        self.use('평가내용 띠', x0, y0, x1, y1, f'h{h}')
        lab = self.r(s, x0, y0, x0 + label_w, y1, fill=TONE['g1'], line=TONE['g4'], lw=2.25, shape=MSO_SHAPE.ROUNDED_RECTANGLE, rad=10, name='평가내용 라벨')
        self.fill_text(lab, [dict(runs=[('평가내용 ', dict(color=C['navy'])), (str(n), dict(color=TONE['g4'], sz=SZ_SHAPE))], sz=SZ_C, b=True, align='c')], anchor='m', margins=(0.3, 0.3, 0.3, 0.3))
        self.r(s, x0 + label_w + 2, y0 + 2, x1, y1 - 2, fill=C['white'], line=TONE['line'], lw=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, rad=10, name='평가내용 제목 박스')
        self.t(s, x0 + label_w + 22, y0 + 4, x1 - 14, y1 - 4, [dict(t=title, sz=SZ_SHAPE, b=True, color=C['navy'])], name='평가내용 제목', tag=title[:12])
        for i in range(5):    # 라벨 아래 점선(원본의 점 5개)
            self.r(s, x0 + label_w / 2 - 28 + i * 14, y1 - 11, x0 + label_w / 2 - 23 + i * 14, y1 - 6, fill=TONE['g4'], shape=MSO_SHAPE.OVAL, name='점')

    def sec_bar(self, s, x0, y0, n, title, h=56, w=1150):
        """번호 띠: 번호 탭(그라데이션 + 비스듬한 끝) + 제목 띠"""
        self.use('번호 띠', x0, y0, x0 + w, y0 + h)
        band = self.r(s, x0, y0, x0 + w, y0 + h, fill=TONE['g0'], line=TONE['hair'], lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE, rad=9, name='번호 띠')
        self.grad(band, TONE['g1'], C['white'], 0)
        yb = y0 + h - 4
        tab = self.poly(s, [(x0 + 4, y0 + 4), (x0 + 76, y0 + 4), (x0 + 90, yb), (x0 + 4, yb)], TONE['g4'], name='번호 탭')
        self.grad(tab, TONE['g5'], TONE['line'], 0)
        self.poly(s, [(x0 + 76, y0 + 4), (x0 + 88, y0 + 4), (x0 + 102, y0 + h - 4), (x0 + 90, y0 + h - 4)], TONE['g2'], name='번호 탭 빗면')
        self.t(s, x0 + 4, y0, x0 + 74, y0 + h, [dict(t=str(n), sz=22, b=True, color=C['white'], align='c')], name='번호', mg=(0, 0, 0, 0), tag='번호')
        self.t(s, x0 + 118, y0 + 4, x0 + w - 12, y0 + h - 4, [dict(t=title, sz=SZ_TITLE, b=True, color=C['navy'])], name='번호 띠 제목', tag=title[:12])

    def sub_head(self, s, x0, y0, text, chips=(), h=44, w=1150):
        """소제목 가./나. + 태그칩"""
        self.use('소제목', x0, y0, x0 + w, y0 + h)
        tw = text_w(text, SZ_SUB, True)
        self.r(s, x0, y0 + 28, x0 + tw / K + 4, y0 + 36, fill=C['mint_hl'], name='형광 밑줄')
        self.t(s, x0, y0, x0 + w, y0 + h, [dict(t=text, sz=SZ_SUB, b=True, color=C['navy'])], name='소제목', mg=(0, 0, 0, 0), tag=text[:12])
        cx = x0 + tw / K + 22
        for c in chips:
            cw = text_w(c, SZ_D, True) / K + 24
            self.shp(s, cx, y0 + 6, cx + cw, y0 + h - 6, c, TONE['g4'], rad=7, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name='태그칩', mg=(0.3, 0, 0.3, 0))
            cx += cw + 8

    def core_band(self, s, y0, text, x0=98, x1=1248, h=55, label='핵심성과'):
        """핵심성과 띠: 라벨(오각 화살) + 굵은 외곽 박스"""
        self.use('핵심성과 띠', x0, y0, x1, y0 + h)
        self.r(s, x0, y0, x1, y0 + h, fill=C['tint_mint'], line=C['green_400'], lw=1.5, name='핵심성과 박스')
        tag = self.r(s, x0 + 6, y0 + 7, x0 + 126, y0 + h - 7, fill=TONE['g5'], shape=MSO_SHAPE.PENTAGON, name='핵심성과 라벨')
        tag.adjustments[0] = 0.28
        self.fill_text(tag, [dict(t=label, sz=SZ_C, b=True, color=C['white'], align='c')], anchor='m', margins=(0.5, 0, 2.2, 0))
        self.t(s, x0 + 142, y0 + 3, x1 - 12, y0 + h - 3, [dict(t=text, sz=SZ_C, b=True, color=C['navy'], bullet='•', hang=4.2)], name='핵심성과 문구', tag='핵심성과')
        return y0 + h

    def core_band2(self, s, y0, items, x0=132, x1=1281, h=88, label='핵심성과'):
        """핵심성과 띠(불릿 2줄형): 라벨이 박스 높이를 채운다"""
        self.use('핵심성과 띠(2줄형)', x0, y0, x1, y0 + h)
        self.r(s, x0, y0, x1, y0 + h, fill=C['tint_mint'], line=C['green_400'], lw=1.5, name='핵심성과 박스')
        self.shp(s, x0 + 6, y0 + 6, x0 + 126, y0 + h - 6, label, TONE['g5'], sz=SZ_C, name='핵심성과 라벨')
        self.t(s, x0 + 142, y0 + 4, x1 - 12, y0 + h - 4, [dict(t=t, sz=SZ_C, b=True, color=C['navy'], bullet='•', hang=4.2, after=1.0) for t in items],
               name='핵심성과 문구', tag='핵심성과2')
        return y0 + h

    # ---- 사다리 표 -------------------------------------------------
    def rail(self, s, x0, y0, x1, y1, label, tone='blue', tag=None, notch=False):
        """왼쪽 레일 한 칸 = KORAD RowLabel 타일(trellis, 흰 굵은 글자). tag가 있으면 흰 작은 태그가 라벨 위에 붙는다."""
        tone = LEGACY.get(tone, tone)
        fore, back = RAILS[tone]
        sp = self.r(s, x0, y0, x1, y1, fill=back, name='레일')
        if fore != back:
            self.trellis(sp, fore, back)
        col = C['white']
        paras = [dict(t=ln, sz=SZ_D, b=True, color=col, align='c') for ln in label.split('\n')]
        if tag:
            th = 34
            top = y0 + (30 if notch else 8)
            tw_ = text_w(tag, SZ_D, True) / K + 22
            cx = (x0 + x1) / 2
            self.shp(s, cx - tw_ / 2, top, cx + tw_ / 2, top + th, tag, C['white'], color=C['navy'], name='레일 태그', mg=(0.2, 0, 0.2, 0))
            self.t(s, x0, top + th, x1, y1 - 4, paras, name='레일 라벨', mg=(0.3, 0, 0.3, 0))
        else:
            self.fill_text(sp, paras, anchor='m', margins=(0.3, 0, 0.3, 0))
            w = S(x1 - x0) - 0.6
            if any(text_w(ln, SZ_D, True) > w for ln in label.split('\n')):
                self.warn.append(f'p{self.pageno} 레일 라벨 폭 {label!r}')
        return sp

    def rail_notch(self, s, x0, y, x1, prev_tone, h=24):
        """레일 사이 아래 방향 삼각형: 앞 단계 색이 다음 칸 위로 삼각형으로 내려온다"""
        self.poly(s, [(x0, y), (x1, y), ((x0 + x1) / 2, y + h)], RAILS[LEGACY.get(prev_tone, prev_tone)][1], name='레일 삼각형')

    def rail_sep(self, s, x0, y, x1):
        self.hl(s, x0 + 6, y, x1 - 6, y, color=C['white'], lw=1.5)

    def head_row(self, s, y0, y1, cells, gap=3, fill='g1'):
        """머리칸 줄. cells=[(x0,x1,label)] — label은 가운데 굵게"""
        for x0, x1, lab in cells:
            sp = self.r(s, x0, y0, x1 - gap, y1, fill=TONE[fill], name='머리칸')
            col = ink_on(TONE[fill])
            paras = [dict(t=ln, sz=SZ_D, b=True, color=col, align='c') for ln in lab.split('\n')]
            self.fill_text(sp, paras, anchor='m', margins=(0.6, 0.1, 0.6, 0.1))
            if text_w(lab.split('\n')[0], SZ_D, True) > S(x1 - x0 - gap) - 1.2:
                self.warn.append(f'p{self.pageno} 머리칸 폭 {lab!r}')

    def cols(self, s, y0, y1, edges, items, divider=True, bullet=True, gap=2, tag=''):
        """칸별 불릿 글. edges=[x0, x1, x2 ...]  items=[[줄,..],[..]]"""
        for i, its in enumerate(items):
            a, b = edges[i], edges[i + 1]
            paras = [B(t) if bullet else dict(t=t, sz=SZ_D, color=C['navy'], after=0.6) for t in its]
            self.t(s, a + gap, y0, b - gap, y1, paras, anchor='m', mg=(1.4, 0.2, 0.6, 0.2), name='칸 본문', tag=f'{tag}{i}')
            if divider and i > 0:
                self.hl(s, a, y0 + 6, a, y1 - 6, color=TONE['hair'], lw=0.75)

    def step_strip(self, s, y0, y1, edges, labels, style='chev'):
        """단계 띠: 직각 칸 + 칸 끝이 삼각형으로 뾰족하게 다음 칸을 가리킨다. 마지막 칸이 가장 진하다."""
        n = len(labels)
        tones = ['g1', 'g2', 'g3', 'g4'] if n == 4 else (['g2', 'g3', 'g4'] if n == 3 else ['g1', 'g2', 'g3', 'g4', 'g4'][:n])
        self.use('단계 띠', edges[0], y0, edges[-1], y1, f'{n}단계')
        for i, lab in enumerate(labels):
            sp = self.r(s, edges[i], y0, edges[i + 1], y1, fill=TONE[tones[i]], name='단계')
            self.fill_text(sp, [dict(t=lab, sz=SZ_D, b=True, color=ink_on(TONE[tones[i]]), align='c')], anchor='m', margins=(2.4, 0, 2.4, 0))
        cy = (y0 + y1) / 2
        for i, e in enumerate(edges[1:-1]):
            self.poly(s, [(e, y0), (e + 20, cy), (e, y1)], TONE[tones[i]], name='단계 삼각형')

    def tri_arrow(self, s, cx, cy, w, h, down=True, fill=None, name='삼각 화살표'):
        """속이 찬 삼각 화살표(▼ 또는 ▶)"""
        f = fill or TONE['g4']
        if down:
            return self.poly(s, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx, cy + h / 2)], f, name=name)
        return self.poly(s, [(cx - h / 2, cy - w / 2), (cx - h / 2, cy + w / 2), (cx + h / 2, cy)], f, name=name)

    def bracket(self, s, x0, y0, x1, h=36):
        """연결 화살표: 위 묶음에서 아래 한 칸으로 가운데 아래 삼각형(▼)"""
        self.use('연결 화살표', x0, y0, x1, y0 + h)
        self.tri_arrow(s, (x0 + x1) / 2, y0 + h / 2, 64, 26, down=True)

    def label_box(self, s, y0, y1, label, label_w=110, x0=98, x1=1248, tone='blue', tag_arrow=False, name='라벨 박스'):
        """라벨 박스: 외곽선 박스 + 왼쪽 라벨 칸. 안쪽 시작 x를 돌려준다."""
        self.use('라벨 박스', x0, y0, x1, y1)
        self.r(s, x0, y0, x1, y1, fill=C['white'], line=TONE['line'], lw=0.75, name=name)
        self.rail(s, x0 + 2, y0 + 2, x0 + label_w, y1 - 2, label, tone)
        return x0 + label_w + 6

    def tag_row(self, s, y0, y1, tag, text, x0, tag_w, x1, tone='g2'):
        """태그 + 설명 한 줄 (시사점·주요내용·활용사례)"""
        self.use('태그 줄', x0, y0, x1, y1)
        self.shp(s, x0, y0 + 2, x0 + tag_w, y1 - 2, tag, TONE[tone], shape=MSO_SHAPE.ROUNDED_RECTANGLE, rad=6, name='태그', mg=(0.3, 0, 0.3, 0))
        self.t(s, x0 + tag_w + 8, y0, x1, y1, [dict(t=text, sz=SZ_D, color=C['navy'])], name='태그 설명', mg=(0.6, 0, 0.3, 0), tag=tag)

    def photo(self, s, x0, y0, x1, y1, caption='사진'):
        self.use('사진 칸', x0, y0, x1, y1)
        sp = self.r(s, x0, y0, x1, y1, fill=TONE['g1'], line=TONE['line'], lw=0.75, name='사진 칸')
        self.fill_text(sp, [dict(t=caption, sz=SZ_D, color=C['slate_500'], align='c')], anchor='m')

    # ---- 두 갈래 패널 ----------------------------------------------
    def twin_panel(self, s, y0, y1, left, right, head_h=44, label_w=(135, 148), rows_y=None, gap=9):
        """2분할 패널. left/right = dict(title, x0, x1, rows=[(tag|None, 라벨, [줄들])])"""
        for side, lab_w in ((left, label_w[0]), (right, label_w[1])):
            x0, x1 = side['x0'], side['x1']
            self.use('2분할 패널', x0, y0, x1, y1, side['title'])
            self.r(s, x0, y0, x1, y1, fill=C['white'], line=TONE['g2'], lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, rad=9, name='패널 외곽')
            hd = self.r(s, x0, y0, x1, y0 + head_h, fill=TONE['g2'], shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, name='패널 머리')
            self.fill_text(hd, [dict(t=side['title'], sz=SZ_D, b=True, color=C['navy'], align='c')], anchor='m')
            n = len(side['rows'])
            ys = rows_y or [y0 + head_h + 4 + i * (y1 - y0 - head_h - 8) / n for i in range(n + 1)]
            ys = list(ys)
            for i, (tag, lab, its) in enumerate(side['rows']):
                ry0, ry1 = ys[i], ys[i + 1]
                self.rail(s, x0 + 6, ry0 + 2, x0 + 6 + lab_w, ry1 - 2, lab, 'blue', tag=tag)
                paras = [B(t) for t in its]
                self.t(s, x0 + 6 + lab_w + 8, ry0, x1 - 6, ry1, paras, anchor='m', mg=(1.2, 0.3, 0.5, 0.3), name='패널 본문', tag=lab[:6])
                if i < n - 1:
                    self.hl(s, x0 + 6 + lab_w + 8, ry1, x1 - 10, ry1, color=TONE['hair'], lw=0.75)

    # ---- 표 ------------------------------------------------------------
    def grid_table(self, s, x0, y0, col_w, row_h, rows, head=True, align=None, merge=(), name='표', fills=None, bold_cols=()):
        """실제 PPT 표(편집 가능). col_w·row_h는 px. merge=[(r0,c0,r1,c1)]"""
        from pptx.enum.text import MSO_ANCHOR
        nr, nc = len(rows), len(col_w)
        gf = s.shapes.add_table(nr, nc, mm(X(x0)), mm(Y(y0)), mm(S(sum(col_w))), mm(S(sum(row_h))))
        gf.name = name
        tbl = gf.table
        tp = tbl._tbl.tblPr
        for a in ('bandRow', 'firstRow', 'bandCol', 'firstCol', 'lastRow', 'lastCol'):
            if a in tp.attrib:
                del tp.attrib[a]
        for ch in list(tp):
            tp.remove(ch)
        for i, w in enumerate(col_w):
            tbl.columns[i].width = mm(S(w))
        for i, h in enumerate(row_h):
            tbl.rows[i].height = mm(S(h))
        for (r0, c0, r1, c1) in merge:
            tbl.cell(r0, c0).merge(tbl.cell(r1, c1))
        for ri, r in enumerate(rows):
            for ci, txt in enumerate(r):
                c = tbl.cell(ri, ci)
                is_head = head and ri == 0
                fill = (fills or {}).get((ri, ci), TONE['g1'] if is_head else C['white'])
                self._cell_border(c, TONE['hair'], 9525)
                c.fill.solid(); c.fill.fore_color.rgb = rgb(fill)
                c.margin_left = c.margin_right = mm(1.0)
                c.margin_top = c.margin_bottom = mm(0.2)
                c.vertical_anchor = MSO_ANCHOR.MIDDLE
                al = 'c' if (is_head or ci in bold_cols) else (align[ci] if align else 'l')
                body = c.text_frame._txBody
                for p in body.findall(qn('a:p')):
                    body.remove(p)
                for ln in str(txt).split('\n'):
                    body.append(self._para_el(dict(t=ln, sz=SZ_D, b=is_head or ci in bold_cols, color=ink_on(fill), align=al)))
        return gf


# ---------------------------------------------------------------- 마스터·레이아웃
def build_road_system(prs):
    lay = kp.build_system(prs)           # 표지·간지·본문 3종 + 테마(Pretendard·KORAD 색)
    odd, even = lay['본문'], lay['간지']
    for ly, nm in ((odd, '지면-홀수'), (even, '지면-짝수')):
        ly._element.cSld.set('name', nm)
        lay[nm] = ly
        tree = ly.shapes._spTree
        for sp in list(tree):
            if sp.tag in (qn('p:sp'), qn('p:pic'), qn('p:grpSp')):
                tree.remove(sp)
    # --- 홀수쪽: 왼쪽 위 큰 번호 + 범주·영역명, 왼쪽 아래 쪽번호 + 보고서명 탭
    t = odd.shapes._spTree
    _add(t, _ph_sp(2, '대분류 번호', 'type="body" sz="quarter" idx="13"', X(98), Y(90), 13, 11, 34, True, C['blue_deep'], 'ctr', 'l', '4'))
    _add(t, _sp_xml(3, '번호 구분선', X(150), Y(97), 0.3, S(53), fill=C['blue_bright']))
    _add(t, _ph_sp(4, '범주', 'type="body" sz="quarter" idx="14"', X(166), Y(96), 100, 5.0, SZ_D, False, C['slate_500'], 'ctr', 'l', 'Ⅰ. 경영관리 범주'))
    _add(t, _ph_sp(5, '영역명', 'type="body" sz="quarter" idx="15"', X(166), Y(96) + 5.0, 120, 5.8, SZ_TITLE, True, C['navy'], 'ctr', 'l', '조직 운영 및 관리'))
    _add(t, _sp_xml(6, '쪽 탭 빗면', X(160) + 46.5, Y(1921), 11, S(30), prst='parallelogram', fill=C['tint_200'], geom_extra='<a:gd name="adj" fmla="val 60000"/>'))
    _add(t, _ph_sp(7, '쪽번호', 'type="body" sz="quarter" idx="16"', X(98), Y(1921), 10, S(30), SZ_SHAPE, False, C['slate_500'], 'ctr', 'l', '93'))
    _add(t, _sp_xml(8, '쪽 구분선', X(150), Y(1925), 0.3, S(22), fill=C['slate_300']))
    _add(t, _ph_sp(9, '보고서명', 'type="body" sz="quarter" idx="17"', X(160), Y(1921), 50, S(30), 10, False, C['slate_500'], 'ctr', 'l', '2025년도 경영실적보고서'))
    # --- 짝수쪽: 오른쪽 위 지표명 + 밑줄, 오른쪽 아래 CI + 쪽번호 탭
    t = even.shapes._spTree
    _add(t, _ph_sp(2, '지표명', 'type="body" sz="quarter" idx="13"', X(1281) - 60, Y(108), 60, 6.4, SZ_D + 2, False, C['navy'], 'b', 'r', '노사관계'))
    _add(t, _sp_xml(3, '지표명 밑줄', X(1187), Y(153), X(1281) - X(1187), 0.3, fill=C['blue_bright']))
    _add(t, _sp_xml(4, '밑줄 끝', X(1281) - 1.2, Y(153) - 0.45, 1.2, 1.2, fill=C['blue_bright']))
    tab_x = X(950)
    _add(t, _sp_xml(5, '쪽 탭 빗면', tab_x, Y(1914), 14, S(44), prst='parallelogram', fill=C['tint_100'], geom_extra='<a:gd name="adj" fmla="val 70000"/>'))
    _add(t, _sp_xml(6, '쪽 탭', tab_x + 6, Y(1914), X(1281) - tab_x - 6, S(44), fill=C['tint_100']))
    rid = _img_rid(even, CI)
    ci_w = 27.0
    _add(t, _pic_xml(7, 'KORAD CI', rid, tab_x + 14, Y(1914) + (S(44) - ci_w * 66 / 356) / 2, ci_w, ci_w * 66 / 356))
    _add(t, _ph_sp(8, '쪽번호', 'type="body" sz="quarter" idx="14"', X(1281) - 12, Y(1914), 10, S(44), SZ_SHAPE, False, C['navy'], 'ctr', 'r', '94'))
    return lay


def _img_rid(layout, path):
    _, rid = layout.part.get_or_add_image_part(path)
    return rid
