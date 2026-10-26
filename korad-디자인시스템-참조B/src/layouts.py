from shell import *
from mods import *
L=34.9; R=925.1; W=round(R-L,1)

# ───────── L49 과제 카드 ×2 ─────────
def L49():
    rp1='''<div class="ko-b-pi"><div class="no">E</div><b>방폐물 재활용 플랫폼 구축</b><span>방사성의약품 수입 대체 효과 43.6억 원 발생</span></div>
<div class="ko-b-pi" style="margin-top:3px"><div class="no">S</div><b>협력사 상생 안전관리 강화</b><span>상주 협력사 위험성평가 우수사업장 인정</span></div>
<div class="ko-b-pi" style="margin-top:3px"><div class="no">G</div><b>법·윤리경영체계 확립</b><span>권익위 부패방지시책평가 최우수 등급 달성</span></div>'''
    rp2='''<div style="font-size:14px;font-weight:700;color:var(--blue-dark);display:flex;align-items:center;gap:6px;margin-bottom:3px"><img src="%s" alt="" style="width:14px;height:14px">연간 효율개선 효과</div>
<div class="ko-b-pi" style="padding-left:28px;margin:0 0 2px"><div class="no" style="top:0;width:18px;height:18px;font-size:11px">1</div><span style="font-size:14px;font-weight:500;line-height:18px">방폐물 검사 <b class="em" style="display:inline">2,000시간</b> 단축</span></div>
<div class="ko-b-pi" style="padding-left:28px;margin:0 0 2px"><div class="no" style="top:0;width:18px;height:18px;font-size:11px">2</div><span style="font-size:14px;font-weight:500;line-height:18px">지하수 관측 <b class="em" style="display:inline">192시간</b> 단축</span></div>
<div class="ko-b-pi" style="padding-left:28px;margin:0 0 2px"><div class="no" style="top:0;width:18px;height:18px;font-size:11px">3</div><span style="font-size:14px;font-weight:500;line-height:18px">순찰점검 <b class="em" style="display:inline">104시간</b> 단축</span></div>
<div class="ko-b-pi" style="padding-left:28px;margin:0"><div class="no" style="top:0;width:18px;height:18px;font-size:11px">4</div><span style="font-size:14px;font-weight:500;line-height:18px">안전관리 <b class="em" style="display:inline">48시간</b> 단축</span></div>''' % blob('check')
    c1=taskcard(130.7,'경영관리','01','ESG 경영 도입을 통한 KORAD 미래가치 제고',
        '<span class="ko-highlight">ESG 확산</span> 등 국가적 ESG 인프라 확충 및 공공기관의 ESG 경영 선도 요구',
        '<ul class="ko-b-ul"><li>경영전략과 연계한 「KORAD ESG 경영 추진 계획」 수립</li><li>ESG 성과창출 기반 강화: 추진체계(ESG 위원회·노사공동 선언)와 제도정비(ISO14001 인증)</li></ul>',
        544.4,132.5,591.8,333.3,rp1,46)
    c2=taskcard(325.2,'경영관리','02','방폐물 관리의 스마트 전환을 통한 경영효율화 및 안전관리시스템',
        '디지털 기반의 방폐물 관리 및 <span class="ko-highlight">스마트 안전체계 구축</span>으로 한국판 뉴딜 뒷받침',
        '<ul class="ko-b-ul"><li>[추진전략 수립] 지능형 스마트 처분시설 구축 로드맵 수립</li><li>[디지털 인프라 구축] 설비간 연계 운영을 위한 처분시설 전용 무선통신망 구축<ul><li>방폐물 자동판정 시스템 등 ’21년 스마트 처분시설 세부과제 이행</li></ul></li></ul>',
        544.4,132.5,591.8,333.3,rp2,46)
    items=[('과제 카드 1 · 육각 배지+딥블루 띠',34.9,130.7,890.2,48),('표(구분/세부 내용)',34.9,186.7,544.4,132.5),('성과 패널',591.8,186.7,333.3,132.5),
           ('과제 카드 2',34.9,325.2,890.2,48),('표',34.9,381.2,544.4,132.5),('성과 패널',591.8,381.2,333.3,132.5)]
    hd=header('03','주요 추진실적','ESG 경영 및 스마트 전환','5','3-1','ESG 경영 도입과 스마트 전환으로 경영효율화 추진')
    sp=spec('L49','과제 카드 ×2','2021 기관설명회 5~9번 파생 · TaskCard(육각 배지·딥블루 띠·라벨 표) + ResultPanel',items,
      '과제(추진실적) 한 개를 “배경 → 노력 → 성과” 순으로 보여 주는 카드를 위아래로 2개 쌓을 때.',
      ['카드 높이 188.5 · 사이 6 (3단×2행 행 높이와 같은 값)','표 : 패널 = 544.4 : 333.3, 사이 12.5 (원본 5:3 비율 → 2단 간격 12.5)','패널 윗선 = 표 윗선, 패널 아랫선 = 카드 아랫선','표 본문 14pt·불릿 2단계 12pt · 추진노력 3~4줄','라벨 = trellis 타일(추진배경 블루 → 추진노력 틸), 성과 패널 = 그린 계열(결과)','패널 항목 3개(제목 14pt + 설명 12pt 한 줄) 또는 4줄 목록','시스템 규칙대로 Governing Message 필요 · 복합 조합 아님(같은 카드 2회 복제)'])
    return page('L49','L49 과제 카드 ×2 · 2021 기관설명회 5~9번 파생',hd,c1+c2,guides(items),sp,810)

