# -*- coding: utf-8 -*-
"""KORAD 경영평가 PPT 시스템 — 경영실적보고서 지면(A4 세로) 기준 재설계."""
import sys
from kp import *
from data import TYPES, ORGS, stats
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

OUT = sys.argv[1] if len(sys.argv) > 1 else 'KORAD_경영평가_노사관계_A4세로.pptx'
d = Deck()
prim, sec, lab, ov = stats()
CRUMB = 'Ⅰ. 경영관리 | 04. 조직 운영 및 관리 | 노사관계'
CRUMB_R = 'KORAD 경영평가 | 노사관계 지표 전수검토'
SRC = '자료: 기관별 공식평가 재검증(2026.9.24.)'
WARN = []

L = lambda t, **k: dict(t=t, sz=SZ_BODY, bullet='○', hang=4.2, after=1.5, **k)
Q = lambda t, **k: dict(t=t, sz=SZ_BODY, bullet='□', b=True, hang=4.2, after=2, **k)
N = lambda t, **k: dict(t=t, sz=SZ_BODY, bullet='※', color=C['slate_700'], hang=4.2, after=1, **k)
EASY = lambda t: dict(runs=[('쉽게 말하면) ', dict(b=True)), (t, {})], sz=SZ_BODY, bullet='○', hang=4.2, after=1.5)
G = lambda o: f'{o[1]} / {o[2]}'


def ph(paras, w):
    h = 0.0
    for p in paras:
        txt = p.get('t') or ''.join(r[0] for r in p['runs'])
        ind = (p.get('hang', 0) + p.get('indent', 0)) if p.get('bullet') else 0
        h += est_lines(txt, w - ind, p.get('sz', SZ_BODY)) * 4.95 + p.get('after', 0) * 0.3528
    return h


def fit(s, y, lim=BODY_B, tag=''):
    if y > lim + 0.01:
        WARN.append(f'slide {len(d.prs.slides)} {tag}: y={y:.1f} > {lim}')


# ---------------------------------------------------------------- 공통 부품
def sbar(s, y, text, h=8.5):
    """섹션 띠(평가내용 N …) — 15pt 굵게 흰 글자"""
    bar = d.rect(s, CX0, y, CW, h, fill=C['blue_deep'], name='섹션 띠')
    d.fill_text(bar, [dict(t=text, sz=SZ_TITLE, b=True, color=C['white'])], anchor='m', margins=(3, 0, 3, 0))
    return y + h + 2.5


def title_row(s, y, text, chips, h=8.0):
    """추진실적 제목(15pt) + 우측 라벨(14pt)"""
    d.text(s, CX0, y, 108, h, [dict(t=text, sz=SZ_TITLE, b=True)], anchor='m', name='추진실적 제목')
    x = CX1
    for t, w, fill, col in reversed(chips):
        x -= w
        d.badge(s, x, y + 0.5, w - 1.5, h - 1.0, t, fill=fill, color=col, name='라벨')
    return y + h + 2.5


def result_band(s, y, label, runs, h=15):
    """성과 띠(result_box): 남색 바탕 + 라벨"""
    d.rect(s, CX0, y, CW, h, fill=C['navy_band'], name='성과 띠')
    d.badge(s, CX0 + 2.5, y + (h - 8) / 2, 20, 8, label, fill=C['blue_bright'], color=C['white'], name='성과 라벨')
    d.text(s, CX0 + 26, y, CW - 30, h, [dict(runs=runs, sz=SZ_BODY, color=C['white'])], anchor='m', name='성과 문구')
    return y + h + 3


def KW(t):
    return (t, dict(color=C['cyan_hl'], b=True))


def TX(t):
    return (t, {})


def hero_strip(s, y, items, h=22):
    """hero_kpi_strip: 라벨(12) + 값(14 굵게) 칸 n개"""
    n = len(items)
    gap = 3.0
    w = (CW - gap * (n - 1)) / n
    for i, (lbl, val, sub) in enumerate(items):
        x = CX0 + i * (w + gap)
        d.text(s, x, y, w, h, [dict(t=lbl, sz=SZ_BODY, align='c', after=1), dict(t=val, sz=SZ_SHAPE, b=True, color=C['blue_strong'], align='c', after=1),
                               dict(t=sub, sz=SZ_BODY, align='c', color=C['slate_700'])], anchor='m', fill=C['tint_sky'], line=C['tint_200'], name='핵심 수치')
    return y + h + 3


# =========================================================== 1. 표지
s = d.prs.slides.add_slide(d.lay['표지'])
s.shapes.title.text_frame.text = '공공기관 노사관계 지표\n전수검토'
for p in s.placeholders:
    if p.placeholder_format.idx == 1:
        p.text_frame.text = '종합 B등급 이상 44개 기관의 서사 유형과\nKORAD 경영실적보고서 지면 레이아웃(A4 세로)'
