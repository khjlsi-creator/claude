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
  <svg style="position:absolute;left:0px;top:97.54px;width:39.37px;height:2px;overflow:visible" width="39.37" height="2"><line x1="0" y1="1" x2="39.37" y2="1" stroke="#001a7a" stroke-opacity="1" stroke-width="1.25"/></svg>
  <div style="position:absolute;left:35px;top:84.91px;width:27.24px;height:27.24px;box-sizing:border-box;background:#001a7a;border-radius:50%;"></div>
  <svg style="position:absolute;left:42.79px;top:92.28px;width:11.69px;height:10.51px;overflow:visible;" width="11.69" height="10.51" viewBox="0 0 11.69 10.51"><path d="M10.56 10.51L1.13 10.51C0.71 10.51 0.37 10.29 0.14 9.94C-0.05 9.59 -0.05 9.18 0.14 8.8L4.84 0.57C5.03 0.22 5.42 0 5.83 0C6.24 0 6.59 0.22 6.81 0.57L11.55 8.8C11.74 9.15 11.74 9.56 11.55 9.94C11.36 10.29 10.97 10.51 10.56 10.51ZM5.83 0.54C5.61 0.54 5.45 0.64 5.32 0.83L0.62 9.08C0.52 9.28 0.52 9.47 0.62 9.66C0.71 9.85 0.91 9.94 1.13 9.94L10.56 9.94C10.78 9.94 10.94 9.85 11.07 9.66C11.17 9.47 11.17 9.28 11.07 9.08L6.34 0.83C6.24 0.64 6.05 0.54 5.83 0.54L5.83 0.54Z" fill="#ffffff" fill-opacity="1"/></svg>
  <svg style="position:absolute;left:40.27px;top:90.15px;width:16.71px;height:16.74px;overflow:visible;" width="16.71" height="16.74" viewBox="0 0 16.71 16.74"><path d="M8.35 16.74C8.35 16.74 8.07 16.61 8.07 16.45C8.07 16.3 8.2 16.17 8.35 16.17C12.64 16.17 16.17 12.67 16.17 8.35C16.17 4.03 12.67 0.57 8.35 0.57C4.03 0.57 0.57 4.07 0.57 8.35C0.57 8.51 0.44 8.64 0.29 8.64C0.13 8.64 0 8.51 0 8.35C0 3.75 3.75 0 8.35 0C12.96 0 16.71 3.75 16.71 8.35C16.71 12.96 12.96 16.71 8.35 16.71Z" fill="#ffffff" fill-opacity="1"/></svg>
  <svg style="position:absolute;left:40.27px;top:98.22px;width:0.57px;height:1.02px;overflow:visible;" width="0.57" height="1.02" viewBox="0 0 0.57 1.02"><path d="M0.29 1.02C0.29 1.02 0 0.89 0 0.76C0 0.6 0 0.44 0 0.29C0 0.13 0.13 0 0.29 0C0.44 0 0.57 0.13 0.57 0.29C0.57 0.44 0.57 0.57 0.57 0.73C0.57 0.89 0.48 1.02 0.32 1.02C0.32 1.02 0.32 1.02 0.32 1.02Z" fill="#ffffff" fill-opacity="1"/></svg>
  <svg style="position:absolute;left:47.6px;top:94.63px;width:2.01px;height:5.24px;overflow:visible;" width="2.01" height="5.24" viewBox="0 0 2.01 5.24"><path d="M1.46 5.24L0.57 5.24C0.57 5.24 0.32 5.11 0.29 4.99L0 0.32C0 0.32 0 0.16 0.06 0.1C0.13 0.03 0.19 0 0.25 0L1.75 0C1.75 0 1.91 0.03 1.94 0.1C1.97 0.16 2.03 0.22 2 0.32L1.72 4.99C1.72 4.99 1.59 5.24 1.43 5.24ZM0.86 4.7L1.21 4.7L1.46 0.6L0.57 0.6L0.83 4.7Z" fill="#ffffff" fill-opacity="1"/></svg>
  <div style="position:absolute;left:62.54px;top:82.78px;width:860px;height:31.5px;box-sizing:border-box;padding:3.6px 7.2px 3.6px 7.2px;display:flex;flex-direction:column;justify-content:flex-start;white-space:nowrap;"><p style="margin:0;font-size:20px;font-weight:500;text-align:left;line-height:1.2;color:#000359;">{gm_no} {gm}</p></div>
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
