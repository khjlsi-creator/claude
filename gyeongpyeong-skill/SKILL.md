---
name: gyeongpyeong-skill
description: KPE 경영평가 1단계 Mind 평가논리 분석과 2단계 Writing 평가보고서 문안 작성 및 출처 대조. 공공기관 실적의 사실·증빙 경계, 인과 유보, 지표 동일성, 문장 근거 연결을 검증할 때 사용한다.
---
# 경평스킬 (1단계 Mind + 2단계 Writing)

## 범위
- 수행: **1단계 Mind**(평가논리)와 **2단계 Writing**(문안 작성·대조)만.
- 수행하지 않음: 0단계 원본 검증의 통과 선언, 3단계 Visual, PDF 렌더링, Master 공식 승인.
- 사용자가 요청한 건을 그 대화에서 1회 수행한다. 예약·반복·백그라운드 실행을 스스로 만들거나 이전 실행을 이어서 재개하지 않는다.
- `Gold SEALED`, `Original Guard`, `Renderer Preflight`, `Master`는 **이 패키지 밖 상위 체계의 용어**다. 이 스킬은 그 상태를 선언·변경·해제하지 않는다. 해야 할 행동은 하나뿐이다: 모든 결과물에 "공식 Master PASS 아님"을 표기한다(`references/glossary.md`).

## 입력 계약
받는 항목: 기관, 보고서명·연도, 원문 URL·페이지·표/셀, 지표명·정의·대상·단위·기준연도·비교연도·원값·신값, 정책활동·관측실적·외부변수, 자료상태(확보/미확보/비해당), 검증상태(검증/미검증).

입력 형태별 처리:
| 받은 입력 | 처리 | 단계 판정 상한 |
|---|---|---|
| 검증된 사실카드 | 그대로 봉인(A)하고 진행 | PASS 가능 |
| 사실카드 없이 원문 발췌·수치만 | 받은 내용만으로 **잠정 사실카드**(검증상태=미검증)를 만들어 사용자에게 먼저 보여 주고 진행 | CONDITIONAL |
| 수치도 출처도 없음 | 작성하지 않고 필요한 항목을 질문 | 미실행 |

출처 없는 수치·분모·이용률·인과는 생성하지 않는다. 누락 항목은 임의로 채우지 않고 해당 항목에 HOLD를 건다. JSON 사실카드 형식은 `references/fact-card-schema.md`를 따른다.

## 판정 체계 (세 층을 섞지 않는다)
| 층 | 값 | 기록 위치 |
|---|---|---|
| 항목(필드·지표) | `HOLD` + 사유코드. HOLD는 **표시(flag)이며 단계 상태값이 아니다** | `source_conflicts`, `risks` |
| 주장(Mind) | SUPPORTED / CONDITIONAL / UNSUPPORTED / CONFLICT | `claim_evidence_matrix` |
| 문장 대조(Writing C표) | MATCH / ALTERED / OMITTED / HOLD | `claim_evidence_matrix`의 대조 열 |
| 단계 | PASS / CONDITIONAL / FAIL / 미실행 | `stage1_status`, `stage2_status` |

단계 판정 환산 규칙(위에서부터 먼저 해당하는 것):
1. **미실행** — 그 단계를 수행하지 않았다.
2. **FAIL** — UNSUPPORTED 주장이 단정 문장으로 남았거나, C표에 ALTERED/OMITTED가 수정되지 않고 1건 이상 남았다.
3. **CONDITIONAL** — HOLD, CONFLICT, CONDITIONAL 주장이 1건 이상 있거나 사실카드가 미검증이다.
4. **PASS** — G1~G3을 충족하고 위 사유가 없다.

여기서 PASS는 **연구용 단계 판정**이다. 공식 PASS(아래 "공식 인증")와 다르며, 출력에는 항상 `PASS(연구용, 공식 아님)`으로 적는다. "HOLD로 종료"는 단계 상태 CONDITIONAL + 해당 항목 HOLD 목록을 뜻한다.

