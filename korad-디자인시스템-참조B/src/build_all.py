import os,re,sys,shutil,json
sys.path.insert(0,'.')
import layouts, shell, mods
from shell import blob
OUT='out/project'
BASE='/tmp/claude-0/-home-user-claude/4317952e-d0b8-5bd7-9c70-df2a4869001a/scratchpad/artifact-files/6a907df1-8229-419f-aa9f-da0a93e77a67/project/'
def w(path,txt):
    p=os.path.join(OUT,path); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w',encoding='utf8').write(txt)

# 1) 레이아웃 미리보기 + README
README={
'L49':('L49 과제 카드 ×2 — 과제(추진실적) 한 개를 “배경 → 노력 → 성과”로 보여 주는 카드를 위아래 2개.',
 '2021 기관설명회 5~9번(과제 카드 서식). 좌표에서 읽은 관계(표:패널 = 5:3, 패널 윗선 = 표 윗선, 카드 2개가 본문 높이를 반씩)를 16:9 KORAD 그리드로 다시 설계한 참조 B 파생.',
 '카드마다 육각 번호 배지 · 분야명 · 과제명, 추진배경 문장 1~2줄, 추진노력 불릿 3~4줄, 성과 3~4항목.',
 '| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 카드 1 배지+띠 | 34.9 | 130.7 | 890.2 | 48 |\n| 표 1 | 34.9 | 186.7 | 544.4 | 132.5 |\n| 성과 패널 1 | 591.8 | 186.7 | 333.3 | 132.5 |\n| 카드 2 배지+띠 | 34.9 | 325.2 | 890.2 | 48 |\n| 표 2 | 34.9 | 381.2 | 544.4 | 132.5 |\n| 성과 패널 2 | 591.8 | 381.2 | 333.3 | 132.5 |',
 ['카드 높이 188.5, 카드 사이 6 — 3단×2행의 행 높이와 같은 값','표 : 패널 = 544.4 : 333.3, 사이 12.5(`col2-gap`)','표 본문 14pt, 2단계 불릿 12pt, 추진노력 3줄 이내(2단계 포함 4줄)','성과 항목 제목은 14pt Bold, 설명은 12pt 한 줄']),
'L50':('L50 과제 카드 ×1 — L49의 카드 모듈 1개를 본문 높이로 키운 형태.',
 'L49와 같은 모듈에서 표·패널 높이만 327.1로 확장(참조 B 파생).',
 '추진노력이 5줄 이상이거나 성과 수치가 2개 이상인 과제.',
 '| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 배지+띠 | 34.9 | 130.7 | 890.2 | 48 |\n| 표 | 34.9 | 186.7 | 544.4 | 327.1 |\n| 성과 패널 | 591.8 | 186.7 | 333.3 | 327.1 |',
 ['표 행: 머리글 24 · 추진배경 96 · 추진노력 207.1','본문 16pt, 2단계 14pt(`.ko-b-tt.big`)','성과 패널 안 흰 수치 카드 2칸(사이 10) — 숫자 36pt Bold `teal-600`']),
'L51':('L51 정의 박스 + 포토 타임라인 — “한 줄 정의 → 연혁 사진 7칸 → 요약 3칸”.',
 '2021 기관설명회 2번 상·중(설립목적 박스, 주요연혁 사진 띠). 소제목 리듬과 7칸 간격비(카드 폭 : 사이 = 1 : 0.16)를 읽어 16:9로 재설계.',
 '소제목 3개, 정의 문장 1개, 연혁 7칸(제목 2줄 이내 + 사진 1장), 요약 3칸.',
 '| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 정의 박스 | 34.9 | 164.7 | 890.2 | 36 |\n| 포토 카드 ×7 | 34.9 + 129.75×i | 248.7 | 112 | 140 |\n| 요약 3칸 | 34.9 / 334.6 / 634.4 | 436.7 | 291.1 | 77.1 |',
 ['소제목 26 → 8 → 박스 → 14 → 다음 소제목','카드 머리 40(줄당 7자) + 사진 100','사진은 프레임 안에서만 교체(미리보기는 자리표시)']),
'L52':('L52 조직도 + 정원 표 — 이사장·부이사장 아래 직속 4곳과 본부 7칸, 아래에 정원 표.',
 '2021 기관설명회 2번 하(조직도·정원 표). 조직도 계층(진한 2칸 → 옅은 4칸 → 윤곽 7칸)과 연결선 규칙을 읽어 재설계.',
 '이사장·부이사장 2칸, 직속 4칸, 본부·단·원 7칸 이하, 표 머리글 + 2행.',
 '| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 조직도 | 34.9 | 164.7 | 890.2 | 192 |\n| 표 | 34.9 | 404.7 | 890.2 | 90 |',
 ['본부 7칸은 L51 포토 카드와 같은 격자(폭 112, 피치 129.75)','연결선 1pt `blue-bright`, 가로 버스는 박스 위 20','직속 조직(감사실·기금관리센터)은 선 없이 양 끝']),
'L53':('L53 정의 박스 + [요약 ▶ 상세] ×2행 — 왼쪽 요약 패널에서 오른쪽 상세 패널로 흐르는 2묶음.',
 '2021 기관설명회 3번. 좌우 1 : 2 분할, 화살표 구간 54, 행 높이 160 : 97로 환산. 도넛 차트는 KORAD 차트 규칙(파이 금지)에 따라 점유율 막대로 바꿈.',
 '정의 1줄, 요약 패널(수치 4항목 이내), 상세 패널(사진 3칸 또는 불릿 3줄).',
 '| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 요약 패널 1행 | 34.9 | 248.7 | 291.1 | 160 |\n| 상세 패널 1행 | 380 | 248.7 | 545.1 | 160 |\n| 요약 패널 2행 | 34.9 | 416.7 | 291.1 | 97.1 |\n| 상세 패널 2행 | 380 | 416.7 | 545.1 | 97.1 |',
 ['화살표 구간 54, 블록 화살표 40×60','요약 패널 안 점유율 막대는 KpiBreakdown 행 서식을 줄인 `.ko-b-sh`','패널 헤더 = trellis-blue 28(2행은 26)']),
'L54':('L54 번호 행 ▶ 결과 카드 + 표 ▶ 성과 카드 — 근거(번호 항목·표)에서 결과 한 장으로.',
 '2021 기관설명회 4번. 좌우 3 : 1 분할(오른쪽 = 4단 열 폭 207.4), 위 163 : 아래 138.1로 환산. 빨강 강조는 계열색(결과 = `teal-600`) + 민트 밑줄로 교체.',
 '번호 행 3개(제목 + 한 줄), 결과 카드 1개(핵심 수치), 표 머리글 + 5행, 성과 카드(막대 2개).',
 '| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 번호 행 박스 | 34.9 | 164.7 | 628.8 | 163 |\n| 결과 카드 | 717.7 | 164.7 | 207.4 | 163 |\n| 표 | 34.9 | 375.7 | 628.8 | 138.1 |\n| 성과 카드 | 717.7 | 375.7 | 207.4 | 138.1 |',
 ['화살표 구간 54','결과 카드 큰 숫자 40pt Bold `teal-600`(결과 = 그린 계열)','성과 카드 막대는 짝막대 패턴형(26, 간격 12) — 축을 줄이면 각주로 밝힘']),
}
import layouts2
layouts.ALL.update(layouts2.ALL2)

