# -*- coding: utf-8 -*-
"""KORAD 경영평가 PPT 시스템 — A4 세로 라이브러리 (python-pptx)."""
import copy, math, re, os, json
from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_PATTERN
from pptx.oxml.ns import qn

ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets') + '/'
CI = ASSET + 'korad-ci.png'
BAND = ASSET + 'header-band.png'
COVERBG = ASSET + 'cover-background.png'

# ---- 페이지·여백 표준 (mm) : 사용자 지정 A4, 좌우 15 · 상하 10 -------------
PW, PH = 210.0, 297.0
ML, MR, MT, MB = 15.0, 15.0, 10.0, 10.0
CX0, CX1 = ML, PW - MR            # 15 ~ 195
CW = CX1 - CX0                    # 180
CY0, CY1 = MT, PH - MB            # 10 ~ 287
HDR_H = 9.0                       # 머리글(경로 + CI)
HDR_RULE_Y = CY0 + HDR_H          # 19
GM_Y = HDR_RULE_Y + 2.5           # 21.5
GM_H = 13.5
RULE_Y = GM_Y + GM_H + 1.0        # 36
BODY_Y = RULE_Y + 4.0             # 40
NAV_Y = 265.0                     # 하단 탭
NAV_H = 10.0
FOOT_Y = CY1 - 8.5                # 278.5
BODY_B = NAV_Y - 3.0              # 262 (탭 있는 지면)
BODY_B_FREE = FOOT_Y - 2.5        # 276 (탭 없는 지면)
BODY_H = BODY_B - BODY_Y          # 222

MEAS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meas.json')
MEAS = json.load(open(MEAS_PATH)) if os.path.exists(MEAS_PATH) else {}

# ---- 글자 크기 표준 (pt) ---------------------------------------------------
SZ_BODY = 12      # 글상자·박스 안 텍스트
SZ_TITLE = 15     # 박스 밖 제목
SZ_SHAPE = 14     # 네모·동그라미(라벨/번호) 안 글자

# ---- KORAD 색 토큰 -----------------------------------------------------------
C = dict(
    navy='000359', navy_deep='001A7A', blue_strong='0061DE', blue_bright='008EFF',
    blue_panel='0080EA', blue_panel_light='0990FF', blue_deep='0051BC', blue_cyan='30C2FF',
    ground_pale='E6F4FF', tint_100='DEEEFF', tint_200='BDE0FF', tint_sky='E1F4FF',
    tint_aqua='E1F9FF', tint_mint='E6FCF9', tint_panel='EFF9FF', tint_10='E5F3FF',
    rule_pale='DEE6F6', teal_500='00A4A8', teal_panel='00B0B4', green_400='00BE83',
    mint_hl='29FFBD', slate_700='3B4951', slate_500='5D7280', slate_300='8D9CBF',
    navy_band='002060', cyan_hl='00FFFF', chart_base='C1D1ED', chart_cyan='00B0F6',
    white='FFFFFF', amber='FBAE40', number_muted='ABB9CE', page_ink='003764')
FONT = 'Pretendard'


def mm(v):
    return Emu(int(round(v * 36000)))


def rgb(h):
    return RGBColor.from_string(h)


# ---------------------------------------------------------------- 글자 폭 추정
_F = ImageFont.truetype(os.environ.get('PRETENDARD_TTF', os.path.expanduser('~/.fonts/Pretendard-Regular.ttf')), 1000)
_CW = {}


def cw_mm(ch, pt=SZ_BODY):
    if ch not in _CW:
        _CW[ch] = _F.getlength(ch) / 1000.0
    return max(_CW[ch] - 0.05, 0.2) * pt * 0.3528


def est_lines(text, width_mm, pt=SZ_BODY, indent=0.0):
    """줄바꿈 추정(단어 단위, 한글은 글자 단위)."""
    avail = max(width_mm - indent, 5)
    total = 0
    for para in str(text).split('\n'):
        w = 0.0
        lines = 1
        for tok in re.findall(r'\S+\s*|\s+', para):
            tw = sum(cw_mm(c, pt) for c in tok)
            if w + tw <= avail + 0.01:
                w += tw
            else:
                # 한글이 섞인 토큰은 글자 단위로 쪼갬
                if tw > avail:
                    for c in tok:
                        cwid = cw_mm(c, pt)
                        if w + cwid > avail:
                            lines += 1
                            w = 0
                        w += cwid
                else:
                    lines += 1
                    w = tw
        total += lines
    return total