# ───────── L50 과제 카드 ×1 ─────────
def L50():
    rp='''<div style="display:flex;flex-direction:column;gap:10px;height:100%">
<div style="flex:1;background:var(--white);border:0.5px solid var(--green-400);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:14px;gap:2px">방사선작업자 개인별<b style="font-size:16px">“목표치 초과자”</b><span class="ko-highlight" style="font-size:36px;font-weight:700;color:var(--teal-600);line-height:1.15">ZERO</span></div>
<div style="flex:1;background:var(--white);border:0.5px solid var(--green-400);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:14px;gap:2px">전년 대비 피폭 저감<span style="font-size:36px;font-weight:700;color:var(--teal-600);line-height:1.15">17%</span><small style="font-size:12px">0.35 → 0.29 mSv/인</small></div></div>'''
    bg='<ul class="ko-b-ul"><li>방폐물 관리수량 증가로 인한 작업자 방사선 피폭량 증가추세</li><li>특히 ’20년 피폭량의 80%를 차지하는 <span class="ko-highlight">RI 폐기물 관리업무</span> 대책마련 필요</li></ul>'
    ef='<ul class="ko-b-ul" style="line-height:1.35"><li>[P] 전년도 성과 및 ’21년 작업계획 분석을 통해 방사선 관리목표 설정</li><li>[D] 다피폭 예상 RI 폐기물 관리업무 환경개선 추진<ul><li>RI 폐기물 일부 분리보관, 원격검사설비 도입 등</li></ul></li><li>[C·A] ALARA 위원회 모니터링, 다피폭 작업자 순환배치</li></ul>'
    c=taskcard(130.7,'안전관리','01','방사선작업자 피폭선량 저감으로 안전한 근무환경 조성',bg,ef,544.4,327.1,591.8,333.3,rp,96,hdr_h=24,cls='big')
    items=[('과제 카드 · 육각 배지+딥블루 띠',34.9,130.7,890.2,48),('표(구분/세부 내용)',34.9,186.7,544.4,327.1),('성과 패널',591.8,186.7,333.3,327.1)]
    hd=header('03','주요 추진실적','안전관리','8','3-3','방사선 피폭 저감으로 안전한 근무환경 조성')
    sp=spec('L50','과제 카드 ×1','L49 카드 모듈 1개를 본문 높이로 확장 · TaskCard + ResultPanel(수치 카드 2칸)',items,
      '과제 하나를 크게 — 추진노력이 5줄 이상이거나 성과 수치(KPI)가 2개 이상일 때.',
      ['카드 높이 383.1(본문 전체) — 표 높이만 327.1로 늘림','표 행: 머리글 24 · 추진배경 96 · 추진노력 207.1','성과 패널(그린 계열): 흰 수치 카드 2칸(높이 1:1, 사이 10) — 숫자 36pt Bold teal-600','수치 강조는 빨강이 아니라 계열색(결과 = teal-600) + 민트 형광 밑줄'])
    return page('L50','L50 과제 카드 ×1 · L49 카드 1개 확장',hd,c,guides(items),sp,780)

