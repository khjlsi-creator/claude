---
name: kp
description: "경평" 또는 "/kp"로 호출. KPE 경영평가 1단계 Mind 평가논리 분석과 2단계 Writing 평가보고서 문안 작성 및 출처 대조. 공공기관 실적의 사실·증빙 경계, 인과 유보, 지표 동일성, 문장 근거 연결을 검증할 때 사용한다.
---
# 경평스킬 (1단계 Mind + 2단계 Writing)

## 범위
이 스킬은 **1단계 Mind**와 **2단계 Writing**만 수행한다. 0단계는 제공받은 검증된 사실카드의 적격성·출처 확인을 입력조건으로 사용하되 0단계 자체의 원본 Guard PASS를 선언하지 않는다. 3단계 Visual, Master 공식 승인, PDF 렌더링은 수행하지 않는다. Gold SEALED 유지. 자동 실행을 시작하거나 재개하지 않는다.

## 입력 계약
기관, 보고서명·연도, 원문 URL·페이지·표/셀, 지표명·정의·대상·단위·기준연도·비교연도·원값·신값, 정책활동·관측실적·외부변수, 자료확보/미확보/비해당 상태, 검증상태를 받는다. 출처가 없는 수치·분모·이용률·인과는 생성하지 않는다. 누락 정보는 임의로 보충하지 말고 HOLD를 기록한다.

## 1단계 Mind — 평가논리
1. 제도·활동(Input/Activity), 산출(Output), 결과(Outcome), 영향(Impact)을 구별한다. 관측된 사용자 수 증가를 정책의 순효과로 바꾸지 않는다.
2. 핵심주장별로 출처 원문, 지표, 범위, 기준시점, 대안설명, 미해결 위험을 연결한다. 근거가 부족하면 CONDITIONAL 또는 FAIL로 남긴다.
3. 지표 정규화 키는 `(기관, 보고연도, 기준연도, 비교연도, 제도, 대상범위, 단위)`다. 페이지는 성과 ID가 아니라 출처 집합이다. 중복 인용은 합산하지 않는다.
4. 전체/남성, 사람/일수, 육아시간/육아시간제, 증가율/이용률, 지표 등급/기관 등급을 혼동하지 않는다.
5. 원문·파생시안·연구자의 해석을 별도 provenance로 표시한다. 파생시안의 주석은 원문 인용이 아니다.
6. 표제·그래프·본문의 지표명 충돌은 다수결로 해결하지 않고 원본 인쇄면 및 정의 확인까지 HOLD한다.
7. 페이지 역할, 서사패턴, Proof Anchor, 분모 무결성, tail/coverage, flow/stock, 기여도·외생효과, feedback lineage를 검토하되 근거 없는 규칙의 '검증완료' 승격을 금지한다.
8. `references/mind-rules.md`의 검증 질문과 `references/case-kps.md`의 충돌 사례를 적용한다.

## 2단계 Writing — 평가보고서 어법
1. Mind 결과를 **사실 → 활동 → 관측성과 → 해석 한계/잔여과제** 순으로 작성하되 입증되지 않은 연결은 '함께 제시', '보고서에 기재'처럼 중립적으로 표현한다.
2. 모든 정량 문장은 지표명, 대상, 연도, 단위, 원값/신값, 출처를 보존한다. 필요하면 증가율을 `(신값-원값)/원값×100`으로 재계산하고 원문 표기와 비교한다.
3. 미검증 인과·이용률·효과성 단정, 지표명 치환, 중복성과 합산, 출처 오인, 확정되지 않은 해석은 차단한다.
4. 작성 전에 입력 사실카드 A를 봉인하고, 독립 문안 B를 작성한 뒤, 별도 표 C로 원문/카드와 원자 주장 단위 대조한다. 비블라인드 표현변형을 독립 반복으로 산입하지 않는다.
5. 원자료 오류는 Mind/원본 확인으로 반환하고, 문안 변조·누락은 Writing으로 반환한다. 구조적 검사 PASS와 자연어 의미검토 PASS는 별도다.
6. 미확보/비해당/0/false는 서로 다르다. 출처 없는 빈칸을 '해당 없음'으로 처리하지 않는다.
7. `references/writing-rules.md` 및 `references/output-template.md`에 따라 문안을 작성하고 검토표를 함께 낸다.

## 필수 품질 게이트
- G1: 출처·지표·범위·단위·연도 및 중복성 검사. 미확정이면 HOLD.
- G2: 활동/성과/인과 경계 및 반례 검사.
- G3: 문안과 원본의 원자 주장 대조. 수치/정의/인과 변조 0건 요구.
- G4: 독립 반복 검증은 사전 봉인된 입력으로 블라인드 3회, 홀드아웃 30건을 별도 실행·기록한 경우에만 인정.
- 공식 PASS는 Original Guard, Renderer Preflight, Quality Gate 3, 사용자 승인 근거 없이는 금지. 이 패키지는 해당 공식 인증을 제공하지 않는다.

## 출력
`mind_analysis`, `writing_draft`, `claim_evidence_matrix`, `source_conflicts`, `stage1_status`, `stage2_status`, `risks`, `next_experiment`, `source_links`, `validation_scope`를 제공한다. 상태값은 PASS / CONDITIONAL / FAIL / 미실행. 입력이 불충분하면 질문하거나 CONDITIONAL/HOLD로 종료한다.

## 참고
- `references/case-kps.md`: 한전KPS P94/P102/P216 사례 및 수치 충돌
- `references/mind-rules.md`: 평가논리 점검표
- `references/writing-rules.md`: 작성·검증·반례
- `references/output-template.md`: 결과 형식
- `references/source-index.md`: Google Drive 원본·체크포인트 링크와 범위
- `scripts/validate_metrics.py`: 표준 JSON 사실카드의 수치·중복성 보조검사 (원문 사실성 판정기는 아님)