LINE_MM = SZ_BODY * 0.3528 * 1.10 * 1.0   # 110% 행간 ≈ 4.66mm


def text_h(text, width_mm, pt=SZ_BODY, indent=0.0, spacing=1.10):
    return est_lines(text, width_mm, pt, indent) * pt * 0.3528 * spacing * 1.17


# ----------------------------------------------------------------- XML 보조
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def _sp_xml(id_, name, x, y, w, h, prst='rect', fill=None, line=None, line_w=0.5, text_xml='',
            ph=None, anchor='ctr', ins=(0, 0, 0, 0), txbox=False, wrap='square', geom_extra=''):
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    line_xml = (f'<a:ln w="{int(line_w*12700)}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
                if line else '<a:ln><a:noFill/></a:ln>')
    ph_xml = f'<p:nvPr><p:ph {ph}/></p:nvPr>' if ph else '<p:nvPr/>'
    cnv = '<p:cNvSpPr txBox="1"/>' if txbox else '<p:cNvSpPr/>'
    l, t, r, b = [int(v * 36000) for v in ins]
    return f'''<p:sp xmlns:a="{NS['a']}" xmlns:p="{NS['p']}" xmlns:r="{NS['r']}">
<p:nvSpPr><p:cNvPr id="{id_}" name="{name}"/>{cnv}{ph_xml}</p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{int(x*36000)}" y="{int(y*36000)}"/><a:ext cx="{int(w*36000)}" cy="{int(h*36000)}"/></a:xfrm>
<a:prstGeom prst="{prst}"><a:avLst>{geom_extra}</a:avLst></a:prstGeom>{fill_xml}{line_xml}</p:spPr>
<p:txBody><a:bodyPr wrap="{wrap}" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" anchor="{anchor}"><a:noAutofit/></a:bodyPr><a:lstStyle/>{text_xml or '<a:p><a:endParaRPr lang="ko-KR"/></a:p>'}</p:txBody></p:sp>'''


def _ph_sp(id_, name, ph, x, y, w, h, sz, bold, color, anchor='ctr', algn='l', prompt='', spc=0):
    b = ' b="1"' if bold else ''
    spc_x = f' spc="{spc}"' if spc else ''
    lst = (f'<a:lstStyle><a:lvl1pPr marL="0" indent="0" algn="{algn}"><a:lnSpc><a:spcPct val="110000"/></a:lnSpc>'
           f'<a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/>'
           f'<a:defRPr sz="{int(sz*100)}"{b}{spc_x}><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
           f'<a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/></a:defRPr></a:lvl1pPr></a:lstStyle>')
    return f'''<p:sp xmlns:a="{NS['a']}" xmlns:p="{NS['p']}" xmlns:r="{NS['r']}">
<p:nvSpPr><p:cNvPr id="{id_}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph {ph}/></p:nvPr></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{int(x*36000)}" y="{int(y*36000)}"/><a:ext cx="{int(w*36000)}" cy="{int(h*36000)}"/></a:xfrm></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"><a:noAutofit/></a:bodyPr>{lst}
<a:p><a:r><a:rPr lang="ko-KR"/><a:t>{prompt}</a:t></a:r></a:p></p:txBody></p:sp>'''


def _pic_xml(id_, name, rid, x, y, w, h, crop=None):
    src = ''
    if crop:
        l, t, r, b = [int(v * 100000) for v in crop]
        src = f'<a:srcRect l="{l}" t="{t}" r="{r}" b="{b}"/>'
    return f'''<p:pic xmlns:a="{NS['a']}" xmlns:p="{NS['p']}" xmlns:r="{NS['r']}">
<p:nvPicPr><p:cNvPr id="{id_}" name="{name}" descr="{name}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="{rid}"/>{src}<a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="{int(x*36000)}" y="{int(y*36000)}"/><a:ext cx="{int(w*36000)}" cy="{int(h*36000)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'''


