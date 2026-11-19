import json,sys,html
MM=283.465
pages=json.load(open(sys.argv[1],encoding='utf-8'))
o=['<html><head><meta charset="utf-8"><style>body{margin:0;background:#888}.pg{position:relative;width:210mm;height:297mm;background:#fff;margin:4mm auto;overflow:hidden}.s{position:absolute;box-sizing:border-box;font-family:"Malgun Gothic",sans-serif;display:flex;flex-direction:column;word-break:keep-all;overflow:visible}p{margin:0}</style></head><body>']
for pg in pages:
    o.append('<div class="pg">')
    for s in pg:
        st=f"left:{s['x']/MM}mm;top:{s['y']/MM}mm;width:{s['w']/MM}mm;height:{s['h']/MM}mm;"
        if s['geom']=='poly':
            pts=' '.join(f"{a/MM},{b/MM}" for a,b in s['pts'])
            o.append(f'<svg class="s" style="{st}" viewBox="0 0 {s["w"]/MM} {s["h"]/MM}"><polygon points="{pts}" fill="#{s["fill"]}"/></svg>');continue
        if s.get('fill'): st+=f"background:#{s['fill']};"
        if s.get('line'): st+=f"border:{s['lw']/MM}mm solid #{s['line']};"
        if s['geom']=='ellipse': st+='border-radius:50%;'
        inner=''
        if s.get('paras'):
            st+='justify-content:'+{'t':'flex-start','b':'flex-end'}.get(s.get('anchor'),'center')+';'
            for p in s['paras']:
                inner+=f'<p style="text-align:{p["al"]};line-height:{p["ls"]/100}">'+''.join(f'<span style="font-size:{r["sz"]/100}pt;font-weight:{700 if r["b"] else 400};color:#{r["c"]};letter-spacing:{r["sp"]/100}em">{html.escape(r["t"])}</span>' for r in p['runs'])+'</p>'
        o.append(f'<div class="s" style="{st}">{inner}</div>')
    o.append('</div>')
o.append('</body></html>')
open(sys.argv[2],'w',encoding='utf-8').write(''.join(o))
