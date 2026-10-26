# -*- coding: utf-8 -*-
"""PPT 슬라이드의 도형을 그대로 HTML(절대 위치)로 옮긴다 — 디자인 시스템 미리보기용(그림이 아니라 선·색·글자 있는 실제 도형)."""
from html import escape
from pptx.util import Emu
from pptx.oxml.ns import qn

PX = 960 / (210 * 36000)          # EMU → px (A4 폭 960px)
PT = 960 / 595.2756               # pt → px


def _clr(el):
    if el is None: return None
    c = el.find(qn('a:srgbClr'))
    return '#' + c.get('val') if c is not None else None


def _fill(spPr):
    if spPr is None: return 'transparent', None
    s = spPr.find(qn('a:solidFill'))
    if s is not None: return _clr(s), None
    g = spPr.find(qn('a:gradFill'))
    if g is not None:
        cs = [_clr(x) for x in g.iter(qn('a:gs'))]
        lin = g.find(qn('a:lin')); ang = (int(lin.get('ang')) / 60000 + 90) if lin is not None else 90
        return None, f'linear-gradient({ang:.0f}deg,{",".join(cs)})'
    p = spPr.find(qn('a:pattFill'))
    if p is not None:
        fg = _clr(p.find(qn('a:fgClr'))); bg = _clr(p.find(qn('a:bgClr')))
        return bg, f'repeating-linear-gradient(45deg,{fg} 0 1px,transparent 1px 4px)'
    return 'transparent', None


def _line(spPr):
    if spPr is None: return None
    ln = spPr.find(qn('a:ln'))
    if ln is None or ln.find(qn('a:noFill')) is not None: return None
    c = _clr(ln.find(qn('a:solidFill')))
    if not c: return None
    return f'{max(ln.get("w") and int(ln.get("w")) / 12700 * PT or 1, 0.8):.1f}px solid {c}'


def _paras(tb):
    out = []
    for p in tb.findall(qn('a:p')):
        ppr = p.find(qn('a:pPr')); al = {'ctr': 'center', 'r': 'right'}.get(ppr.get('algn') if ppr is not None else None, 'left')
        bu = ppr.find(qn('a:buChar')).get('char') if ppr is not None and ppr.find(qn('a:buChar')) is not None else ''
        marL = int(ppr.get('marL', 0)) * PX if ppr is not None else 0
        runs = ''
        for r in p.findall(qn('a:r')):
            rp = r.find(qn('a:rPr'))
            if rp is None: rp = r.makeelement(qn('a:rPr'), {})
            sz = int(rp.get('sz', 1000)) / 100 * PT; b = 'bold' if rp.get('b') == '1' else 'normal'
            c = _clr(rp.find(qn('a:solidFill'))) or '#000359'
            runs += f'<span style="font-size:{sz:.1f}px;font-weight:{b};color:{c}">{escape(r.find(qn("a:t")).text or "")}</span>'
        if runs or bu:
            out.append(f'<div class="p" style="text-align:{al};padding-left:{marL:.1f}px;text-indent:-{marL:.1f}px">' + (f'<span class="bu" style="width:{marL:.1f}px">{escape(bu)}</span>' if bu else '') + runs + '</div>')
    return ''.join(out)


