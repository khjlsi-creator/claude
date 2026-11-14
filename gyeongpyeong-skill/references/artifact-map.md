# 함께 쓰는 아티팩트

모두 claude.ai의 Design System 아티팩트다. 내용은 각 아티팩트의 `project/` 아래 파일에 있다. Artifact 도구의 `read`로 `project/README.md`부터 읽는다(페이지 화면이나 파일 목록을 긁지 않는다). 읽기 전용으로 쓰며, 이 스킬은 아티팩트를 고치지 않는다.

> 아래 요약은 2026-11-14에 읽은 내용이다. 레이아웃이 계속 추가되므로 번호 범위와 수치는 매번 아티팩트에서 다시 확인한다. 요약과 아티팩트가 다르면 아티팩트가 맞다.

## 1. KORAD 경영평가 — A4 세로 지면의 공통 규격
- 주소: https://claude.ai/artifact/6FYfaPGryfkEho7wvjoc7X (현재 제목 "KORAD 경영평가 (Copy)")
- 역할: 경영실적보고서 지면을 **서사 단락 블록**으로 쌓는 기본 시스템. 쪽 틀 `PageMaster`(홀수·짝수), 색·글꼴 토큰, 블록(ChapterBand·EvalBand·NumBar·SubHead·Ladder·LabelRows·TwinPanel·ThreePanel·DataTable·Connector·Note·Result), 레이아웃 L01~L291.
- 아래 두 지표 시스템이 이 규격(색·글꼴·직각 형태·쪽 틀)을 그대로 빌려 쓴다.
- 읽는 순서: `README.md` → `compose.md`(서사 → 레이아웃 → PPT) → `layout-groups.md` 또는 `layout-index.md` → 고른 `components/LayoutLxx/README.md` → `capacity.md` → `flow.md` → `quality-gate.md`.
- 실물: 저장소 `korad-경영평가-ppt/`의 A4 세로 템플릿 PPTX와 `assets/Code/compose.py`(노드 JSON → PPT).

## 2. 친환경탄소중립 지표 — 의미단락 레이아웃 L01~L120
- 주소: https://claude.ai/artifact/5xQ2hMCwUYtwsbyE5LLB7v
- 근거 지면: 12개 기관 2025년도 경영실적보고서의 친환경·탄소중립 쪽.
- 고르는 법: `layout-groups.md`의 내용 11묶음(01 표지·간지 / 02 전략체계 / 03 거버넌스·지적 환류 / 04 온실가스·Scope / 05 재생에너지·RE100 / 06 에너지 효율·친환경 건물 / 07 수송·업무전환·디지털 / 08 자원순환·녹색구매 / 09 생태·환경보전 / 10 지역사회·대국민 확산 / 11 임직원 내재화)에서 주제를 고른 뒤 쪽 비중(1/4·2/4·3/4·1쪽)과 모양이 맞는 것을 고른다.
- 쌓는 순서(`flow.md`): 지표 간지·목차 → Ⅰ 외부 지적사항 표 → Ⅱ 주요실적 비교 표 → Ⅲ 평가내용 띠 + BP·체계 → 번호 띠 사업 단락 → 소제목 단락.
- 읽는 순서: `README.md` → `layout-groups.md` → `components/LayoutLxx/README.md` → `capacity.md` → `flow.md` → `page-frame.md` → `quality-gate.md`. 새 지면 대조는 `ledger.md`.

## 3. 시설개방 지표 — 서사 단락 레이아웃 L01~L40
- 주소: https://claude.ai/artifact/XNCT1aRFBa1ri6ENKhCek3
- 범위: 「상생·협력 및 지역발전 › 평가내용 3(공공기관 보유 시설·장비 개방)」.
- 고르는 법: `layout-index.md`의 7묶음(1 전략·방향 수립형 / 2 사다리형 / 3 표 중심형 / 4 사례 패널형 / 5 BP 상자형 / 6 카드·프로그램형 / 7 한 쪽 통합형).
- KORAD 자체 지면: L13~L15(인쇄 73·74쪽), L19(청년 구직 학습공간), L20(주말 체육관, 1/4쪽). KORAD 실적은 이들을 먼저 검토한다.
- 추진성과 없이 남는 꼬리 대목용 **보충 레이아웃**: L14, L23, L30.
- 이 시스템만의 형태 규칙: 형광 밑줄을 쓰지 않고 강조는 굵은 글자로만, 번호 탭은 정사각 단색.
- 읽는 순서: `README.md` → `layout-index.md` → `components/LayoutLxx/README.md` → `flow.md` → `page-frame.md` → `ledger.md`.

## 4. KORAD — 16:9 보고용 장표 L01~L63
- 주소: https://claude.ai/artifact/EHjwTFzPdhMbDNmFhdpCb7
- 역할: 기관설명회·보고 발표 장표. **원본 장표 33장을 복제해 내용만 바꾸는** 규칙집. A4 보고서 지면에는 쓰지 않는다.
- 읽는 순서: `README.md` → `slide-production.md` → `layout-grid.md` → `panel-guide.md` → `quality-gate.md`. Slides·Design 탭에서 만들면 `slides-guide.md` 먼저.
- 과제(추진실적) 카드 L49·L50·L55·L56은 "추진배경 → 추진노력 → 성과" 구조라 경평 실적 요약에 맞는다.
- 장표마다 Source Slide 번호와 레이아웃 ID가 있어야 한다. Governing Message는 좌측 가로형 한 줄(약 43자).

## 네 시스템 공통 규칙
- 글꼴은 Pretendard 하나. 본문 글자색은 `navy-ink`. A4 지면 본문은 10pt이며 그 아래로 줄이지 않는다.
- 흐름 색은 블루 → 틸 → 딥블루, **결과·성과만 그린 계열**.
- 박스는 직각. 새 박스·장식·그라데이션을 만들지 않는다.
- 글이 넘치면 문장 압축 → 중복 삭제 → 개조식 변환 → 줄바꿈 → 다른 레이아웃 → 쪽·장표 분할. 칸 크기와 글자 크기는 바꾸지 않는다.
- 실적 수치는 실제 자료만. 예시·가짜 수치 금지.
- 다른 기관의 로고·사진·견본 문장은 쓰지 않는다. 사진 자리는 그림 칸으로 남긴다.
