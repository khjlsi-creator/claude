# 공통 셸: 헤더·GM·가이드·스펙표 (기존 LayoutLxx 미리보기와 같은 골격)
import re
BLOB={'band':'8332faa82fac6e7ba652fea9daf6f126','ci':'caf1b3dc496f96a42a06f02beb5c1190','check':'ca89e9fc1599adfc64af693870bf5a60',
 'image':'1dd06023da9001f6882ae80c050ef49d','badge':'b9031ff6c873aeed98c918e8990343f7','trophy':'a06084087eda298dee7d2407ae27a6e5'}
def blob(k): return '/_blob/'+BLOB[k]

STYLE = '''html,body{margin:0;background:var(--white);} :root{--ko-check-url:url("/_blob/ca89e9fc1599adfc64af693870bf5a60");}
.gd{position:absolute;border:0.75px dashed #e6007e;pointer-events:none;z-index:50}
.gd b{position:absolute;left:-0.75px;top:-12px;padding:0 4px;height:11px;line-height:11px;font-size:8px;font-weight:600;color:#fff;background:#e6007e;white-space:nowrap}
.gd.area{border-color:#7a8797;border-style:dotted}.gd.area b{background:#7a8797}
.spec{position:absolute;left:0;top:548px;width:960px;height:%(sh)spx;background:#f6f9ff;border-top:2px solid var(--blue-bright);font-family:var(--font-sans);color:var(--navy-ink)}
.spec h4{position:absolute;left:20px;top:10px;margin:0;font-size:15px;font-weight:700}
.spec h4 small{font-size:11px;font-weight:400;color:var(--slate-500);margin-left:8px}
.spec table{position:absolute;left:20px;top:38px;width:560px;border-collapse:collapse;font-size:10px}
.spec th{background:var(--blue-panel);color:#fff;font-weight:500;padding:3px 5px;text-align:center}
.spec td{border-bottom:0.5px solid var(--tint-blue-200);padding:3px 5px;text-align:right;white-space:nowrap}
.spec td:first-child{text-align:left;font-weight:500}
.spec td.px{color:var(--blue-strong)}
.spec .r{position:absolute;left:600px;top:38px;width:340px;font-size:11px;line-height:1.45}
.spec .r p{margin:0 0 6px}.spec .r ul{margin:0;padding-left:14px}.spec .r li{margin-bottom:3px}'''

# 제목 폭(26pt SemiBold) 실측값 — 구분선·소제목 x 계산용 (measure.py 결과)
TITLE_W = {}
def header(num, title, sub, page, gm_no, gm, doc='2021년 경영실적평가 기관설명회'):
    w = TITLE_W.get(title, len(title)*23.5)
    dv = round(86 + w + 8, 1)
    n0, n1 = num[0], num[1]
    return f'''  <div class="ko-abs ko-header-fill"></div>
  <img class="ko-header-band" src="{blob('band')}" alt="">
  <p class="ko-abs ko-header-chapter">Chapter</p>
  <p class="ko-abs ko-header-doc">{doc}</p>
  <p class="ko-abs ko-header-num"><span class="z">{n0}</span>{n1}</p>
  <p class="ko-abs ko-header-title ko-on-blue">{title}</p>
  <div class="ko-abs ko-header-divider" style="left:{dv}px"></div>
  <p class="ko-abs ko-header-sub" style="left:{dv+7.8:.1f}px">{sub}</p>
  <img class="ko-ci" src="{blob('ci')}" alt="한국원자력환경공단" style="left:801.5px;top:12px;width:132.2px">
  <div class="ko-abs ko-page-tab">{page}</div>
  <div class="ko-abs ko-gm-lead"></div>
  <div class="ko-abs ko-gm-dot"></div>
  <p class="ko-abs ko-gm-text">{gm_no} {gm}</p>
  <div class="ko-abs ko-gm-rule"></div>
'''

def guides(items):
    out=['<div class="gd area" style="left:34.6px;top:130.7px;width:890.5px;height:383.1px"><b>본문 영역 34.6~925.1 × 130.7~513.8</b></div>']
    for (name,x,y,w,h) in items:
        out.append(f'<div class="gd" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><b>{name} · {w}×{h}</b></div>')
    return ''.join(out)

def px(v): return str(round(v*2))
def spec(lid, name, sub, items, when, bullets, sh=262):
    rows=''.join(f'<tr><td>{n}</td><td>{x}</td><td>{y}</td><td>{w}</td><td>{h}</td><td class="px">{px(x)}, {px(y)} · {px(w)}×{px(h)}</td></tr>' for (n,x,y,w,h) in items)
    lis=''.join(f'<li>{b}</li>' for b in bullets)
    return f'''<div class="spec"><h4>{lid} {name}<small>{sub}</small></h4>
<table><tr><th>영역</th><th>x</th><th>y</th><th>폭</th><th>높이</th><th>Slides px (x, y · 폭×높이)</th></tr>{rows}</table>
<div class="r"><p><b>언제</b> {when}</p><ul>{lis}</ul></div></div>'''

def page(lid, title_card, hdr, body, gd, sp, height):
    return f'''<!-- @dsCard group="레이아웃 상세" height={height} width=960 subtitle="{title_card}" -->
<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><title>Layout{lid} — preview</title>
<style>{STYLE % {'sh': height-548}}</style>
</head>
<body>
<div style="position:relative;width:960px;height:{height}px">
<div class="ko-slide" style="background:var(--white)">
{hdr}{body}{gd}</div>
{sp}
</div>
</body>
</html>
'''
