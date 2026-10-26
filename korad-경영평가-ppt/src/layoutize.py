# -*- coding: utf-8 -*-
"""조합한 쪽을 진짜 PowerPoint 슬라이드 레이아웃으로 바꾼다.
- 글이 들어가는 칸 → 레이아웃의 자리표시자(placeholder). 슬라이드에서 칸을 눌러 바로 입력한다.
- 틀(레일·머리칸·테두리·삼각형·사진 칸 테두리) → 레이아웃의 고정 도형. 슬라이드에서 실수로 움직이지 않는다.
- 표(실적표·인라인 표)는 슬라이드에 편집 가능한 표로 남긴다.
"""
import copy
from lxml import etree
from pptx.oxml.ns import qn
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.parts.slide import SlideLayoutPart

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def _text(sp):
    return ''.join(t.text or '' for t in sp.iter(qn('a:t')))


def _max_id(tree):
    return max([int(e.get('id')) for e in tree.iter(qn('p:cNvPr')) if e.get('id', '').isdigit()] + [1])


def _clone_layout(prs, base, name):
    master = prs.slide_master
    part = base.part
    pkg = part.package
    import re
    from pptx.opc.packuri import PackURI
    nums = [int(re.search(r'(\d+)\.xml$', str(l.part.partname)).group(1)) for l in prs.slide_layouts]
    partname = PackURI('/ppt/slideLayouts/slideLayout%d.xml' % (max(nums) + 1))
    el = copy.deepcopy(base._element)
    new = SlideLayoutPart(partname, part.content_type, pkg, el)
    new.relate_to(master.part, RT.SLIDE_MASTER)
    # 그림 관계 복제
    rmap = {}
    for rid, rel in part.rels.items():
        if rel.reltype == RT.IMAGE:
            rmap[rid] = new.relate_to(rel.target_part, RT.IMAGE)
    for e in el.iter():
        for att in (f'{{{R_NS}}}embed', f'{{{R_NS}}}link'):
            if e.get(att) in rmap:
                e.set(att, rmap[e.get(att)])
    el.cSld.set('name', name)
    rid = master.part.relate_to(new, RT.SLIDE_LAYOUT)
    lst = master._element.find(qn('p:sldLayoutIdLst'))
    nid = max(int(x.get('id')) for x in lst) + 1
    sid = etree.SubElement(lst, qn('p:sldLayoutId')); sid.set('id', str(nid)); sid.set(f'{{{R_NS}}}id', rid)
    return new


def _lst_style(sp):
    """첫 문단의 글자·문단 모양을 레이아웃 자리표시자의 lstStyle로 옮긴다(새로 입력해도 같은 모양)."""
    p = sp.find('.//' + qn('a:p'))
    lvl = etree.Element(qn('a:lvl1pPr'))
    ppr = p.find(qn('a:pPr')) if p is not None else None
    if ppr is not None:
        for k, v in ppr.attrib.items():
            lvl.set(k, v)
        for ch in ppr:
            lvl.append(copy.deepcopy(ch))
    r = p.find(qn('a:r')) if p is not None else None
    if r is not None and r.find(qn('a:rPr')) is not None:
        rp = copy.deepcopy(r.find(qn('a:rPr')))
        rp.tag = qn('a:defRPr')
        for att in ('lang', 'dirty'):
            if att in rp.attrib: del rp.attrib[att]
        lvl.append(rp)
    lst = etree.Element(qn('a:lstStyle')); lst.append(lvl)
    return lst