d.badge(s, CX0 + 6, 66, 62, 8.0, 'KORAD 경영평가 · 노사관계', fill=C['tint_200'], color=C['navy'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5, name='표지 라벨')
d.badge(s, CX0 + 6, 168, 46, 8.0, '2026. 10. 26. (월)', fill=C['tint_200'], color=C['navy'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5, name='표지 일자')

# =========================================================== 2. 보고요지
s = d.body(CRUMB_R, '보고요지: 노사 우수는 \'채널\'이 아니라 닫힌 고리에서 갈리고, 지면은 보고서 형식을 따른다', SRC)
y = BODY_Y
bar = d.rect(s, CX0, y, CW, 8.5, fill=C['blue_deep'], name='보고요지 띠')
d.fill_text(bar, [dict(t='보고요지', sz=SZ_TITLE, b=True, color=C['white'])], anchor='m', margins=(3, 0, 3, 0))
y += 11
paras = [
    Q('종합 B등급 이상 44개 기관(A 15·B 29)의 노사관계 공식 평가를 전수 분류'),
    L('노사 B0 이상은 15개(34%), C는 20개(45%), D+는 9개(20%) — 종합등급이 노사 우수성을 보장하지 않음'),
    L('실적 서사는 8유형이며 37개 기관이 분류되고 7개는 상세 문장 미확인'),
    Q('레이아웃은 일반 PPT가 아니라 경영실적보고서 지면 체계로 설계'),
    L('보고서 순서: 지표 개요 → 지표 차례 → Ⅰ 지적사항 조치실적 → Ⅱ 주요 추진실적 → Ⅲ 평가내용별 추진실적'),
    L('평가내용별 추진실적(FULL·HALF BP)에 8유형 본문 모듈을 끼우고, 하단 성과 띠로 마무리'),
    Q('A4 세로, 여백 좌우 15·상하 10mm, 글자 12·14·15pt로 마스터에 고정'),
]
hh_ = ph(paras, CW) + 3
d.text(s, CX0, y, CW, hh_, paras, name='보고요지 본문')
y += hh_ + 6
bar = d.rect(s, CX0, y, CW, 8.5, fill=C['tint_sky'], name='핵심 진단 띠')
d.fill_text(bar, [dict(t='핵심 진단', sz=SZ_TITLE, b=True, color=C['navy'])], anchor='m', margins=(3, 0, 3, 0))
y += 11
rows = [['구분', '확인된 흐름', '지면 반영'],
        ['최다 서사', '법제·준법 선제대응형 9개 기관(주 유형 기준)', 'BP 모듈 C 위험·통제·잔여 표'],
        ['등급 편차', '노사 B0 이상 비율 — 에너지 공기업 83%, 기금관리 0%', '보고요지·분포 표'],
        ['반복 지적', '미종결 안건·대표성·효과 검증이 공통', 'Ⅰ 지적사항 조치실적 지면']]
gf, th = d.table(s, CX0, y, [26, 88, 66], rows, name='핵심 진단 표', label_col=True)
y += th + 3
d.text(s, CX0, y, CW, 16, [N('서사 분류는 분석자 판단이며 공식 경영평가 체계가 아님. 근거는 2025 공식 평가 재검증 문서.')], name='주석')
fit(s, y + 10, BODY_B_FREE, '보고요지')

# =========================================================== 3. 목차
s = d.body(CRUMB_R, '목차', SRC)
toc = [('Ⅰ', '검토 개요', '4'), ('Ⅱ', '44개 기관 전수 분류와 서사 유형', '5'), ('Ⅲ', '경영실적보고서 지면 체계(원본 구조)', '8'),
       ('Ⅳ', '지면 레이아웃 R0~R4 (지표 간지·개요·차례·지적사항·주요실적)', '9'), ('Ⅴ', '평가내용별 추진실적 BP 모듈 A~H', '14'),
       ('Ⅵ', '반쪽 BP·성과 입증 지면과 A4 표준', '22')]
y = BODY_Y + 6
for no, t, pg in toc:
    d.text(s, CX0 + 2, y, 14, 9, [dict(t=no, sz=SZ_TITLE, b=True, color=C['blue_strong'], align='c')], anchor='m', name='목차 번호')
    d.text(s, CX0 + 18, y, 140, 9, [dict(t=t, sz=SZ_TITLE)], anchor='m', name='목차 제목')
    d.text(s, CX1 - 16, y, 14, 9, [dict(t=pg, sz=SZ_TITLE, b=True, color=C['number_muted'], align='r')], anchor='m', name='쪽')
    d.line(s, CX0 + 18, y + 11, CX1 - 2, y + 11, color=C['blue_bright'], w=0.75)
    y += 19
d.tint_box(s, CX0, y + 4, CW, 34, [Q('읽는 순서'), L('Ⅰ~Ⅱ에서 44개 기관을 분류하고, Ⅲ에서 실제 보고서 지면 구조를 확인'),
                                 L('Ⅳ~Ⅵ에서 지면별 레이아웃을 사례와 함께 제시')])

# =========================================================== 4. Ⅰ 검토 개요
s = d.body(CRUMB_R, '1-1. 종합 B등급 이상 44개 기관 중 노사 우수는 15개', SRC)
y = BODY_Y
cw = (CW - 2 * 4) / 3
cards = [('검토 기관', '44개', '종합 A 15 · B 29'), ('노사 B0 이상', '15개 (34%)', 'B+ 2 · B0 13'), ('노사 D+', '9개 (20%)', 'KORAD 포함')]
for i, (a, b, c) in enumerate(cards):
    x = CX0 + i * (cw + 4)
    d.text(s, x, y, cw, 25, [dict(t=a, sz=SZ_BODY, align='c', after=1), dict(t=b, sz=SZ_SHAPE, b=True, color=C['blue_strong'], align='c', after=1),
                              dict(t=c, sz=SZ_BODY, align='c')], anchor='m', fill=C['tint_sky'], line=C['tint_200'], name='핵심 수치')
y += 29
d.pill(s, CX0 + CW / 2 - 40, y, 80, '종합등급 × 노사등급 (기관 수)')
y += 9
rows = [['구분', '노사 B+ · B0 (15)', '노사 C (20)', '노사 D+ (9)'],
        ['종합 A (15)',
         '남동(B+)·한전·남부·수력원자력·한전KDN·산업기술진흥원·예금보험공사·교통안전공단',
         '조폐·KOTRA·무역보험·건보심사평가원·근로복지·가스안전', '국민연금'],
        ['종합 B (29)',
         '도로공사(B+)·중부·부동산원·한전KPS·수자원·관광·산업기술기획평가원',
         '지역난방·마사회·인천공항·산단공·에너지공단·지능정보원·중진공·주택금융·사회보장정보원·소비자원·장학·환경공단·산업안전보건·전기안전',
         '주택도시보증·LH·소진공·농수산유통·보훈복지의료·재정정보원·KORAD·전력거래소']]
gf, th = d.table(s, CX0, y, [24, 52, 56, 48], rows, name='종합×노사 매트릭스', label_col=True)
y += th + 4
d.tint_box(s, CX0, y, CW, 24, [EASY('학교 전체 석차(종합)가 상위권이어도 \'대인관계\' 과목(노사)은 낙제점일 수 있습니다. 종합 A 15개 중 노사 C 이하가 7개입니다.')])
y += 28
d.text(s, CX0, y, CW, 24, [N('B등급 이상은 종합등급 A·B 기준(분석자 해석). 노사 B+·B0를 우수군으로 봄.'), N('기관명은 줄여 표기. 등급은 2025 공식 평가 재검증 문서 기준.')], name='주석')
fit(s, y + 14, BODY_B_FREE, '개요')


# =========================================================== 5~6. 전수 분류
def class_rows(sub):
    rows = [['기관', '종합 / 노사', '주 서사 유형', '보조 유형']]
    for o in sub:
        sec_txt = ' · '.join(TYPES[t][0] for t in o[5]) if o[5] else '―'
        rows.append([dict(t=o[0]), dict(t=G(o), b=o[2] in ('B+', 'B0')), TYPES[o[4]][0] if o[4] != 'U' else dict(t='미분류(건수만 확인)', color=C['slate_500']), sec_txt])
    return rows


for part, sub, ttl in ((1, ORGS[:22], '1/2'), (2, ORGS[22:], '2/2')):
    s = d.body(CRUMB_R, f'2-1. 기관별 주 서사 유형 ({ttl})', '자료: 공식평가 재검증(2026.9.24.) · 분석자 분류')
    gf, th = d.table(s, CX0, BODY_Y, [48, 24, 50, 58], class_rows(sub), align=['l', 'c', 'l', 'l'], min_row=6.6, row_pad=0.9, name=f'분류표 {ttl}')
    y = BODY_Y + th + 3
    d.text(s, CX0, y, CW, 14, [N('굵게 표시한 등급은 노사 B+·B0(우수군). 주 유형은 기관 실적 서사의 중심, 보조 유형은 함께 나타난 서사.')], name='주석')
    fit(s, y + 10, BODY_B_FREE, f'분류{ttl}')

# =========================================================== 7. 분포 차트
s = d.body(CRUMB_R, '2-2. 법제·준법형이 가장 많고, 교육 적용형은 보조 서사로 나타남', SRC)
cats = ['폐쇄루프', '협의체', '법제·준법', '다층소통', '지표개선', '제도변화', '교육적용', '위기·전환', '미분류']
keys = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'U']
cd = CategoryChartData()
cd.categories = cats
cd.add_series('주 서사 (기관 수)', [prim.get(k, 0) for k in keys])
cd.add_series('보조 서사 (기관 수)', [sec.get(k, 0) for k in keys])
gfc = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, mm(CX0), mm(BODY_Y + 9), mm(CW), mm(96), cd)
gfc.name = '유형별 분포 차트'
ch = gfc.chart
ch.font.size = Pt(SZ_BODY); ch.font.name = FONT; ch.font.color.rgb = rgb(C['navy'])
ch.has_title = False
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
ch.legend.font.size = Pt(SZ_BODY)
va = ch.value_axis; va.maximum_scale = 10; va.minimum_scale = 0; va.major_unit = 2
va.major_gridlines.format.line.color.rgb = rgb(C['rule_pale']); va.format.line.fill.background()
va.tick_labels.font.size = Pt(SZ_BODY)
ca = ch.category_axis; ca.tick_labels.font.size = Pt(SZ_BODY); ca.format.line.color.rgb = rgb(C['slate_300'])
pl = ch.plots[0]; pl.gap_width = 60; pl.overlap = -10
pl.has_data_labels = True
dl = pl.data_labels; dl.font.size = Pt(SZ_BODY); dl.position = XL_LABEL_POSITION.OUTSIDE_END; dl.show_value = True
sr = pl.series
sr[0].format.fill.patterned(); sr[0].format.fill.pattern = MSO_PATTERN.WIDE_UPWARD_DIAGONAL
sr[0].format.fill.fore_color.rgb = rgb(C['chart_cyan']); sr[0].format.fill.back_color.rgb = rgb(C['blue_cyan'])
sr[1].format.fill.patterned(); sr[1].format.fill.pattern = MSO_PATTERN.WIDE_UPWARD_DIAGONAL
sr[1].format.fill.fore_color.rgb = rgb(C['chart_base']); sr[1].format.fill.back_color.rgb = rgb('CCD9F0')
d.badge(s, CX0, BODY_Y, 88, 7.0, '유형별 기관 수 (주 37 · 미분류 7)', fill=C['blue_deep'], name='차트 제목')
y = BODY_Y + 108
d.tint_box(s, CX0, y, CW, 64, [Q('읽는 법'),
                                 L('주 서사는 기관당 1개(37개 기관), 보조 서사는 기관당 0~2개로 중복 집계'),
                                 L('법제·준법형 9개: 노란봉투법·사용자성·준법점검을 중심에 둔 기관이 많음'),
                                 L('교육 적용형은 주 서사가 없고 5개 기관에서 보조 서사로만 등장'),
                                 N('미분류 7개: 인천공항·KOTRA·소진공·산단공·에너지공단·지능정보원·사회보장정보원은 공식 문장 수만 확인')], fill=C['tint_sky'])