README.update({
'L55':('L55 과제 카드 ×2 · 성과 먼저 — L49에서 표와 성과 패널의 좌우를 맞바꾼 변주.','L49 파생(좌우 맞바꿈).','L49와 같음. 성과가 수치로 강할 때 결론을 먼저 읽히게 함.','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 성과 패널 | 34.9 | 186.7 / 381.2 | 333.3 | 132.5 |\n| 표 | 380.7 | 186.7 / 381.2 | 544.4 | 132.5 |',['패널 x 34.9, 표 x 380.7, 사이 12.5','배지·띠는 L49와 같음','계열 순서·색은 L49와 같음(성과 = 그린)']),
'L56':('L56 과제 카드 + 요약 3칸 — 과제 1개와 핵심 수치 3개.','L50 카드(높이 300) + L51 하단 요약 3칸 조합.','과제 카드 1개, 요약 3칸(숫자 + 설명).','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 배지+띠 | 34.9 | 130.7 | 890.2 | 48 |\n| 표 / 성과 패널 | 34.9 / 591.8 | 186.7 | 544.4 / 333.3 | 244 |\n| 요약 3칸 | 34.9 / 334.6 / 634.4 | 436.7 | 291.1 | 77.1 |',['카드 높이 300 + 사이 6 + 요약 77.1 = 본문 383.1','요약 3칸 틴트 = sky → aqua → mint','요약 숫자는 카드 성과 패널과 같은 값']),
'L57':('L57 포토 4칸 + 설명 — 사진을 크게 쓰는 연혁·사례.','L51 포토 모듈 파생(칸 7 → 4단 열, 사진 100 → 160).','소제목 1개, 4칸(제목 2줄 + 사진 + 설명 1~2줄).','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 포토 카드 ×4 | 34.9 / 262.5 / 490.2 / 717.7 | 164.7 | 207.4 | 200 |\n| 설명 박스 ×4 | 같음 | 364.7 | 207.4 | 149.1 |',['4단 열 207.4, 간격 20.2','틴트 순서 sky → aqua → mint → tint-blue-100','꺾쇠는 칸 사이 한가운데']),
'L58':('L58 조직도 + 요약 3칸 — 조직도와 핵심 인원 수치.','L52 파생(표 → 3단 요약 틴트).','조직도(7칸 이하) + 숫자 3개.','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 조직도 | 34.9 | 164.7 | 890.2 | 192 |\n| 요약 3칸 | 34.9 / 334.6 / 634.4 | 404.7 | 291.1 | 109.1 |',['조직도는 L52와 같음','요약 숫자는 정원 표 값에서 계산']),
'L59':('L59 요약 ▶ 상세 1행 + 결론 띠 — 한 묶음에 종합 결론.','L53 한 행을 확대(높이 275.2) + L23 결론 띠.','요약 패널, 상세 패널(사진 3칸 또는 불릿), 결론 1~2문장.','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 요약 패널 | 34.9 | 130.7 | 291.1 | 275.2 |\n| 상세 패널 | 380 | 130.7 | 545.1 | 275.2 |\n| 결론 띠 | 0 | 418.1 | 960 | 121.9 |',['좌우 1 : 2 + 화살표 54','패널은 결론 띠 위에서 끝남','결론 띠는 기존 ConclusionBar 그대로']),
'L60':('L60 번호 행 ▶ 결과 카드 (1묶음) — 근거 4행과 결과 한 장.','L54 위 묶음 확장(행 3 → 4, 높이 163 → 349.1).','행 4개(제목 + 한 줄), 결과 카드 1개.','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 번호 행 박스 | 34.9 | 164.7 | 628.8 | 349.1 |\n| 결과 카드 | 717.7 | 164.7 | 207.4 | 349.1 |',['3 : 1 + 화살표 54','행 피치 = 박스 높이 ÷ 행 수','행은 4개 이내']),
'L61':('L61 표 ▶ 성과 카드 (1묶음) — 표 한 개와 성과 한 장.','L54 아래 묶음 확장(+ 정의 박스, 합계 행).','정의 한 줄, 표(머리글 + 5행 + 합계), 성과 카드.','| 영역 | x | y | 폭 | 높이 |\n|---|---|---|---|---|\n| 정의 박스 | 34.9 | 164.7 | 890.2 | 36 |\n| 표 | 34.9 | 214.7 | 628.8 | 299.1 |\n| 성과 카드 | 717.7 | 214.7 | 207.4 | 299.1 |',['합계 행은 가중평균 파생값','그래프 축을 줄이면 각주 표기']),
})