def layoutize_slide(prs, slide, name):
    """slide 하나를 새 레이아웃(name)과 자리표시자 슬라이드로 바꾼다."""
    base = slide.slide_layout
    new = _clone_layout(prs, base, name)
    ltree = new._element.cSld.spTree
    stree = slide.shapes._spTree
    nid = _max_id(ltree) + 1
    idx = 20
    pic_map = {}
    for sp in list(stree):
        tag = sp.tag
        if tag in (qn('p:nvGrpSpPr'), qn('p:grpSpPr')):
            continue
        if tag == qn('p:graphicFrame'):
            continue                                   # 표는 슬라이드에 그대로
        if tag == qn('p:sp') and sp.find('.//' + qn('p:ph')) is not None:
            continue                                   # 머리글·쪽번호 자리표시자는 이미 연결됨
        if tag == qn('p:pic'):
            emb = sp.find('.//' + qn('a:blip')).get(f'{{{R_NS}}}embed')
            part = slide.part.related_part(emb)
            _, rid = new.get_or_add_image_part(part.blob and __import__('io').BytesIO(part.blob)) if False else (None, None)
            rid = new.relate_to(part, RT.IMAGE)
            e = copy.deepcopy(sp)
            e.find('.//' + qn('a:blip')).set(f'{{{R_NS}}}embed', rid)
            e.find('.//' + qn('p:cNvPr')).set('id', str(nid)); nid += 1
            ltree.append(e); stree.remove(sp)
            continue
        txt = _text(sp) if tag == qn('p:sp') else ''
        if tag == qn('p:sp') and txt.strip():
            # 1) 고정 틀: 글을 뺀 복사본(채움·선이 있을 때만)
            spPr = sp.find(qn('p:spPr'))
            has_vis = spPr is not None and (spPr.find(qn('a:solidFill')) is not None or spPr.find(qn('a:pattFill')) is not None or spPr.find(qn('a:gradFill')) is not None
                                             or (spPr.find(qn('a:ln')) is not None and spPr.find(qn('a:ln')).find(qn('a:noFill')) is None))
            if has_vis:
                frame = copy.deepcopy(sp)
                tb = frame.find(qn('p:txBody'))
                if tb is not None:
                    for p_ in tb.findall(qn('a:p')): tb.remove(p_)
                    etree.SubElement(tb, qn('a:p'))
                frame.find('.//' + qn('p:cNvPr')).set('id', str(nid)); nid += 1
                ltree.append(frame)
            # 2) 자리표시자(투명): 레이아웃 + 슬라이드
            for which in ('layout', 'slide'):
                e = copy.deepcopy(sp)
                cnv = e.find(qn('p:nvSpPr')).find(qn('p:cNvSpPr'))
                for ch in list(cnv): cnv.remove(ch)
                for att in list(cnv.attrib): del cnv.attrib[att]
                etree.SubElement(cnv, qn('a:spLocks')).set('noGrp', '1')
                nvpr = e.find(qn('p:nvSpPr')).find(qn('p:nvPr'))
                for ch in list(nvpr): nvpr.remove(ch)
                ph = etree.SubElement(nvpr, qn('p:ph')); ph.set('type', 'body'); ph.set('sz', 'quarter'); ph.set('idx', str(idx))
                sppr = e.find(qn('p:spPr'))
                if which == 'layout':
                    for ch in list(sppr):
                        if ch.tag in (qn('a:solidFill'), qn('a:pattFill'), qn('a:gradFill'), qn('a:ln'), qn('a:noFill')): sppr.remove(ch)
                    etree.SubElement(sppr, qn('a:noFill')); ln = etree.SubElement(sppr, qn('a:ln')); etree.SubElement(ln, qn('a:noFill'))
                    tb = e.find(qn('p:txBody'))
                    old = tb.find(qn('a:lstStyle'))
                    lst = _lst_style(e)
                    if old is not None: tb.replace(old, lst)
                    else: tb.insert(1, lst)
                    e.find('.//' + qn('p:cNvPr')).set('id', str(nid)); nid += 1
                    ltree.append(e)
                else:
                    for ch in list(sppr): sppr.remove(ch)          # 위치·모양은 레이아웃에서 상속
                    tb = e.find(qn('p:txBody'))
                    bp = tb.find(qn('a:bodyPr'))
                    for ch in list(bp): bp.remove(ch)
                    for att in list(bp.attrib): del bp.attrib[att]
                    ls = tb.find(qn('a:lstStyle'))
                    if ls is not None:
                        for ch in list(ls): ls.remove(ch)
                    stree.replace(sp, e)
            idx += 1
            continue
        # 글 없는 도형·선·다각형 → 고정 틀
        e = copy.deepcopy(sp)
        for c in e.iter(qn('p:cNvPr')):
            c.set('id', str(nid)); nid += 1
            break
        ltree.append(e); stree.remove(sp)
    # 슬라이드의 레이아웃 연결 교체
    for rel in slide.part.rels.values():
        if rel.reltype == RT.SLIDE_LAYOUT:
            rel._target = new
            for k in ('target_part', 'target_partname', 'target_ref'):
                rel.__dict__.pop(k, None)
    return new


def drop_slides(prs):
    lst = prs.slides._sldIdLst
    for sid in list(lst):
        prs.part.drop_rel(sid.get(f'{{{R_NS}}}id'))
        lst.remove(sid)
