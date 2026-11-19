import json, re, zipfile, html, sys
SRC='yb/sample'
MM=283.465  # HWPUNIT per mm
def esc(t): return html.escape(t,quote=False)
class Doc:
    def __init__(s):
        s.hdr=open(f'{SRC}/Contents/header.xml',encoding='utf-8').read().replace('secCnt="3"','secCnt="1"')
        s.nchar=int(re.search(r'<hh:charProperties itemCnt="(\d+)"',s.hdr).group(1))
        s.npara=int(re.search(r'<hh:paraProperties itemCnt="(\d+)"',s.hdr).group(1))
        s.chars={}; s.paras={}; s.zo=0; s.sid=1900000000
    def charid(s,sz,b,c,sp=0):
        k=(int(round(sz)),bool(b),(c or '000359').upper(),int(sp))
        if k not in s.chars: s.chars[k]=s.nchar+len(s.chars)
        return s.chars[k]
    def paraid(s,al,ls):
        k=({'center':'CENTER','right':'RIGHT','justify':'JUSTIFY'}.get(al,'LEFT'),int(round(ls)))
        if k not in s.paras: s.paras[k]=s.npara+len(s.paras)
        return s.paras[k]
    def head(s,w,h,line,lw,fill):
        r=(f'<hp:offset x="0" y="0"/><hp:orgSz width="{w}" height="{h}"/><hp:curSz width="{w}" height="{h}"/><hp:flip horizontal="0" vertical="0"/>'
           f'<hp:rotationInfo angle="0" centerX="{w//2}" centerY="{h//2}" rotateimage="1"/>'
           '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>')
        st='SOLID' if line else 'NONE'
        r+=f'<hp:lineShape color="#{line or "000000"}" width="{int(lw) if line else 0}" style="{st}" endCap="FLAT" headStyle="NORMAL" tailStyle="NORMAL" headfill="1" tailfill="1" headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM" outlineStyle="NORMAL" alpha="0"/>'
        if fill: r+=f'<hc:fillBrush><hc:winBrush faceColor="#{fill}" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
        return r+'<hp:shadow type="NONE" color="#B2B2B2" offsetX="0" offsetY="0" alpha="0"/>'
    def tail(s,x,y,w,h):
        return (f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
          f'<hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="0" allowOverlap="1" holdAnchorAndSO="0" vertRelTo="PAPER" horzRelTo="PAPER" vertAlign="TOP" horzAlign="LEFT" vertOffset="{y}" horzOffset="{x}"/>'
          '<hp:outMargin left="0" right="0" top="0" bottom="0"/>')
    def attrs(s,tag):
        s.zo+=1; s.sid+=1
        return f'<hp:{tag} id="{s.sid}" zOrder="{s.zo}" numberingType="PICTURE" textWrap="IN_FRONT_OF_TEXT" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{s.sid-1000000000}"'
    def shape(s,sh):
        x,y,w,h=[int(round(v)) for v in (sh['x'],sh['y'],sh['w'],sh['h'])]; w=max(w,1); h=max(h,1)
        if sh['geom']=='poly':
            r=s.attrs('polygon')+'>'+s.head(w,h,None,0,sh.get('fill'))
            r+=''.join(f'<hc:pt x="{int(px)}" y="{int(py)}"/>' for px,py in sh['pts']+[sh['pts'][0]])
            return r+s.tail(x,y,w,h)+'<hp:shapeComment>다각형입니다.</hp:shapeComment></hp:polygon>'
        if sh['geom']=='ellipse':
            r=s.attrs('ellipse')+' intervalDirty="0" hasArcPr="0" arcType="NORMAL">'+s.head(w,h,sh.get('line'),sh.get('lw',0),sh.get('fill'))
            r+=f'<hc:center x="{w//2}" y="{h//2}"/><hc:ax1 x="{w}" y="{h//2}"/><hc:ax2 x="{w//2}" y="{h}"/><hc:start1 x="{w}" y="{h//2}"/><hc:end1 x="{w}" y="{h//2}"/><hc:start2 x="{w}" y="{h//2}"/><hc:end2 x="{w}" y="{h//2}"/>'
            return r+s.tail(x,y,w,h)+'<hp:shapeComment>타원입니다.</hp:shapeComment></hp:ellipse>'
        r=s.attrs('rect')+f' ratio="{int(sh.get("ratio",0))}">'+s.head(w,h,sh.get('line'),sh.get('lw',0),sh.get('fill'))
        if sh.get('paras'):
            ps=[]
            for p in sh['paras']:
                pid=s.paraid(p.get('al'),p.get('ls',130)); runs=''
                for rr in p['runs']:
                    if not rr['t']: continue
                    runs+=f'<hp:run charPrIDRef="{s.charid(rr["sz"],rr.get("b"),rr.get("c"),rr.get("sp",0))}"><hp:t>{esc(rr["t"])}</hp:t></hp:run>'
                if not runs: runs=f'<hp:run charPrIDRef="{s.charid(1000,False,None)}"/>'
                ps.append(f'<hp:p id="0" paraPrIDRef="{pid}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">{runs}</hp:p>')
            va={'t':'TOP','b':'BOTTOM'}.get(sh.get('anchor'),'CENTER')
            l,t,rt,b=sh.get('ins',(0,0,0,0))
            r+=(f'<hp:drawText lastWidth="{w}" name="" editable="0"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{va}" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
                +''.join(ps)+f'</hp:subList><hp:textMargin left="{l}" right="{rt}" top="{t}" bottom="{b}"/></hp:drawText>')
        r+=f'<hc:pt0 x="0" y="0"/><hc:pt1 x="{w}" y="0"/><hc:pt2 x="{w}" y="{h}"/><hc:pt3 x="0" y="{h}"/>'
        return r+s.tail(x,y,w,h)+'<hp:shapeComment>사각형입니다.</hp:shapeComment></hp:rect>'
    def charxml(s,i,k):
        sz,b,c,sp=k; spx=' '.join(f'{l}="{sp}"' for l in ('hangul','latin','hanja','japanese','other','symbol','user'))
        return (f'<hh:charPr id="{i}" height="{sz}" textColor="#{c}" shadeColor="none" useFontSpace="0" useKerning="0" symMark="NONE" borderFillIDRef="2">'
          '<hh:fontRef hangul="5" latin="5" hanja="5" japanese="5" other="4" symbol="4" user="4"/>'
          '<hh:ratio hangul="100" latin="100" hanja="100" japanese="100" other="100" symbol="100" user="100"/>'
          f'<hh:spacing {spx}/>'
          '<hh:relSz hangul="100" latin="100" hanja="100" japanese="100" other="100" symbol="100" user="100"/>'
          '<hh:offset hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>'
          +('<hh:bold/>' if b else '')+
          '<hh:underline type="NONE" shape="SOLID" color="#000000"/><hh:strikeout shape="NONE" color="#000000"/><hh:outline type="NONE"/><hh:shadow type="NONE" color="#B2B2B2" offsetX="10" offsetY="10"/></hh:charPr>')
    def paraxml(s,i,k):
        al,ls=k
        m='<hh:margin><hc:intent value="0" unit="HWPUNIT"/><hc:left value="0" unit="HWPUNIT"/><hc:right value="0" unit="HWPUNIT"/><hc:prev value="0" unit="HWPUNIT"/><hc:next value="0" unit="HWPUNIT"/></hh:margin>'
        sp=f'<hh:lineSpacing type="PERCENT" value="{ls}" unit="HWPUNIT"/>'
        return (f'<hh:paraPr id="{i}" tabPrIDRef="0" condense="0" fontLineHeight="0" snapToGrid="0" suppressLineNumbers="0" checked="0">'
          f'<hh:align horizontal="{al}" vertical="BASELINE"/><hh:heading type="NONE" idRef="0" level="0"/>'
          '<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="KEEP_WORD" widowOrphan="0" keepWithNext="0" keepLines="0" pageBreakBefore="0" lineWrap="BREAK"/>'
          '<hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
          f'<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">{m}{sp}</hp:case><hp:default>{m}{sp}</hp:default></hp:switch>'
          '<hh:border borderFillIDRef="2" offsetLeft="0" offsetRight="0" offsetTop="0" offsetBottom="0" connect="0" ignoreMargin="0"/></hh:paraPr>')
    def build(s,pages,out,title,prv_png,prv_text):
        sec=open(f'{SRC}/Contents/section0.xml',encoding='utf-8').read()
        root_open=sec[:sec.find('<hp:p ')]
        secpr=re.search(r'<hp:secPr .*?</hp:secPr>',sec,re.S).group(0)
        secpr=re.sub(r'<hp:margin header="\d+" footer="\d+" gutter="\d+" left="\d+" right="\d+" top="\d+" bottom="\d+"/>','<hp:margin header="0" footer="0" gutter="0" left="5669" right="5669" top="5669" bottom="5669"/>',secpr).replace('borderFillIDRef="14"','borderFillIDRef="1"')
        colpr='<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" sameSz="1" sameGap="0"/></hp:ctrl>'
        body=[]; base=s.charid(1000,False,None)
        for pi,shs in enumerate(pages):
            objs=''.join(f'<hp:run charPrIDRef="{base}">{s.shape(x)}</hp:run>' for x in shs)
            pid=s.paraid('left',100)
            if pi==0: body.append(f'<hp:p id="0" paraPrIDRef="{pid}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{base}">{secpr}{colpr}</hp:run>{objs}</hp:p>')
            else: body.append(f'<hp:p id="0" paraPrIDRef="{pid}" styleIDRef="0" pageBreak="1" columnBreak="0" merged="0">{objs}</hp:p>')
        section=root_open+''.join(body)+'</hs:sec>'
        hdr=s.hdr
        cx=''.join(s.charxml(i,k) for k,i in sorted(s.chars.items(),key=lambda kv:kv[1]))
        px=''.join(s.paraxml(i,k) for k,i in sorted(s.paras.items(),key=lambda kv:kv[1]))
        hdr=re.sub(r'<hh:charProperties itemCnt="\d+">',f'<hh:charProperties itemCnt="{s.nchar+len(s.chars)}">',hdr).replace('</hh:charProperties>',cx+'</hh:charProperties>')
        hdr=re.sub(r'<hh:paraProperties itemCnt="\d+">',f'<hh:paraProperties itemCnt="{s.npara+len(s.paras)}">',hdr).replace('</hh:paraProperties>',px+'</hh:paraProperties>')
        hpf=open(f'{SRC}/Contents/content.hpf',encoding='utf-8').read()
        hpf=re.sub(r'<opf:item id="image\d+"[^>]*/>','',hpf)
        hpf=re.sub(r'<opf:title>.*?</opf:title>',f'<opf:title>{esc(title)}</opf:title>',hpf)
        hpf=re.sub(r'(<opf:meta name="creator" content="[^"]*">).*?(</opf:meta>)',r'\1한국원자력환경공단\2',hpf)
        st=open(f'{SRC}/settings.xml',encoding='utf-8').read().replace('listIDRef="7"','listIDRef="0"').replace('pos="3"','pos="0"')
        with zipfile.ZipFile(out,'w') as z:
            z.writestr(zipfile.ZipInfo('mimetype'),open(f'{SRC}/mimetype','rb').read(),compress_type=zipfile.ZIP_STORED)
            for n,data in [('version.xml',open(f'{SRC}/version.xml','rb').read()),('Contents/header.xml',hdr.encode()),('Contents/section0.xml',section.encode()),
                ('Contents/content.hpf',hpf.encode()),('settings.xml',st.encode()),('META-INF/container.xml',open(f'{SRC}/META-INF/container.xml','rb').read()),
                ('META-INF/container.rdf',open(f'{SRC}/META-INF/container.rdf','rb').read()),('META-INF/manifest.xml',open(f'{SRC}/META-INF/manifest.xml','rb').read()),
                ('Preview/PrvText.txt',prv_text.encode()),('Preview/PrvImage.png',open(prv_png,'rb').read())]:
                z.writestr(n,data,compress_type=zipfile.ZIP_DEFLATED)

