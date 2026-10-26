from shell import *
from mods import *
from layouts import L,R,W
RP_HEAD_SHARE=lambda l,v,c,ct: f'<div class="ko-b-sh" style="--c:var({c});--c-text:var({ct})"><span class="l">{l}</span><span class="v">{v}%</span><div class="tk"><i style="width:{v}%"></i></div></div>'
CHK=lambda: blob('check')
TINTS=['--tint-sky-50','--tint-aqua-50','--tint-mint-50']
def tints(y,h,items,cols=(34.9,334.6,634.4),wd=291.1):
    return ''.join(f'<div class="ko-abs" style="left:{x}px;top:{y}px;width:{wd}px;height:{h}px;background:var({t});border-radius:2.9px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:14px;font-weight:500;gap:2px">{s}</div>' for x,t,s in zip(cols,TINTS,items))
def bigstat(v,cap): return f'<span style="font-size:28px;font-weight:700;line-height:1.1">{v}</span><span style="font-size:14px;font-weight:500">{cap}</span>'
RP_BULLETS=lambda: '''<div class="ko-b-pi"><div class="no">E</div><b>방폐물 재활용 플랫폼 구축</b><span>방사성의약품 수입 대체 효과 43.6억 원 발생</span></div><div class="ko-b-pi" style="margin-top:3px"><div class="no">S</div><b>협력사 상생 안전관리 강화</b><span>상주 협력사 위험성평가 우수사업장 인정</span></div><div class="ko-b-pi" style="margin-top:3px"><div class="no">G</div><b>법·윤리경영체계 확립</b><span>권익위 부패방지시책평가 최우수 등급 달성</span></div>'''
BG1='<span class="ko-highlight">ESG 확산</span> 등 국가적 ESG 인프라 확충 및 공공기관의 ESG 경영 선도 요구'
EF1='<ul class="ko-b-ul"><li>경영전략과 연계한 「KORAD ESG 경영 추진 계획」 수립</li><li>ESG 성과창출 기반 강화: 추진체계(ESG 위원회·노사공동 선언)와 제도정비(ISO14001 인증)</li></ul>'
BG2='디지털 기반의 방폐물 관리 및 <span class="ko-highlight">스마트 안전체계 구축</span>으로 한국판 뉴딜 뒷받침'
EF2='<ul class="ko-b-ul"><li>[추진전략 수립] 지능형 스마트 처분시설 구축 로드맵 수립</li><li>[디지털 인프라 구축] 설비간 연계 운영을 위한 처분시설 전용 무선통신망 구축<ul><li>방폐물 자동판정 시스템 등 ’21년 스마트 처분시설 세부과제 이행</li></ul></li></ul>'
RP2=lambda: '''<div style="font-size:14px;font-weight:700;color:var(--blue-dark);display:flex;align-items:center;gap:6px;margin-bottom:3px"><img src="%s" alt="" style="width:14px;height:14px">연간 효율개선 효과</div>'''%CHK()+''.join(f'<div class="ko-b-pi" style="padding-left:28px;margin:0 0 2px"><div class="no" style="top:0;width:18px;height:18px;font-size:11px">{n}</div><span style="font-size:14px;font-weight:500;line-height:18px">{t} <b class="em" style="display:inline">{v}</b> 단축</span></div>' for n,t,v in [(1,'방폐물 검사','2,000시간'),(2,'지하수 관측','192시간'),(3,'순찰점검','104시간'),(4,'안전관리','48시간')])

def hdrs(num,title,sub,page,gno,gm): return header(num,title,sub,page,gno,gm)

# L55 과제 카드 ×2 · 성과 왼쪽
def L55():
    tx=380.7
    c1=taskcard(130.7,'경영관리','01','ESG 경영 도입을 통한 KORAD 미래가치 제고',BG1,EF1,544.4,132.5,34.9,333.3,RP_BULLETS(),46,tbl_x=tx)
    c2=taskcard(325.2,'경영관리','02','방폐물 관리의 스마트 전환을 통한 경영효율화 및 안전관리시스템',BG2,EF2,544.4,132.5,34.9,333.3,RP2(),46,tbl_x=tx)
    items=[('과제 카드 1',34.9,130.7,890.2,48),('성과 패널',34.9,186.7,333.3,132.5),('표',tx,186.7,544.4,132.5),('과제 카드 2',34.9,325.2,890.2,48),('성과 패널',34.9,381.2,333.3,132.5),('표',tx,381.2,544.4,132.5)]
    sp=spec('L55','과제 카드 ×2 · 성과 먼저','L49 파생(표와 성과 패널 좌우 맞바꿈) · TaskCard ×2',items,'결론(성과)을 먼저 보여 주고 근거를 오른쪽에 읽게 할 때 — 성과가 수치로 강할 때.',['L49와 같은 모듈, 패널 x 34.9 · 표 x 380.7(사이 12.5)','배지·띠는 그대로 왼쪽 시작','성과 패널 색은 항상 그린 계열(결과), 표 라벨은 블루 → 틸'])
    return page('L55','L55 과제 카드 ×2 · 성과 먼저 · L49 파생',hdrs('03','주요 추진실적','ESG 경영 및 스마트 전환','5','3-1','ESG 경영 도입과 스마트 전환으로 경영효율화 추진'),c1+c2,guides(items),sp,810)