fit(s, y + 64, BODY_B_FREE, '분포')

# =========================================================== 8. Ⅲ 보고서 지면 체계
s = d.body(CRUMB_R, '3-1. 보고서는 지표 개요에서 평가내용별 추진실적 순으로 구성된다', '자료: 한국재정정보원·보훈복지의료공단 보고서 구성 · KPE 지면 역할')
rows = [['지면', '보고서에서 하는 일', '지면 역할 · 점유', '레이아웃'],
        ['지표 간지', '장 번호·장 제목, 지표 목록과 쪽', '구분 · FULL', 'R0'],
        ['지표 개요', '지표명·가중치·평가방법·지표정의·평가내용·담당자표', '개요 · FULL', 'R1'],
        ['지표 차례', 'Ⅰ 지적사항, Ⅱ 주요 추진실적, Ⅲ 평가내용별 추진실적 쪽 안내', '안내 · FULL', 'R2'],
        ['Ⅰ 지적사항 조치', '지적 → 조치 → 개선효과 → 잔여 Gap 추적', 'PR04 · FULL/HALF', 'R3'],
        ['Ⅱ 주요 추진실적', '전년 수준 → 금년 변화 → 개선효과 요약', 'PR01 · FULL', 'R4'],
        ['Ⅲ 추진실적', '평가내용 N 아래 추진실적 BP: 두괄식 제목, 본문 모듈, 성과 띠', 'PR03 · FULL BP', 'R5 A~H'],
        ['반쪽 BP', '서로 다른 두 사례를 한 쪽에 위아래로', 'PR03 · HALF×2', 'R6'],
        ['성과·효과', 'Before/After, 수혜 범위, 재측정', 'PR05 · FULL', 'R7']]
gf, th = d.table(s, CX0, BODY_Y, [32, 78, 44, 26], rows, name='지면 체계표', label_col=True, align=['c', 'l', 'l', 'c'])
y = BODY_Y + th + 4
d.tint_box(s, CX0, y, CW, 50, [Q('원본 보고서에서 확인한 것'),
                              L('지표 쪽은 지표명·가중치·평가방법·지표정의·평가내용·담당자표로 시작'),
                              L('이어 Ⅰ 외부 지적사항 조치실적 → Ⅱ 주요 추진실적 → Ⅲ 세부평가내용별 추진실적 순'),
                              N('KORAD 보고서 쪽(104~112)은 이미지 PDF라 텍스트로 읽지 못해 다른 기관 구성과 KPE 지면 규칙으로 보완')], fill=C['tint_sky'])
fit(s, y + 50, BODY_B_FREE, '지면체계')

# =========================================================== 9. R0 지표 간지 (간지 레이아웃)
s = d.prs.slides.add_slide(d.lay['간지'])
for p in s.placeholders:
    if p.placeholder_format.idx == 13:
        p.text_frame.text = '04'
    elif p.placeholder_format.type is not None and p.placeholder_format.idx == 0:
        p.text_frame.text = '조직 운영 및 관리'
items = ['조직 및 인적자원관리 ··············· [00]', '노사관계 ··············· [00]', '보수 및 복리후생 ··············· [00]', '총인건비 관리(계량) ··············· [00]']
d.text(s, CX0 + 6, 186, CW - 12, 50, [dict(t=t, sz=SZ_TITLE, color=C['white'], after=3, b=(i == 1)) for i, t in enumerate(items)], name='지표 목록')
d.text(s, CX0 + 6, 98, CW - 12, 9, [dict(t='Chapter  경영관리', sz=SZ_TITLE, color=C['white'])], name='장 이름')
d.text(s, CX0 + 6, CY1 - 16, 100, 8, [dict(t='한국원자력환경공단', sz=SZ_TITLE, color=C['white'], b=True)], name='기관명')

