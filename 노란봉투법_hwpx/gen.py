import json, re, zipfile, sys, html, copy
SRC='sample'; OUT=sys.argv[1]
d=json.load(open('shapes.json',encoding='utf-8'))
MM=36000  # EMU per mm
def mm(v): return int(round(v*MM))
def R(x,y,w,h,fill=None,line=None,lw=9525,paras=None,anchor='ctr',ins=(36000,0,36000,0),geom='rect',rot=0):
    return dict(geom=geom,x=mm(x),y=mm(y),w=mm(w),h=mm(h),rot=rot,fill=fill,line=line,lw=lw,paras=paras,anchor=anchor,ins=list(ins))
def P(*runs,algn='ctr'): return dict(algn=algn,lnsp=115000,runs=list(runs))
def T(t,sz=950,b=False,c='000359'): return dict(t=t,sz=sz,b=b,c=c)
# ---- K-water형 로드맵 타임라인(1쪽 shapes 7~16 대체) ----
tl=[]
events=[(47.2,'’25.11.~12.',['노란봉투법 시행령 입법예고','정부 해석지침(안) 배포'],'0080EA',False),
        (105.0,'’26.2.',['원·하청 상생','교섭절차 매뉴얼 배포'],'00B0B4',False),
        (162.8,'’26.3.10.',['노란봉투법 시행'],'0051BC',True)]
tl.append(R(17.5,49.2,13,5,paras=[P(T('START',1000,True,'0051BC'))],ins=(0,0,0,0)))
tl.append(R(31.5,50.9,159.5,1.8,fill='BDE0FF'))                      # 트랙
tl.append(R(187.5,49.9,3.6,3.8,geom='triangle',rot=90,fill='BDE0FF'))  # 끝 ▶
for cx,date,lines,c,last in events:
    tl.append(R(cx-26,37.2,52,8.6,fill='FFFFFF',line='BDE0FF',lw=9525,paras=[P(T(l,950)) for l in lines],ins=(18000,0,18000,0)))
    tl.append(R(cx-1.3,45.9,2.6,1.4,geom='triangle',rot=180,fill='BDE0FF'))
    tl.append(R(cx-2.1,49.7,4.2,4.2,geom='ellipse',fill=c if last else 'FFFFFF',line=c,lw=25400))
    tl.append(R(cx-22,54.5,44,4.6,paras=[P(T(date,1050,True,c))],ins=(0,0,0,0)))
drop=set(range(7,17))|{20,33}
pages=[d[0][:7]+tl+[x for i,x in enumerate(d[0]) if i>=17 and i not in drop], d[1]]
# ---- header ----
hdr=open(f'{SRC}/Contents/header.xml',encoding='utf-8').read()
hdr=hdr.replace('secCnt="3"','secCnt="1"')
nchar=int(re.search(r'<hh:charProperties itemCnt="(\d+)"',hdr).group(1))
npara=int(re.search(r'<hh:paraProperties itemCnt="(\d+)"',hdr).group(1))
chars={}; paras={}
def charid(sz,b,c):
    k=(sz or 1000,bool(b),(c or '000359').upper())
    if k not in chars: chars[k]=nchar+len(chars)
    return chars[k]
def paraid(algn,lnsp):
    k=({'ctr':'CENTER','r':'RIGHT','just':'JUSTIFY'}.get(algn,'LEFT'), int(round((lnsp or 100000)/1000*1.2)))
    if k not in paras: paras[k]=npara+len(paras)
    return paras[k]
def charxml(i,k):
    sz,b,c=k
    return (f'<hh:charPr id="{i}" height="{sz}" textColor="#{c}" shadeColor="none" useFontSpace="0" useKerning="0" symMark="NONE" borderFillIDRef="2">'
      '<hh:fontRef hangul="5" latin="5" hanja="5" japanese="5" other="4" symbol="4" user="4"/>'
      '<hh:ratio hangul="100" latin="100" hanja="100" japanese="100" other="100" symbol="100" user="100"/>'
      '<hh:spacing hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>'
      '<hh:relSz hangul="100" latin="100" hanja="100" japanese="100" other="100" symbol="100" user="100"/>'
      '<hh:offset hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>'
      + ('<hh:bold/>' if b else '') +
      '<hh:underline type="NONE" shape="SOLID" color="#000000"/><hh:strikeout shape="NONE" color="#000000"/><hh:outline type="NONE"/><hh:shadow type="NONE" color="#B2B2B2" offsetX="10" offsetY="10"/></hh:charPr>')
