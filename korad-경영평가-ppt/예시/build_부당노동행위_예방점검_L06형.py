# -*- coding: utf-8 -*-
"""부당노동행위 정밀 예방점검 체크리스트 고도화 — 경영평가 보고서 서사(추진배경 → 추진내용 → 추진성과) 예시"""
import sys; sys.path.insert(0, '/home/user/claude/korad-경영평가-ppt/src')
from compose import compose
_c = lambda items, mn=80, b=True: dict(k='cols', items=items, min=mn, bullet=b)
_b = lambda t: dict(k='banner', text=t)
_s = lambda labels, mn=70: dict(k='steps', labels=labels, items=[[] for _ in labels], min=mn)
def row(label, *bands, tag=None):
    r = dict(label=label, bands=list(bands))
    if tag: r['tag'] = tag
    return r
nodes = [
 dict(t='sub', text='나. 판례 DB 기반 부당노동행위 정밀 예방점검 체계 구축', chips=['신규']),
 dict(t='ladder', rows=[
   dict(label='추진\n배경', bands=[dict(k='cols', heads=['복수노조 쟁점 다양화', '기본 체크리스트의 한계'],
        items=[['교섭·차별·지배개입 등 복수노조 환경의 쟁점이 다양해짐'], ['법령 유형별 체크리스트(20여개)만으로 대응 한계, 신규 담당자 학습 곤란']])]),
   dict(label='고도화\n방향', bands=[dict(k='cols', heads=['판례 연계 정밀화', '점검·학습 겸용'],
        items=[['노동위·법원 판례 DB로 실제 사례와 연계한 250여개 체크리스트'], ['사전 예방형 질문 + 판단기준·판례 병기로 담당자 역량 동시 강화']])]),
   dict(label='추진\n단계', bands=[dict(k='steps', labels=['판례 DB 구축', '체크리스트 확대', '노사 공동점검', '집중관리'],
        items=[['결정요지 1,346건·판례 304건 수집'], ['세부유형 214개 + 예방점검 36문항'], ['노조 간부·노무담당 점검, 전문가 자문'], ['DB 통계로 빈발 분야 우선 점검']])]),
 ]),
 dict(t='result', text='20여개 → 250여개 사전 예방형 체크리스트 구축, 노사 공동점검 체계 정립', label='추진성과'),
]
out = sys.argv[1]
d, f = compose(dict(start_no=1, first='odd', note='구조 확인용 초안입니다. 추진성과의 점검 결과 수치는 실적 확정 후 보완합니다.', nodes=nodes), out)
print([ (p['page'],round(p.get('y',0)),round(p.get('h',0))) for p in f.placed]); print('쪽', f.pages(), '경고', d.warn)