# =========================================================== 10. R1 지표 개요
s = d.body(CRUMB, 'R1. 지표 개요: 지표명·가중치·평가방법을 먼저 보이고 지표정의와 평가내용을 이어 쓴다', '자료: 2026 경영평가편람 노사관계 · 담당자는 기재', nav=0)
y = BODY_Y
rows = [['지표명', dict(t='노사관계', b=True), '가중치', '2.5점', '평가방법', '비계량']]
gf, th = d.table(s, CX0, y, [24, 44, 24, 24, 28, 36], rows, head=False, name='지표 기본정보', min_row=9)
y += th + 3
rows = [['지표정의', '협력체계의 적법·실질 운영, 의사소통과 관리역량 강화, 노사협력을 통한 근로조건의 실질적 향상을 함께 평가한다.']]
gf, th = d.table(s, CX0, y, [24, 156], rows, head=False, label_col=True, name='지표정의', min_row=14)
y += th + 3
rows = [['평가내용', '① 협력체계의 적법·실질 운영 — 노사공동 준법점검, 근로시간면제, 적법도급, 현장관리 기준\n② 의사소통과 관리역량 강화 — 전 계층 맞춤교육, 전문가 육성체계, 노동이사·노조간부 역량\n③ 근로조건의 실질적 향상 — 실제 합의·규정·근로조건 변화와 사후이행']]
gf, th = d.table(s, CX0, y, [24, 156], rows, head=False, label_col=True, name='평가내용', min_row=30)
y += th + 4
d.pill(s, CX0, y, 40, '담당자')
y += 9
rows = [['직위', '성명', '연락처', 'E-mail'], ['[직위 기재]', '[성명]', '[000-000-0000]', '[이메일]'], ['[직위 기재]', '[성명]', '[000-000-0000]', '[이메일]'], ['[직위 기재]', '[성명]', '[000-000-0000]', '[이메일]']]
gf, th = d.table(s, CX0, y, [44, 36, 46, 54], rows, name='담당자표', align=['c', 'c', 'c', 'c'])
y += th + 4
d.text(s, CX0, y, CW, 16, [N('세부평가내용은 2026 경영평가편람 기준이며 해당 연도 편람으로 교체. 대괄호는 기재 항목.')], name='주석')
fit(s, y + 10, BODY_B, 'R1')

# =========================================================== 11. R2 지표 차례
s = d.body(CRUMB, 'R2. 지표 차례: Ⅰ 지적사항, Ⅱ 주요 추진실적, Ⅲ 평가내용별 추진실적 쪽을 안내한다', '자료: 지표 쪽 구성 · 쪽 번호는 기재', nav=0)
y = BODY_Y + 2
toc = [('Ⅰ', '외부 지적사항 조치실적', '[00]', True), ('Ⅱ', '2025년 주요 추진실적', '[00]', True), ('Ⅲ', '2025년 세부평가내용별 추진실적', '[00]', True)]
for no, t, pg, big in toc:
    d.text(s, CX0, y, 14, 8, [dict(t=no, sz=SZ_TITLE, b=True, color=C['blue_strong'], align='c')], anchor='m', name='장 번호')
    d.text(s, CX0 + 16, y, 130, 8, [dict(t=t, sz=SZ_TITLE, b=True)], anchor='m', name='장 제목')
    d.text(s, CX1 - 18, y, 16, 8, [dict(t=pg, sz=SZ_TITLE, b=True, align='r')], anchor='m', name='쪽')
    y += 11
y += 2
for k in (1, 2, 3):
    bar = d.rect(s, CX0, y, CW, 8.5, fill=C['tint_100'], name='평가내용 띠')
    d.fill_text(bar, [dict(t=f'평가내용 {k}  [세부평가내용 제목 기재]', sz=SZ_TITLE, b=True, color=C['navy'])], anchor='m', margins=(3, 0, 3, 0))
    y += 10.5
    for j in (1, 2):
        d.text(s, CX0 + 6, y, 150, 7, [dict(t=f'{j}. [추진실적 제목 기재] ··················································', sz=SZ_BODY)], anchor='m', name='추진실적 목차')
        d.text(s, CX1 - 18, y, 16, 7, [dict(t='[00]', sz=SZ_BODY, align='r')], anchor='m', name='쪽')
        y += 7.5
    y += 3
d.text(s, CX0, y, CW, 14, [N('평가내용은 지표당 3개 안팎, 평가내용마다 추진실적 1~5건. 쪽 번호는 조판 후 기재.')], name='주석')
fit(s, y + 10, BODY_B, 'R2')

# =========================================================== 12. R3 지적사항 조치실적 (PR04)
s = d.body(CRUMB, 'R3. Ⅰ 외부 지적사항 조치실적: 지적 → 조치 → 개선효과 → 잔여 Gap을 한 줄로 이어 쓴다', '자료: KORAD 평가문장(R4094~R4106) 지적 · 조치는 기재', nav=0)
y = BODY_Y
y = sbar(s, y, 'Ⅰ  외부 지적사항 조치실적')
rows = [['No', '외부 지적사항(2025 평가)', '조치내용', '개선효과', '잔여 Gap·후속'],
        ['1', '경비 교대제·피복·출퇴근버스 등 장기 안건의 종결관리', '[조치 기재]', '[효과 기재]', '[잔여·기한]'],
        ['2', '사용자성 판단회의체·현장관리자 가이드의 사전 모의 적용·현장 검증', '[조치 기재]', '[효과 기재]', '[잔여·기한]'],
        ['3', '공무직·교대직군 인식 차이의 집단별 환류', '[조치 기재]', '[효과 기재]', '[잔여·기한]'],
        ['4', '내부 HRM·노무 전문성 투자 성과 관리', '[조치 기재]', '[효과 기재]', '[잔여·기한]'],
        ['5', '제도 개선 이후 조직문화·재발방지 효과의 정량 확인', '[조치 기재]', '[효과 기재]', '[잔여·기한]'],
        ['6', '협력사 안전관리 역량의 현장 확산 검증', '[조치 기재]', '[효과 기재]', '[잔여·기한]']]
gf, th = d.table(s, CX0, y, [10, 70, 34, 32, 34], rows, name='지적-조치 추적표', fill_to=BODY_B - 46, align=['c', 'l', 'l', 'l', 'l'], row_pad=2.2, min_row=17)
y += th + 4
y = result_band(s, y, '환류', [TX('조치 완료'), TX('가 아니라 '), KW('효과와 잔여 Gap'), TX('을 함께 쓴다 — 미완료는 후속 기한과 함께 남김')], h=15)
d.text(s, CX0, y, CW, 24, [N('지적 6건은 KORAD 공식 평가문장에서 확인된 내용. 조치·효과는 실제 실적으로 기재.'), N('미완료 사항은 숨기지 않고 잔여 Gap으로 표기.')], name='주석')
fit(s, y + 16, BODY_B, 'R3')

# =========================================================== 13. R4 주요 추진실적 (PR01)
s = d.body(CRUMB, 'R4. Ⅱ 2025년 주요 추진실적: 전년 수준 → 금년 변화 → 개선효과로 한눈에 보인다', '자료: KORAD 노사관계 역량강화 종합계획(2026.10.7.) · 기재 항목', nav=0)
y = BODY_Y
y = sbar(s, y, 'Ⅱ  2025년 주요 추진실적')
y = hero_strip(s, y, [('노사관계 소통지수', '81.05점', '2025년'), ('노사관계 역량수준', '81.9점', '2025년'), ('인사관리 학습조직', '17 → 28명', '확대')], h=24)
rows = [['평가내용', '전년 수준', '금년 변화', '개선효과'],
        ['① 적법·실질 운영', '[기재]', '[기재]', '[기재]'],
        ['② 의사소통·관리역량', '[기재]', '노사필통(매주)·공통채널(격주)·노사소위원회(매월) 다층 소통 운영', '[기재]'],
        ['③ 근로조건 향상', '[기재]', '[기재]', '[기재]']]