# ───────── L51 정의 박스 + 포토 타임라인 + 요약 3칸 ─────────
def L51():
    heads=['동굴처분시설<br>착공(’07)','공단 설립<br>(’09)','본사 이전<br>(’11)','사명 변경<br>(’13)','동굴처분시설<br>준공(’15)','품질경쟁력<br>우수기관(’20)','표층처분시설<br>인허가(’21)']
    pitch=129.75; ty=248.7; ph=100
    cards=''.join(photocard(round(L+i*pitch,2),ty,i,h,ph) for i,h in enumerate(heads))
    chev=''.join(f'<div class="ko-b-chev" style="left:{round(L+i*pitch+112+3.9,2)}px;top:{ty+12}px"></div>' for i in range(6))
    # 하단 3칸 요약
    base=ty+40+ph+14  # 402.7
    tints=['--tint-sky-50','--tint-aqua-50','--tint-mint-50']
    txt=['방폐물 인수·처분 및 처분시설 운영','방사선 안전관리 및 환경 모니터링','방폐물 관리 기술개발·인재 양성']
    cols=[34.9,334.6,634.4]
    tint=''.join(f'<div class="ko-abs" style="left:{x}px;top:{base+34}px;width:291.1px;height:{513.8-base-34:.1f}px;background:var({t});border-radius:2.9px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:500;text-align:center">{s}</div>' for x,t,s in zip(cols,tints,txt))
    body=sec(L,130.7,'설립목적')+defbox(L,164.7,W,'방사성폐기물의 안전하고 효율적인 관리로 국민생활의 안전과 환경보전에 기여 <small style="font-weight:400;font-size:12px;color:var(--slate-700)">(방사성폐기물관리법 제18조)</small>')
    body+=sec(L,214.7,'주요연혁')+cards+chev+sec(L,base,'주요사업')+tint
    items=[('소제목 · 26',L,130.7,W,26),('정의 박스 · 36',L,164.7,W,36),('소제목',L,214.7,W,26),('포토 카드 ×7 (112, 피치 129.75)',L,248.7,W,140),('소제목',L,round(base,1),W,26),('요약 3칸 (291.1 ×3)',L,round(base+34,1),W,round(513.8-base-34,1))]
    hd=header('01','기관 일반현황','설립목적과 주요연혁','2','1-1','방사성폐기물의 안전하고 효율적인 관리로 국민 안전과 환경보전에 기여')
    sp=spec('L51','정의 박스 + 포토 타임라인','2021 기관설명회 2번 상·중 파생 · SectionTitle + DefinitionBox + PhotoTimeline',items,
      '기관·사업 소개처럼 “한 줄 정의 → 연혁(사진) → 요약”을 한 장에 쌓을 때.',
      ['소제목 26 → 8 → 박스 36 → 14 → 다음 소제목 (원본 7 : 19 : 13 리듬을 20pt 소제목에 맞춰 환산)','포토 카드 7칸: 폭 112, 사이 17.75(= 카드 폭의 0.16배, 원본 83 : 13.7)','카드 머리 40(제목 2줄 이내, 줄당 7자) + 사진 100','연혁 칸 사이 작은 ▶ 연결 꺾쇠 (blue-bright 10×16)','하단 요약 3칸은 3단 열(291.1)과 하늘→아쿠아→민트 틴트','사진은 프레임 안에서만 교체(미리보기는 자리표시)'])
    return page('L51','L51 정의 박스 + 포토 타임라인 · 2021 기관설명회 2번 파생',hd,body,guides(items),sp,810)