def paraxml(i,k):
    al,ls=k
    m='<hh:margin><hc:intent value="0" unit="HWPUNIT"/><hc:left value="0" unit="HWPUNIT"/><hc:right value="0" unit="HWPUNIT"/><hc:prev value="0" unit="HWPUNIT"/><hc:next value="0" unit="HWPUNIT"/></hh:margin>'
    sp=f'<hh:lineSpacing type="PERCENT" value="{ls}" unit="HWPUNIT"/>'
    return (f'<hh:paraPr id="{i}" tabPrIDRef="0" condense="0" fontLineHeight="0" snapToGrid="0" suppressLineNumbers="0" checked="0">'
      f'<hh:align horizontal="{al}" vertical="BASELINE"/><hh:heading type="NONE" idRef="0" level="0"/>'
      '<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="KEEP_WORD" widowOrphan="0" keepWithNext="0" keepLines="0" pageBreakBefore="0" lineWrap="BREAK"/>'
      '<hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
      f'<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">{m}{sp}</hp:case><hp:default>{m}{sp}</hp:default></hp:switch>'
      '<hh:border borderFillIDRef="2" offsetLeft="0" offsetRight="0" offsetTop="0" offsetBottom="0" connect="0" ignoreMargin="0"/></hh:paraPr>')
# ---- shapes ----
U=lambda e: int(round(e/127))
zo=[0]; sid=[1900000000]
def esc(t): return html.escape(t,quote=False)
def common_head(w,h,line,lw,fill,dash=None):
    s=(f'<hp:offset x="0" y="0"/><hp:orgSz width="{w}" height="{h}"/><hp:curSz width="{w}" height="{h}"/><hp:flip horizontal="0" vertical="0"/>'
       f'<hp:rotationInfo angle="0" centerX="{w//2}" centerY="{h//2}" rotateimage="1"/>'
       '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>')
    if line and line!='default':
        st='DASH' if dash in ('dash','sysDash','lgDash') else 'SOLID'
        s+=f'<hp:lineShape color="#{line}" width="{U(lw)}" style="{st}" endCap="FLAT" headStyle="NORMAL" tailStyle="NORMAL" headfill="1" tailfill="1" headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM" outlineStyle="NORMAL" alpha="0"/>'
    else:
        s+='<hp:lineShape color="#000000" width="0" style="NONE" endCap="FLAT" headStyle="NORMAL" tailStyle="NORMAL" headfill="1" tailfill="1" headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM" outlineStyle="NORMAL" alpha="0"/>'
    if fill and fill not in ('default',) and not str(fill).startswith('scheme'):
        s+=f'<hc:fillBrush><hc:winBrush faceColor="#{fill}" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
    s+='<hp:shadow type="NONE" color="#B2B2B2" offsetX="0" offsetY="0" alpha="0"/>'
    return s
def tail(x,y,w,h):
    return (f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
      f'<hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="0" allowOverlap="1" holdAnchorAndSO="0" vertRelTo="PAPER" horzRelTo="PAPER" vertAlign="TOP" horzAlign="LEFT" vertOffset="{y}" horzOffset="{x}"/>'
      '<hp:outMargin left="0" right="0" top="0" bottom="0"/>')
def objattrs(tag):
    zo[0]+=1; sid[0]+=1
    return f'<hp:{tag} id="{sid[0]}" zOrder="{zo[0]}" numberingType="PICTURE" textWrap="IN_FRONT_OF_TEXT" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{sid[0]-1000000000}"'
