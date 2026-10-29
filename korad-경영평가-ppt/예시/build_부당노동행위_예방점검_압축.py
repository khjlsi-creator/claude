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
 dict(t='topic', n=1, title='판례 DB 기반 부당노동행위 정밀 예방점검 체계 구축', chip='✔ 신규'),
 dict(t='ladder', rows=[
   row('추진배경', _c([['복수노조 쟁점 다양화로 법령 유형별 기본 체크리스트(20여개)의 대응 한계'], ['신규 노무 담당자의 판단기준 학습 곤란, 사후 확인형 질문 위주']], 76)),
   row('고도화\n방향', _b('노동위·법원 판례 DB → 사례 연계 정밀 체크리스트(250여개) → 점검·학습 겸용 예방도구')),
   row('추진내용', _c([['① DB 구축: 노동위 결정요지 1,346건·법원 판례 304건'], ['② 체크리스트 확대: 세부유형 214개 + 예방점검 36문항'], ['③ 노사 공동점검: 노조 간부·노무담당 + 전문가 자문'], ['④ 집중관리: DB 통계로 빈발 분야(지배·개입 등) 우선 점검']], 130, False)),
 ]),
 dict(t='result', label='추진성과', items=['20여개 → 250여개 사전 예방형 체크리스트로 신규 담당자 학습과 리스크 예방 병행']),
]
out = sys.argv[1]
d, f = compose(dict(start_no=1, first='odd', note='구조 확인용 초안입니다. 추진성과의 점검 결과 수치는 실적 확정 후 보완합니다.', nodes=nodes), out)
print([ (p['page'],round(p.get('y',0)),round(p.get('h',0))) for p in f.placed]); print('쪽', f.pages(), '경고', d.warn)