# ───────── L52 조직도 + 표 ─────────
def L52():
    pitch=129.75; T=164.7
    cx=(L+R)/2
    def box(cls,x,y,w,h,t,extra=''): 
        return f'<div class="ko-b-ob {cls}" style="left:{round(x,1)}px;top:{round(y,1)}px;width:{w}px;height:{h}px;{extra}">{t}</div>'
    def hl(x1,x2,y): return f'<div class="ko-b-ln" style="left:{round(x1,1)}px;top:{round(y,1)}px;width:{round(x2-x1,1)}px;height:1px"></div>'
    def vl(x,y1,y2): return f'<div class="ko-b-ln" style="left:{round(x,1)}px;top:{round(y1,1)}px;width:1px;height:{round(y2-y1,1)}px"></div>'
    o=''
    o+=box('top ko-trellis-deep',cx-100,T,200,30,'이사장')
    o+=box('top ko-trellis-deep',cx-100,T+74,200,30,'부이사장')
    o+=box('stf',L,T+2,112,30,'감사실')+box('stf',R-112,T+2,112,30,'기금관리센터')
    o+=box('stf',cx-172,T+37,112,30,'미래혁신실')+box('stf',cx+60,T+37,112,30,'소통협력단')
    o+=vl(cx,T+30,T+74)+hl(cx-60,cx+60,T+52)
    o+=vl(cx,T+104,T+132)
    names=['경영관리본부','품질안전본부','중저준위<br>운영본부','방폐물<br>기술연구원','건설사업단','고준위추진단','방폐물<br>인재개발원']
    xs=[L+i*pitch for i in range(7)]
    o+=hl(xs[0]+56,xs[6]+56,T+132)
    for x,n in zip(xs,names):
        o+=vl(x+56,T+132,T+152)+box('dv',x,T+152,112,40,n)
    # 정원 표
    ty=370.7+34
    tbl=f'''<table class="ko-table l b14" style="left:{L}px;top:{ty}px;width:{W}px"><colgroup><col style="width:110px"><col span="7"></colgroup><thead><tr><th>구 분</th><th>상임이사</th><th>일반직</th><th>연구직</th><th>기능직</th><th>공무직</th><th>별도정원</th><th>합 계</th></tr></thead><tbody><tr><th>정 원</th><td>2</td><td>276</td><td>30</td><td>5</td><td>93</td><td>4</td><td style="font-weight:600">410</td></tr><tr><th>비중(%)</th><td>0.5</td><td>67.3</td><td>7.3</td><td>1.2</td><td>22.7</td><td>1.0</td><td style="font-weight:600">100.0</td></tr></tbody></table>'''
    body=sec(L,130.7,'조직현황',' (’22.3월 현재)')+o+sec(L,370.7-0,'정원현황',' (’22.3월 현재)')+tbl
    items=[('소제목',L,130.7,W,26),('조직도',L,164.7,W,192),('소제목',L,370.7,W,26),('표(머리글+2행)',L,404.7,W,90)]
    hd=header('01','기관 일반현황','조직 및 정원','3','1-2','7개 본부·단·원 체계로 운영하는 조직과 정원 현황')
    sp=spec('L52','조직도 + 정원 표','2021 기관설명회 2번 하 파생 · SectionTitle + OrgChart + DataTable(기본형)',items,
      '조직 구조(최대 2단계 + 7개 소속)와 정원 표를 함께 보여 줄 때.',
      ['조직도: 이사장·부이사장 박스 200×30(딥블루), 직속 4곳은 틴트 박스 112×30, 본부 7칸은 112×40 흰 박스 + 1pt blue-bright','본부 7칸은 L51 포토 카드와 같은 격자(폭 112, 피치 129.75)','연결선 1pt blue-bright, 가로 버스 y = 박스 위 20','직속 조직(감사실·기금관리센터)은 선 없이 좌우 끝에 둠(원본 그대로)','표는 DataTable 기본형(머리글 blue-bright, 합계 열 tint-blue-100) — 숫자 열 가운데·12행 이하'])
    return page('L52','L52 조직도 + 정원 표 · 2021 기관설명회 2번 파생',hd,body,guides(items),sp,780)