## 1단계 Mind — 평가논리
1. 제도·활동(Input/Activity), 산출(Output), 결과(Outcome), 영향(Impact)을 구별한다. 관측된 사용자 수 증가를 정책의 순효과로 바꾸지 않는다.
2. 핵심주장별로 출처 원문, 지표, 범위, 기준시점, 대안설명, 미해결 위험을 연결하고 주장 판정값을 매긴다.
3. 지표 정규화 키는 `(기관, 보고연도, 기준연도, 비교연도, 제도, 대상범위, 단위)`다. 페이지는 성과 ID가 아니라 출처 집합이다. 같은 키가 여러 페이지에 인용되는 것은 정상이며 한 번만 센다.
4. 전체/남성, 사람/일수, 육아시간/육아시간제, 증가율/이용률, 지표 등급/기관 등급을 혼동하지 않는다.
5. 원문·파생시안·연구자 해석을 별도 provenance로 표시한다. 파생시안의 주석은 원문 인용이 아니다.
6. 표제·그래프·본문의 지표명 충돌은 다수결로 해결하지 않고 원본 인쇄면 및 정의 확인까지 HOLD한다.
7. 분모 무결성, 커버리지·잔여대상, flow/stock, 기여도·외생효과 등은 `references/mind-rules.md`의 질문으로 점검한다. 근거 없는 규칙을 '검증완료'로 승격하지 않는다.
8. `references/case-kps.md`의 충돌 사례를 기준 예로 적용한다.

## 2단계 Writing — 평가보고서 어법
1. Mind 결과를 **사실 → 활동 → 관측성과 → 해석 한계/잔여과제** 순으로 쓴다. 입증되지 않은 연결은 '함께 제시', '보고서에 기재'처럼 중립적으로 표현한다. 해석 한계는 작성자 서술(provenance=해석)로 쓰며 원문 인용처럼 표시하지 않는다.
2. 모든 정량 문장은 지표명, 대상, 연도, 단위, 원값/신값, 출처를 보존한다. 증가율은 `(신값-원값)/원값×100`으로 재계산해 원문 표기와 비교한다. 원값이 0이면 증가율을 쓰지 않는다.
3. 미검증 인과·이용률·효과성 단정, 지표명 치환, 중복성과 합산, 출처 오인, 확정되지 않은 해석은 차단한다.
4. 절차: **A** 사실카드 봉인(이후 수정 금지) → **B** 문안 작성 → **C** 원자 주장 단위 대조표 → **D** 금지패턴 점검 → 최종 문안·유보사항 출력. D의 방법은 `references/writing-rules.md`에 있다.
5. 원자료 오류는 Mind/원본 확인으로 되돌리고, 문안 변조·누락은 Writing에서 고친다. 구조 검사(스크립트) 통과와 자연어 의미검토 통과는 따로 기록한다.
6. 미확보/비해당/0/false는 서로 다르다. 출처 없는 빈칸을 '해당 없음'으로 처리하지 않는다.
7. 출력은 `references/output-template.md` 형식을 따른다.

## 품질 게이트
- **G1** 출처·지표·범위·단위·연도·중복성 검사. 미확정 항목은 HOLD.
- **G2** 활동/성과/인과 경계 검사 + 금지패턴 점검(D).
- **G3** 문안과 사실카드의 원자 주장 대조. 수치·정의·인과 ALTERED 0건.
- **G4** 독립 반복검증(사전 봉인 입력으로 블라인드 3회, 홀드아웃 30건을 별도 실행·기록). **단계 판정 요건이 아니다.** G4를 수행하지 못했어도 G1~G3을 충족하고 HOLD 등 감점 사유가 없으면 단계 판정은 PASS(연구용, 공식 아님)다. 한 대화에서 표현만 바꿔 쓴 것은 반복으로 세지 않는다. 수행 기록이 없으면 `validation_scope`에 "독립 반복검증 미실행"이라고 적고, '반복 검증됨'이라는 표현을 쓰지 않는다.

### 공식 인증
공식 PASS는 상위 체계의 Original Guard, Renderer Preflight, 상위 체계의 Quality Gate 3(위 **G3과 다른 절차**), 사용자 승인 근거가 모두 있어야 하며, 이 패키지는 그것을 제공하지 않는다. 따라서 이 스킬의 출력은 어떤 경우에도 공식 PASS를 선언하지 않는다.

## 출력
아래 10개 키를 `references/output-template.md`의 해당 절에 담는다(대응표는 그 파일에 있음):
`mind_analysis`, `writing_draft`, `claim_evidence_matrix`, `source_conflicts`, `stage1_status`, `stage2_status`, `risks`, `next_experiment`, `source_links`, `validation_scope`.

## 참고
- `references/glossary.md`: 용어와 행동 규칙
- `references/fact-card-schema.md`: JSON 사실카드 필드
- `references/mind-rules.md`: 평가논리 점검표
- `references/writing-rules.md`: 작성·대조·금지패턴 점검
- `references/output-template.md`: 결과 형식과 출력 키 대응
- `references/case-kps.md`: 한전KPS P94/P102/P216 사례 및 수치 충돌
- `references/source-index.md`: Google Drive 원본·체크포인트 링크와 범위
- `scripts/validate_metrics.py`: JSON 사실카드의 수치·식별키·중복 보조검사(원문 사실성 판정기는 아님). 예시 입력은 `assets/sample-fact-card.json`.
