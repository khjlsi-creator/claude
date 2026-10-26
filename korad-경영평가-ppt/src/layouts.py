# -*- coding: utf-8 -*-
"""번호 붙은 레이아웃 카탈로그 — KORAD 디자인 시스템(L01~L61)과 같은 방식.
RL = 영역 레이아웃(서사 단락 하나가 차지하는 영역 구성), PL = 쪽 조합(레시피).
각 레이아웃은 샘플 노드와 근거 쪽(참조 지면 쪽 번호)을 가진다."""
from recipes import R, NOTE

K = {k.split()[0]: v for k, v in R.items()}
from recipes import R as _R
CH = dict(t='chapter', title='Ⅲ. 2025년도 추진실적 및 성과')


def N(letter, *idx):
    return [K[letter][i] for i in idx]


CH = dict(t='chapter', title='Ⅲ. 2025년도 추진실적 및 성과')

LAYOUTS = [
 dict(id='RL01', name='장 제목 띠', when='지면 첫 쪽 맨 위. 장 제목 한 줄과 오른쪽 CI 칸.', src='93', nodes=[CH]),
 dict(id='RL02', name='평가내용 + 번호 띠', when='평가내용을 알리고 대주제로 들어갈 때. 평가내용 제목이 한 줄이면 63px, 두 줄이면 109px.', src='93, 95, 97', nodes=N('A', 0, 1)),
 dict(id='RL03', name='소제목 + 태그칩', when='가·나·다 소제목. 태그칩(신규·강화·B.P·지적·개선) 0~2개, 글자 아래 민트 형광 밑줄.', src='93~98', nodes=N('A', 2)),
 dict(id='RL04', name='환경분석 → 시사점 → 협력체계', when='진단에서 시사점을 뽑고 체계를 세우는 3단계 서사(블루→틸→딥블루 레일).', src='93', nodes=N('A', 3)),
 dict(id='RL05', name='현황 → 이해관계 → 추진노력 + 성과 사이드', when='현안 해결 서사. 사다리 오른쪽에 성과 패널이 삼각형 화살표로 붙는다.', src='94', nodes=N('C', 2)),
 dict(id='RL06', name='단계 추진(그간의 노력 → 상세화 → 선임 추진)', when='시간순 추진 경과. 마지막 단계는 4단계 단계 띠(칸 끝 삼각형).', src='94', nodes=N('D', 1)),
 dict(id='RL07', name='수준진단 → 공감대 형성 → 시사점', when='진단 한 줄, 대표 발언(두 칸), 시사점 태그 줄로 이어지는 소통 서사.', src='95', nodes=N('F1', 3)),
 dict(id='RL08', name='공감대 → 선언(사진) → 확산(배너)', when='선언·행사·협약처럼 사진이 붙는 서사. 레일에 결실·확산 태그.', src='95', nodes=N('F2', 2)),
 dict(id='RL09', name='추진성과 레일(그린)', when='사다리 끝에 성과를 두 칸으로 못 박을 때. 그린 레일과 그린 외곽선.', src='95', nodes=N('F2', 3)),
 dict(id='RL10', name='협의체 참여 · 외부역량 활용', when='배너 + 3칸 + 태그 줄을 한 단계에 쌓는 운영 서사.', src='96', nodes=N('G', 6)),
 dict(id='RL11', name='이해관계 → 의견조율 → 협약체결(인라인 표)', when='갈등을 풀어 합의에 이르는 서사. 칸 안에 수치 표를 넣을 수 있다.', src='97', nodes=N('H', 5)),
 dict(id='RL12', name='이해관계 → 교섭(사진 열)', when='교섭 경과에 합의서·체결식 사진이 오른쪽에 여러 행에 걸쳐 붙는다.', src='98', nodes=N('I1', 4)),
 dict(id='RL13', name='현황 · 문제점 · 노사 공동노력', when='짧은 한 줄 행 둘 + 3칸 대응 행. 레일은 같은 색.', src='98', nodes=N('I2', 1)),
 dict(id='RL14', name='추진 체계 5행(목표·방향·과제·채널·지표)', when='전략 체계를 라벨 박스 행으로 쌓는다.', src='93', nodes=N('A', 5)),
 dict(id='RL15', name='추진배경 · 점검방법', when='배경과 방법을 한 줄씩. 아래에 주석이 붙을 수 있다.', src='94', nodes=N('E', 1)),
 dict(id='RL16', name='점검항목 · 점검결과', when='머리칸 3개 항목 행 + 결과 3칸 행.', src='94', nodes=N('E', 3)),
 dict(id='RL17', name='비전 · 환경 · 목표 · 방향', when='비전 한 줄, 환경분석 2칸, 목표 바, 방향 3칸을 쌓는다.', src='96', nodes=N('G', 2)),
 dict(id='RL18', name='환경분석 + 칸 안 라벨 소행', when='한 칸 안에 TF·위원회별 소항목이 들어갈 때.', src='98', nodes=N('I1', 2)),
 dict(id='RL19', name='두 갈래 패널', when='정기 | 상시처럼 좌우 두 갈래를 행마다 맞춘다.', src='93, 95', nodes=N('B', 1)),
 dict(id='RL20', name='3분할 패널 + 요약 바', when='병렬 3갈래를 머리·불릿·하단 수치 바로 보여 준다.', src='98', nodes=N('I2', 4)),
 dict(id='RL21', name='실적 구분표', when='구분 × 내용 실적 나열. 앞 두 열 자동 병합, 편집 가능한 표.', src='96', nodes=N('G', 4)),
 dict(id='RL22', name='핵심성과 한 줄 띠', when='단락 끝 성과 한 줄.', src='93~98', nodes=N('A', 6)),
 dict(id='RL23', name='핵심성과 두 줄 띠', when='성과가 둘 이상일 때 불릿으로.', src='94', nodes=N('E', 4)),
 dict(id='RL24', name='추진성과 띠', when='사다리 바로 아래 추진성과 한 줄(라벨만 다름).', src='94, 98', nodes=N('D', 2)),
]

