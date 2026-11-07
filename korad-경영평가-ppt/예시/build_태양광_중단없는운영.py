# -*- coding: utf-8 -*-
"""중단없는 태양광 발전 운영을 통한 에너지 절감 — 경영평가 보고서 서사(현황 → 문제인식 → 개선노력 → 추진성과) 예시"""
import sys; sys.path.insert(0, '/home/user/claude/korad-경영평가-ppt/src')
from compose import compose
_c = lambda items, heads=None, mn=80, b=True: dict(k='cols', items=items, **({'heads': heads} if heads else {}), min=mn, bullet=b)
_b = lambda t: dict(k='banner', text=t)
_s = lambda labels, items, mn=90: dict(k='steps', labels=labels, items=items, min=mn)
def row(label, *bands): return dict(label=label, bands=list(bands))
nodes = [
 dict(t='topic', n=1, title='중단없는 태양광 발전 운영으로 기준연도 대비 2.8% 에너지 절감', chip='✔ 개선'),
 dict(t='ladder', rows=[
   row('그간의\n현 황', _c([['공휴일·휴무일에는 직원이 근무하지 않아도 서버 등 상시 가동 설비로 일정량의 전력 소모'],
                           ['태양광 발전량이 전력 소모량보다 많아지면 화재 예방을 위해 인버터 4대 중 2대를 중단하고 운영'],
                           ['혹서기 임신 직원 등으로부터 냉방에 관한 민원이 노동조합에 집중']],
                          heads=['휴일에도 계속되는 전력 소모', '발전 가능한데도 멈춰 두던 설비', '혹서기 냉방 민원 집중'], mn=110)),
   row('문제\n인 식', _b('휴일·공휴일 소모 전력량 수준으로 발전이 이루어진다면, 설비 중단 없는 태양광 발전이 가능')),
   row('개선\n노 력', _s(['① 현황 진단', '② 인버터 타이머 설치', '③ 발전량 > 소모량 감지', '④ 일시 발전 조절'],
                       [['휴일 소모 전력 수준과 발전량 비교'], ['인버터 4대에 타이머 설치(기존 2대 중단 → 4대 가동)'], ['소모량보다 발전량이 많아지면 타이머 작동'], ['일시적 전력생산 중단으로 화재 예방과 가동 유지 병행']], 124)),
 ]),
 dict(t='result', label='추진성과', items=['약 31,698kWh 추가 전력 생산으로 기준연도 대비 2.8% 에너지 절감 효과', '전년대비 혹서기 냉방기 가동시간 0시간 연장(냉방 부담 증가 없이 달성)']),
 dict(t='resultcharts', label='성과\n요약', banner='인버터 가동 확대로 추가 전력을 생산하고, 냉방 가동시간은 늘리지 않음', cards=[
     dict(lines=['추가 전력 생산', '약 31,698kWh']), dict(lines=['에너지 절감', '기준연도 대비 2.8%']), dict(lines=['혹서기 냉방기 가동', '전년대비 0시간 연장'])]),
 dict(t='sub', num='참고', box='', text='기술·제도 근거(웹 조사)'),
 dict(t='gridtable', header=['구 분', '내 용', '출 처'], col_w=[15, 58, 27], merge_cols=(), align=['c', 'l', 'l'], bold_cols=(0,), rows=[
     ['자가소비형\n태양광 원리', '자가소비형 설비에서 역송(한전 계통으로의 전력 역류)이 생기지 않도록 인버터 출력을 자동 조정하는 ‘역송전 제어’ 기술이 상용화되는 추세', '전기신문 ‘멈춤 없이 가동한다…역송전 제어’'],
     ['역송 시 설비\n정지 위험', '50kW 이상 발전소는 상계처리를 신청하지 않으면 역전력계전기 설치 대상이며, 역송이 발생하려 하면 태양광 차단기가 차단됨', 'Zurigo 에너지 브리프(자가소비형 초과발전 처리방식)'],
     ['공공기관\n정책 연계', '「공공기관 에너지이용 합리화 추진에 관한 규정」(2026.4.30. 시행)이 BEMS·ESS·AMI 등 의무를 강화해 에너지 절감 노력이 중요', '국가법령정보센터, 법률 해설 자료']]),
 dict(t='note', text='* 근거는 웹 조사 자료이며 KORAD 실적 아님'),
]
d, f = compose(dict(start_no=1, first='odd', name='에너지 절감', note='작성 초안: 괄호·표의 기술 근거는 웹 조사, 수치는 제공받은 내용 기준', nodes=nodes), sys.argv[1])
print('쪽', f.pages(), '경고', d.warn)