gf, th = d.table(s, CX0, y, [36, 36, 66, 42], rows, name='연간 요약표', fill_to=BODY_B - 46, label_col=True, row_pad=2.4, min_row=20)
y += th + 4
y = result_band(s, y, '요약', [TX('활동 건수보다 '), KW('전년 대비 변화와 효과'), TX('를 앞에 두고, 세부는 Ⅲ 추진실적으로 연결')], h=15)
d.text(s, CX0, y, CW, 24, [N('수치는 KORAD 종합계획 보고요지의 기존 지표(소통지수·역량수준·학습조직). 나머지 칸은 실적으로 기재.'), N('분모 없는 증감은 이용률로 쓰지 않음.')], name='주석')
fit(s, y + 16, BODY_B, 'R4')

# =========================================================== BP 모듈 공통 머리
SEC = {1: '평가내용 ①  협력체계의 적법·실질 운영', 2: '평가내용 ②  의사소통과 관리역량 강화', 3: '평가내용 ③  근로조건의 실질적 향상'}


def bp_page(code, tkey, gm, sec_no, ttl, pat, src):
    s = d.body(CRUMB, gm, src, nav=0)
    y = BODY_Y
    y = sbar(s, y, SEC[sec_no])
    y = title_row(s, y, f'1. {ttl}', [(f'모듈 {code}', 26, C['blue_deep'], C['white']), (f'KPE {pat}', 46, C['tint_100'], C['blue_strong'])])
    return s, y


# =========================================================== 14. A 폐쇄루프
s, y = bp_page('A', 'T1', 'A. 폐쇄루프형: 진단에서 환류까지 단계마다 증빙을 한 줄에 놓는다', 2, '쟁점이 이행 확인까지 닫힌 사례', 'V114·V120', '자료: 공식평가 재검증 · 사례 5개 기관')
cols = [26, 34, 34, 46, 40]
x = CX0
d.badge(s, x, y, cols[0] - 1, 8, '기관', fill=C['blue_deep'], name='단계 헤더')
x += cols[0]
for i, t in enumerate(['진단·분석', '협의·결정', '제도 변경', '이행·환류']):
    d.badge(s, x, y, cols[i + 1] + 1.5, 8, t, fill=[C['blue_panel'], C['blue_panel'], C['blue_bright'], C['teal_500']][i], shape=MSO_SHAPE.PENTAGON, name='단계 헤더')
    x += cols[i + 1]
y += 10
rows = [[dict(t='한국수자원공사\nB / B0', b=True), '갈등진단', '―', '승진·전보·직군격차 개선', 'K-노무포털로 합의사항 이행 모니터링'],
        [dict(t='한국관광공사\nB / B0', b=True), '근로환경 만족도 분석', '협의 → 의사결정', '자녀수당 확대 등 실제 결과 연결', '환류(4단계 마지막)'],
        [dict(t='한국교통안전공단\nA / B0', b=True), '갈등 발생·제도 분석', '제도 설계', '제도 시행(토요검사 합의·직무급 확대)', '모니터링'],
        [dict(t='한국산업기술진흥원\nA / B0', b=True), '노사공동 TF 논의', '―', '직무역량평가·IDP·직무급·자율출퇴근제', '―'],
        [dict(t='예금보험공사\nA / B0', b=True), '채널별 인식·활용·만족도 진단', '협의체를 인사·조직 현안 의사결정에 연결', '―', '진단 후 환류·정비']]
gf, th = d.table(s, CX0, y, cols, rows, head=False, name='단계 레일 사례표', fill_to=BODY_B - 46, row_pad=2.2, min_row=20, label_col=True)
y += th + 5
y = result_band(s, y, '성과', [TX('B0를 가르는 것은 채널이 아니라 '), KW('판단 → 합의 → 제도변경 → 이행 추적'), TX('이 닫혔는가')], h=16)
d.text(s, CX0, y, CW, 36, [N('― 는 공식 평가문장에서 확인되지 않은 단계(빈칸으로 두지 않고 표시).'), EASY('민원이 접수만 되고 끝나는 게 아니라 처리·회신·재점검까지 가는지를 봅니다.')], name='주석')
fit(s, y + 28, BODY_B, 'A')

# =========================================================== 15. B 협의체
s, y = bp_page('B', 'T2', 'B. 협의체형: 복수노조·직군별 협의체가 안건을 합의로 닫는지 매트릭스로 쓴다', 1, '협의체로 안건을 종결한 사례', 'V320·V319', '자료: 공식평가 재검증 · 사례 4개 기관')
rows = [['기관', '협의 구조', '합의·성과', '평가가 본 보완'],
        [dict(t='한국도로공사\nB / B+', b=True), '9개 복수노조에 상생협의체를 본사·지사로 운영', '노란봉투법 전담 TF·외부 전문기관 협업', '자회사 노무역량 공유·온라인 환류'],
        [dict(t='근로복지공단\nA / C', b=True), '7개 복수노조 참여 통합노사협의회', '현장 미해결 안건 협의 구조 유지', '노조 간 조정 기준·합의 절차, 이행 점검'],
        [dict(t='한국무역보험공사\nA / C', b=True), '복수노조별 별도 협의체, 해외지사 포함 소위원회', '19개 근로조건 개선안 실제 이행', '복수노조 소통 절차 매뉴얼화'],
        [dict(t='한국주택금융공사\nB / C', b=True), '장기과제협의체', '교착 과제 2건 완전합의·3건 개선안', '3건 최종합의·완료시점 없음']]
gf, th = d.table(s, CX0, y, [30, 52, 50, 48], rows, name='협의체 매트릭스', fill_to=BODY_B - 46, label_col=True, row_pad=2.4, min_row=24)
y += th + 5
y = result_band(s, y, '성과', [TX('협의체 수가 아니라 '), KW('합의율·미합의 사유·완료시점'), TX('으로 평가 — 완전합의와 개선안을 구분')], h=16)
d.text(s, CX0, y, CW, 36, [N('복수노조는 같은 채널 제공보다 충돌 시 조정 기준·절차의 문서화가 핵심.'), N('보완 열은 평가위원이 짚은 잔여 과제.')], name='주석')
fit(s, y + 28, BODY_B, 'B')