# L56 과제 카드 + 하단 요약 3칸
def L56():
    ef='<ul class="ko-b-ul" style="line-height:1.35"><li>[P] 전년도 성과 및 ’21년 작업계획 분석을 통해 방사선 관리목표 설정</li><li>[D] 다피폭 예상 RI 폐기물 관리업무 환경개선 추진<ul><li>RI 폐기물 일부 분리보관, 원격검사설비 도입 등</li></ul></li><li>[C·A] ALARA 위원회 모니터링, 다피폭 작업자 순환배치</li></ul>'
    bg='<ul class="ko-b-ul"><li>방폐물 관리수량 증가로 작업자 방사선 피폭량 증가추세</li><li>’20년 피폭량의 80%를 차지하는 <span class="ko-highlight">RI 폐기물 관리업무</span> 대책마련 필요</li></ul>'
    rp='<div class="ko-b-pi"><div class="no">1</div><b>목표치 초과자 ZERO</b><span>방사선작업자 개인별</span></div><div class="ko-b-pi" style="margin-top:6px"><div class="no">2</div><b>전년 대비 피폭 17% 저감</b><span>0.35 → 0.29 mSv/인</span></div>'
    card=taskcard(130.7,'안전관리','01','방사선작업자 피폭선량 저감으로 안전한 근무환경 조성',bg,ef,544.4,244,591.8,333.3,rp,80)
    t=tints(436.7,77.1,[bigstat('ZERO','목표치 초과자'),bigstat('17%','전년 대비 피폭 저감'),bigstat('0.29mSv','1인 평균 피폭선량')])
    items=[('과제 카드 · 배지+띠',34.9,130.7,890.2,48),('표',34.9,186.7,544.4,244),('성과 패널',591.8,186.7,333.3,244),('요약 3칸',34.9,436.7,890.2,77.1)]
    sp=spec('L56','과제 카드 + 요약 3칸','L50 카드(높이 300) + L51 하단 요약 3칸 · TaskCard + 틴트 요약',items,'과제 1개를 설명하고 아래에 핵심 수치 3개를 한눈에 모을 때.',['카드 높이 300(= 본문 383.1 − 요약 77.1 − 사이 6)','요약 3칸은 3단 열(291.1)·tint-sky → aqua → mint, 숫자 28pt Bold','숫자는 카드 성과 패널의 수치와 같은 값만(중복 허용, 새 수치 금지)'])
    return page('L56','L56 과제 카드 + 요약 3칸 · L50·L51 조합',hdrs('03','주요 추진실적','안전관리','8','3-3','방사선 피폭 저감으로 안전한 근무환경 조성'),card+t,guides(items),sp,780)

# L57 포토 4칸 + 설명
def L57():
    xs=[34.9,262.5,490.2,717.7]; cw=207.4; y=164.7; ph=160
    heads=['동굴처분시설<br>착공(’07)','공단 설립<br>(’09)','동굴처분시설<br>준공(’15)','표층처분시설<br>인허가(’21)']
    descs=['동굴처분시설 건설 시작','방폐물 관리 전담기관 설립','동굴처분시설 준공·운영 개시','표층처분시설 인허가 추진']
    tint_order=['--tint-sky-50','--tint-aqua-50','--tint-mint-50','--tint-blue-100']
    dh=round(513.8-(y+40+ph),1)
    cols=''
    for x,h,d,t in zip(xs,heads,descs,tint_order):
        cols+=photocard(x,y,0,h,ph,w=cw)
        cols+=f'<div class="ko-abs" style="left:{x}px;top:{y+40+ph}px;width:{cw}px;height:{dh}px;background:var({t});display:flex;align-items:center;justify-content:center;text-align:center;padding:0 14px;font-size:14px;font-weight:500;line-height:1.3">{d}</div>'
    chev=''.join(f'<div class="ko-b-chev" style="left:{round(x+cw+5.1,1)}px;top:{y+12}px"></div>' for x in xs[:3])
    body=sec(L,130.7,'주요연혁')+cols+chev
    items=[('소제목',L,130.7,W,26)]+[(f'포토 카드 {i+1}',x,y,cw,round(40+ph,1)) for i,x in enumerate(xs)]+[('설명 박스 ×4',L,round(y+40+ph,1),W,dh)]
    sp=spec('L57','포토 4칸 + 설명','L51 포토 모듈 파생(칸 7 → 4단 열 207.4, 사진 100 → 160) + 설명 틴트 박스',items,'연혁·사례가 4개 이하일 때 사진을 크게 쓰고 설명을 붙이는 구성.',['4단 열(폭 207.4, 간격 20.2) — `designer-grid.md` 4단 그대로','카드 머리 40 · 사진 160 · 설명 박스는 남은 높이(본문 아래 끝 513.8까지)','설명 박스 틴트는 sky → aqua → mint → tint-blue-100 (계열 순서)','꺾쇠는 칸 사이 20.2 한가운데'])
    return page('L57','L57 포토 4칸 + 설명 · L51 파생',hdrs('01','기관 일반현황','주요연혁','3','1-1','핵심 이정표로 보는 방폐물 관리 체계 구축 과정'),body,guides(items),sp,780)