for lid,fn in layouts.ALL.items():
    html=fn()
    w(f'components/Layout{lid}/preview.html',html)
    t,src,give,tbl,rules=README[lid]
    txt=f'''{t}

**출처:** {src}

**제공할 것:** {give}

**영역 (pt, 960×540 · Slides는 ×2 px):**

{tbl}

**규칙:**
'''+'\n'.join('- '+r for r in rules)+'''

- 분할 비율·간격의 근거는 `designer-rules-2021.md`, 칸 값은 `designer-grid.md` 6절입니다.
- 미리보기의 분홍 점선은 설계용 가이드이며 실제 장표에는 그리지 않습니다. 회색 점선은 공통 본문 영역입니다.
- Governing Message는 필수입니다(좌측 가로형, 헤더 아래).
- Do: 내용 구조가 맞을 때만 고르고 좌표·폭은 위 표 그대로 씁니다.
- Don't: 칸 폭·간격 변경, 모듈 밖에서 새 박스·장식 추가, 빨강 등 팔레트 밖 색 사용, 사진 프레임 크기 변경.
'''
    w(f'components/Layout{lid}/README.md',txt)

# 2) 모듈 컴포넌트
def canvas(title, sub, h, inner, name):
    return f'''<!-- @dsCard group="본문 패널" height={h} width=960 subtitle="{sub}" -->
<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><title>{name} — preview</title>
<style>html,body{{margin:0;background:var(--white);}} :root{{--ko-check-url:url("/_blob/ca89e9fc1599adfc64af693870bf5a60");}}</style>
</head>
<body>
<div class="ko-slide" style="background:var(--white);height:{h}px">
{inner}
</div>
</body>
</html>
'''
L=34.9;R=925.1;W=890.2
# SectionTitle
inner=mods.sec(L,20,'설립목적')+mods.defbox(L,54,W,'방사성폐기물의 안전하고 효율적인 관리로 국민생활의 안전과 환경보전에 기여')
inner+=mods.sec(L,114,'조직현황',' (’22.3월 현재)')+mods.defbox(L,148,W,'소제목 26 → 8 → 박스 36 → 14 → 다음 소제목')
w('components/SectionTitle/preview.html',canvas('SectionTitle','소제목 + 한 줄 정의 박스 · 2021 기관설명회 2·3번 파생',200,inner,'SectionTitle'))
w('components/SectionTitle/README.md','''SectionTitle은 본문 칸 위에 붙는 소제목(20pt Medium)과 한 줄 정의 박스(DefinitionBox)입니다. 2021 기관설명회의 “빨간 마커 소제목 + 테두리 박스”를 KORAD 색으로 옮긴 모듈입니다.

**제공할 것:** 소제목 글(보조 설명은 16pt 괄호), 정의 문장 1줄(60자 이내).

- 마커 22×22 `blue-strong` + 흰 ↘ 화살표, 글자 20pt Medium `navy-ink`, 마커와 글자 사이 8.
- 소제목 높이 26 → 아래 박스까지 8 → 박스 36 → 다음 소제목까지 14.
- 정의 박스: 흰 바탕, 1pt `blue-bright` 테두리 + 안쪽 3pt `tint-sky-50` 띠, 체크 불릿 16, 글자 16pt Medium.
- 원본의 빨간 마커는 팔레트 밖 색이라 `blue-strong`으로 바꿨습니다.
- Do: 한 장표에 소제목 3개 이내. Don't: 소제목 없이 박스만 쌓기, 마커 색 변경.

HTML 재현: `.ko-b-sec`(> `i` 마커, `small` 보조), `.ko-b-def`.
''')
# TaskCard
rp='''<div class="ko-b-pi"><div class="no">E</div><b>방폐물 재활용 플랫폼 구축</b><span>방사성의약품 수입 대체 효과 43.6억 원 발생</span></div><div class="ko-b-pi" style="margin-top:3px"><div class="no">S</div><b>협력사 상생 안전관리 강화</b><span>상주 협력사 위험성평가 우수사업장 인정</span></div><div class="ko-b-pi" style="margin-top:3px"><div class="no">G</div><b>법·윤리경영체계 확립</b><span>권익위 부패방지시책평가 최우수 등급 달성</span></div>'''
tc=mods.taskcard(20,'경영관리','01','ESG 경영 도입을 통한 KORAD 미래가치 제고','<span class="ko-highlight">ESG 확산</span> 등 국가적 ESG 인프라 확충 및 공공기관의 ESG 경영 선도 요구','<ul class="ko-b-ul"><li>경영전략과 연계한 「KORAD ESG 경영 추진 계획」 수립</li><li>ESG 성과창출 기반 강화: 추진체계(ESG 위원회·노사공동 선언)와 제도정비(ISO14001 인증)</li></ul>',544.4,132.5,591.8,333.3,rp,46)
w('components/TaskCard/preview.html',canvas('TaskCard','육각 번호 배지 + 딥블루 띠 + 라벨 표 + 성과 패널 · 2021 기관설명회 5~9번 파생',220,tc,'TaskCard'))
w('components/TaskCard/README.md','''TaskCard는 과제 한 개를 “제목 띠 → 추진배경·추진노력 표 → 추진성과 패널”로 보여 주는 카드입니다(2021 기관설명회 5~9번 서식).

**제공할 것:** 분야명(4자 이내), 번호(2자리), 과제명(30자 이내), 추진배경 1~2줄, 추진노력 불릿, 성과 항목 3~4개.

- 배지: 육각형 56×48, 바깥 `tint-blue-200` + 안쪽 3pt 들여 `ko-trellis-blue`, 번호 20pt Bold 흰색.
- 띠: 높이 32, 배지 중심에서 시작해 오른쪽 끝(925.1)까지, `ko-trellis-deep`, 분야명 14pt Medium(`tint-blue-200`) + 흰 세로선 + 과제명 20pt SemiBold 흰색.
- 표: 머리글 행(구분 / 세 부 내 용)은 윗선 1.25pt `blue-strong`만, 라벨 열 76(trellis 타일 — 추진배경 `ko-trellis-blue`, 추진노력 `ko-trellis-teal`, 흰 14pt Bold + RowLabel 그림자), 본문 14pt, 불릿 `•` 1단계 / `–` 2단계(12pt).
- 성과 패널(결과 = 그린 계열): 1pt `green-400` 테두리, `tint-mint-50` 바탕, 머리 28 `ko-trellis-green` + 흰 16pt Bold 자간 0.15em, 번호 원 `navy-deep`, 수치 `teal-600`. 요약·현황 패널은 블루(`.ko-b-rp`), 과정·상세 패널은 틸(`.is-teal`).
- 표 윗선 = 패널 윗선, 둘의 아랫선 = 카드 아랫선.
- Do: 같은 장표의 카드는 같은 높이. Don't: 배지에 분야명 넣기(원본의 4자 캡션은 띠로 옮김), 띠 오른쪽 모서리 둥글게.

HTML 재현: `.ko-b-hex`, `.ko-b-band`(> `.cat` `.dv`), `.ko-b-tt`(`th.bg` `th.ef`), `.ko-b-ul`, `.ko-b-rp`, `.ko-b-pi`.
''')
# ResultCard
nr_rows=[('경영관리','청렴도 제고를 위한 내·외부 이해관계자 소통 기회 확대 필요 등 지적사항 32건'),('주요사업','종사자 방사선 노출 저감을 위한 장기적인 노력 필요 등 지적사항 5건'),('국회','연구인력 및 R&D 확충을 위한 예산 반영 필요 지적사항 1건')]
h1=163;pitch=h1/3
nr=''.join(f'<div class="hd" style="top:{round(i*pitch+3,1)}px"><i>{i+1}</i>{t}</div><div class="tx" style="top:{round(i*pitch+29,1)}px">{d}</div>' for i,(t,d) in enumerate(nr_rows))
rcin=f'<img src="{blob("badge")}" alt="" style="width:36px;height:36px;margin-bottom:6px"><span class="t">2020년 지적사항</span><span class="big">100<small>%</small></span><span class="cap">조치완료</span>'
inner=f'<div class="ko-b-nr" style="left:{L}px;top:20px;width:628.8px;height:{h1}px">{nr}</div>'+mods.arrow(L+628.8,20+h1/2)+mods.resultcard(717.7,20,207.4,h1,rcin)
w('components/ResultCard/preview.html',canvas('ResultCard','번호 행 박스 ▶ 블록 화살표 ▶ 이중 틀 결과 카드 · 2021 기관설명회 4번 파생',200,inner,'ResultCard'))
w('components/ResultCard/README.md','''ResultCard는 “근거(번호 행 박스·표) ▶ 결과 한 장”을 잇는 모듈 3개 묶음입니다: NumberRows(번호 행 박스), FlowArrow(블록 화살표), ResultCard(이중 틀 카드). 2021 기관설명회 4번 서식입니다.

**제공할 것:** 행 제목 + 한 줄 설명 3개, 결과 카드의 한 줄 머리글·핵심 수치·결과어.

- NumberRows: 1pt `blue-bright` 테두리 + `shadow-card`, 행 머리 띠 24(`fade-blue` → 투명 그라데이션) + `navy-deep` 번호 원 18(흰 숫자) + 16pt Bold 제목, 설명은 14pt 앞에 `–`. 행 피치 = 박스 높이 ÷ 3.
- FlowArrow: 구간 54 안에 40×60 블록 화살표, `tint-blue-100` → `blue-cyan` 그라데이션. 구간은 왼쪽 모듈 폭과 오른쪽 모듈 사이.
- ResultCard(결과 = 그린 계열): 바깥 `tint-mint-50`(6pt 틀, `radius-card`) + 안쪽 흰 카드(`radius-tint`, `shadow-card`). 큰 숫자 40pt Bold `teal-600`(원본의 빨강 대체), 결과어 20pt Bold. `.ko-b-rc.is-green`.
- Do: 핵심 수치는 한 카드에 하나. Don't: 카드 안에 표·긴 문장, 숫자에 빨강·주황 사용.

HTML 재현: `.ko-b-nr`(> `.hd` `.tx`), `.ko-b-arrow`, `.ko-b-rc`(> div `.t` `.big` `.cap`).
''')
# PhotoTimeline
heads=['동굴처분시설<br>착공(’07)','공단 설립<br>(’09)','본사 이전<br>(’11)','사명 변경<br>(’13)','동굴처분시설<br>준공(’15)','품질경쟁력<br>우수기관(’20)','표층처분시설<br>인허가(’21)']
cards=''.join(mods.photocard(round(L+i*129.75,2),20,i,h,100) for i,h in enumerate(heads))+''.join(f'<div class="ko-b-chev" style="left:{round(L+i*129.75+115.9,2)}px;top:32px"></div>' for i in range(6))
w('components/PhotoTimeline/preview.html',canvas('PhotoTimeline','사진 7칸 연혁 띠 · 2021 기관설명회 2번 파생',180,cards,'PhotoTimeline'))
w('components/PhotoTimeline/README.md','''PhotoTimeline은 사진과 짧은 제목을 한 줄로 늘어놓는 연혁 띠입니다(2021 기관설명회 2번 “주요연혁”).

**제공할 것:** 칸마다 제목 2줄(줄당 7자 이내, 둘째 줄에 연도) + 사진 1장. 칸 수 7(최대).

- 칸 폭 112, 사이 17.75(= 폭의 0.16배, 원본 83 : 13.7), 피치 129.75, x 시작 34.9.
- 머리 40 `ko-trellis-deep` + 흰 14pt Medium, 사진 100(`tint-sky-50` 자리표시 + 0.5pt `blue-bright`).
- 칸 사이 ▶ 꺾쇠 10×16 `blue-bright`, 머리 높이 중앙.
- 칸 수가 4~6이면 같은 폭·피치로 왼쪽부터 채우지 말고 `designer-grid.md` 6절의 열 그리드(4단·3단)로 바꿉니다.
- Do: 사진은 프레임 안에서만 교체, 같은 크기로 자르기. Don't: 칸 폭 변경, 둥근 모서리.

HTML 재현: `.ko-b-ph`(> `.h` `.p`), `.ko-b-chev`.
''')
# OrgChart
pitch=129.75;cx=(L+R)/2;T=20
def box(cls,x,y,ww,hh,t): return f'<div class="ko-b-ob {cls}" style="left:{round(x,1)}px;top:{round(y,1)}px;width:{ww}px;height:{hh}px">{t}</div>'
def hl(x1,x2,y): return f'<div class="ko-b-ln" style="left:{round(x1,1)}px;top:{round(y,1)}px;width:{round(x2-x1,1)}px;height:1px"></div>'
def vl(x,y1,y2): return f'<div class="ko-b-ln" style="left:{round(x,1)}px;top:{round(y1,1)}px;width:1px;height:{round(y2-y1,1)}px"></div>'
o=box('top ko-trellis-deep',cx-100,T,200,30,'이사장')+box('top ko-trellis-deep',cx-100,T+74,200,30,'부이사장')+box('stf',L,T+2,112,30,'감사실')+box('stf',R-112,T+2,112,30,'기금관리센터')+box('stf',cx-172,T+37,112,30,'미래혁신실')+box('stf',cx+60,T+37,112,30,'소통협력단')+vl(cx,T+30,T+74)+hl(cx-60,cx+60,T+52)+vl(cx,T+104,T+132)
names=['경영관리본부','품질안전본부','중저준위<br>운영본부','방폐물<br>기술연구원','건설사업단','고준위추진단','방폐물<br>인재개발원']
xs=[L+i*pitch for i in range(7)]
o+=hl(xs[0]+56,xs[6]+56,T+132)+''.join(vl(x+56,T+132,T+152)+box('dv',x,T+152,112,40,n) for x,n in zip(xs,names))
w('components/OrgChart/preview.html',canvas('OrgChart','조직도 · 2021 기관설명회 2번 파생',240,o,'OrgChart'))
w('components/OrgChart/README.md','''OrgChart는 최상위 2칸 · 직속 4칸 · 소속 7칸의 3층 조직도입니다(2021 기관설명회 2번 “조직현황”).

**제공할 것:** 조직 이름(한 칸 8자, 2줄 가능). 소속은 7칸 이하.

- 최상위 200×30 `ko-trellis-deep` + 16pt Bold 흰색, 직속 112×30 `tint-sky-50` + 14pt Medium, 소속 112×40 흰 바탕 1pt `blue-bright` + 14pt Medium.
- 연결선 1pt `blue-bright`. 최상위 → 부사위 세로선, 직속 2칸은 가로선으로 세로선에 붙이고, 소속은 가로 버스(소속 상단 위 20)에서 내려 줍니다.
- 소속 7칸 격자는 PhotoTimeline과 같습니다(폭 112, 피치 129.75).
- 좌우 끝 직속(감사실·기금관리센터)은 선 없이 둡니다(원본 그대로).
- Do: 계층 3층 이내. Don't: 박스 색으로 서열 이외의 의미 부여.

HTML 재현: `.ko-b-ob`(`.top` `.stf` `.dv`), `.ko-b-ln`.
'''.replace('부사위','부이사장'))
print('layouts+modules written')