# =========================================================== 16. C 위험·통제·잔여
s, y = bp_page('C', 'T3', 'C. 법제·준법형: 법 변화 위험은 통제 장치와 잔여 위험을 한 줄로 쓴다', 1, '법 변화 위험을 통제한 사례', 'V517', '자료: 공식평가 재검증 · 사례 5개 기관')
rows = [['기관', '위험·이슈', '통제 장치', '잔여 위험'],
        [dict(t='한전KDN\nA / B0', b=True), '노란봉투법·통상임금·정년연장', '복수노조 통합 지원 등 선제 대응', '무기명 설문 대표성, 미해결 안건 보류 기준'],
        [dict(t='한국원자력환경공단\nB / D+', b=True), '노란봉투법·적법도급', '대응 시나리오·협력사 핫라인·점검기준 계약 반영', '사용자성 판단회의체·가이드 모의적용'],
        [dict(t='산업안전보건공단\nB / C', b=True), '노동관계 법령 변화', '공동대응, 자체 AI 사용자성 기준', '판례 축적 부족, 외부 검증 필요'],
        [dict(t='건강보험심사평가원\nA / C', b=True), '단체협약 신고·부당노동행위', '사내노무사·외부 노무법인 공동점검', '점검 후 결과 환류·재발방지 미종결'],
        [dict(t='한국전기안전공사\nB / C', b=True), '노동관계 리스크', '외부 컨설팅 로드맵, 노사합동 자체점검', '내부 실행계획·KPI·책임체계']]
gf, th = d.table(s, CX0, y, [36, 40, 52, 52], rows, name='위험-통제-잔여 표', fill_to=BODY_B - 46, label_col=True, row_pad=2.0, min_row=20)
y += th + 5
y = result_band(s, y, '성과', [TX('규정·매뉴얼 보유보다 '), KW('모의 적용·현장 적용·재검증'), TX('이 높게 평가됨')], h=16)
d.text(s, CX0, y, CW, 36, [N('외부 자문은 시작점이며 내부 Owner·KPI·종결 관리가 있어야 증빙.'), N('잔여 위험 칸은 비우지 않고 평가 문장을 인용.')], name='주석')
fit(s, y + 28, BODY_B, 'C')

# =========================================================== 17. D 대상별 채널
s, y = bp_page('D', 'T4', 'D. 다층소통형: 누구의 의견을 들었는지 대상별 표로 쓴다', 2, '대상별 채널·대표성 사례', 'V614·V619', '자료: 공식평가 재검증 · 사례 6개 기관')
rows = [['대상 · 기관', '운영한 채널·실적', '평가가 본 한계'],
        [dict(t='세대·직급\n한국장학재단 B / C', b=True), '세대·직급별 채널, 전직원 노무교육', '일부 관리자 중심 소통, 교육 격차'],
        [dict(t='소수노조\n한국수력원자력 A / B0', b=True), '복수노조 소수노조 소통', '근무자 간 권익 인식 차이, 잠재 노노갈등'],
        [dict(t='하위직·공무직\n국민연금공단 A / D+', b=True), '본부-지역 협의 역할 명확화, 참여 비율 조정', '갑질 신고가 수년간 개선되지 않음'],
        [dict(t='직종·연령\n한국마사회 B / C', b=True), '맞춤형 채널 확대, 대면소통', '노동이사 제언 증가의 의사결정·성과 환류 부족'],
        [dict(t='전직원 설문\n주택도시보증공사 B / D+', b=True), '조사 참여 286→387명, 협력지수 87.0→91.3', '노조 간부 중심, 일반직원 직접 대면 미흡'],
        [dict(t='CEO 직접\n한국중부발전 B / B0', b=True), 'CEO 직접채널 상설화', '갈등관리 매뉴얼 정교화']]
gf, th = d.table(s, CX0, y, [54, 64, 62], rows, name='대상별 채널표', fill_to=BODY_B - 46, label_col=True, row_pad=1.8, min_row=16)
y += th + 5
y = result_band(s, y, '성과', [TX('채널 수보다 '), KW('대표성·회신·결정 변경'), TX('이 보이는지를 평가')], h=16)
d.text(s, CX0, y, CW, 36, [EASY('반장 의견만 듣지 않고 전학생 의견도 들었는지를 봅니다.'), N('한계 칸에는 평가 문장만 인용.')], name='주석')
fit(s, y + 28, BODY_B, 'D')

# =========================================================== 18. E 수치
s, y = bp_page('E', 'T5', 'E. 지표개선형: 수치는 전·후 값으로 보이고 한계를 바로 옆에 둔다', 2, '수치가 개선된 사례', 'V418·V215', '자료: 공식평가 재검증 · 사례 4개 기관')
y = hero_strip(s, y, [('주택도시보증공사 · D+', '87.0 → 91.3', '노사소통협력지수'), ('한국남부발전 · B0', '4.32 → 4.41', '소통 만족'), ('한국지역난방공사 · C', '70.0 → 77.1', '노사 만족도'), ('한전KDN · B0', '8.7 → 15.6%', '직무급 비중')], h=27)
rows = [['구분', '인정된 것', '한계로 본 것'],
        ['지수·참여', '지수·만족도·참여율 상승(조사 참여 286 → 387명)', '만족도 상승만으로는 고등급이 아님(지역난방 C·주택도시 D+)'],
        ['세부 지표', '3년 연속 직무급 합의(남부발전)', '4.0 미만 세부지표와 교육 현업적용도 별도 관리'],
        ['제안 처리', '제안 12건 상정·5건 해소(한전KDN)', '미해결 안건의 보류·재검토·중장기 과제화 기준']]
gf, th = d.table(s, CX0, y, [30, 72, 78], rows, name='수치 인정·한계표', fill_to=BODY_B - 46, label_col=True, row_pad=2.2, min_row=18)
y += th + 5
y = result_band(s, y, '성과', [TX('상승 폭이 아니라 '), KW('체감도·제도변경과 분리 측정'), TX('한 결과를 함께 제시')], h=16)
d.text(s, CX0, y, CW, 24, [N('수치 카드는 4개 이내, 전→후 값 1쌍씩.'), N('종합 71.0 → 78.2는 지역난방공사 종합 만족도.')], name='주석')
fit(s, y + 20, BODY_B, 'E')

# =========================================================== 19. F 제도 변화
s, y = bp_page('F', 'T6', 'F. 제도변화형: 합의된 제도와 남은 쟁점을 한 행에 나란히 쓴다', 3, '합의가 제도로 바뀐 사례', 'V214', '자료: 공식평가 재검증 · 사례 6개 기관')
rows = [['제도 · 기관', '노사 합의·변경', '남은 쟁점'],
        [dict(t='직무급\n한전KDN A / B0', b=True), '직무급 비중 8.7 → 15.6%', '미해결 안건 보류·재검토 기준'],
        [dict(t='임금체계\n중소벤처기업진흥공단 B / C', b=True), '연공수당 폐지·호봉상한·직무급 비중 확대', '고연차 반대, 단계적 수용성 관리'],
        [dict(t='근로조건\n한국무역보험공사 A / C', b=True), '태아검진동행휴가·출산휴가·장기근속휴가 등 19개 이행', '직무급 불만 소통·보완책'],
        [dict(t='직무평가\n산업기술기획평가원 B / B0', b=True), '전 직원 참여형 직무평가·노사공동 심의 → 성과·승진·배치', '지적 1건(세부 미기재)'],
        [dict(t='임금체계\n한국소비자원 B / C', b=True), '노사협의·워크숍 → 직무급 확대·임금체계 변경', '직무급 신뢰·수용성, 지표 객관성'],
        [dict(t='통상임금\n보훈복지의료공단 B / D+', b=True), '통상임금 분쟁 일부 해결·직무급 확대', '합의 후 보상격차·잔여 분쟁']]