# L58 조직도 + 요약 3칸
def L58():
    pitch=129.75;T=164.7;cx=(L+R)/2
    def box(cls,x,y,w,h,t): return f'<div class="ko-b-ob {cls}" style="left:{round(x,1)}px;top:{round(y,1)}px;width:{w}px;height:{h}px">{t}</div>'
    def hl(x1,x2,y): return f'<div class="ko-b-ln" style="left:{round(x1,1)}px;top:{round(y,1)}px;width:{round(x2-x1,1)}px;height:1px"></div>'
    def vl(x,y1,y2): return f'<div class="ko-b-ln" style="left:{round(x,1)}px;top:{round(y1,1)}px;width:1px;height:{round(y2-y1,1)}px"></div>'
    o=box('top ko-trellis-deep',cx-100,T,200,30,'이사장')+box('top ko-trellis-deep',cx-100,T+74,200,30,'부이사장')+box('stf',L,T+2,112,30,'감사실')+box('stf',R-112,T+2,112,30,'기금관리센터')+box('stf',cx-172,T+37,112,30,'미래혁신실')+box('stf',cx+60,T+37,112,30,'소통협력단')+vl(cx,T+30,T+74)+hl(cx-60,cx+60,T+52)+vl(cx,T+104,T+132)
    names=['경영관리본부','품질안전본부','중저준위<br>운영본부','방폐물<br>기술연구원','건설사업단','고준위추진단','방폐물<br>인재개발원']
    xs=[L+i*pitch for i in range(7)]
    o+=hl(xs[0]+56,xs[6]+56,T+132)+''.join(vl(x+56,T+132,T+152)+box('dv',x,T+152,112,40,n) for x,n in zip(xs,names))
    t=tints(404.7,109.1,[bigstat('410명','총 정원'),bigstat('276명','일반직(67.3%)'),bigstat('93명','공무직(22.7%)')])
    body=sec(L,130.7,'조직현황',' (’22.3월 현재)')+o+sec(L,370.7,'정원현황',' (’22.3월 현재)')+t
    items=[('소제목',L,130.7,W,26),('조직도',L,164.7,W,192),('소제목',L,370.7,W,26),('요약 3칸',L,404.7,W,109.1)]
    sp=spec('L58','조직도 + 요약 3칸','L52 파생(표 → 3단 요약 틴트 박스)',items,'조직도 아래 핵심 인원 수치 3개만 보여 줄 때(표가 필요 없을 때).',['L52의 조직도 그대로(폭 112·피치 129.75)','요약 3칸 = 3단 열 291.1, 높이 109.1(본문 아래 끝까지)','숫자 28pt Bold + 설명 14pt, 숫자는 정원 표의 값에서 계산'])
    return page('L58','L58 조직도 + 요약 3칸 · L52 파생',hdrs('01','기관 일반현황','조직 및 정원','3','1-2','7개 본부·단·원 체계와 정원 410명 규모로 운영'),body,guides(items),sp,780)

