import sys; sys.path.insert(0, "/home/user/claude/korad-경영평가-ppt/src")
import layouts, collections
NAMES={'quadpanel':'4분면 진단','tiermatrix':'단계×열 매트릭스','stakegrid':'이해관계자 카드','survey':'설문 수치 패널','influence':'영향력·관심도','timeline':'로드맵(타임라인)','taskmap':'과제 지도','pairlinks':'짝 연결 패널','bracketcols':'화살 머리 3열','crosspanel':'십자 패널','rolling':'미션·비전·가치 3열','datecols':'월별 3열','needsmatrix':'니즈·실적·성과 행렬','roadmap':'CSF·PI·KPI 로드맵 표','strategy':'라벨 행(전략)','twin':'좌우 2패널','panel3':'3분할 패널','awards':'사진 카드 행(수상)'}
def feats(L):
    nt=[n['t'] for n in L['nodes']]; rows=0; bk=set()
    for n in L['nodes']:
        if n['t']=='ladder':
            rows+=len(n['rows'])
            for r in n['rows']:
                for b in r['bands']: bk.add(b['k'])
    return nt,set(nt),rows,bk
def start(nt):
    if 'topic' in nt[:2]: return '번호 띠로 시작'
    if 'sub' in nt[:2]: return '소제목으로 시작'
    if nt[0] in('chapter','eval'): return '쪽 머리'
    return '머리 없이 시작(쪽 머리 아래)'
def size(rows): return '소형(~3행)' if rows<=3 else ('중형(4~5행)' if rows<=5 else '대형(6행 이상)')
def main(L):
    nt,s,rows,bk=feats(L)
    if L['id'] in('L01','L02'): return '1 쪽 머리'
    if s&{'gridtable','table'}: return '2 표 중심'
    if s&{'cardgrid','tabcards','resultcharts'}: return '3 카드·막대 그래프'
    if s&set(NAMES): return '4 특수 도식'
    if 'steps' in bk: return '5 사다리 + 단계 띠'
    return '6 사다리 + 칸(불릿)'
G=collections.defaultdict(lambda: collections.defaultdict(list))
for L in layouts.LAYOUTS:
    nt,s,rows,bk=feats(L); m=main(L)
    if m.startswith('4'): key=[NAMES[t] for t in nt if t in NAMES][0]
    else: key=start(nt)+' · '+size(rows)
    G[m][key].append(L)
def rng(ids):
    nums=[int(i[1:]) for i in ids]; out=[]; a=b=nums[0]
    for n in nums[1:]:
        if n==b+1: b=n
        else: out.append((a,b)); a=b=n
    out.append((a,b))
    return ', '.join(f'L{a:02d}' if a==b else f'L{a:02d}~L{b:02d}' for a,b in out)
md=['# 레이아웃 유형별 색인 (L01~L%d)'%len(layouts.LAYOUTS),'',
'> 쉽게 말해 "비슷하게 생긴 레이아웃의 번호를 한 줄로 모은 찾아보기"입니다. 예) 표로 된 지면이면 **2 표 중심**에서, 번호 띠 아래에 짧게 이어지는 서사면 **6 사다리 + 칸**의 해당 묶음에서 번호를 고릅니다. 번호(L번호)는 그대로이고 순서만 유형별로 모았습니다. 번호 순서로 보려면 `layout-index.md`를 보세요.','',
'**찾는 순서**: ① 지면에 표·카드 막대·특수 도식이 있나? → 있으면 2·3·4번 묶음 ② 없고 가로 단계 띠가 있나? → 5번 ③ 없으면 6번. 같은 묶음 안에서 시작 모양(번호 띠 / 소제목 / 머리 없음)과 크기(행 수)로 고릅니다. 깔때기 띠·칩 배너·성과 박스는 장식 부품이라 유형 기준에서 뺐습니다.','']
tm={}
for m in sorted(G):
    n=sum(len(v) for v in G[m].values())
    md+= [f'## {m} ({n}개)','','| 묶음 | 개수 | 레이아웃 번호 |','|---|---|---|']
    for k in sorted(G[m],key=lambda k:-len(G[m][k])):
        v=G[m][k]; md.append(f'| {k} | {len(v)} | {rng([x["id"] for x in v])} |')
        for x in v: tm[x['id']]=m[2:]+' / '+k
    md.append('')
md+=['## 번호 → 유형 · 한 줄 설명(전체)','','| 번호 | 유형 | 서사 | 근거 쪽 |','|---|---|---|---|']
for L in layouts.LAYOUTS:
    nm=L['name'][5:] if L['name'].startswith('서사 · ') else L['name']
    md.append(f"| {L['id']} | {tm[L['id']]} | {nm[:70]} | {L.get('src','')} |")
open('/home/user/claude/korad-경영평가-ppt/레이아웃_유형별_색인.md','w',encoding='utf-8').write('\n'.join(md)+'\n')
for m in sorted(G):
    print(m,sum(len(v) for v in G[m].values()))
    for k,v in sorted(G[m].items(),key=lambda kv:-len(kv[1])): print('  ',k,len(v))
