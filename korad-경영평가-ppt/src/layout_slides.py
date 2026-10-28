# -*- coding: utf-8 -*-
"""layouts/registry.json의 쪽 레이아웃(PG-)을 KORAD 지면(A4 세로, 여백 15/10, 12·14·15pt)으로 옮긴 슬라이드.

원본(타 기관 경영실적보고서) 좌표를 본문 영역(x 15~195, y 40~262)으로 환산한다.
슬라이드는 '위치·구조 가이드': 블록 종류별 KORAD 색을 입히고, 영역마다 들어갈 내용 이름을 적는다.
"""
import json, os
from kp import *

REG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'layouts', 'registry.json')
K = 210.0 / 1240          # px → mm
SRC_X0, SRC_X1 = 118 * K, 1122 * K

# 영역 이름 → 한글 안내 (12pt, 박스 안)
KO = dict(
    top_banner='상단 배너(핵심 메시지)', top_pair_strip='법·정관 목적 2단 띠', row1_cells='기존 해석 3칸', row2_cells='변화 필요성 3칸',
    row3_cells='재정의 3칸', bottom_conclusion_bar='결론 띠', card_tl='카드 좌상', card_tr='카드 우상', card_bl='카드 좌하', card_br='카드 우하',
    hub_circle_images='중앙 허브(이미지)', label_chevron_stack='라벨 화살표 3단', chevron_process_4step='4단계 프로세스', lead_bullets='도입 개조식',
    col3_header='3열 머리', col3_body='3열 본문', message_band='메시지 띠', table_row_value='표 1행(가치체계)', table_row_strategy='표 2행(전략체계)',
    check_column='우측 확인 열', ribbon_title='【리본 제목】', chevron3_header='3단 화살표 머리', cards='카드 3칸', desc_strip='설명 띠', bullets='개조식',
    quadrant_matrix='4분면 매트릭스', channel_by_type='유형별 채널 4행', spread_channels_with_thumbs='확산 채널 + 썸네일', year_chevron3='연도별 3단 화살표',
    cols3_body='3열 본문', flow_block='흐름: 라벨+3단 머리+결과 3칸', future_block='2030 미래상: 배너+타임라인/차트', process_title_bar='프로세스 제목 띠',
    roadmap_timeline='로드맵 타임라인(좌 로고, 우 2레인)', policy_bar='정책 제안 띠', support_pair_bar='지원 2단 띠', month_cols3='월별 3열', wide_message_bar='통 메시지 띠',
    split_header='좌우 2단 머리', category_rows5='분야 5행(아이콘+좌/우 목록)', direction_bar='방향 설정 띠', pill_rows4='화살표 pill → 목표 4행',
    duo_header_plus='2단 머리(+)', bullets2='개조식 2단', caption2='회색 해설 2단', left_stack_expand_new='좌: 확대/신규 적층', right_two_step_eval='우: 2단계 평가',
    cols3_header='3열 머리', scatter_before='산점도(전)', arrow='화살표', scatter_after='산점도(후)', footnote_legend='각주·범례',
    stacked_bar_chart='누적 막대 차트', table_4rows_x3='표 4행×3기간')


def _scale(page):
    ys = [b['y_mm'] for b in page['blocks']]
    y0, y1 = min(a for a, _ in ys), max(b for _, b in ys)
    sx = CW / (SRC_X1 - SRC_X0)
    sy = min(sx, (BODY_B - BODY_Y) / (y1 - y0))
    return y0, sx, sy