def slide_html(slide, y0_px=0, y1_px=None, x0_px=0):
    """slide의 도형을 div로. 좌표 단위 px(용지 960 기준). y0_px~y1_px 영역만 잘라 낸다."""
    items = []
    for sh in slide.shapes:
        el = sh._element
        x, y, w, h = [v * PX for v in (sh.left, sh.top, sh.width, sh.height)]
        if y + h < y0_px or (y1_px and y > y1_px): continue
        tag = el.tag
        if tag == qn('p:graphicFrame'):
            tb = sh.table; rows = ''
            for r in tb.rows:
                rows += f'<tr style="height:{r.height * PX:.1f}px">'
                for c in r.cells:
                    if c.is_spanned: continue
                    tcPr = c._tc.find(qn('a:tcPr')); f = _fill(tcPr)[0] if tcPr is not None else '#fff'
                    rows += f'<td rowspan="{c.span_height}" colspan="{c.span_width}" style="background:{f}">{_paras(c._tc.find(qn("a:txBody")))}</td>'
                rows += '</tr>'
            items.append(f'<table style="left:{x - x0_px:.1f}px;top:{y - y0_px:.1f}px;width:{w:.1f}px"><colgroup>' + ''.join(f'<col style="width:{c.width * PX:.1f}px">' for c in tb.columns) + f'</colgroup>{rows}</table>')
            continue
        spPr = el.find(qn('p:spPr'))
        if tag == qn('p:cxnSp'):
            ln = _line(spPr) or '1px solid #bde0ff'
            if h < 2: items.append(f'<div class="s" style="left:{x - x0_px:.1f}px;top:{y - y0_px:.1f}px;width:{w:.1f}px;border-top:{ln}"></div>')
            else: items.append(f'<div class="s" style="left:{x - x0_px:.1f}px;top:{y - y0_px:.1f}px;height:{h:.1f}px;border-left:{ln}"></div>')
            continue
        if tag == qn('p:pic'):
            continue
        bg, grad = _fill(spPr); ln = _line(spPr)
        geom = spPr.find(qn('a:prstGeom')) if spPr is not None else None
        prst = geom.get('prst') if geom is not None else 'custom'
        st = f'left:{x - x0_px:.1f}px;top:{y - y0_px:.1f}px;width:{w:.1f}px;height:{h:.1f}px;'
        if prst == 'custom':
            pts = [(int(pt.get('x')), int(pt.get('y'))) for pt in spPr.iter(qn('a:pt'))]
            if pts:
                mx = max(p[0] for p in pts) or 1; my = max(p[1] for p in pts) or 1
                poly = ','.join(f'{p[0] / mx * 100:.1f}% {p[1] / my * 100:.1f}%' for p in pts)
                st += f'background:{bg if bg and bg != "transparent" else "#bde0ff"};clip-path:polygon({poly});'
        else:
            if bg: st += f'background:{bg};'
            if grad: st += f'background-image:{grad};'
            if ln: st += f'border:{ln};box-sizing:border-box;'
            if prst == 'triangle': st += 'clip-path:polygon(50% 0,0 100%,100% 100%);'
            rot = sh.rotation
            if rot: st += f'transform:rotate({rot:.0f}deg);'
        txt = ''
        tb = el.find(qn('p:txBody'))
        if tb is not None:
            bp = tb.find(qn('a:bodyPr')); anc = {'ctr': 'center', 'b': 'flex-end'}.get(bp.get('anchor') if bp is not None else 't', 'flex-start')
            pad = [int(bp.get(k, 0)) * PX for k in ('lIns', 'tIns', 'rIns', 'bIns')] if bp is not None else [0] * 4
            inner = _paras(tb)
            if inner:
                txt = f'<div class="t" style="justify-content:{anc};padding:{pad[1]:.1f}px {pad[2]:.1f}px {pad[3]:.1f}px {pad[0]:.1f}px">{inner}</div>'
        items.append(f'<div class="s" style="{st}">{txt}</div>')
    return ''.join(items)


CSS = '''.pg{position:relative;width:960px;background:#fff;font-family:var(--font-sans),Pretendard,sans-serif;overflow:hidden}.pg .s{position:absolute}.pg .t{position:absolute;inset:0;display:flex;flex-direction:column;line-height:1.28;overflow:hidden}.pg .p{margin:0}.pg .bu{display:inline-block;text-indent:0}
.pg table{position:absolute;border-collapse:collapse;table-layout:fixed}.pg td{border:1px solid #bde0ff;padding:1px 4px;vertical-align:middle;line-height:1.25}.pg .p{white-space:pre-wrap}'''