# ───────── L53 정의 박스 + [요약 패널 ▶ 상세 패널] ×2행 ─────────
def L53():
    LW=291.1; AZ=54; RX=round(L+LW+AZ,1); RW=round(R-RX,1)
    def panel(x,y,w,h,title,inner,hh=28,fam='blue'):
        cls='ko-b-rp is-teal' if fam=='teal' else 'ko-b-rp'
        return f'<div class="{cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:var(--white)"><h4 class="ko-trellis-{fam}" style="height:{hh}px">{title}</h4><div class="bd" style="top:{hh}px;padding:6px 12px">{inner}</div></div>'
    def share(l,v,c,ct):
        return f'<div class="ko-b-sh" style="--c:var({c});--c-text:var({ct})"><span class="l">{l}</span><span class="v">{v}%</span><div class="tk"><i style="width:{v}%"></i></div></div>'
    r1y=248.7; r1h=160; r2y=round(r1y+r1h+8,1); r2h=round(513.8-r2y,1)
    left1='<div style="font-size:14px;font-weight:500;margin-bottom:5px;color:var(--blue-dark)">중ㆍ저준위 방폐물 총 <b style="font-size:16px">152,145</b>드럼</div>'+share('원자력발전소',75,'--blue-bright','--blue-strong')+share('연구원',17,'--teal-400','--teal-600')+share('연료제조사',6,'--blue-strong','--blue-strong')+share('병원·산업체 등',2,'--blue-cyan','--blue-dark')
    cw=round((RW-24-16)/3,1)
    caps=['① 동굴처분시설(’15년 준공)','② 표층처분시설(’24년 예정)','③ 매립형처분시설(’27년 예정)']
    right1='<div style="display:flex;gap:8px">'+''.join(f'<div style="width:{cw}px"><div style="font-size:12px;font-weight:500;height:18px;line-height:18px;white-space:nowrap">{c}</div><div class="p" style="height:88px;border:0.5px solid var(--blue-bright);background:var(--tint-sky-50);display:flex;align-items:center;justify-content:center;gap:4px;flex-direction:column;font-size:12px;color:var(--slate-700)"><img src="{blob("image")}" alt="" style="width:28px;height:28px">사진</div></div>' for c in caps)+'</div>'
    left2='<ul class="ko-b-ul" style="font-size:14px;line-height:1.3"><li>경수로 20,952다발</li><li>중수로 486,796다발</li></ul>'
    right2='<ul class="ko-b-ul" style="font-size:14px;line-height:1.3"><li>① 정책 지원 — 공론화를 통한 정부 정책수립 및 특별법 제정 지원</li><li>② 사업기반 구축 — 부지선정 기준·절차 수립, 인수기준 개발</li><li>③ 핵심기술 확보 — 운반·저장·처분 분야별 핵심기술 개발</li></ul>'
    body=sec(L,130.7,'방사성폐기물(방폐물)의 정의')+defbox(L,164.7,W,'방사성물질 또는 그에 따라 오염된 물질로서 폐기의 대상이 되는 물질 <small style="font-weight:400;font-size:12px;color:var(--slate-700)">(원자력안전법 제2조)</small>')
    body+=sec(L,214.7,'방사성폐기물의 종류·발생 및 관리현황')
    body+=panel(L,r1y,LW,r1h,'발 생 현 황 <small style="letter-spacing:0;font-weight:500;font-size:12px;margin-left:6px">(’21.12월 기준)</small>',left1)
    body+=arrow(L+LW,r1y+r1h/2)+panel(RX,r1y,RW,r1h,'관 리 현 황',right1,fam='teal')
    body+=panel(L,r2y,LW,r2h,'고준위방폐물',left2,26)+arrow(L+LW,r2y+r2h/2)+panel(RX,r2y,RW,r2h,'관리정책 및 기반구축',right2,26,fam='teal')
    items=[('소제목 · 정의 박스',L,130.7,W,70),('소제목',L,214.7,W,26),('요약 패널 1행',L,r1y,LW,r1h),('상세 패널 1행',RX,r1y,RW,r1h),('요약 패널 2행',L,r2y,LW,r2h),('상세 패널 2행',RX,r2y,RW,r2h)]
    hd=header('02','방사성폐기물 개요','정의·종류·발생·관리','4','2-1','방사성폐기물의 정의와 종류, 발생 및 관리 현황')
    sp=spec('L53','정의 박스 + 요약 ▶ 상세 ×2행','2021 기관설명회 3번 파생 · DefinitionBox + ResultPanel(요약) ▶ FlowArrow ▶ ResultPanel(상세)',items,
      '“요약(수치) → 상세(사진·설명)”로 흐르는 항목이 2묶음일 때. 위쪽 행이 크고 아래 행은 짧은 설명.',
      ['좌우 = 1 : 2 (291.1 + 화살표 54 + 545.1) — 원본 205 : 53 : 405 비율 → 3단 열 폭 291.1 기준','화살표 구간 54 · 블록 화살표 40×60(tint-blue-100 → blue-cyan)','행 높이 160 : 97 (원본 187 : 71), 행 사이 8','원본의 도넛 차트는 KORAD 차트 규칙(파이 금지)에 따라 KpiBreakdown 식 점유율 막대로 바꿈','요약 패널 헤더 = trellis-blue 28(한 줄 제목)'])
    return page('L53','L53 정의 박스 + 요약 ▶ 상세 ×2행 · 2021 기관설명회 3번 파생',hd,body,guides(items),sp,810)

