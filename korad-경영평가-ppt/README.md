# KORAD 경영평가 노사관계 PPT 시스템 (A4 세로)

- `KORAD_경영평가_노사관계_A4세로.pptx` — 최종 PPT (24쪽, 마스터·레이아웃 3종 + 지면 R0~R7 + BP 모듈 A~H)
- `KORAD_경영평가_노사관계_A4세로_미리보기.pdf` — LibreOffice 렌더링 미리보기
- `B등급이상_44개기관_서사유형_분류.csv` — 종합 A·B 44개 기관의 서사 유형 분류(분석자 판단)
- `src/` — 생성 코드(python-pptx). `python3 src/build.py 출력.pptx`

## 표준
- A4 세로 210×297mm, 여백 좌우 15mm·상하 10mm (`src/kp.py` 상단 상수)
- 글자 12pt(본문·박스 안) / 14pt(네모·동그라미 라벨) / 15pt(박스 밖 제목), 글꼴 Pretendard
- 표지·간지 큰 제목은 예외

## 확인되지 않은 것
- KORAD 경영실적보고서 노사관계 쪽(104~112)은 이미지 PDF·10MB 초과로 읽지 못해 실측 좌표를 반영하지 못함
- 44개 기관 분류는 공식 평가 재검증 문서 기준이며, 7개 기관은 평가문장 건수만 확인되어 미분류

## 레이아웃 레지스트리 (누적형) — `layouts/`, `src/layout_registry.py`
다른 기관 경영실적보고서 쪽(한국수자원공사 p.5~9부터)의 좌표를 읽어 KORAD 평가 보고서용 레이아웃으로 쌓는다.
- `layouts/specs/pNN.json` — 한 쪽의 블록 종류·좌표(원본 이미지 px, 1240px 폭 = 210mm)
- `layouts/registry.json` — 누적 결과: 프레임 PF-, 블록 레이아웃 BL-, 쪽 레이아웃 PG-
- `layouts/preview/PG-NN.png`, `layouts/KORAD_경영평가_레이아웃_카탈로그.pptx` — 와이어프레임(도형 편집 가능)
- 새 쪽 추가: 스펙 JSON 작성 → `python3 src/layout_registry.py check <스펙>`(비교만) → `add <스펙>`(새것만 누적) → `render`
- 판정: 블록 지문(종류·본문유형·라벨열·열수·행수)이 같으면 REUSE, 쪽 구성(프레임+블록 순서)이 같으면 SKIP, 아니면 NEW
- 좌표는 렌더 이미지에서 읽은 값(±5px ≈ ±1mm). 원본 PDF 벡터에서 뽑은 값이 아님
