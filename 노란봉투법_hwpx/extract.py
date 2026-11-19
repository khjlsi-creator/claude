import json,sys
from pptx import Presentation
from pptx.enum.dml import MSO_FILL
from lxml import etree
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
def col(el):
    if el is None: return None
    s=el.find('a:srgbClr',ns)
    if s is not None: return s.get('val')
    s=el.find('a:schemeClr',ns)
    if s is not None: return 'scheme:'+s.get('val')
    return None
p=Presentation(sys.argv[1]); out=[]
for si,s in enumerate(p.slides):
    items=[]
    for sh in s.shapes:
        e=sh._element; sp=e.find('.//p:spPr',ns)
        d=dict(kind=str(sh.shape_type),geom=None,x=sh.left,y=sh.top,w=sh.width,h=sh.height,rot=getattr(sh,'rotation',0))
        xf=sp.find('a:xfrm',ns) if sp is not None else None
        if xf is not None: d['flipH']=xf.get('flipH')=='1'; d['flipV']=xf.get('flipV')=='1'
        pg=sp.find('a:prstGeom',ns) if sp is not None else None
        d['geom']=pg.get('prst') if pg is not None else None
        sf=sp.find('a:solidFill',ns) if sp is not None else None
        d['fill']=col(sf) if sf is not None else (None if sp is None or sp.find('a:noFill',ns) is not None else 'default')
        ln=sp.find('a:ln',ns) if sp is not None else None
        if ln is not None:
            d['lw']=int(ln.get('w',12700))
            if ln.find('a:noFill',ns) is not None: d['line']=None
            else: d['line']=col(ln.find('a:solidFill',ns))
            d['tail']=ln.find('a:tailEnd',ns).get('type') if ln.find('a:tailEnd',ns) is not None else None
            d['head']=ln.find('a:headEnd',ns).get('type') if ln.find('a:headEnd',ns) is not None else None
            d['dash']=ln.find('a:prstDash',ns).get('val') if ln.find('a:prstDash',ns) is not None else None
        else: d['line']='default'
        bp=e.find('.//p:txBody/a:bodyPr',ns)
        if bp is not None:
            d['ins']=[int(bp.get(k,dv)) for k,dv in (('lIns',91440),('tIns',45720),('rIns',91440),('bIns',45720))]
            d['anchor']=bp.get('anchor','t'); d['wrap']=bp.get('wrap')
        paras=[]
        for ap in e.findall('.//p:txBody/a:p',ns):
            ppr=ap.find('a:pPr',ns); algn=ppr.get('algn') if ppr is not None else None
            lnsp=None
            if ppr is not None and ppr.find('a:lnSpc/a:spcPct',ns) is not None: lnsp=int(ppr.find('a:lnSpc/a:spcPct',ns).get('val'))
            runs=[]
            for r in ap:
                tag=etree.QName(r).localname
                if tag=='r':
                    rp=r.find('a:rPr',ns); t=r.find('a:t',ns).text or ''
                    rr=dict(t=t)
                    if rp is not None:
                        rr['sz']=int(rp.get('sz')) if rp.get('sz') else None; rr['b']=rp.get('b')=='1'
                        rr['c']=col(rp.find('a:solidFill',ns)); rr['base']=rp.get('baseline')
                        f=rp.find('a:latin',ns); rr['font']=f.get('typeface') if f is not None else None
                        hl=rp.find('a:highlight',ns); rr['hl']=col(hl) if hl is not None else None
                    runs.append(rr)
                elif tag=='br': runs.append(dict(br=True))
            ep=ap.find('a:endParaRPr',ns)
            paras.append(dict(algn=algn,lnsp=lnsp,runs=runs,esz=int(ep.get('sz')) if ep is not None and ep.get('sz') else None))
        if any(r.get('t') for pp in paras for r in pp['runs']): d['paras']=paras
        items.append(d)
    out.append(items)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter((i.get('fill'),) for sl in out for i in sl).most_common(30))
print(collections.Counter(r.get('font') for sl in out for i in sl for pp in i.get('paras',[]) for r in pp['runs']))
print(collections.Counter(r.get('sz') for sl in out for i in sl for pp in i.get('paras',[]) for r in pp['runs']))
print([ (i['geom'],i['rot'],i.get('flipH'),i.get('flipV')) for sl in out for i in sl if i['geom']!='rect'])