gf, th = d.table(s, CX0, y, [56, 70, 54], rows, name='제도 변화표', fill_to=BODY_B - 46, label_col=True, row_pad=1.8, min_row=16)
y += th + 5
y = result_band(s, y, '성과', [TX('제도 도입 다음에 '), KW('이용률·수용성·집단별 편차'), TX('가 다시 평가됨')], h=16)
d.text(s, CX0, y, CW, 24, [N('직무급 확대는 반대 집단·미합의 쟁점의 장기 관리까지 평가.')], name='주석')
fit(s, y + 18, BODY_B, 'F')

# =========================================================== 20. G 교육 적용
s, y = bp_page('G', 'T7', 'G. 교육적용형: 교육은 수료가 아니라 현업 적용과 예방 성과까지 올린다', 2, '교육이 현업 적용으로 이어진 사례', 'V422', '자료: 공식평가 재검증 · 사례 3개 기관')
rows = [['단계', '평가가 보는 증거', '사례 기관', '증거 강도'],
        ['1 교육 투입', '대상별 노무교육 실시', '주택금융공사(직급·직군별), 장학재단(전직원)', '낮음'],
        ['2 이해·만족', '교육을 만족도만으로 측정하는 한계(평가 반복 지적)', '유형 공통 총평', '중간'],
        ['3 현업 적용', '중장기 노무 HRD, 실전형 모의신고 훈련', '예금보험공사', '높음'],
        ['4 예방 성과', '잠재 리스크 사전 점검, 관련 사고 Zero', '예금보험공사', '가장 높음']]
gf, th = d.table(s, CX0, y, [30, 62, 60, 28], rows, name='교육 성과 단계표', fill_to=BODY_B - 46, label_col=True, row_pad=2.4, min_row=20, align=['c', 'l', 'l', 'c'])
y += th + 5
y = result_band(s, y, '성과', [TX('교육 횟수보다 '), KW('현업 검토서·모의훈련·사고 예방'), TX('의 적용 증거를 평가')], h=16)
d.text(s, CX0, y, CW, 36, [EASY('소방 교육을 들었는지가 아니라 실제 화재 훈련에서 움직였는지를 봅니다.'), N('증거 강도는 평가 반복 지적에 근거한 분석자 구분.')], name='주석')
fit(s, y + 28, BODY_B, 'G')

# =========================================================== 21. H 위기·전환
s, y = bp_page('H', 'T8', 'H. 위기·전환형: 위기·전환 과제는 노사 공동 대응 장치로 보여준다', 3, '위기·전환을 공동 대응한 사례', 'V212', '자료: 공식평가 재검증 · 사례 5개 기관')
cols = [34, 40, 58, 48]
x = CX0
d.badge(s, x, y, cols[0] - 1, 8, '기관', fill=C['blue_deep'], name='헤더')
x += cols[0]
for i, t in enumerate(['현안·전환', '노사 공동대응', '평가·잔여']):
    d.badge(s, x, y, cols[i + 1] + 1.5, 8, t, fill=[C['blue_panel'], C['blue_bright'], C['teal_500']][i], shape=MSO_SHAPE.PENTAGON, name='헤더')
    x += cols[i + 1]
y += 10
rows = [[dict(t='한국전력공사\nA / B0', b=True), '전력망 확충·재무위기', '핵심 경영과제를 노사 공동 의제로 전환, 핵심 사업소 대면소통', '구조개편 중 현장 불안 관리'],
        [dict(t='한국지역난방공사\nB / C', b=True), 'AI 대전환', '노사공동위·실무 TF, 노동이사 경영제언 9건', '채널 형식화 방지·체감 갈등 해소'],
        [dict(t='한국수력원자력\nA / B0', b=True), '조직 전환', 'R&R 공동조정, 취약직군·협력사 근로조건 개선', '노노갈등 예방·후속조치 체감 모니터링'],
        [dict(t='한국중부발전\nB / B0', b=True), '에너지 전환', '노사정 협의회, 전 사업소 노사관계우수기업 인증', '디지털 전환 대비 갈등관리 매뉴얼'],
        [dict(t='한전KPS\nB / B0', b=True), '정의로운 전환 등 정책 변화', '노사합동 TF, 수준진단 25→30문항', '감사 지적 일부 조치 미완']]
gf, th = d.table(s, CX0, y, cols, rows, head=False, name='현안-대응-평가표', fill_to=BODY_B - 46, label_col=True, row_pad=2.0, min_row=20)
y += th + 5
y = result_band(s, y, '성과', [TX('위기를 '), KW('노사 공동 의제'), TX('로 바꾸고 전환기 인력·근로조건 계획까지 연결')], h=16)
d.text(s, CX0, y, CW, 24, [N('종합등급이 C여도 노사 B0가 가능하므로 사례를 분리해 인용.')], name='주석')
fit(s, y + 18, BODY_B, 'H')

# =========================================================== 22. R6 반쪽 BP × 2
s = d.body(CRUMB, 'R6. 반쪽 BP: 서로 다른 두 사례를 한 쪽에 위아래로 같은 밀도로 쓴다', '자료: 공식평가 재검증 · 사례 2개 기관', nav=0)
y = BODY_Y
hh = 104
cases = [('평가내용 ②  의사소통과 관리역량 강화', '1-1. 갈등진단에서 이행 점검까지 (수자원공사 B / B0)', 'V120',
          [['진단', '갈등진단 실시'], ['제도 변경', '승진·전보·직군격차 개선'], ['이행·환류', 'K-노무포털로 합의사항 이행 모니터링']],
          [TX('진단에서 '), KW('이행 모니터링'), TX('까지 한 고리로 연결')]),
         ('평가내용 ①  협력체계의 적법·실질 운영', '1-2. 협의체와 법 변화 TF 병행 (도로공사 B / B+)', 'V320',
          [['협의 구조', '9개 복수노조에 상생협의체를 본사·지사로 운영'], ['법 변화 대응', '노란봉투법 전담 TF·외부 전문기관 협업'], ['보완', '자회사 노무역량 공유·온라인 상시 환류']],
          [TX('협의 구조와 '), KW('법 변화 대응'), TX('을 함께 제시')])]
for k, (sb, tt, pat, rws, res) in enumerate(cases):
    y0 = BODY_Y + k * (hh + 4)
    bar = d.rect(s, CX0, y0, CW, 7.5, fill=C['blue_deep'], name='섹션 띠')
    d.fill_text(bar, [dict(t=sb, sz=SZ_TITLE, b=True, color=C['white'])], anchor='m', margins=(3, 0, 3, 0))
    d.text(s, CX0, y0 + 9, 130, 10, [dict(t=tt, sz=SZ_TITLE, b=True)], anchor='m', name='추진실적 제목')
    d.badge(s, CX1 - 36, y0 + 9.5, 36, 8, f'KPE {pat}', fill=C['tint_100'], color=C['blue_strong'], name='라벨')
    gf, th = d.table(s, CX0, y0 + 21, [34, 146], rws, head=False, label_col=True, name=f'반쪽 표 {k+1}', row_pad=2.0, min_row=17)
    result_band(s, y0 + 21 + th + 3, '성과', res, h=13)