# L59 요약 ▶ 상세 1행 + 결론 띠
def L59():
    LW=291.1;AZ=54;RX=round(L+LW+AZ,1);RW=round(R-RX,1);y=130.7;h=275.2
    left=f'<div style="font-size:14px;font-weight:500;margin-bottom:6px;color:var(--blue-dark)">중ㆍ저준위 방폐물 총 <b style="font-size:16px">152,145</b>드럼</div>'+''.join(RP_HEAD_SHARE(a,b,c,d) for a,b,c,d in [('원자력발전소',75,'--blue-bright','--blue-strong'),('연구원',17,'--teal-400','--teal-600'),('연료제조사',6,'--blue-strong','--blue-strong'),('병원·산업체 등',2,'--blue-cyan','--blue-dark')])
    cw=round((RW-24-16)/3,1)
    caps=['① 동굴처분시설(’15년 준공)','② 표층처분시설(’24년 예정)','③ 매립형처분시설(’27년 예정)']
    right='<div style="display:flex;gap:8px">'+''.join(f'<div style="width:{cw}px"><div style="font-size:12px;font-weight:500;height:18px;line-height:18px;white-space:nowrap">{c}</div><div style="height:176px;border:0.5px solid var(--teal-400);background:var(--tint-aqua-50);display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;font-size:12px;color:var(--slate-700)"><img src="{blob("image")}" alt="" style="width:28px;height:28px">사진</div></div>' for c in caps)+'</div>'
    def pnl(x,w,title,inner,fam):
        cls='ko-b-rp is-teal' if fam=='teal' else 'ko-b-rp'
        return f'<div class="{cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:var(--white)"><h4 class="ko-trellis-{fam}">{title}</h4><div class="bd" style="padding:8px 12px">{inner}</div></div>'
    body=pnl(L,LW,'발 생 현 황 <small style="letter-spacing:0;font-weight:500;font-size:12px;margin-left:6px">(’21.12월 기준)</small>',left,'blue')+arrow(L+LW,y+h/2)+pnl(RX,RW,'관 리 현 황',right,'teal')
    body+='<div class="ko-conclusion" style="top:418.1px;height:121.9px"><ul style="top:52px"><li>방폐물 발생의 <em>75%가 원자력발전소</em>에서 발생 — 처분시설 단계적 확충으로 안정적 관리</li></ul></div>'
    items=[('요약 패널',L,y,LW,h),('상세 패널',RX,y,RW,h),('결론 띠',0,418.1,960,121.9)]
    sp=spec('L59','요약 ▶ 상세 1행 + 결론 띠','L53 한 행을 크게(높이 275.2) + L23의 결론 띠',items,'요약 → 상세 한 묶음에 종합 결론을 붙일 때.',['좌우 1 : 2 + 화살표 54(L53과 같은 값)','패널 높이 275.2 — 결론 띠(y 418.1) 위에서 끝남','결론 띠는 기존 ConclusionBar 그대로(1~2문장, 강조 cyan)','Governing Message 있음: 패널은 y 130.7부터'])
    return page('L59','L59 요약 ▶ 상세 1행 + 결론 띠 · L53·L23 조합',hdrs('02','방사성폐기물 개요','발생 및 관리현황','4','2-1','방사성폐기물 발생 현황과 관리 체계'),body,guides(items),sp,780)

# L60 번호 행 ▶ 결과 카드 (단일)
def L60():
    LW=628.8;AZ=54;RX=round(L+LW+AZ,1);RW=round(R-RX,1);y=164.7;h=349.1;n=4;pitch=h/n
    rows=[('경영관리','청렴도 제고를 위한 내·외부 이해관계자 소통 기회 확대 필요 등 지적사항 32건'),('주요사업','종사자 방사선 노출 저감을 위한 장기적인 노력 필요 등 지적사항 5건'),('국회','연구인력 및 R&D 확충을 위한 예산 반영 필요 지적사항 1건'),('종합','총 38건 지적사항 전건 조치 완료')]
    nr=''.join(f'<div class="hd" style="top:{round(i*pitch+6,1)}px"><i>{i+1}</i>{t}</div><div class="tx" style="top:{round(i*pitch+6+30,1)}px">{d}</div>' for i,(t,d) in enumerate(rows))
    box=f'<div class="ko-b-nr" style="left:{L}px;top:{y}px;width:{LW}px;height:{h}px">{nr}</div>'
    rc=resultcard(RX,y,RW,h,f'<img src="{blob("badge")}" alt="" style="width:48px;height:48px;margin-bottom:10px"><span class="t">2020년 지적사항</span><span class="big">100<small>%</small></span><span class="cap">조치완료</span><span style="font-size:12px;margin-top:6px;color:var(--slate-700)">총 38건 전건</span>')
    body=sec(L,130.7,'2020년 외부 지적사항 조치실적')+box+arrow(L+LW,y+h/2)+rc
    items=[('소제목',L,130.7,W,26),('번호 행 박스(4행)',L,y,LW,h),('결과 카드',RX,y,RW,h)]
    sp=spec('L60','번호 행 ▶ 결과 카드 (1묶음)','L54 위 묶음을 본문 높이로 확장(행 3 → 4, 높이 163 → 349.1)',items,'근거 항목이 4개 안팎이고 결과를 한 장으로 강조할 때.',['3 : 1 + 화살표 54(L54와 같은 값)','행 피치 = 박스 높이 ÷ 행 수(87.3), 행은 4개 이내','행 수가 늘면 모듈을 복제하고 피치만 줄임'])
    return page('L60','L60 번호 행 ▶ 결과 카드 · L54 파생',hdrs('03','주요 추진실적','경영평가 환류','4','3-2','2020년 외부 지적사항 38건 전건 조치 완료'),body,guides(items),sp,780)

