# 참조 B 모듈 HTML 조각 (모든 좌표는 슬라이드 pt, 절대 위치)
from shell import blob
def sec(x,y,text,small=''):
    s=f'<small>{small}</small>' if small else ''
    return f'<div class="ko-b-sec" style="left:{x}px;top:{y}px">{"<i></i>"}{text}{s}</div>'
def defbox(x,y,w,text):
    return f'<div class="ko-b-def" style="left:{x}px;top:{y}px;width:{w}px"><img src="{blob("check")}" alt="">{text}</div>'
def hexbadge(x,y,no):
    return f'<div class="ko-b-hex" style="left:{x}px;top:{y}px"><div class="ko-trellis-blue"><b>{no}</b></div></div>'
def band(x,y,w,text,cat=''):
    c=f'<span class="cat">{cat}</span><i class="dv"></i>' if cat else ''
    return f'<div class="ko-b-band ko-trellis-deep" style="left:{x}px;top:{y}px;width:{w}px">{c}{text}</div>'
def taskcard(y0, cap, no, title, bg_html, ef_html, tbl_w, tbl_h, panel_x, panel_w, panel_html, bg_h, x0=34.9, right=925.1, hdr_h=22, head='세 부 내 용', cls='', tbl_x=None):
    ef_h = round(tbl_h-hdr_h-bg_h,1)
    tx=x0 if tbl_x is None else tbl_x
    ty=round(y0+56,1)
    o=band(52,round(y0+8,1),round(right-52,1),title,cap)+hexbadge(x0,y0,no)
    o+=f'''<table class="ko-b-tt {cls}" style="left:{tx}px;top:{ty}px;width:{tbl_w}px;height:{tbl_h}px"><colgroup><col style="width:76px"><col></colgroup><thead><tr><th>구 분</th><th>{head}</th></tr></thead><tbody><tr style="height:{bg_h}px"><th class="ko-trellis-blue">추진배경</th><td>{bg_html}</td></tr><tr style="height:{ef_h}px"><th class="ko-trellis-teal">추진노력</th><td>{ef_html}</td></tr></tbody></table>'''
    o+=f'<div class="ko-b-rp is-green" style="left:{panel_x}px;top:{ty}px;width:{panel_w}px;height:{tbl_h}px"><h4 class="ko-trellis-green">추 진 성 과</h4><div class="bd">{panel_html}</div></div>'
    return o
def arrow(zone_left,y_center,zone=54):
    return f'<div class="ko-b-arrow" style="left:{round(zone_left+7,1)}px;top:{round(y_center-30,1)}px"></div>'
def resultcard(x,y,w,h,inner):
    return f'<div class="ko-b-rc is-green" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div>{inner}</div></div>'
def photocard(x,y,i,head,photo_h,cap='사진',w=112):
    return f'<div class="ko-b-ph" style="left:{x}px;top:{y}px;width:{w}px"><div class="h ko-trellis-deep">{head}</div><div class="p" style="height:{photo_h}px"><img src="{blob("image")}" alt="">{cap}</div></div>'
