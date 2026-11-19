import re,sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
lines=s.split('\n'); keep=[]; skip=False
for l in lines:
    m=re.search(r'position:absolute;left:[\d.]+px;top:([\d.]+)px',l)
    if m: skip=float(m.group(1))>=240
    elif not l.startswith("<") and skip and not l.startswith(("class","renderVals","return","}")): continue
    if m and skip: continue
    keep.append(l)
s='\n'.join(keep)
T='margin:0;letter-spacing:-0.05em;'; B='font-weight:700;'
def moon(n):
    bg='#0051bc' if n==5 else ('#ffffff' if n==1 else f'conic-gradient(#0051bc 0 {(n-1)*25}%, #ffffff 0)')
    return f'<div role="img" aria-label="{n}단계" style="width:20px;height:20px;box-sizing:border-box;border-radius:50%;border:1.5px solid #0051bc;background:{bg};"></div>'
P=lambda t,fs=18,w='',c='#000359',al='left',x='': f'<p style="{T}font-size:{fs}px;{w}line-height:1.3;color:{c};text-align:{al};{x}">{t}</p>'
# 1. comparison boxes
old_rows=[('지속성(40점)','4개 요소 · 전 채널 동일<br>제도화 수준 · 정례 운영성<br>운영이력 연속성 · 참여 안정성'),('효과성(60점)','효과성 4개 요소 · 전 채널 동일<br>문제해결 · 제도반영<br>갈등예방 · 채널만족')]
oldbox=(f'<div style="border:1.5px solid #008eff;border-radius:14px;display:flex;flex-direction:column;align-items:center;">'
 f'<div style="background:#deeeff;border-radius:0 0 16px 16px;padding:5px 18px;">{P("기존(’25)",19,B,al="center")}</div>'
 f'<div style="flex:1;align-self:stretch;display:flex;flex-direction:column;justify-content:space-around;gap:6px;padding:10px 12px;">'
 + ''.join(f'<div>{P(a,18,B,"#0080ea")}{P(b,17,"","#3b4951")}</div>' for a,b in old_rows) + '</div></div>')
def ftab(title,chip,body):
    return (f'<div style="display:flex;flex-direction:column;"><div style="display:flex;align-items:center;gap:8px;">'
      f'<div style="background:#0051bc;border-radius:12px 12px 0 0;padding:4px 16px;">{P(title,19,B,"#ffffff")}</div>'
      f'<p style="{T}font-size:16px;{B}line-height:1.3;color:#002060;border:1.5px solid #002060;padding:0 8px;background:#ffffff;">{chip}</p></div>'
      f'<div style="border:1.5px solid #0051bc;border-radius:0 12px 12px 12px;padding:8px 12px;background:#ffffff;">{body}</div></div>')
cellb=lambda t: f'<p style="{T}font-size:17px;line-height:1.3;color:#000359;text-align:center;background:#eff9ff;padding:4px 6px;">{t}</p>'
f1=ftab('지속성(40점) · 3개 요소, 전 유형 공통','개선',
 f'<div style="display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:6px;">{cellb("제도화 수준<br>(운영 근거 명문화)")}{cellb("정례 운영<br>(이행률, 협의·의결형 참석률 포함)")}{cellb("운영 연속성<br>(최근 3년 중단 없는 운영)")}</div>')
res=[('협의·의결형','안건 해결(상정 안건 해결률)','합의 이행(기한 내 이행률)'),('고충·발굴형','고충 해결(기한 내 해결·회신율)','개선 반영(제도·업무 반영률)'),('공감·참여형','자율 참여(목표 대비 참여율)','공감 형성(사후 공감도 설문)'),('정보공유형','정보 도달(목표 대비 열람률)','이해·활용(독자 설문)')]
hd=lambda t: f'<p style="{T}font-size:17px;{B}line-height:1.3;color:#000359;text-align:center;background:#deeeff;padding:3px;">{t}</p>'
f2=ftab('결과(60점) · 4개 유형별 2요소(총 8요소)','신설',
 '<div style="display:grid;grid-template-columns:130px 1fr 1fr;gap:4px 6px;">'+hd('유형(목적)')+hd('1차 결과')+hd('최종 성과')+''.join(
  f'<p style="{T}font-size:17px;{B}line-height:1.3;color:#ffffff;background:#00b0b4;text-align:center;padding:4px;">{t}</p>'+cellb(a)+cellb(b) for t,a,b in res)+'</div>')