def drawtext(sh,w):
    ps=[]
    for p in sh['paras']:
        pid=paraid(p.get('algn'),p.get('lnsp'))
        runs=''; 
        for r in p['runs']:
            if r.get('br'): runs+='<hp:run charPrIDRef="%d"><hp:lineBreak/></hp:run>'%charid(1000,False,None); continue
            if not r.get('t'): continue
            runs+=f'<hp:run charPrIDRef="{charid(r.get("sz") or p.get("esz") or 1000,r.get("b"),r.get("c"))}"><hp:t>{esc(r["t"])}</hp:t></hp:run>'
        if not runs: runs=f'<hp:run charPrIDRef="{charid(p.get("esz") or 1000,False,None)}"/>'
        ps.append(f'<hp:p id="0" paraPrIDRef="{pid}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">{runs}</hp:p>')
    va={'t':'TOP','b':'BOTTOM'}.get(sh.get('anchor'),'CENTER')
    l,t,r,b=[U(v) for v in (sh.get('ins') or [91440,45720,91440,45720])]
    return (f'<hp:drawText lastWidth="{w}" name="" editable="0"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{va}" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">'
            + ''.join(ps) + f'</hp:subList><hp:textMargin left="{l}" right="{r}" top="{t}" bottom="{b}"/></hp:drawText>')
def poly(pts,sh,x,y,w,h):
    s=objattrs('polygon')+'>'+common_head(w,h,sh.get('line'),sh.get('lw',12700),sh.get('fill'))
    s+=''.join(f'<hc:pt x="{int(px)}" y="{int(py)}"/>' for px,py in pts)
    return s+tail(x,y,w,h)+'<hp:shapeComment>다각형입니다.</hp:shapeComment></hp:polygon>'
def shape(sh):
    g=sh['geom']; x,y,w,h=U(sh['x']),U(sh['y']),max(U(sh['w']),1),U(sh['h']); rot=round(sh.get('rot') or 0)
    if g=='straightConnector1':
        s=objattrs('line')+' isReverseHV="0">'+common_head(w,max(h,1),sh.get('line'),sh.get('lw',12700),None,sh.get('dash'))
        s+=f'<hc:startPt x="0" y="0"/><hc:endPt x="{w}" y="{h}"/>'
        return s+tail(x,y,w,max(h,1))+'<hp:shapeComment>선입니다.</hp:shapeComment></hp:line>'
    if g=='ellipse':
        s=objattrs('ellipse')+' intervalDirty="0" hasArcPr="0" arcType="NORMAL">'+common_head(w,h,sh.get('line'),sh.get('lw',12700),sh.get('fill'))
        s+=f'<hc:center x="{w//2}" y="{h//2}"/><hc:ax1 x="{w}" y="{h//2}"/><hc:ax2 x="{w//2}" y="{h}"/><hc:start1 x="{w}" y="{h//2}"/><hc:end1 x="{w}" y="{h//2}"/><hc:start2 x="{w}" y="{h//2}"/><hc:end2 x="{w}" y="{h//2}"/>'
        return s+tail(x,y,w,h)+'<hp:shapeComment>타원입니다.</hp:shapeComment></hp:ellipse>'
    if g in ('triangle','rtTriangle'):
        if rot in (90,270):
            cx,cy=x+w/2,y+h/2; x,y,w,h=int(cx-h/2),int(cy-w/2),h,w
        if g=='triangle':
            pts={0:[(w/2,0),(w,h),(0,h)],180:[(0,0),(w,0),(w/2,h)],90:[(0,0),(w,h/2),(0,h)],270:[(w,0),(0,h/2),(w,h)]}[rot]
        else:
            pts={0:[(0,0),(0,h),(w,h)],180:[(w,h),(w,0),(0,0)]}.get(rot,[(0,0),(0,h),(w,h)])
        return poly(pts+[pts[0]],sh,x,y,w,h)
    if g=='mathPlus':
        m=min(w,h); a=m*0.2352/2; ex=w*0.7349/2; ey=h*0.7349/2; cx,cy=w/2,h/2
        pts=[(cx-a,cy-ey),(cx+a,cy-ey),(cx+a,cy-a),(cx+ex,cy-a),(cx+ex,cy+a),(cx+a,cy+a),(cx+a,cy+ey),(cx-a,cy+ey),(cx-a,cy+a),(cx-ex,cy+a),(cx-ex,cy-a),(cx-a,cy-a),(cx-a,cy-ey)]
        return poly(pts,sh,x,y,w,h)
    # rect
    s=objattrs('rect')+' ratio="0">'+common_head(w,h,sh.get('line'),sh.get('lw',12700),sh.get('fill'))
    if sh.get('paras'): s+=drawtext(sh,w)
    s+=f'<hc:pt0 x="0" y="0"/><hc:pt1 x="{w}" y="0"/><hc:pt2 x="{w}" y="{h}"/><hc:pt3 x="0" y="{h}"/>'
    return s+tail(x,y,w,h)+'<hp:shapeComment>사각형입니다.</hp:shapeComment></hp:rect>'