def from_extract(js, s_mm, ox, oy):
    """convert extract.js items (px) to shapes in HWPUNIT. s_mm = mm per px; ox,oy page offset mm."""
    d=json.load(open(js,encoding='utf-8')); out=[]
    U=lambda v: v*s_mm*MM
    pt_per_px=s_mm/0.352778
    for it in d['items']:
        x,y,w,h=ox*MM+U(it['x']),oy*MM+U(it['y']),U(it['w']),U(it['h'])
        if it['k']=='poly':
            out.append(dict(geom='poly',x=x,y=y,w=w,h=h,fill=it['fill'],pts=[(U(a),U(b)) for a,b in it['pts']])); continue
        if it['k']=='moon':
            import math
            pct={5:1.0,4:0.75,3:0.5,2:0.25,1:0.0}[it['level']]
            out.append(dict(geom='ellipse',x=x,y=y,w=w,h=h,fill='FFFFFF' if pct<1 else it['c'],line=None,lw=0))
            if 0<pct<1:
                cx,cy,r=w/2,h/2,min(w,h)/2; pts=[(cx,cy)]
                n=max(2,int(pct*36))
                for i in range(n+1):
                    a=-math.pi/2+2*math.pi*pct*i/n; pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
                out.append(dict(geom='poly',x=x,y=y,w=w,h=h,fill=it['c'],pts=pts))
            out.append(dict(geom='ellipse',x=x,y=y,w=w,h=h,fill=None,line=it['c'],lw=U(it['lw'])))
            continue
        if it['k']=='rect':
            out.append(dict(geom='rect',x=x,y=y,w=w,h=h,fill=it.get('fill'),line=it.get('line'),lw=U(it.get('lw',0)),ratio=it.get('ratio',0))); continue
        paras=[]
        for pa in it['paras']:
            runs=[dict(t=r['t'],sz=r['sz']*pt_per_px*100,b=r['b'],c=r['c'],sp=max(-30,min(30,round(100*r.get('ls',0)/r['sz'])))) for r in pa]
            paras.append(dict(al=it['al'],ls=it['lh']*100,runs=runs))
        # slight width slack so Hangul word wrap does not differ from browser
        out.append(dict(geom='rect',x=x-U(2),y=y,w=w+U(4),h=h,paras=paras,anchor=it['anchor'],ins=(0,0,0,0)))
    return out