def _draw_block(d, s, lay, b, y0, sx, sy):
    k = lay['kind']
    x = CX0 + (b['x_mm'][0] - SRC_X0) * sx
    w = (b['x_mm'][1] - b['x_mm'][0]) * sx
    y = BODY_Y + (b['y_mm'][0] - y0) * sy
    h = (b['y_mm'][1] - b['y_mm'][0]) * sy
    tag = f"{b['layout']} {k}"
    lab = b.get('label') or ''
    if k == 'section_bar':
        sp = d.rect(s, x, y, w, h, fill=C['blue_deep'], name=tag)
        d.fill_text(sp, [dict(t='N  번호 띠 제목 (두괄식 15pt)', sz=SZ_TITLE, b=True, color=C['white'])], anchor='m', margins=(3, 0, 3, 0))
        d.badge(s, x + w - 24, y + 1.2, 22, h - 2.4, '✔개선', fill=C['tint_100'], color=C['blue_strong'], name=tag + ' 칩')
        return
    if k in ('chapter_title', 'subhead'):
        d.text(s, x, y, w, h, [dict(t='제목' if k == 'chapter_title' else '소제목 (가·나·다)', sz=SZ_TITLE, b=True)], anchor='m', name=tag)
        return
    if k in ('eval_item_box', 'bp_banner', 'insight_bar', 'arrow_caption', 'divider_chevron', 'ribbon_title'):
        name = dict(eval_item_box='평가내용 N | 평가내용 문장', bp_banner='Best Practice | 두괄식 제목 + 개조식 2줄', insight_bar='Insight | 시사점 한 줄',
                    arrow_caption='【검증 대상 한 줄】', divider_chevron='', ribbon_title='【리본 제목】')[k]
        sp = d.rect(s, x, y, w, h, fill=C['tint_200'] if k in ('bp_banner', 'ribbon_title', 'divider_chevron') else C['tint_sky'], line=C['blue_bright'], name=tag,
                    shape=MSO_SHAPE.PENTAGON if k == 'divider_chevron' else MSO_SHAPE.RECTANGLE)
        if name:
            d.fill_text(sp, [dict(t=name, sz=SZ_BODY, b=True, align='c')], anchor='m', margins=(2, 0, 2, 0))
        return
    # 라벨열이 있는 블록 / 라벨 없는 복합 블록 / TF 모듈
    d.rect(s, x, y, w, h, fill=C['white'], line=C['blue_bright'], name=tag)
    lw = (lay.get('label_w') or 0) * K * sx
    if lw and k == 'tf_module':       # 라벨열은 흐름·미래상 영역에만 붙는다(리본 제외)
        for r, t in (('flow_block', lab or 'TF명'), ('future_block', '2030 미래상')):
            rg = next(g for g in lay['regions'] if g['name'] == r)
            d.badge(s, x, y + rg['rel_mm'][1] * sy, lw, rg['rel_mm'][3] * sy, t, fill=C['blue_deep'], name=tag + ' 라벨열')
    elif lw:
        d.badge(s, x, y, lw, h, lab or '라벨', fill=C['blue_deep'], name=tag + ' 라벨열')
    for r in lay['regions']:
        rx, ry, rw, rh = r['rel_mm']
        X, Y, Wd, Hd = x + rx * sx, y + ry * sy, rw * sx, rh * sy
        nm = KO.get(r['name'], r['name'])
        if lw and k == 'tf_module' and r['name'] in ('flow_block', 'future_block'):
            X, Wd = X + lw, Wd - lw
        sp = d.rect(s, X, Y, Wd, Hd, fill=C['tint_panel'], line=C['tint_200'], name=r['name'])
        if Hd >= 4.0:
            d.fill_text(sp, [dict(t=nm, sz=SZ_BODY, color=C['slate_700'], align='c')], anchor='m', margins=(1, 0.3, 1, 0.3))


def add_layout_slides(d, crumb, src='자료: 타 기관 보고서 5~9쪽 좌표 분석'):
    reg = json.load(open(REG, encoding='utf-8'))
    names = {'PG-01': '평가내용 첫 쪽: 장 제목·평가내용·BP 배너·환경진단·기존해석→재정의',
             'PG-02': '이해관계자 재분류·가치전략 진단·롤링·소통 확산',
             'PG-03': '그간 혁신연계와 TF 3개 모듈(리본·흐름·2030 미래상)',
             'PG-04': '선제적 제안·반영 로드맵과 정책 정합성 확보',
             'PG-05': '진단 TOOL·사업 포트폴리오 재구성·중장기 재무·인력 계획'}
    n = 10
    for pid, pg in reg['pages'].items():
        s = d.body(crumb, f'R{n}. {names.get(pid, pg["title"])}', src, nav=0)
        y0, sx, sy = _scale(pg)
        for b in pg['blocks']:
            _draw_block(d, s, reg['blocks'][b['layout']], b, y0, sx, sy)
        n += 1
    return n - 10
