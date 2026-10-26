import itertools, sys
from compose import make, compose
from blocks import W
from layouts import K, PL_NODES, CH
from recipes import R

res = lambda t, l='핵심성과': dict(t='result', text=t, label=l)
P = {
 'A': K['A'], 'B': K['B'], 'C': K['C'], 'D': K['D'], 'E': K['E'], 'F1': K['F1'], 'F2': K['F2'],
 'G1': K['G'][:5], 'G2': K['G'][5:], 'H1': K['H'], 'H2': K['H2'],
 'I1': K['I1'] + [res('교통직 처우개선 수시단체교섭 노사합의 체결', '추진성과')],
 'I2a': K['I2'][:3], 'I2b': [K['I2'][3] if False else n for n in K['I2'] if n['t'] in ('sub', 'panel3', 'result')][-3:],
}
# I2b: 라. sub + panel3 + result
i2 = K['I2']; P['I2b'] = i2[-3:]
def head(p): return p[0]['t']
rank = {'eval': 0, 'topic': 1, 'sub': 2, 'chapter': 0}
H = {}
for k, v in P.items():
    H[k] = sum(make(n).height(W) + (make(n).gap if i else 0) for i, n in enumerate(v))
AV = 1707
def total(keys):
    nodes = []; 
    for k in keys: nodes += P[k]
    return sum(make(n).height(W) + (make(n).gap if i else 0) for i, n in enumerate(nodes)), nodes
cands = []
for r in (2, 3, 4):
    for combo in itertools.combinations(P, r):
        ks = sorted(combo, key=lambda k: rank[head(P[k])])
        heads = [head(P[k]) for k in ks]
        if heads.count('eval') > 1 or heads.count('topic') > 1: continue
        if heads[0] == 'sub' : continue          # 쪽은 평가내용·번호 띠로 시작
        t, nodes = total(ks)
        if 0.90 <= t / AV <= 0.99:
            cands.append((round(t / AV * 100), ks))
used = [set(['A', 'B']), {'C', 'D', 'E'}, {'F1', 'F2'}, {'G1', 'G2'}, {'H1', 'H2'}, {'I1', 'I2a', 'I2b'}]
print(len(cands))
for c in sorted(cands, key=lambda x: -x[0])[:60]: print(c)
