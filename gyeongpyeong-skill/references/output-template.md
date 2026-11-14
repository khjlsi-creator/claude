# 통합 결과 템플릿

결과는 아래 한글 제목 구조의 마크다운으로 낸다. 각 절 제목 옆 괄호가 그 절에 담는 출력 키다. 사용자가 JSON을 요청하면 같은 키 10개를 최상위 키로 쓴다.

| 출력 키 | 담는 절 |
|---|---|
| `source_links` | 1. 입력 및 출처 |
| `mind_analysis` | 2. Mind |
| `stage1_status` | 2. Mind의 마지막 줄 |
| `source_conflicts` | 3. 출처 충돌과 HOLD |
| `writing_draft` | 4. Writing |
| `stage2_status` | 4. Writing의 마지막 줄 |
| `claim_evidence_matrix` | 5. 주장-증거 매트릭스 |
| `validation_scope` | 6. 검증 기록 |
| `risks` | 7. 잔여 리스크 |
| `next_experiment` | 8. 다음 실험 |

## 1. 입력 및 출처 (`source_links`)
기관 / 평가연도 / 보고서 / 페이지 / 원본 URL / 검증시점 / 사실카드 버전 / 사실카드 검증상태(검증·미검증)

## 2. Mind (`mind_analysis`, `stage1_status`)
- 핵심 평가주장 및 평가요건
- 정책활동 → 관측산출 → 관측성과의 연결 (검증된 인과만 표시)
- 지표 정의·정규화 키·분모·중복 출처
- 대안 설명, 외생요인, 미확보 근거
- 1단계 판정: PASS(연구용, 공식 아님) / CONDITIONAL / FAIL / 미실행 + 사유 한 줄

## 3. 출처 충돌과 HOLD (`source_conflicts`)
항목 | HOLD 사유코드 | 충돌 내용 | 해소에 필요한 확인

## 4. Writing (`writing_draft`, `stage2_status`)
- 평가보고서 문안 (문장별 출처 주석)
- 유보 문구
- 2단계 판정: PASS(연구용, 공식 아님) / CONDITIONAL / FAIL / 미실행 + 사유 한 줄

## 5. 주장-증거 매트릭스 (`claim_evidence_matrix`)
`writing-rules.md`의 대조표(C) 필드 그대로. Mind 판정과 대조 판정을 각각 적는다.

## 6. 검증 기록 (`validation_scope`)
- A 봉인 시점과 버전, B 작성, C 대조, D 금지패턴 점검 결과
- 구조 검사(스크립트) 결과와 자연어 의미검토 결과를 따로
- 독립 반복검증(G4): 수행 기록 또는 "미실행"
- 공식 Master PASS 아님

## 7. 잔여 리스크 (`risks`)

## 8. 다음 실험 (`next_experiment`)
