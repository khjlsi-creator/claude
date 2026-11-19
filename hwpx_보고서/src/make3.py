import sys, json
sys.path.insert(0,'conv'); from hwpxbuild import Doc, from_extract
s=175/1190
jobs=[
 ('음수시설_위생관리_개선_A4세로.hwpx','본사 음수시설·커피머신 위생관리 개선',[from_extract('conv/water.json',s,17.5-120*s,20-80*s)],'conv/water.png'),
 ('물품관리_업무_운영_개선_A4세로_2쪽.hwpx','물품관리 업무 운영 개선',[from_extract('conv/goods1.json',s,17.5-100*s,20-40*s),from_extract('conv/goods2.json',s,17.5-100*s,20-40*s)],'conv/goods1.png'),
 ('노사관계_노무전문인력_역량강화_A4세로.hwpx','HRD 연계 노무교육 체계화로 노사 상생 역량 강화',[from_extract('conv/labor.json',210/1191,0,0)],'conv/labor.png'),
]
for fn,title,pages,png in jobs:
    Doc().build(pages,'conv/'+fn,title,png,title+'\r\n')
    json.dump(pages,open('conv/'+fn+'.shapes.json','w'),ensure_ascii=False)
    print(fn,[len(p) for p in pages])
