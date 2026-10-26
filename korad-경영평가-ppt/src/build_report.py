# -*- coding: utf-8 -*-
"""KORAD 경영평가 PPT 시스템 — 경영실적보고서 지면(A4 세로) 기준 재설계."""
import sys
from kp import *
from data import TYPES, ORGS, stats
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

OUT = sys.argv[1] if len(sys.argv) > 1 else 'KORAD_경영평가_노사관계_보고서_A4세로.pptx'
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



CR='Ⅰ. 경영관리 | 04. 조직 운영 및 관리 | 노사관계'
# ---- 1쪽 지표 소개
s = d.body(CR, '노사관계: 소통·역량·근로조건 세 축에서 지수가 모두 전년보다 올랐다', '자료: 한국도로교통공단 2025년도 경영실적보고서 본보고서(경영관리 B.P 요약)')
y = BODY_Y
y = sbar(s, y, '노사관계  |  소통을 통한 공감대 형성, 노사가 함께하는 조직문화', h=9)
y = title_row(s, y, '1. 우수사례(Best Practice)와 핵심 성과', [('요약', 20, C['blue_deep'], C['white'])])
rows = [[dict(t='우수사례 1', b=True), '다양한 노사소통 채널 및 협력체계 운영을 통한 분야별 리스크 공동 대응'],
        [dict(t='우수사례 2', b=True), '관리자·신입직원·노사실무자 등 대상별 맞춤형 교육, 노무 역량교육체계 수립·운영'],
        [dict(t='우수사례 3', b=True), '직급별 차등 인상률로 상하위직 격차 완화, 교통직·실무직 처우 개선']]
gf, th = d.table(s, CX0, y, [30, CW - 30], rows, head=False, name='우수사례표', label_col=True, row_pad=2.2, min_row=16)
y += th + 4
rows = [[dict(t='지수', b=True), dict(t='전년', b=True), dict(t='당해', b=True), dict(t='증감', b=True)],
        ['노사소통지수', '89.3점', '90.9점', '1.6점↑'],
        ['노사역량지수', '90.1점', '90.9점', '0.8점↑'],
        ['근로개선지수', '90.1점', '91.6점', '1.5점↑']]
gf, th = d.table(s, CX0, y, [60, 40, 40, 40], rows, name='지수표', label_col=True, align=['l','c','c','c'], row_pad=1.6, min_row=11)
y += th + 4
y = result_band(s, y, '성과', [TX('세 지수 모두 상승, '), KW('노사 공동 TF 구축·통상임금 재정립'), TX('으로 제도 합의까지 연결')], h=16)
d.tint_box(s, CX0, y, CW, 40, [Q('읽는 법'), L('증감과 전년→당해 값을 함께 적어 수치가 맞는지 바로 확인할 수 있게 한다'),
                              EASY('점수가 올랐는지만이 아니라 "얼마에서 얼마로" 올랐는지를 같이 보여 줍니다.'),
                              N('노사관계 본문(보고서 92~99쪽)은 열람하지 못해 요약 쪽 내용만 담았습니다.')])

# ---- 2쪽 고정양식 두 단위
s = d.body(CR, '고정양식: 실행과 성과는 기관 주장, 평가·해석은 평가자 판단으로 나눠 쓴다', '자료: 한국도로교통공단 2025년도 경영실적보고서(요약 쪽), 양식은 KORAD 노사관계 고정양식')
y = BODY_Y
for no, ttl, rows in [
  ('01', '노사소통 채널을 지수 상승으로 연결', [['진단', '―'], ['실행', '다양한 노사소통 채널·협력체계 운영으로 분야별 리스크 공동 대응'],
      ['성과', '노사소통지수 전년대비 1.6점↑ (89.3 → 90.9점)\n근거: 경영관리 B.P 요약'], ['평가·해석', '―  (공식평가 문장 미확인)'], ['환류(안)', '―']]),
  ('02', '처우 격차 완화와 통상임금 합의', [['진단', '―'], ['실행', '직급별 차등 인상률로 상하위직 격차 완화, 교통직·실무직 처우 개선'],
      ['성과', '근로개선지수 전년대비 1.5점↑ (90.1 → 91.6점) / 노사 공동 TF 구축, 통상임금 재정립\n근거: 경영관리 B.P 요약'], ['평가·해석', '―  (공식평가 문장 미확인)'], ['환류(안)', '―']])]:
    d.rect(s, CX0, y, CW, 9.5, fill=C['tint_100'], name='단위 머리줄')
    d.badge(s, CX0 + 2, y + 1.3, 9, 7, no, fill=C['navy'], color=C['white'], name='번호 칩')
    d.text(s, CX0 + 14, y, CW - 16, 9.5, [dict(t=ttl, sz=SZ_TITLE, b=True)], anchor='m', name='단위 제목')
    y += 9.5
    rr = [[dict(t=a, b=True), t] for a, t in rows]
    gf, th = d.table(s, CX0, y, [24, CW - 24], rr, head=False, name='단위 '+no, label_col=True, row_pad=1.8, min_row=12)
    y += th + 6
fit(s, y, BODY_B, '2쪽')
d.save(OUT)
print('saved', OUT)
for w in WARN: print('WARN', w)