CHAPTER = [CH]


def _cut(letter, *drop):
    return [n for i, n in enumerate(K[letter]) if i not in drop]


# PL = 참조 보고서 한 쪽(93~98쪽)을 A4 한 쪽에 꽉 채운 조합. 서사 대목(RL)을 쌓아 한 쪽을 채운다.
PL_NODES = {
 'PL01': CHAPTER + K['A'][:6] + K['B'][:2] + [K['A'][6]],
 'PL02': _cut('C', 3) + K['D'] + K['E'],
 'PL03': K['F1'][:4] + K['F1'][5:] + K['F2'],
 'PL04': K['G'],
 'PL05': K['H'] + K['H2'],
 'PL06': K['I1'] + K['I2'],
}
PAGES = [
 ('PL01', 'PL01', '전략 수립 + 운영 현황면', '장 제목 → 평가내용 → 번호 띠 → 사다리 3단 → 추진 체계 5행 → 두 갈래 패널 → 핵심성과', '93'),
 ('PL02', 'PL02', '현안 해결 + 단계 추진 + 점검면', '번호 띠 → 사다리(성과 사이드) → 사다리(단계 띠) → 추진성과 → 점검 체계 → 핵심성과 2줄', '94'),
 ('PL03', 'PL03', '소통·공감대 + 상생의 달면', '평가내용 → 사다리 3단 → 두 갈래 패널 → 선포(사진)·확산 → 성과 레일 → 핵심성과', '95'),
 ('PL04', 'PL04', '교육체계 + 협의체 참여면', '번호 띠 → 비전·환경·방향 → 실적표 → 협의체 참여·외부역량 → 핵심성과', '96'),
 ('PL05', 'PL05', '임금·단체협약면', '평가내용 → 임금협약(환경·이해관계·의견조율·협약체결) → 단체협약(사진) → 핵심성과', '97'),
 ('PL06', 'PL06', '근로환경·복리후생면', '번호 띠 → 환경분석(소행) → 교섭(사진 열) → 현황·문제점 → 성과 → 3분할 패널 → 핵심성과', '98'),
]


def catalog_spec():
    """PL 6쪽을 이어 붙인 카탈로그(홀수·짝수쪽 교대)"""
    nodes = []
    for i, pid in enumerate(PL_NODES):
        if i: nodes.append(dict(t='newpage'))
        nodes += PL_NODES[pid]
    return dict(start_no=93, first='odd', note=NOTE, nodes=nodes)