fit(s, BODY_Y + 2 * (hh + 4), BODY_B + 6, 'R6')

# =========================================================== 23. R7 성과·효과 입증
s = d.body(CRUMB, 'R7. 성과·효과 입증: Before/After와 범위·분모를 함께 쓰고 재측정으로 닫는다', '자료: 공식평가 재검증(한전KDN) · 분모 없는 비율은 쓰지 않음', nav=0)
y = BODY_Y
y = sbar(s, y, '평가내용 ③  근로조건의 실질적 향상')
y = title_row(s, y, '1. 직무급 확대와 제안 처리 (한전KDN)', [('모듈 R7', 26, C['blue_deep'], C['white']), ('KPE V422', 38, C['tint_100'], C['blue_strong'])])
y = hero_strip(s, y, [('직무급 비중', '8.7 → 15.6%', '노사 합의 확대'), ('경영진 상정 제안', '12건', '무기명 온라인 조사'), ('해소', '5건', '상정 12건 중')], h=24)
rows = [['구분', 'Before', 'After', '범위·분모', '재측정·한계'],
        ['직무급 비중', '8.7%', '15.6%', '전체 보수체계 기준', '미해결 안건의 보류·재검토 기준 필요'],
        ['제안 처리', '―', '상정 12건·해소 5건', '상정 12건이 분모', '직급·소속·노조가입별 대표성 한계'],
        ['제도 대응', '―', '복수노조 통합 지원, 법제 선제 대응', '노란봉투법·통상임금·정년연장', '접수→상정→해결→장기과제화→공유 설계']]
gf, th = d.table(s, CX0, y, [26, 20, 40, 44, 50], rows, name='Before-After 표', fill_to=BODY_B - 46, label_col=True, row_pad=2.2, min_row=18)
y += th + 5
y = result_band(s, y, '성과', [TX('Hero 수치 옆에 '), KW('분모·범위·재측정'), TX('을 붙여 과장 없이 입증')], h=16)
d.text(s, CX0, y, CW, 36, [N('― 는 공식 문장에서 확인되지 않은 값.'), N('성과는 평가문장 기준이며 인과 효과로 단정하지 않음.')], name='주석')
fit(s, y + 28, BODY_B, 'R7')

# =========================================================== 24. R8 KORAD 노사관계 고정양식(실측)
s = d.body(CRUMB_R, '4-1. KORAD 노사관계 고정양식: 진단→실행→성과→평가·해석→환류를 한 단위로 묶는다', '자료: KORAD_고정양식_실제자료_검증용_v0.1(PDF 실측), 기관 실적보고서 108~109쪽, 공식평가 902~903쪽')
y = BODY_Y
y = sbar(s, y, '고정양식 1단위: 번호 머리줄 + 라벨열 5행')
rows = [[dict(t='진단', b=True), '본사·사업소 간 수평 소통과 현장 고충 해결의 상대적 취약성을 진단'],
        [dict(t='실행', b=True), '노사소위원회 사업소 순회 개최 정례화 · 노동이사가 비정규직·비조합원 의견수렴 보완'],
        [dict(t='성과', b=True), '현장 안건 해결 6건 → 10건 / 소통지수 81.05점(신설)  ※ 근거: 기관 실적보고서 108쪽'],
        [dict(t='평가·해석', b=True), '소통 사각 보완 노력 인정. 장기안건·참여율·직군별 인식차의 후속관리 필요  ※ 근거: 공식평가 902~903쪽'],
        [dict(t='환류(안)', b=True), '안건별 원인·책임부서·조정기한을 기록해 논의-결정-이행-재측정을 연결(검토안, 이행실적 아님)']]
gf, th = d.table(s, CX0, y, [24, CW - 24], rows, head=False, name='고정양식 1단위', label_col=True, row_pad=2.0, min_row=14)
y += th + 5
y = result_band(s, y, '읽는 법', [TX('기관 주장(실행·성과)과 '), KW('평가자 판단(평가·해석)'), TX('을 행으로 분리하고, 근거 쪽수를 줄마다 붙인다')], h=16)
d.tint_box(s, CX0, y, CW, 54, [Q('실측값 (고정양식 PDF 1쪽)'),
                              L('A4 595×842pt, 바깥 여백 33.75pt = 약 11.9mm(사방 12mm), 본문 폭 186mm'),
                              L('글꼴 본문 11pt·부제 9pt·소제목 12.6pt·표제 16pt, 라벨열 약 24mm'),
                              EASY('명세서처럼 "무엇을 했고(실행) 어떤 결과가 났고(성과) 심사위원은 뭐라 했고(평가) 다음엔 뭘 하나(환류)"를 한 줄씩 적는 칸입니다.')])
fit(s, y + 54, BODY_B, 'R8')

# =========================================================== 25. 표준
s = d.body(CRUMB_R, '5-1. A4 세로 표준: 여백 좌우 15·상하 10, 글자 12·14·15pt', '자료: 사용자 지정 기준', )
rows = [['항목', '표준값', '적용'],
        ['용지', 'A4 세로 210 × 297mm', '슬라이드 크기'],
        ['여백', '좌·우 15mm / 상·하 10mm (지정값)', '본문 180 × 277mm · 고정양식 실측은 사방 12mm(186mm)'],
        ['머리글', 'y 10~19 경로(좌)·CI(우)·실선', '장·지표 경로'],
        ['Governing Message', 'y 21.5~35 좌측 기준선 가로형', '15pt 굵게, 두괄식 1~2줄'],
        ['본문 영역', 'y 40~262 (222mm), 하단 탭 y 265~275', '지면 R1~R7·모듈 A~H'],
        ['하단', '출처·주석 y 278.5~287 + 쪽 번호 탭', '12pt'],
        ['글자 12pt', '본문 글상자 · 박스·표 안 텍스트', '개조식 □ ○ - ※'],
        ['글자 14pt', '네모·동그라미 라벨·번호·핵심 수치', '단계 헤더·성과 라벨'],
        ['글자 15pt', '박스 밖 제목', 'GM·섹션 띠·추진실적 제목'],
        ['글꼴', 'Pretendard (Regular·Bold)', '행간 110%, 자간 -5%']]
gf, th = d.table(s, CX0, BODY_Y, [36, 80, 64], rows, name='표준표', label_col=True, row_pad=1.0)
y = BODY_Y + th + 4
d.tint_box(s, CX0, y, CW, 56, [Q('예외와 확인 사항'), L('표지·간지의 큰 제목은 KORAD 원본 크기를 따르며 12·14·15pt 규칙에서 제외'),
                              L('여백 수치는 마스터 한 곳에서 바꾸면 모든 지면에 반영'),
                              N('KORAD 고정양식 PDF는 실측함(사방 12mm). 보고서 원본 104~112쪽 이미지는 10MB 초과로 미확보: 여백을 12mm로 바꿀지 확인 필요')])
fit(s, y + 56, BODY_B_FREE, '표준')

d.save(OUT)
print('saved', OUT, len(d.prs.slides._sldIdLst))
for w in WARN:
    print('WARN', w)