# ───────── L54 번호 행 ▶ 결과 카드 + 표 ▶ 성과 카드 ─────────
def L54():
    LW=628.8; AZ=54; RX=round(L+LW+AZ,1); RW=round(R-RX,1)
    y1=164.7; h1=163; s2=round(y1+h1+14,1); y2=round(s2+34,1); h2=round(513.8-y2,1)
    rows=[('경영관리','청렴도 제고를 위한 내·외부 이해관계자 소통 기회 확대 필요 등 지적사항 32건'),('주요사업','종사자 방사선 노출 저감을 위한 장기적인 노력 필요 등 지적사항 5건'),('국회','연구인력 및 R&D 확충을 위한 예산 반영 필요 지적사항 1건')]
    pitch=h1/3
    nr=''.join(f'<div class="hd" style="top:{round(i*pitch+3,1)}px"><i>{i+1}</i>{t}</div><div class="tx" style="top:{round(i*pitch+3+26,1)}px">{d}</div>' for i,(t,d) in enumerate(rows))
    nrbox=f'<div class="ko-b-nr" style="left:{L}px;top:{y1}px;width:{LW}px;height:{h1}px">{nr}</div>'
    rc1=resultcard(RX,y1,RW,h1,f'<img src="{blob("badge")}" alt="" style="width:36px;height:36px;margin-bottom:6px"><span class="t">2020년 지적사항</span><span class="big">100<small>%</small></span><span class="cap">조치완료</span>')
    tbl=f'''<table class="ko-table l b14 r23" style="left:{L}px;top:{y2}px;width:{LW}px"><colgroup><col style="width:200px"><col><col style="width:130px"></colgroup><thead><tr><th>구 분</th><th>지표명(가중치)</th><th>2021년 실적</th></tr></thead><tbody>
<tr><th>방폐물 관리사업(중ㆍ저준위)</th><td class="tl" style="text-align:center">방폐물 안전처분 성과(9점)</td><td class="tr">100점</td></tr>
<tr><th>방폐물 관리사업(고준위)</th><td class="tl" style="text-align:center">방폐물 관리기술 개발 및 확산 성과(5점)</td><td class="tr">100점</td></tr>
<tr><th>안전 관리사업(인적안전)</th><td class="tl" style="text-align:center">종사자 피폭선량 저감화 성과(8점)</td><td class="tr">97.552점</td></tr>
<tr><th>안전 관리사업(인적안전)</th><td class="tl" style="text-align:center">근로자 안전사고 예방지수(7점)</td><td class="tr">95.200점</td></tr>
<tr><th>안전 관리사업(시설안전)</th><td class="tl" style="text-align:center">처분시설 안전운영 노력(2점)</td><td class="tr">92.004점</td></tr></tbody></table>'''
    bars=f'<div class="ko-bars" style="left:44px;top:58px;width:104px;height:44px"><div class="ko-bargroup" style="gap:12px"><div class="ko-bar base" style="width:26px;height:30px"><b style="font-size:12px">95.58</b></div><div class="ko-bar accent" style="width:26px;height:38px"><b style="font-size:12px">97.77</b></div></div></div><div class="ko-axis" style="left:44px;top:104px;width:104px;font-size:12px;justify-content:space-between;padding:0 4px"><span>’20년</span><span>’21년</span></div>'
    rc2=resultcard(RX,y2,RW,h2,f'<div style="position:absolute;left:10px;top:6px;font-size:28px;font-weight:700;color:var(--teal-600);line-height:1.1">2.3<small style="font-size:16px">%</small> <span style="font-size:16px;color:var(--navy-ink);font-weight:500">향상</span></div>{bars}')
    body=sec(L,130.7,'2020년 외부 지적사항 조치실적')+nrbox+arrow(L+LW,y1+h1/2)+rc1
    body+=sec(L,s2,'2021년 주요사업 계량지표 실적',' (잠정)')+tbl+arrow(L+LW,y2+h2/2)+rc2
    items=[('소제목',L,130.7,W,26),('번호 행 박스',L,y1,LW,h1),('결과 카드',RX,y1,RW,h1),('소제목',L,s2,W,26),('표(머리글+5행)',L,y2,LW,h2),('성과 카드',RX,y2,RW,h2)]
    hd=header('03','주요 추진실적','경영평가 환류','4','3-2','2020년 외부 지적사항 100% 조치 및 계량지표 실적 향상')
    sp=spec('L54','번호 행 ▶ 결과 카드 + 표 ▶ 성과 카드','2021 기관설명회 4번 파생 · NumberRows·DataTable ▶ FlowArrow ▶ ResultCard',items,
      '“근거(번호 항목·표) ▶ 결과 한 장(카드)”을 위아래 두 묶음으로 보여 줄 때.',
      ['좌우 = 3 : 1 (628.8 + 화살표 54 + 207.4) — 오른쪽은 4단 열 폭 207.4','위 묶음 163 / 아래 묶음 138.1 (원본 194 : 162), 사이 14','번호 행: 머리 띠 24(fade-blue → 투명) + navy-deep 번호 원 18 + 본문 14pt 대시','결과 카드: 이중 틀(tint-mint-50 + 흰 카드, 결과 = 그린 계열), 큰 숫자 40pt Bold teal-600(원본의 빨강 대체)','성과 카드 막대 = 짝막대 패턴형(막대 26, 간격 12), 축 일부 생략 시 각주 표기','표 = DataTable 기본형 그대로(구분 열 흰색 — 색 강조 열 금지, 원본의 노랑·하늘 구분색 폐지)'])
    return page('L54','L54 번호 행 ▶ 결과 카드 + 표 ▶ 성과 카드 · 2021 기관설명회 4번 파생',hd,body,guides(items),sp,810)

ALL={'L49':L49,'L50':L50,'L51':L51,'L52':L52,'L53':L53,'L54':L54}
