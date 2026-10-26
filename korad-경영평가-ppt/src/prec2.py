import sys, numpy as np, edges
from PIL import Image
pre=sys.argv[1]; show=len(sys.argv)>2
H,V=160,50
for n in range(1,6):
    sy,sx=edges.detect(edges.SRC%n,hmin=H,vmin=V); sy=[y for y in sy if 90<y<1960]
    im=Image.open(f'{pre}-{n}.png').convert('RGB'); c=Image.new('RGB',(1380,2000),(255,255,255)); c.paste(im,(0,48))
    ry,rx=edges.detect(c,hmin=H,vmin=V)
    res={}
    for name,a,b in (('y',sy,ry),('x',sx,rx)):
        b=np.array(b); e=[];bad=[]
        for v in a:
            d=b-v; i=np.abs(d).argmin() if len(b) else None
            if i is not None and abs(d[i])<=10: e.append(abs(d[i]));
            if i is None or abs(d[i])>3: bad.append((round(v,1),round(float(d[i]),1) if i is not None else None))
        res[name]=(e,bad)
    print(n,'가로 n=%d 평균 %.2f ≤2px %.0f%%'%(len(sy),np.mean(res['y'][0]),100*np.mean(np.array(res['y'][0])<=2)),'| 세로 n=%d 평균 %.2f ≤2px %.0f%%'%(len(sx),np.mean(res['x'][0]),100*np.mean(np.array(res['x'][0])<=2)))
    if show: print('  y 불일치',res['y'][1],'\n  x 불일치',res['x'][1])
