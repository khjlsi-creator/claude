import re, zipfile, sys
sys.path.insert(0,'conv')
import hwpxbuild as hb
GRAY={  # KORAD palette -> 한글 원본 회색조
 '002060':'595959','0051BC':'595959','0080EA':'666666','00B0B4':'666666','008C6B':'595959','30C2FF':'999999','0061DE':'595959','0A6BE6':'666666',
 'DEEEFF':'EEEEEE','BDE0FF':'D4D4D4','EFF9FF':'F2F2F2','E6FCF9':'F2F2F2','F4F6FA':'F7F7F7','E6F4FF':'EEEEEE','E6F6F6':'EEEEEE','DEE6F6':'D9D9D9','F4F9FF':'F2F2F2',
 '008EFF':'999999','8D9CBF':'999999','00BE83':'666666','5D7280':'666666','29FFBD':'D9D9D9'}
TXT={'000359':'000000','0051BC':'000000','0080EA':'333333','008C6B':'000000','002060':'000000','3B4951':'333333','5D7280':'555555','00585A':'000000','BDE0FF':'FFFFFF','DEEEFF':'FFFFFF','29FFBD':'FFFFFF'}
def recolor(shapes):
    for sh in shapes:
        for k in ('fill','line'):
            v=sh.get(k)
            if v: sh[k]=GRAY.get(v.upper(),v)
        for p in sh.get('paras',[]):
            for r in p['runs']:
                if r.get('c'): r['c']=TXT.get(r['c'].upper(),r['c'])
    return shapes
class TDoc(hb.Doc):
    def __init__(s,tpl,bold_font=8,reg_font=9):
        s.tpl=tpl; s.bf=bold_font; s.rf=reg_font
        s.z=zipfile.ZipFile(tpl)
        s.hdr=s.z.read('Contents/header.xml').decode('utf-8')
        s.nchar=int(re.search(r'<hh:charProperties itemCnt="(\d+)"',s.hdr).group(1))
        s.npara=int(re.search(r'<hh:paraProperties itemCnt="(\d+)"',s.hdr).group(1))
        s.chars={}; s.paras={}; s.zo=0; s.sid=1900000000
    def charxml(s,i,k):
        x=hb.Doc.charxml(s,i,k)
        f=s.bf if k[1] else s.rf
        return re.sub(r'<hh:fontRef [^/]*/>',f'<hh:fontRef hangul="{f}" latin="{f}" hanja="{f}" japanese="{f}" other="{f}" symbol="{f}" user="{f}"/>',x)
    def build(s,pages,out,title,prv_png,prv_text):
        sec=s.z.read('Contents/section0.xml').decode('utf-8')
        i=sec.find('<hp:p ')
        root_open=sec[:i]
        first=re.search(r'<hp:p [^>]*><hp:run [^>]*><hp:secPr.*?</hp:secPr>.*?</hp:run>',sec[i:],re.S).group(0)
        body=[]
        base=s.charid(1000,False,None)
        for pi,shs in enumerate(pages):
            objs=''.join(f'<hp:run charPrIDRef="{base}">{s.shape(x)}</hp:run>' for x in shs)
            if pi==0: body.append(first+objs+'</hp:p>')
            else: body.append(f'<hp:p id="0" paraPrIDRef="{s.paraid("left",100)}" styleIDRef="0" pageBreak="1" columnBreak="0" merged="0">{objs}</hp:p>')
        section=root_open+''.join(body)+'</hs:sec>'
        hdr=s.hdr
        cx=''.join(s.charxml(i,k) for k,i in sorted(s.chars.items(),key=lambda kv:kv[1]))
        px=''.join(s.paraxml(i,k) for k,i in sorted(s.paras.items(),key=lambda kv:kv[1]))
        hdr=re.sub(r'<hh:charProperties itemCnt="\d+">',f'<hh:charProperties itemCnt="{s.nchar+len(s.chars)}">',hdr).replace('</hh:charProperties>',cx+'</hh:charProperties>')
        hdr=re.sub(r'<hh:paraProperties itemCnt="\d+">',f'<hh:paraProperties itemCnt="{s.npara+len(s.paras)}">',hdr).replace('</hh:paraProperties>',px+'</hh:paraProperties>')
        with zipfile.ZipFile(out,'w') as z:
            z.writestr(zipfile.ZipInfo('mimetype'),s.z.read('mimetype'),compress_type=zipfile.ZIP_STORED)
            for info in s.z.infolist():
                n=info.filename
                if n=='mimetype': continue
                data=s.z.read(n)
                if n=='Contents/section0.xml': data=section.encode()
                elif n=='Contents/header.xml': data=hdr.encode()
                elif n=='Preview/PrvText.txt': data=prv_text.encode()
                elif n=='Preview/PrvImage.png': data=open(prv_png,'rb').read()
                z.writestr(n,data,compress_type=zipfile.ZIP_DEFLATED)