newbox=(f'<div style="border:1.5px solid #0051bc;border-radius:14px;display:flex;flex-direction:column;align-items:center;padding-bottom:10px;">'
 f'<div style="background:#0051bc;border-radius:0 0 16px 16px;padding:5px 22px;">{P("변경(’26)",19,B,"#ffffff","center")}</div>'
 f'<div style="align-self:stretch;display:flex;flex-direction:column;gap:8px;padding:6px 12px 0;">'
 f'{f1}{f2}</div></div>')
notes=P('* 참여율: 회의체는 위원 참석률(지속성), 노사공동 행사는 자율 참여율·레터는 열람률(결과)로 반영',16,'','#3b4951')
def chev(t,bg,c,first):
    cp='polygon(0 0,calc(100% - 18px) 0,100% 50%,calc(100% - 18px) 100%,0 100%)' if first else 'polygon(0 0,calc(100% - 18px) 0,100% 50%,calc(100% - 18px) 100%,0 100%,18px 50%)'
    return f'<div style="flex:1;display:flex;align-items:center;justify-content:center;background:{bg};clip-path:{cp};padding:3px 24px;min-height:48px;box-sizing:border-box;"><p style="{T}font-size:16px;line-height:1.25;color:{c};text-align:center;">{t}</p></div>'
steps=[('<b>평가자</b> 노조 간부·노무 담당 2인<br>같은 증빙으로 요소별 개별 평가','#eff9ff','#000359'),('<b>척도</b> 요소별 5단계 문차트<br>비율 지표 90·80·70·60% 기준','#deeeff','#000359'),('<b>산정</b> 2인 평균(2단계↑ 차이 재협의)<br>종합 = 지속성 40 + 결과 60','#bde0ff','#000359'),('<b>판정</b> 80↑ 유지 · 60~80 개선<br>(과제 연계) · 60↓ 폐지 검토','#0051bc','#ffffff')]
method=(f'<div style="display:flex;align-items:stretch;gap:6px;"><div style="width:110px;display:flex;align-items:center;justify-content:center;background:#00b0b4;">{P("진단방법",19,B,"#ffffff","center")}</div>'
 '<div style="flex:1;display:flex;">'+'<div style="width:3px"></div>'.join(chev(t,bg,c,i==0) for i,(t,bg,c) in enumerate(steps))+'</div></div>')
trap=lambda t,bg,c,fs: f'<div style="align-self:center;width:80%;clip-path:polygon(0 0,100% 0,93% 100%,7% 100%);background:{bg};padding:6px 0;">{P(t,fs,B,c,"center")}</div>'
rows=[('협의·의결형',[('노사협의회','법정 협의기구, 노사현안 협의',5,2,3,'개선','강화'),('노사소위원회','노사현안 실무 협의',5,2,3,'개선','강화'),('공통채널','노무라인–노조 집행부 상시 소통',5,4,4,'유지','유지'),('노사필통','노무담당–사무국장 주간 점검',5,4,4,'유지','유지')]),
('고충·발굴형',[('CEO 찾아가는 소통','CEO–직원 현장 간담회',4,2,3,'개선','강화'),('노동이사 사각소통','취약·소수인력 고충 청취',4,4,4,'유지','신설'),('소수노조 소통','공단·대표노조 합동 현장 방문',3,1,2,'개선','강화')]),
('공감·참여형',[('노사한마음','본사·사업소 직원 공감 행사',5,2,3,'개선','강화'),('노사공동 워크숍','노사 리더 상생협력 실천',5,4,4,'유지','강화')]),
('정보공유형',[('CEO 업무일지','경영철학·의지 전 직원 공유',5,4,4,'유지','유지'),('노무 뉴스레터','노사관계자·실무자 노무 정보 송부',4,4,4,'유지','–')])]
H=lambda t,bg='#deeeff',c='#000359': f'<div style="display:flex;align-items:center;justify-content:center;padding:5px;background:{bg};">{P(t,18,B,c,"center")}</div>'
tbl=[H('유형'),H('채널'),H('소통 방식'),H('지속성'),H('결과'),H('종합'),H('판정','#0051bc','#ffffff'),H('전년(’25)')]
for typ,chs in rows:
    tbl.append(f'<div style="grid-row:span {len(chs)};display:flex;align-items:center;justify-content:center;background:#eff9ff;border-bottom:1.5px solid #8d9cbf;">{P(typ,18,B,al="center")}</div>')
    for i,(ch,way,a,b,c,j,pj) in enumerate(chs):
        bb='border-bottom:1.5px solid #8d9cbf;' if i==len(chs)-1 else 'border-bottom:1px solid #bde0ff;'
        tbl.append(f'<div style="display:flex;align-items:center;justify-content:center;padding:3px 6px;{bb}">{P(ch,18,B,al="center")}</div>')
        tbl.append(f'<div style="display:flex;align-items:center;padding:3px 8px;{bb}">{P(way,17)}</div>')
        for v in (a,b,c): tbl.append(f'<div style="display:flex;align-items:center;justify-content:center;{bb}">{moon(v)}</div>')
        jud=P('개선',17,B,'#ffffff','center','background:#0051bc;padding:0 10px;') if j=='개선' else P('유지',17,al='center')
        tbl.append(f'<div style="display:flex;align-items:center;justify-content:center;{bb}">{jud}</div>')
        tbl.append(f'<div style="display:flex;align-items:center;justify-content:center;{bb}">{P(pj,17,"","#3b4951","center")}</div>')