# L61 표 ▶ 성과 카드 (단일)
def L61():
    LW=628.8;AZ=54;RX=round(L+LW+AZ,1);RW=round(R-RX,1);ty=214.7;h=round(513.8-ty,1)
    rowh=round((h-30)/6,1)
    data=[('방폐물 관리사업(중ㆍ저준위)','방폐물 안전처분 성과(9점)','100점'),('방폐물 관리사업(고준위)','방폐물 관리기술 개발 및 확산 성과(5점)','100점'),('안전 관리사업(인적안전)','종사자 피폭선량 저감화 성과(8점)','97.552점'),('안전 관리사업(인적안전)','근로자 안전사고 예방지수(7점)','95.200점'),('안전 관리사업(시설안전)','처분시설 안전운영 노력(2점)','92.004점')]
    trs=''.join(f'<tr style="height:{rowh}px"><th>{a}</th><td class="tl" style="text-align:center">{b}</td><td class="tr">{c}</td></tr>' for a,b,c in data)
    trs+=f'<tr class="total" style="height:{rowh}px"><th>합 계</th><td style="text-align:center">가중평균(31점)</td><td class="tr">97.77점</td></tr>'
    tbl=f'<table class="ko-table l b14" style="left:{L}px;top:{ty}px;width:{LW}px"><colgroup><col style="width:210px"><col><col style="width:130px"></colgroup><thead><tr><th>구 분</th><th>지표명(가중치)</th><th>2021년 실적</th></tr></thead><tbody>{trs}</tbody></table>'
    bars=f'<div class="ko-bars" style="left:44px;top:100px;width:104px;height:110px"><div class="ko-bargroup" style="gap:12px"><div class="ko-bar base" style="width:26px;height:92px"><b style="font-size:12px">95.58</b></div><div class="ko-bar accent" style="width:26px;height:104px"><b style="font-size:12px">97.77</b></div></div></div><div class="ko-axis" style="left:44px;top:214px;width:104px;font-size:12px;justify-content:space-between;padding:0 4px"><span>’20년</span><span>’21년</span></div><p class="ko-abs ko-footnote" style="left:12px;bottom:8px;right:12px">※ 그래프 축 일부 생략</p>'
    rc=resultcard(RX,ty,RW,h,f'<div style="position:absolute;left:12px;top:10px;font-size:28px;font-weight:700;color:var(--teal-600);line-height:1.1">2.3<small style="font-size:16px">%</small> <span style="font-size:16px;color:var(--navy-ink);font-weight:500">향상</span></div>{bars}')
    body=sec(L,130.7,'2021년 주요사업 계량지표 실적',' (잠정)')+defbox(L,164.7,W,'계량지표 종합 97.77점으로 전년 대비 2.3% 향상')+tbl+arrow(L+LW,ty+h/2)+rc
    items=[('소제목',L,130.7,W,26),('정의 박스',L,164.7,W,36),('표(머리글+5행+합계)',L,ty,LW,h),('성과 카드',RX,ty,RW,h)]
    sp=spec('L61','표 ▶ 성과 카드 (1묶음)','L54 아래 묶음을 본문 높이로 확장(+ 한 줄 정의 박스, 합계 행)',items,'표 한 개와 성과 한 장을 크게 보여 줄 때.',['3 : 1 + 화살표 54, 표 행 6(합계 행 tint-blue-100)','합계 행 값은 가중평균(= Σ점수×배점 ÷ 31)으로 계산한 파생값','정의 박스는 SectionTitle 바로 아래(8)에서 한 줄 요약'])
    return page('L61','L61 표 ▶ 성과 카드 · L54 파생',hdrs('03','주요 추진실적','계량지표','4','3-2','2021년 주요사업 계량지표 종합 97.77점 달성'),body,guides(items),sp,780)

ALL2={'L55':L55,'L56':L56,'L57':L57,'L58':L58,'L59':L59,'L60':L60,'L61':L61}