sec=open(f'{SRC}/Contents/section0.xml',encoding='utf-8').read()
root_open=sec[:sec.find('<hp:p ')]
secpr=re.search(r'<hp:secPr .*?</hp:secPr>',sec,re.S).group(0)
secpr=re.sub(r'<hp:margin header="\d+" footer="\d+" gutter="\d+" left="\d+" right="\d+" top="\d+" bottom="\d+"/>','<hp:margin header="0" footer="0" gutter="0" left="5669" right="5669" top="5669" bottom="5669"/>',secpr)
secpr=secpr.replace('borderFillIDRef="14"','borderFillIDRef="1"')
colpr='<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" sameSz="1" sameGap="0"/></hp:ctrl>'
body=[]
for pi,shs in enumerate(pages):
    objs=''.join(f'<hp:run charPrIDRef="{charid(1000,False,None)}">{shape(s)}</hp:run>' for s in shs)
    pid=paraid('l',100000)
    if pi==0:
        body.append(f'<hp:p id="0" paraPrIDRef="{pid}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{charid(1000,False,None)}">{secpr}{colpr}</hp:run>{objs}</hp:p>')
    else:
        body.append(f'<hp:p id="0" paraPrIDRef="{pid}" styleIDRef="0" pageBreak="1" columnBreak="0" merged="0">{objs}</hp:p>')
section=root_open+''.join(body)+'</hs:sec>'
# header append
cx=''.join(charxml(i,k) for k,i in sorted(chars.items(),key=lambda kv:kv[1]))
px=''.join(paraxml(i,k) for k,i in sorted(paras.items(),key=lambda kv:kv[1]))
hdr=re.sub(r'<hh:charProperties itemCnt="\d+">',f'<hh:charProperties itemCnt="{nchar+len(chars)}">',hdr).replace('</hh:charProperties>',cx+'</hh:charProperties>')
hdr=re.sub(r'<hh:paraProperties itemCnt="\d+">',f'<hh:paraProperties itemCnt="{npara+len(paras)}">',hdr).replace('</hh:paraProperties>',px+'</hh:paraProperties>')
hpf=open(f'{SRC}/Contents/content.hpf',encoding='utf-8').read()
hpf=re.sub(r'<opf:item id="image\d+"[^>]*/>','',hpf)
hpf=re.sub(r'<opf:title>.*?</opf:title>','<opf:title>노란봉투법 시행 대응, 원·하청 교섭 즉시대응 체계 완성</opf:title>',hpf)
hpf=re.sub(r'(<opf:meta name="creator" content="[^"]*">).*?(</opf:meta>)',r'\1한국원자력환경공단\2',hpf)
st=open(f'{SRC}/settings.xml',encoding='utf-8').read().replace('listIDRef="7"','listIDRef="0"').replace('pos="3"','pos="0"')
prv='노란봉투법 시행 대응, 원·하청 교섭 즉시대응 체계 완성\r\n가. 그간의 노력(선제적 대응기반 구축)과 시사점 도출\r\n'
with zipfile.ZipFile(OUT,'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'),open(f'{SRC}/mimetype','rb').read(),compress_type=zipfile.ZIP_STORED)
    for n,data in [('version.xml',open(f'{SRC}/version.xml','rb').read()),('Contents/header.xml',hdr.encode()),('Contents/section0.xml',section.encode()),
                   ('Contents/content.hpf',hpf.encode()),('settings.xml',st.encode()),('META-INF/container.xml',open(f'{SRC}/META-INF/container.xml','rb').read()),
                   ('META-INF/container.rdf',open(f'{SRC}/META-INF/container.rdf','rb').read()),('META-INF/manifest.xml',open(f'{SRC}/META-INF/manifest.xml','rb').read()),
                   ('Preview/PrvText.txt',prv.encode()),
                   ('Preview/PrvImage.png',open(sys.argv[2],'rb').read())]:
        z.writestr(n,data,compress_type=zipfile.ZIP_DEFLATED)
print('shapes',[len(p) for p in pages],'chars',len(chars),'paras',len(paras))