leg=lambda n,t: f'<div style="display:flex;align-items:center;gap:3px;">{moon(n)}{P(t,16,"","#3b4951")}</div>'
legend=(f'<div style="display:flex;align-items:center;gap:10px;">{P("* 종합 = 지속성 40점 + 결과 60점 · 전년(’25)은 기존 진단 기준",16,"","#3b4951")}<div style="flex:1"></div>'
 f'{leg(5,"90↑")}{leg(4,"80↑")}{P("→ 유지",16,B,"#3b4951")}{leg(3,"70↑")}{leg(2,"60↑")}{P("→ 개선",16,B,"#3b4951")}{leg(1,"60↓")}{P("→ 폐지",16,B,"#3b4951")}</div>')
tasks=[('노사협의회',['노측위원 참석 제고(화상 병행)']),('노사소위원회',['장기 미해결 안건 관리 강화']),('CEO 찾아가는 소통',['CEO 현장 방문·고충 해결']),('소수노조 소통',['소수노조 현장 소통 정례화']),('노사한마음',['본사·사업소 연결 참여 확대','노사 공동 후속 실천 연계'])]
cols=''.join(f'<div style="display:flex;flex-direction:column;"><div style="border:2px solid #8d9cbf;border-bottom:none;border-radius:12px 12px 0 0;padding:4px 4px 2px;background:#ffffff;">{P(h,19,B,al="center")}</div>'
 f'<div style="flex:1;border:1.5px solid #0051bc;padding:6px 8px;background:#ffffff;display:flex;flex-direction:column;gap:2px;">'+''.join(P('● '+x,17) for x in xs)+'</div></div>' for h,xs in tasks)
five=(f'<div style="display:flex;flex-direction:column;gap:8px;border:1.5px solid #8d9cbf;border-radius:8px;padding:8px;background:#f4f6fa;">'
 f'<div style="display:flex;align-items:stretch;border:1.5px solid #8d9cbf;background:#ffffff;"><div style="width:110px;display:flex;align-items:center;justify-content:center;background:#deeeff;padding:6px;">{P("도출 기준",18,B,al="center")}</div>'
 f'<div style="flex:1;padding:6px 12px;">{P("● 종합점수 60점 이상 80점 미만 <b>‘개선’ 판정 5개 채널</b>을 추진과제로 연결",17)}</div></div>'
 f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">{cols}</div></div>')
result=(f'<div style="display:flex;align-items:stretch;border:2px solid #00be83;background:#e6fcf9;"><div style="width:110px;display:flex;align-items:center;justify-content:center;background:#002060;">{P("추진성과",20,B,"#ffffff","center")}</div>'
 f'<div style="flex:1;padding:8px 14px;display:flex;flex-direction:column;gap:4px;">{P("• 진단툴 개선: 효과성 → 4개 유형별 결과 8요소(1차 결과·최종 성과)로 상세화, 노사 공동 진단(’26.[○])",18,B)}{P("• 진단결과: 유지 6·개선 5·폐지 0개, 개선 5개 채널 과제화 / 소통지수 [○]점(개선 진단툴 기준)",18,B)}</div></div>')
block=(f'<div style="position:absolute;left:127.9px;top:240.7px;width:934.6px;display:flex;flex-direction:column;gap:7px;">'
 f'<div style="display:grid;grid-template-columns:230px 1fr;gap:12px;">{oldbox}{newbox}</div>{notes}{method}'
 +trap('4개 유형별 소통채널 진단결과','#bde0ff','#000359',19)
 +f'<div style="display:grid;grid-template-columns:110px 165px 1fr 62px 62px 62px 74px 84px;border-top:2px solid #000359;">{"".join(tbl)}</div>{legend}'
 +trap('진단결과를 반영한 5대 개선과제 도출','#0051bc','#ffffff',20)+five+result+'</div>')
i=s.rfind('</div>',0,s.find('</x-dc>'))
s=s[:i]+block+'\n'+s[i:]
open(dst,'w',encoding='utf-8').write(s)