def _run_xml(text, sz, bold=False, color=C['navy'], spc=None):
    b = ' b="1"' if bold else ''
    s = f' spc="{spc}"' if spc is not None else ''
    t = (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    return (f'<a:r><a:rPr lang="ko-KR" sz="{int(sz*100)}"{b}{s} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/></a:rPr><a:t>{t}</a:t></a:r>')


def _add(tree, xml):
    el = etree.fromstring(xml)
    tree.append(el)
    return el


# ----------------------------------------------------------- 마스터·레이아웃
def build_system(prs):
    prs.slide_width = mm(PW)
    prs.slide_height = mm(PH)
    master = prs.slide_master
    # 1) 레이아웃 정리: 표지/본문/간지 3종만 남김
    keep = {0: '표지', 5: '본문', 2: '간지'}
    lays = list(prs.slide_layouts)
    for i, lay in enumerate(lays):
        if i not in keep:
            lst = master.slide_layouts._sldLayoutIdLst
            for lid in list(lst):
                if master.part.related_part(lid.rId) is lay.part:
                    lst.remove(lid)
                    master.part.drop_rel(lid.rId)
    # 2) 마스터: 도형 제거 후 기본 배경 흰색
    mtree = master.shapes._spTree
    for sp in list(mtree):
        if sp.tag in (qn('p:sp'), qn('p:pic'), qn('p:grpSp')):
            mtree.remove(sp)
    # 3) 테마 글꼴·색
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    theme = master.part.part_related_by(RT.THEME)
    xml = theme.blob.decode('utf8')
    xml = re.sub(r'<a:latin typeface="[^"]*"', f'<a:latin typeface="{FONT}"', xml)
    xml = re.sub(r'(<a:ea typeface=")[^"]*"', rf'\1{FONT}"', xml)
    xml = re.sub(r'(<a:font script="Hang" typeface=")[^"]*"', rf'\1{FONT}"', xml)
    pal = dict(dk1=C['navy'], lt1='FFFFFF', dk2=C['navy_deep'], lt2=C['ground_pale'], accent1=C['blue_bright'],
               accent2=C['teal_500'], accent3=C['blue_deep'], accent4=C['blue_cyan'], accent5=C['green_400'], accent6=C['amber'],
               hlink=C['blue_strong'], folHlink=C['slate_500'])
    for k, v in pal.items():
        xml = re.sub(rf'(<a:{k}>)(.*?)(</a:{k}>)', rf'\1<a:srgbClr val="{v}"/>\3', xml, flags=re.S)
    xml = re.sub(r'<a:clrScheme name="[^"]*"', '<a:clrScheme name="KORAD 경영평가"', xml)
    xml = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="Pretendard"', xml)
    theme._blob = xml.encode('utf8')

    lay_by_name = {}
    for i, lay in enumerate(prs.slide_layouts):
        pass
    layouts = list(prs.slide_layouts)
    names = ['표지', '간지', '본문']
    # 남은 3개의 순서: 원본 0,2,5
    for lay, nm in zip(layouts, names):
        lay._element.cSld.set('name', nm)
        lay_by_name[nm] = lay
        tree = lay.shapes._spTree
        for sp in list(tree):
            if sp.tag in (qn('p:sp'), qn('p:pic'), qn('p:grpSp')):
                tree.remove(sp)
        # 배경 흰색
    _build_body_layout(lay_by_name['본문'])
    _build_cover_layout(lay_by_name['표지'])
    _build_divider_layout(lay_by_name['간지'])
    return lay_by_name


def _img_rid(layout, path):
    _, rid = layout.part.get_or_add_image_part(path)
    return rid


def _build_body_layout(lay):
    t = lay.shapes._spTree
    rid_ci = _img_rid(lay, CI)
    # 머리글: 경로(좌) + CI(우) + 하단 실선 — 경영실적보고서 지면 형식
    _add(t, _ph_sp(2, '지면 경로', 'type="body" sz="quarter" idx="13"', CX0, CY0, 130, HDR_H - 1.0, SZ_BODY, True, C['navy'], 'ctr', 'l', 'Ⅰ. 경영관리 | 04. 조직 운영 및 관리 | 노사관계'))
    ci_w = 33.0
    _add(t, _pic_xml(3, 'KORAD CI', rid_ci, CX1 - ci_w, CY0 + 0.6, ci_w, ci_w * 66 / 356))
    _add(t, _sp_xml(4, '머리글 실선', CX0, HDR_RULE_Y, CW, 0.7, fill=C['blue_deep']))
    # Governing Header: 좌측 기준선, 가로형 두괄식
    _add(t, _sp_xml(5, 'GM 기준선', CX0, GM_Y + 0.5, 1.8, GM_H - 1.0, fill=C['blue_bright']))
    _add(t, _ph_sp(6, 'Governing Message', 'type="title"', CX0 + 4.5, GM_Y, CW - 4.5, GM_H, SZ_TITLE, True, C['navy'], 'ctr', 'l', 'Governing Message'))
    _add(t, _sp_xml(7, 'GM 하단 띠', CX0, RULE_Y, CW, 0.5, fill=C['rule_pale']))
    # 하단: 출처·주석 + 쪽 번호 탭
    _add(t, _ph_sp(8, '출처·주석', 'type="body" sz="quarter" idx="16"', CX0, FOOT_Y, CW - 12.0, 8.5, SZ_BODY, False, C['slate_700'], 'b', 'l', '출처·주석'))
    _add(t, _sp_xml(9, '페이지 탭', CX1 - 9.5, FOOT_Y - 0.5, 9.5, 9.0, prst='round2SameRect', fill=C['ground_pale'],
                    geom_extra='<a:gd name="adj1" fmla="val 22000"/><a:gd name="adj2" fmla="val 0"/>'))
    fld = (f'<a:p><a:pPr algn="ctr"/><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum">'
           f'<a:rPr lang="en-US" sz="{SZ_BODY*100}" b="1"><a:solidFill><a:srgbClr val="{C["page_ink"]}"/></a:solidFill>'
           f'<a:latin typeface="{FONT}"/></a:rPr><a:t>‹#›</a:t></a:fld></a:p>')
    _add(t, _sp_xml(10, '페이지 번호', CX1 - 9.5, FOOT_Y - 0.5, 9.5, 9.0, text_xml=fld, anchor='ctr', txbox=True))


def _build_cover_layout(lay):
    t = lay.shapes._spTree
    rid_bg = _img_rid(lay, COVERBG)
    rid_ci = _img_rid(lay, CI)
    _add(t, _sp_xml(2, '표지 바탕', CX0, CY0, CW, CY1 - CY0, fill=C['ground_pale']))
    bg_h = 150.0
    bg_ar = 2200 / 1238
    keep_w = (CW / bg_h) / bg_ar
    _add(t, _pic_xml(3, '표지 일러스트', rid_bg, CX0, CY1 - bg_h, CW, bg_h, crop=(1 - keep_w, 0, 0, 0)))
    _add(t, _pic_xml(4, 'KORAD CI', rid_ci, CX0 + 6, CY0 + 8, 54.0, 54.0 * 66 / 356))
    _add(t, _ph_sp(5, '표지 제목', 'type="ctrTitle"', CX0 + 6, 78.0, CW - 12, 56.0, 34, True, C['navy'], 't', 'l', '표지 제목'))
    _add(t, _ph_sp(6, '표지 부제', 'type="subTitle" idx="1"', CX0 + 6, 138.0, CW - 12, 22.0, SZ_TITLE, False, C['navy'], 't', 'l', '표지 부제'))


def _build_divider_layout(lay):
    t = lay.shapes._spTree
    rid_ci = _img_rid(lay, CI)
    _add(t, _sp_xml(2, '간지 바탕', CX0, CY0, CW, CY1 - CY0, fill=C['korad_blue'] if 'korad_blue' in C else '0077FF'))
    _add(t, _pic_xml(3, 'KORAD CI', rid_ci, CX0 + 6, CY0 + 8, 54.0, 54.0 * 66 / 356))
    _add(t, _ph_sp(4, '간지 번호', 'type="body" sz="quarter" idx="13"', CX0 + 6, 110.0, 60, 30, 54, False, C['white'], 'b', 'l', '01'))
    _add(t, _ph_sp(5, '간지 제목', 'type="title"', CX0 + 6, 144.0, CW - 12, 36.0, 34, False, C['white'], 't', 'l', '간지 제목'))


# -------------------------------------------------------------- 슬라이드 도구
class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.lay = build_system(self.prs)

    # -- 슬라이드 -------------------------------------------------------
    def body(self, crumb, gm, source='', nav=None):
        s = self.prs.slides.add_slide(self.lay['본문'])
        ph = {p.placeholder_format.idx: p for p in s.placeholders}
        self._set_ph(ph[13], crumb)
        self._set_ph(s.shapes.title, gm)
        self._set_ph(ph[16], source)
        if nav is not None:
            self.nav(s, nav)
        return s

    def nav(self, s, active):
        """하단 대분류 탭: Ⅰ경영관리 Ⅱ주요사업 Ⅲ혁신노력·가점 Ⅳ계량지표요약표 (active 0~3)"""
        names = ['Ⅰ 경영관리', 'Ⅱ 주요사업', 'Ⅲ 혁신노력·성과가점', 'Ⅳ 계량지표요약표']
        ws = [38, 38, 62, 42]
        x = CX0
        for i, (n, w) in enumerate(zip(names, ws)):
            on = (i == active)
            sp = self.rect(s, x, NAV_Y, w - 1.0, NAV_H, fill=C['blue_deep'] if on else C['tint_panel'], line=None if on else C['tint_200'], line_w=0.5, name='하단 탭')
            self.fill_text(sp, [dict(t=n, sz=SZ_BODY, b=on, color=C['white'] if on else C['slate_500'], align='c')], anchor='m')
            x += w

    def _set_ph(self, shape, text):
        tf = shape.text_frame
        tf.text = text

    # -- 기본 도형 -------------------------------------------------------
    def rect(self, s, x, y, w, h, fill=None, line=None, line_w=0.5, shape=MSO_SHAPE.RECTANGLE, name=None, adj=None):
        sp = s.shapes.add_shape(shape, mm(x), mm(y), mm(w), mm(h))
        if adj is not None:
            sp.adjustments[0] = adj
        if fill:
            sp.fill.solid(); sp.fill.fore_color.rgb = rgb(fill)
        else:
            sp.fill.background()
        if line:
            sp.line.color.rgb = rgb(line); sp.line.width = Pt(line_w)
        else:
            sp.line.fill.background()
        sp.shadow.inherit = False
        if name:
            sp.name = name
        tf = sp.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        return sp

    def trellis(self, sp, fore, back):
        sp.fill.patterned()
        sp.fill.pattern = MSO_PATTERN.TRELLIS
        sp.fill.fore_color.rgb = rgb(fore)
        sp.fill.back_color.rgb = rgb(back)

    def line(self, s, x1, y1, x2, y2, color=C['blue_bright'], w=0.75, dash=False):
        ln = s.shapes.add_connector(1, mm(x1), mm(y1), mm(x2), mm(y2))
        ln.line.color.rgb = rgb(color); ln.line.width = Pt(w)
        if dash:
            ln.line.dash_style = 4
        return ln

    def pic(self, s, path, x, y, w=None, h=None, name=None):
        p = s.shapes.add_picture(path, mm(x), mm(y), mm(w) if w else None, mm(h) if h else None)
        if name:
            p.name = name
        return p

    # -- 글 ----------------------------------------------------------------
    def fill_text(self, shape, paras, anchor='t', margins=(0, 0, 0, 0), wrap=True):
        """paras: [ {t|runs, sz, b, color, align, bullet, lvl, after, before} ]"""
        tf = shape.text_frame
        tf.word_wrap = wrap
        tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [mm(v) for v in margins]
        tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
        body = tf._txBody
        for p in body.findall(qn('a:p')):
            body.remove(p)
        for pd in paras:
            body.append(self._para_el(pd))
        return shape

    def _para_el(self, pd):
        sz = pd.get('sz', SZ_BODY)
        color = pd.get('color', C['navy'])
        bold = pd.get('b', False)
        algn = {'l': 'l', 'c': 'ctr', 'r': 'r'}[pd.get('align', 'l')]
        bullet = pd.get('bullet')
        lvl_ind = pd.get('indent', 0.0)       # mm
        after = pd.get('after', 0)
        before = pd.get('before', 0)
        spc = pd.get('spc', int(round(-0.05 * sz * 100)) if pd.get('tight', True) else 0)
        marL = int((lvl_ind + (pd.get('hang', 4.2) if bullet else 0)) * 36000)
        ind = int(-(pd.get('hang', 4.2)) * 36000) if bullet else 0
        bu = '<a:buNone/>'
        if bullet:
            bu = (f'<a:buClr><a:srgbClr val="{pd.get("bucolor", color)}"/></a:buClr><a:buFont typeface="{FONT}"/>'
                  f'<a:buChar char="{bullet}"/>')
        ppr = (f'<a:pPr marL="{marL}" indent="{ind}" algn="{algn}"><a:lnSpc><a:spcPct val="110000"/></a:lnSpc>'
               f'<a:spcBef><a:spcPts val="{int(before*100)}"/></a:spcBef><a:spcAft><a:spcPts val="{int(after*100)}"/></a:spcAft>{bu}</a:pPr>')
        runs = pd.get('runs') or [(pd.get('t', ''), {})]
        rx = ''
        for txt, o in runs:
            rx += _run_xml(txt, o.get('sz', sz), o.get('b', bold), o.get('color', color), spc)
        xml = f'<a:p xmlns:a="{NS["a"]}">{ppr}{rx}</a:p>'
        return etree.fromstring(xml)

    def text(self, s, x, y, w, h, paras, anchor='t', margins=(0, 0, 0, 0), name=None, fill=None, line=None, line_w=0.5, shape=None, adj=None):
        if shape is None:
            sp = s.shapes.add_textbox(mm(x), mm(y), mm(w), mm(h))
            if fill:
                sp.fill.solid(); sp.fill.fore_color.rgb = rgb(fill)
            if line:
                sp.line.color.rgb = rgb(line); sp.line.width = Pt(line_w)
        else:
            sp = self.rect(s, x, y, w, h, fill=fill, line=line, line_w=line_w, shape=shape, adj=adj)
        if name:
            sp.name = name
        self.fill_text(sp, paras, anchor=anchor, margins=margins)
        return sp

    # 박스 밖 소제목 (15pt)
    def h2(self, s, x, y, w, t, bold=True, fill=None):
        return self.text(s, x, y, w, 7.0, [dict(t=t, sz=SZ_TITLE, b=bold)], anchor='m', name='소제목', fill=fill,
                         margins=(2.0, 0.6, 2.0, 0.6) if fill else (0, 0, 0, 0))

    # 네모·동그라미 라벨 (14pt)
    def badge(self, s, x, y, w, h, t, fill=C['blue_deep'], color=C['white'], shape=MSO_SHAPE.RECTANGLE, b=True, line=None, name='라벨', adj=None):
        return self.text(s, x, y, w, h, [dict(t=t, sz=SZ_SHAPE, b=b, color=color, align='c')], anchor='m', fill=fill, line=line,
                         shape=shape, name=name, adj=adj)

    def circle(self, s, x, y, d, t, fill=C['blue_panel'], color=C['white']):
        return self.badge(s, x, y, d, d, t, fill=fill, color=color, shape=MSO_SHAPE.OVAL, name='번호')

    def pill(self, s, x, y, w, t, h=6.6):
        return self.badge(s, x, y, w, h, t, fill=C['tint_100'], color=C['blue_bright'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5, name='캡션')

    # 패널(ContentPanel): 헤더 trellis + 본문 박스
    def panel(self, s, x, y, w, h, title, paras, kind='blue', head_h=8.5, body_margin=3.0):
        col = dict(blue=(C['blue_panel_light'], C['blue_panel'], C['blue_bright']),
                   teal=('00BEC2', C['teal_panel'], C['teal_500']),
                   deep=('0A6BE6', C['blue_deep'], C['blue_deep']))[kind]
        self.rect(s, x, y, w, h, fill=C['white'], line=col[2], line_w=0.5, name='패널')
        hd = self.rect(s, x, y, w, head_h, fill=None, name='패널 헤더')
        self.trellis(hd, col[0], col[1])
        self.fill_text(hd, [dict(t=title, sz=SZ_SHAPE, b=True, color=C['white'], align='c')], anchor='m', margins=(1, 0, 1, 0))
        self.text(s, x + body_margin, y + head_h + 2.2, w - 2 * body_margin, h - head_h - 3.5, paras, name='패널 본문')

    def tint_box(self, s, x, y, w, h, paras, fill=C['tint_sky'], label=None, margins=(3.2, 2.4, 3.2, 2.4)):
        sp = self.rect(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04, name='해설 박스')
        self.fill_text(sp, paras, anchor='m', margins=margins)
        return sp

    # -- 표 ----------------------------------------------------------------
    def table(self, s, x, y, col_w, rows, head=True, total_last=False, align=None, row_pad=1.2, min_row=7.0,
              head_fill=C['blue_bright'], bold_first_col=False, name='표', hdr_h=None, first_col_center=False, label_col=False, fill_to=None):
        ncol = len(col_w)
        # 행 높이 추정
        heights = []
        for ri, r in enumerate(rows):
            hmax = 1
            for ci, cell in enumerate(r):
                txt = cell if isinstance(cell, str) else cell.get('t', '')
                hmax = max(hmax, est_lines(txt, col_w[ci] - 3.2, SZ_BODY))
            hh = max(7.0 if (head and ri == 0) else min_row, hmax * 4.75 + 2 * row_pad + 0.6)
            heights.append(hh)
        key = f'{len(self.prs.slides)}|{name}'
        if key in MEAS and len(MEAS[key]) == len(rows):
            heights = [max(a, b) for a, b in zip(MEAS[key], heights)]
        if fill_to:
            extra = fill_to - y - sum(heights)
            body_n = len(rows) - (1 if head else 0)
            if extra > 0 and body_n > 0:
                heights = [h + (extra / body_n if (ri > 0 or not head) else 0) for ri, h in enumerate(heights)]
        gf = s.shapes.add_table(len(rows), ncol, mm(x), mm(y), mm(sum(col_w)), mm(sum(heights)))
        gf.name = name
        tbl = gf.table
        tblPr = tbl._tbl.tblPr
        for a in ('bandRow', 'firstRow', 'bandCol', 'firstCol', 'lastRow', 'lastCol'):
            if a in tblPr.attrib:
                del tblPr.attrib[a]
        for ch in list(tblPr):
            tblPr.remove(ch)
        for i, w in enumerate(col_w):
            tbl.columns[i].width = mm(w)
        for ri, r in enumerate(rows):
            tbl.rows[ri].height = mm(heights[ri])
            for ci, cell in enumerate(r):
                c = tbl.cell(ri, ci)
                spec = cell if isinstance(cell, dict) else dict(t=cell)
                is_head = head and ri == 0
                is_total = total_last and ri == len(rows) - 1
                self._cell_border(c, C['blue_bright'])
                fill = head_fill if is_head else (C['tint_100'] if is_total else spec.get('fill', C['tint_panel'] if (label_col and ci == 0) else C['white']))
                c.fill.solid(); c.fill.fore_color.rgb = rgb(fill)
                c.margin_left = c.margin_right = mm(1.6)
                c.margin_top = c.margin_bottom = mm(row_pad)
                c.vertical_anchor = MSO_ANCHOR.MIDDLE
                al = 'c' if is_head else (align[ci] if align else 'l')
                if (first_col_center or label_col) and ci == 0 and not is_head:
                    al = 'c'
                b = is_head or is_total or spec.get('b', False) or ((bold_first_col or label_col) and ci == 0)
                col = C['white'] if is_head else spec.get('color', C['navy'])
                txt = spec.get('t', '')
                tf = c.text_frame
                tf.word_wrap = True
                body = tf._txBody
                for p in body.findall(qn('a:p')):
                    body.remove(p)
                for line in str(txt).split('\n'):
                    body.append(self._para_el(dict(t=line, sz=SZ_BODY, b=b, color=col, align=al)))
        return gf, sum(heights)

    def _cell_border(self, cell, color, w=6350):
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
            ln = etree.SubElement(tcPr, qn(tag), w=str(w), cap='flat', cmpd='sng', algn='ctr')
            sf = etree.SubElement(ln, qn('a:solidFill'))
            etree.SubElement(sf, qn('a:srgbClr'), val=color)
            etree.SubElement(ln, qn('a:prstDash'), val='solid')
        # 순서 보정: lnL,lnR,lnT,lnB 가 맨 앞
        lns = [c for c in tcPr if c.tag in (qn('a:lnL'), qn('a:lnR'), qn('a:lnT'), qn('a:lnB'))]
        for c_ in lns:
            tcPr.remove(c_)
        for i, c_ in enumerate(lns):
            tcPr.insert(i, c_)

    def save(self, path):
        self.prs.save(path)
